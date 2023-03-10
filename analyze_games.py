import io
import json
import os
import random
import time

import chess.pgn
import chess.svg
from dotenv import load_dotenv
from stockfish import Stockfish

load_dotenv()

USERNAME = os.getenv('CHESS_USERNAME')
stockfish = Stockfish(path='/usr/local/bin/stockfish', depth=20)

files = os.listdir('data')
game_file = f'data/{files[random.randint(0, len(files) - 1)]}'

with open(game_file) as f:
    data = json.loads(f.read())

if data['white']['username'] == USERNAME:
    sign = 1
    my_pieces = 'white'
else:
    sign = -1
    my_pieces = 'black'

if data['white']['result'] == 'win':
    end = 2000
elif data['black']['result'] == 'win':
    end = -2000
else:
    end = 0

pgn = io.StringIO(data['pgn'])
game = chess.pgn.read_game(pgn)

evals = []
moves = []


def get_evaluation_score(evaluation):
    if evaluation['type'] == 'mate':
        try:
            return 2000 * evaluation['value'] / abs(evaluation['value'])
        except ZeroDivisionError:
            return end
    else:
        return evaluation['value']


print(f"{data['url']}: {data[my_pieces]} as {my_pieces}")
game_id = data['url'].split('/')[-1]
stockfish.set_fen_position(data['initial_setup'])
board = game.board()
for move in game.mainline_moves():
    moves.append(move.uci())
    stockfish.make_moves_from_current_position([move.uci()])
    board.push(move)
    evaluation = get_evaluation_score(stockfish.get_evaluation())
    evals.append(evaluation)
    print(move.uci(), evaluation)


deltas = [evals[i] - evals[i - 1] for i in range(1, len(evals))]

if sign < 0:
    worst_delta = max(deltas)
else:
    worst_delta = min(deltas)

worst_move_index = deltas.index(worst_delta) + 1
worst_move = moves[worst_move_index]
print(worst_move_index, worst_move, worst_delta)

[board.pop() for _ in range(len(moves) - worst_move_index)]
print(board.fen())

board_svg = chess.svg.board(board, size=600, coordinates=True)
with open(f'assets/{game_id}.svg', 'w') as output:
    output.write(board_svg)
    time.sleep(0.1)
