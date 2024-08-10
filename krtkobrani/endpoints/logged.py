import logging

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import flask_login

from krtkobrani.db_models import Team, Player
from krtkobrani.db import db
from krtkobrani.endpoints import forms

logged = Blueprint('logged', __name__)


@logged.route('/my_team', methods=['GET', 'POST'])
@login_required
def my_team():
    team = db.session.query(Team).filter_by(id=flask_login.current_user.id).first()
    players = db.session.query(Player).filter_by(team_id=flask_login.current_user.id).all()
    players = list(players)

    # insert default values into forms
    form = forms.EditTeamForm()
    player_forms = [forms.EditPlayerForm(prefix=f"p{p.id}") for p in players]
    add_player_form = forms.AddPlayerButtonForm()

    if request.method == 'GET':
        form.email.default = team.email
        form.name.default = team.name
        form.four_digits.default = team.four_digit
        form.phone.default = team.phone
        form.car_type.default = team.car_type
        form.car_spz.default = team.car_spz
        form.other_text.default = team.other_text
        form.process()

        player_forms[0].name.label.text = 'Jméno kapitána'
        player_forms[0].name.default = players[0].name
        player_forms[0].shirt_size.label.text = 'Číslo trička kapitána'
        player_forms[0].shirt_size.default = players[0].shirt_size
        player_forms[0].sex.label.text = 'Pohlaví (M/F) kapitána'
        player_forms[0].sex.default = players[0].sex
        player_forms[0].hidden_id.default = players[0].id
        player_forms[0].process()
        for i in range(1, len(players)):
            player_forms[i].name.label.text = f'Jméno {i + 1}. hráče'
            player_forms[i].shirt_size.label.text = f'Číslo trička {i + 1}. hráče'
            player_forms[i].sex.label.text = f'Pohlaví (M/F) {i + 1}. hráče'
            player_forms[i].name.default = players[i].name
            player_forms[i].shirt_size.default = players[i].shirt_size
            player_forms[i].sex.default = players[i].sex
            player_forms[i].hidden_id.default = players[i].id
            player_forms[i].process()

        return render_template('my_team.html',
                               form=form,
                               player_forms=player_forms,
                               add_form=add_player_form)

    # delete players
    deletes = [pf.delete.data for pf in player_forms]
    if any(deletes):
        to_delete_index = [i for i, x in enumerate(deletes) if x][0]
        to_delete_form = player_forms[to_delete_index]
        logging.info(f"deleting player {to_delete_form.hidden_id.data}")
        to_delete_player = db.session.get(Player, to_delete_form.hidden_id.data)
        db.session.delete(to_delete_player)
        db.session.commit()
        return redirect(url_for('logged.my_team'))

    # add players
    if add_player_form.button.data:
        return redirect(url_for('logged.new_player'))

    # update team
    the_team = db.session.get(Team, team.id)
    the_team.email = form.email.data
    the_team.name = form.name.data
    if form.password.data:
        the_team.password = generate_password_hash(form.password.data, method='scrypt')
    the_team.four_digit = form.four_digits.data
    the_team.phone = form.phone.data
    the_team.car_type = form.car_type.data
    the_team.car_spz = form.car_spz.data
    the_team.other_text = form.other_text.data

    # update players
    players = db.session.query(Player).filter_by(team_id=flask_login.current_user.id).all()
    for i, p in enumerate(players):
        p.name = player_forms[i].name.data
        p.shirt_size = player_forms[i].shirt_size.data
        p.sex = player_forms[i].sex.data
        db.session.add(p)
    db.session.commit()

    return redirect(url_for('logged.my_team'))


@logged.route('/new_player', methods=['GET', 'POST'])
@login_required
def new_player():
    form = forms.AddPlayerForm()
    if request.method == 'GET':
        return render_template('add_player.html', form=form)

    player = Player(name=form.name.data,
                    shirt_size=form.shirt_size.data,
                    sex=form.sex.data,
                    is_captain=0,
                    team_id=flask_login.current_user.id
                    )

    db.session.add(player)
    db.session.commit()
    return redirect(url_for('logged.my_team'))