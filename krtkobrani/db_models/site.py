from krtkobrani.db import db


class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_pass = db.Column(db.String(64))
    exit_pass = db.Column(db.String(64))
    help_1_text = db.Column(db.String(256))
    help_2_text = db.Column(db.String(256))
    dead_text  = db.Column(db.String(256))
    next_site_location = db.Column(db.String(256))
