from krtkobrani.db import db


class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_number = db.Column(db.Integer, unique=True)
    entry_pass = db.Column(db.String(64))
    exit_pass = db.Column(db.String(64))
    help_1_text = db.Column(db.String(256))
    help_1_time_minutes = db.Column(db.Integer)
    help_2_text = db.Column(db.String(256))
    help_2_time_minutes = db.Column(db.Integer)
    dead_time_minutes = db.Column(db.Integer)
    next_site_location = db.Column(db.String(256))
