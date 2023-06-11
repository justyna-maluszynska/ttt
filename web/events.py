import datetime
from flask_login import current_user
from web.utils import check_game_result, end_game, can_start_new_game
from web.extensions import socketio, db
from web.models import Game, PlayerGame, Session
from flask_socketio import join_room, leave_room, emit
import random


def check_sender(game):
    if game.session.player_id == current_user.id:
        return True
    return False


@socketio.on('join')
def on_join(data):
    session_id = data['session_id']

    session = db.session.execute(
        db.select(Session).filter_by(id=session_id)).scalar()
    game = next(
        game for game in session.games if not game.finished)

    player_game = PlayerGame(player_id=current_user.id, game_id=game.id)
    db.session.add(player_game)
    db.session.commit()

    print(str(current_user.id) + ' has joined the room')
    join_room(game.room_code)
    emit("join", {
         "users": [player_game.player.username for player_game in game.players if not player_game.left], "game": game.id}, room=game.room_code)


@socketio.on('leave')
def on_leave(data):
    game_id = data['game_id']

    game = db.session.execute(db.select(Game).filter_by(id=game_id)).scalar()

    player_game = db.session.query(PlayerGame).filter_by(
        player_id=current_user.id, game_id=game.id).first()
    player_game.left = True

    db.session.add(player_game)
    db.session.commit()

    leave_room(game.room_code)
    print(current_user.username + ' has left the room.')
    emit("leave", to=game.room_code)


@socketio.on('next_game')
def prepare_next_game(data):
    session_id = data.get('session_id')
    room = data['room']

    game = db.session.execute(
        db.select(Game).filter_by(session_id=session_id, finished=False)).scalar()

    if game is None:
        game = Game(session_id=session_id, room_code=room)
        db.session.add(game)
        db.session.commit()

    player_game = PlayerGame(player_id=current_user.id, game_id=game.id)
    db.session.add(player_game)
    db.session.commit()

    emit("next_game", {"game": game.id})


@socketio.on("starting")
def starting(data):
    game_id = data['game_id']

    game = db.session.execute(
        db.select(Game).filter_by(id=game_id)).scalar()
    if check_sender(game):
        for player_game in game.players:
            player_game.player.credits -= 3
            player_game.pawn = 'X'

        starting_player_game = random.choice(game.players)
        starting_player_game.pawn = 'O'
        starting_player = starting_player_game.player

        game.start_time = datetime.datetime.now()
        db.session.add(game)
        db.session.commit()

        print(f"starting game: {game_id}, room code: {game.room_code}")
        emit("starting", {
             "starting_player": starting_player.id}, to=game.room_code)


@socketio.on("move")
def on_move(data):
    game_id = data['game_id']
    board = data['board']

    game = db.session.execute(db.select(Game).filter_by(id=game_id)).scalar()

    current_player_game = next(
        player_game for player_game in game.players if player_game.player_id == current_user.id)
    next_player_game = next(
        player_game for player_game in game.players if player_game.player_id != current_user.id)
    state = check_game_result(board)

    game_ended = state != ''
    if game_ended:
        end_game(game, current_player_game, next_player_game, state == 'draw')
        new_game = can_start_new_game(game.players)

        if not new_game:
            game.session.closed = True

        db.session.add(game)
        db.session.commit()
        emit('finish', {'winner': current_user.id,
             'new_game': new_game, 'board': board, 'draw': state == 'draw'}, room=game.room_code)
    else:
        emit("move", {'next_player': next_player_game.player_id,
                      'pawn': next_player_game.pawn, 'board': board}, room=game.room_code)
