def check_game_result(board):
    # Checking rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != '':
            return (True, row[0])

    # Checking columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '':
            return (True, board[0][col])

    # Checking diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        return (True, board[0][0])
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        return (True, board[0][2])

    # Chacking draw
    for row in board:
        if '' in row:
            return (False, '')

    return (True, '')
