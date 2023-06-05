from extensions import db
from flask_login import UserMixin


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Player(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
