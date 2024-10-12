import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
import logging
from functools import wraps

from krtkobrani.db_models import Site, News, Action
from krtkobrani.db import db
from krtkobrani.endpoints import forms
from krtkobrani.logic import action_logic
from krtkobrani.logic.action_logic import make_all_teams_admin, start_game

admin = Blueprint('admin', __name__)

def admin_required(func):
    """
    Modified login_required decorator to restrict access to admin group.
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:        # zero means admin, one and up are other groups
            flash("You don't have permission to access this resource.", "warning")
            return redirect(url_for("base.index"))
        return func(*args, **kwargs)
    return decorated_view


@admin.route('/admin_index')
@admin_required
def admin_index():
    return render_template('admin_index.html')


@admin.route('/sites', methods=['GET', 'POST'])
@admin_required
def sites():
    form = forms.AddSite()
    all_sites = db.session.query(Site).all()
    if request.method == 'GET': # process get method
        return render_template('sites.html', form=form, all_sites=all_sites)

    site = Site(site_number=form.site_number.data,
                entry_pass=form.entry_pass.data,
                exit_pass=form.exit_pass.data,
                help_1_text=form.help_1_text.data,
                help_1_time_minutes=form.help_1_time_minutes.data,
                help_2_text=form.help_2_text.data,
                help_2_time_minutes=form.help_2_time_minutes.data,
                dead_time_minutes=form.dead_time_minutes.data,
                next_site_location=form.next_site_location.data
                )
    db.session.add(site)
    db.session.commit()
    return redirect(url_for('admin.sites'))


@admin.route('/admin_news', methods=['GET', 'POST'])
@admin_required
def news():
    form = forms.AddNews()
    all_news = db.session.query(News).all()
    if request.method == 'GET': # process get method
        return render_template('news.html', form=form, news=all_news)

    news = News(timestamp=datetime.datetime.utcnow(),
                text=form.text.data
                )
    db.session.add(news)
    db.session.commit()
    return redirect(url_for('admin.news'))


@admin.route('/game_start', methods=['GET', 'POST'])
@admin_required
def game_start():
    form = forms.GameStart()
    action = db.session.query(Action).first()
    if action:
        game_started = True
    else:
        game_started = False

    if request.method == 'GET':  # process get method
        return render_template('game_start.html', form=form, game_started=game_started)

    action_logic.start_game()
    return redirect(url_for('admin.game_start'))
