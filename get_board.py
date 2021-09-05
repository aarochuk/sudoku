import requests

def new_board(diff=1):
    board = requests.get(f'https://sudoku--api.herokuapp.com/new-board?diff={diff}').json()['response']['unsolved-sudoku']

    return board
