from sqlalchemy import ForeignKey

from krtkobrani.db import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    shirt_size = db.Column(db.String(8), nullable=True)
    sex = db.Column(db.String(2), nullable=True)
    is_captain = db.Column(db.Boolean, nullable=True)
    team_id = db.Column(db.Integer, ForeignKey("team.id"), nullable=False)
