from sqlalchemy.dialects.mysql import LONGTEXT

from krtkobrani.db import db


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    text = db.Column(LONGTEXT, nullable=False)
