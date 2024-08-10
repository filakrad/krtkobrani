from krtkobrani.db import db
from flask_login import UserMixin


class Team(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(512), nullable=False)
    phone = db.Column(db.String(16), nullable=False)
    four_digit = db.Column(db.String(4), nullable=False, unique=True)
    car_type = db.Column(db.String(256))
    car_spz = db.Column(db.String(16))
    other_text = db.Column(db.String(512))
    is_admin = db.Column(db.Boolean, nullable=False, default=0)
