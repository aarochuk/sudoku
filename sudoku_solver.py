from time import sleep
def find_next(board):
    for y in range(9):
        for x in range(9):
            if board[y][x] == 0:
                return y, x

    return None


def valid(board, n, y, x):
    for i in range(9):
        if board[y][i] == n:
            return False

    for i in range(9):
        if board[i][x] == n:
            return False

    x_ = (x//3) * 3
    y_ = (y//3) * 3

    for i in range(3):
        for j in range(3):
            if board[y_ + i][x_ + j] == n:
                return False

    return True


def _solve(board):
    find = find_next(board)
    if find:
        col, row = find
    else:
        return True

    for i in range(1, 10):
        if valid(board, i, col, row):

            board[col][row] = i

            if _solve(board):
                return True

            board[col][row] = 0

    return

