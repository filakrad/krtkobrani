from sqlalchemy import ForeignKey

from krtkobrani.db import db


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, ForeignKey("site.id"), nullable=False)
    team_id = db.Column(db.Integer, ForeignKey("team.id"), nullable=False)
    action_state = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    guess = db.Column(db.String(128))
    success = db.Column(db.Boolean, nullable=False)
