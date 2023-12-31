from typing import List
from web.extensions import db
from flask_login import UserMixin


class PlayerGame(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    player_id = db.Column(db.ForeignKey('player.id'), nullable=False)
    game_id = db.Column(db.ForeignKey('game.id'), nullable=False)
    state = db.Column(db.String)
    pawn = db.Column(db.String)
    left = db.Column(db.Boolean)

    player: db.Mapped["Player"] = db.relationship(back_populates="games")
    game: db.Mapped["Game"] = db.relationship(back_populates="players")


class Player(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    credits = db.Column(db.Integer, default=10)

    games: db.Mapped[List["PlayerGame"]] = db.relationship(
        back_populates="player")
    sessions: db.Mapped[List["Session"]] = db.relationship(
        "Session", backref="player")


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_code = db.Column(db.String, nullable=False)
    draw = db.Column(db.Boolean)
    finished = db.Column(db.Boolean, default=False)
    session_id = db.Column(db.ForeignKey("session.id"), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    players: db.Mapped[List["PlayerGame"]
                       ] = db.relationship(back_populates="game")


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.ForeignKey('player.id'))
    closed = db.Column(db.Boolean, default=False)

    games: db.Mapped[List["Game"]] = db.relationship("Game", backref="session")
