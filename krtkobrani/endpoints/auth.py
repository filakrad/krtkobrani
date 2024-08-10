from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import logging
from wtforms.validators import DataRequired

from krtkobrani.db_models import Team, Player
from krtkobrani.db import db
from krtkobrani.endpoints import forms

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    form = forms.Login()
    logging.info(f"method {request.method}")
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        team = db.session.query(Team).filter_by(email=email).first()

        logging.info(f"got team {team.name}")

        if not team or not check_password_hash(team.password_hash, password):
            flash('Please check your login details and try again.')
            logging.info(f"password validation unsuccessfull")
            return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

        logging.info(f"password validated")

        login_user(team, remember=True)
        logging.debug(f"load_user user_id: {team.id}")

        return redirect(url_for('base.index'))
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base.index'))


@auth.route('/create_team', methods=['POST', 'GET'])
def create_team():
    form = forms.RegistrationForm()
    player_forms = [forms.PlayerForm(prefix=f"p{i}") for i in range(8)]
    player_forms[0].name.label.text = 'Jméno kapitána'
    player_forms[0].name.validators = [DataRequired()]
    player_forms[0].shirt_size.label.text = 'Číslo trička kapitána'
    player_forms[0].sex.label.text = 'Pohlaví (M/F) kapitána'
    for i in range(1, 8):
        player_forms[i].name.label.text = f'Jméno {i+1}. hráče'
        player_forms[i].shirt_size.label.text = f'Číslo trička {i+1}. hráče'
        player_forms[i].sex.label.text = f'Pohlaví (M/F) {i+1}. hráče'


    if request.method == 'GET':
        return render_template('create_team_v2.html', form=form, player_forms=player_forms)

    team = db.session.query(Team).filter((Team.email == form.email.data)
                                         | (Team.name == form.name.data)
                                         | (Team.four_digit == form.four_digits.data)
                                         ).first()
    if team:  # if a team is found, we want to redirect back to signup page so user can try again
        if team.email == form.email.data:
            flash('Tato emailová adresa je již použitá')
        if team.name == form.name.data:
            flash('Toto jméno týmu je již použité')
        if team.four_digit == form.four_digits.data:
            flash('Toto čtyřčíslí je již použité')
        return redirect(url_for('auth.create_team'))

    logging.info("create team: team not found")

    if not player_forms[0].name.data:
        flash('První hráč musí mít jméno!')
        return redirect(url_for('auth.create_team'))

    logging.info("create team: first player name")

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_team = Team(email=form.email.data,
                    name=form.name.data,
                    password_hash=generate_password_hash(form.password.data, method='scrypt'),
                    four_digit=form.four_digits.data,
                    phone=form.phone.data,
                    car_type=form.car_type.data,
                    car_spz=form.car_spz.data,
                    other_text=form.other_text.data
                    )

    # add the new team to the database
    db.session.add(new_team)
    db.session.flush()
    db.session.refresh(new_team)

    # create players
    for i, pf in enumerate(player_forms):
        if pf.name.data:
            new_player = Player(name=pf.name.data,
                                shirt_size=pf.shirt_size.data,
                                sex=pf.sex.data,
                                is_captain=1 if i == 0 else 0,
                                team_id=new_team.id
                                )
            db.session.add(new_player)
        else:
            break

    login_user(new_team, remember=True)
    db.session.commit()

    return redirect(url_for('base.teams'))


@auth.route('/create_admin_team', methods=['POST', 'GET'])
def create_admin_team():
    form = forms.RegistrationForm()
    if request.method == 'GET':
        return render_template('create_admin_team.html', form=form)

    teams = db.session.query(Team).all()
    if len(teams) > 0:
        return redirect(url_for('base.index'))

    new_team = Team(email=form.email.data,
                    name="",
                    password_hash=generate_password_hash(form.password.data, method='scrypt'),
                    four_digit="",
                    phone="",
                    car_type="",
                    car_spz="",
                    is_admin=True
                    )
    db.session.add(new_team)
    db.session.commit()

    return redirect(url_for('base.index'))

