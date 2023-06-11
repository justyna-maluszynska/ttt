import datetime
from web.extensions import db
from web.models import Game, Player, PlayerGame


def check_game_result(board: dict) -> str:
    """ Checks whether the current player finished the game """
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

    for row in board:
        if '' in row:
            return ''

    return 'draw'


def end_game(game: Game, winner: PlayerGame, loser: PlayerGame, is_draw: bool) -> None:
    """ Ends the game and saves the data """
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


def add_credits(player: Player) -> bool:
    """ Adds credits to player if possible """
    if player.credits <= 0:
        player.credits += 10
        db.session.add(player)
        db.session.commit()
        return True
    return False


def _init_stats(stats: dict, day: str, win: int, lose: int, draw: int, time_played: datetime.timedelta) -> dict:
    """ Initialize stats for the given day """
    stats[day] = {
        "win": win,
        "lose": lose,
        "draw": draw,
        "count": 1,
        "time_played": time_played,
    }
    return stats


def _update_stats(stats: dict, day: str, win: int, lose: int, draw: int, time_played: datetime.timedelta) -> dict:
    """ Update stats for the given day """
    stats[day].update({
        "win": stats[day]['win'] + win,
        "lose": stats[day]['lose'] + lose,
        "draw": stats[day]['draw'] + draw,
        "count": stats[day]['count'] + 1,
        "time_played": stats[day]['time_played'] + time_played,
    })
    return stats


def _fetch_stats(player_game: PlayerGame) -> tuple:
    """ Fetches stats from given player game object """
    win = 1 if player_game.state == "winner" else 0
    lose = 1 if player_game.state == "loser" else 0
    draw = 1 if player_game.state == "draw" else 0
    time_played = player_game.game.end_time - player_game.game.start_time
    return win, lose, draw, time_played


def calculate_win_ratio(stats: dict) -> dict:
    """ Calculates the win ratio """
    for key, item in stats.items():
        stats[key]['win_ratio'] = item['win']/item['count']
    return stats


def get_stats(player: Player) -> dict:
    """Get stats for a player"""
    player_games = [
        player_game for player_game in player.games if player_game.game.finished and not player_game.left]

    stats_by_day = {}

    for player_game in player_games:
        game = player_game.game
        day_played = game.start_time.date()
        day_played = day_played.strftime("%m/%d/%Y")

        win, lose, draw, time_played = _fetch_stats(player_game)
        if day_played in stats_by_day.keys():
            stats_by_day = _update_stats(stats_by_day, day_played,
                                         win, lose, draw, time_played)
        else:
            stats_by_day = _init_stats(stats_by_day, day_played,
                                       win, lose, draw, time_played)

    stats_by_day = calculate_win_ratio(stats_by_day)

    return stats_by_day
