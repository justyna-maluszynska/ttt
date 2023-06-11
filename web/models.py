from typing import List
from web.extensions import db
from flask_login import UserMixin


class PlayerGame(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    player_id = db.Column(db.ForeignKey('player.id'), nullable=False)
    game_id = db.Column(db.ForeignKey('game.id'), nullable=False)
    state = db.Column(db.String)
    pawn = db.Column(db.String)

    player: db.Mapped["Player"] = db.relationship(back_populates="games")
    game: db.Mapped["Game"] = db.relationship(back_populates="players")


class Player(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    credits = db.Column(db.Integer, default=10)
    in_room = db.Column(db.Boolean)

    games: db.Mapped[List["PlayerGame"]] = db.relationship(
        back_populates="player")
    sessions: db.Mapped[List["Session"]] = db.relationship(
        "Session", backref="player")


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_code = db.Column(db.String, nullable=False, unique=True)
    draw = db.Column(db.Boolean)
    finished = db.Column(db.Boolean, default=False)
    in_progress = db.Column(db.Boolean, default=False)
    session_id = db.Column(db.ForeignKey("session.id"), nullable=False)

    players: db.Mapped[List["PlayerGame"]
                       ] = db.relationship(back_populates="game")


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.ForeignKey('player.id'))

    games: db.Mapped[List["Game"]] = db.relationship("Game", backref="session")
