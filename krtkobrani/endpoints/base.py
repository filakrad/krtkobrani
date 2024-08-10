from flask import Blueprint, render_template
import logging

from krtkobrani.db_models import News, Team, Player
from krtkobrani.db import db

base = Blueprint('base', __name__)


@base.route('/')
def index():
    return render_template('index.html')


@base.route('/rules')
def rules():
    return render_template('rules.html')


@base.route('/news')
def news():
    news = db.session.execute(db.select(News).order_by(News.id)).scalars()
    return render_template('news.html', news=news)


@base.route('/teams')
def teams():
    teams = db.session.execute(db.select(Team).order_by(Team.id).filter_by(is_admin=0)).scalars()
    _teams = [{'id': t.id, 'name': t.name, 'four_digit': t.four_digit} for t in teams]
    players_dict = {t['id']: [] for t in _teams}
    players = db.session.execute(db.select(Player).order_by(Player.team_id)).scalars()
    for player in players:
        players_dict[player.team_id].append(player.name)
    logging.info(f"{players_dict}")
    return render_template('teams.html', teams=_teams, players=players_dict)


@base.route('/sifry')
def sifry():
    return render_template('ciphers.html')