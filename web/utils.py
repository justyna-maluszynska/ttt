import datetime
from web.extensions import db
from web.models import Game


def check_game_result(board):
    # Checking rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != '':
            return 'winner'

    # Checking columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '':
            return 'winner'

    # Checking diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        return 'winner'
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        return 'winner'

    # Chacking draw
    for row in board:
        if '' in row:
            return ''

    return 'draw'


def end_game(game, winner, loser, is_draw):
    game.finished = True
    game.end_time = datetime.datetime.now()

    if is_draw:
        game.draw = True
        winner.state = 'draw'
        loser.state = 'draw'
    else:
        winner.state = 'winner'
        loser.state = 'loser'
        winner.player.credits += 4


def can_start_new_game(players):
    for player in players:
        if player.player.credits <= 0:
            return False
    return True


def add_credits(player):
    if player.credits <= 0:
        player.credits += 10
        db.session.add(player)
        db.session.commit()


def init_stats(stats, day, win, lose, draw, time_played):
    stats[day] = {
        "win": win,
        "lose": lose,
        "draw": draw,
        "count": 1,
        "time_played": time_played,
    }
    return stats


def update_stats(stats, day, win, lose, draw, time_played):
    stats[day].update({
        "win": stats[day]['win'] + win,
        "lose": stats[day]['lose'] + lose,
        "draw": stats[day]['draw'] + draw,
        "count": stats[day]['count'] + 1,
        "time_played": stats[day]['time_played'] + time_played,
    })
    return stats


def fetch_stats(player_game):
    win = 1 if player_game.state == "winner" else 0
    lose = 1 if player_game.state == "loser" else 0
    draw = 1 if player_game.state == "draw" else 0
    time_played = player_game.game.end_time - player_game.game.start_time
    return win, lose, draw, time_played


def calculate_win_ratio(stats):
    for key, item in stats.items():
        stats[key]['win_ratio'] = item['win']/item['count']


def get_stats(player):
    player_games = [
        player_game for player_game in player.games if player_game.game.finished]

    stats_by_day = {}

    for player_game in player_games:
        game = player_game.game
        day_played = game.start_time.date()
        day_played = day_played.strftime("%m/%d/%Y")

        win, lose, draw, time_played = fetch_stats(player_game)
        if day_played in stats_by_day.keys():
            print(stats_by_day)
            stats_by_day = update_stats(stats_by_day, day_played,
                                        win, lose, draw, time_played)
        else:
            print(stats_by_day)
            stats_by_day = init_stats(stats_by_day, day_played,
                                      win, lose, draw, time_played)

    calculate_win_ratio(stats_by_day)
    print(str(stats_by_day))
    return stats_by_day
