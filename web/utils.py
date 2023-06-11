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
    game.in_progress = False

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
        if player.player.credits == 0:
            return False
    return True
