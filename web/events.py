from web.utils import check_game_result, end_game, can_start_new_game
from web.extensions import socketio, db
from web.models import Player, Game, PlayerGame, Session
from flask_socketio import join_room, leave_room, emit
import random


@socketio.on('join')
def on_join(data):
    user_id = data['user_id']
    session_id = str(data['session_id'])

    session = db.session.execute(
        db.select(Session).filter_by(id=session_id)).scalar()
    game = next(
        game for game in session.games if not game.finished and not game.in_progress)

    player_game = PlayerGame(player_id=user_id, game_id=game.id)
    db.session.add(player_game)
    db.session.commit()

    print(str(user_id) + ' has joined the room')
    join_room(game.room_code)
    emit("join", {
         "users": [player_game.player.username for player_game in game.players]}, room=game.room_code)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']

    game = db.session.execute(
        db.select(Game).filter_by(room_code=str(room))).scalar()
    player = db.session.execute(
        db.select(Player).filter_by(username=username)).scalar()

    player_game = db.session.query(PlayerGame).filter_by(
        player_id=player.id, game_id=game.id).first()
    db.session.delete(player_game)
    db.session.commit()

    leave_room(room)
    print(username + ' has left the room.')
    emit("leave", {"user": username}, to=room)


@socketio.on("starting")
def starting(data):
    room = data['room']

    # TODO: wymyślić coś lepszego niz identygikowanie gry na podstawie room code, bo się będzie przeciez to potem nadpisywać
    game = db.session.execute(
        db.select(Game).filter_by(room_code=str(room))).scalar()

    for player_game in game.players:
        player_game.player.credits -= 3
        player_game.pawn = 'X'

    starting_player_game = random.choice(game.players)
    starting_player_game.pawn = 'O'
    starting_player = starting_player_game.player

    db.session.add(game)
    db.session.commit()

    emit("starting", {"starting_player": starting_player.id})


@socketio.on("move")
def on_move(data):
    room = str(data['room'])
    board = data['board']
    player_id = data['user_id']

    game = db.session.execute(
        db.select(Game).filter_by(room_code=str(room))).scalar()

    current_player_game = next(
        player_game for player_game in game.players if player_game.player_id == player_id)
    next_player_game = next(
        player_game for player_game in game.players if player_game.player_id != player_id)
    state = check_game_result(board)

    game_ended = state != ''
    if game_ended:
        end_game(game, current_player_game, next_player_game, state == 'draw')
        new_game = can_start_new_game(game.players)

        db.session.add(game)
        db.session.commit()
        emit('finish', {'winner': player_id,
             'new_game': new_game, 'board': board, 'draw': state == 'draw'}, room=room)
    else:
        emit("move", {'next_player': next_player_game.player_id,
                      'pawn': next_player_game.pawn, 'board': board}, room=room)
