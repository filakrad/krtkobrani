from krtkobrani.db import db


class Static(db.Model):
    name = db.Column(db.String(64), primary_key=True)
    file_location = db.Column(db.String(128))
