# New chess bot with GUI

# Minimum viable product can:
# 0. Possess a working calculation function lmao
# 1. Handle challenges from LiChess
# 2. Display the board of the current match being played
# 3. Display data about search and eval

# Macro steps
# 1. Build a Qt gui window
# 2. Get the calculation/best-move functions working (instead of just repeating moves)
# 3. Display current board state (including opponent -- would be cool)
# 4. Display calculation data

import sys
import random
import chess
import chess.pgn
import chess.svg
import berserk # lichess api
#from PySide6 import QtCore, QtWidgets, QtGui


# Get board evaluation
def evaluate_board(board):
    score = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if piece is not None:
            value = {
                chess.PAWN: 1,
                chess.KNIGHT: 3,
                chess.BISHOP: 3.3,
                chess.ROOK: 5,
                chess.QUEEN: 9,
                chess.KING: 0  # Assuming kings have no material value for basic evaluation
            }.get(piece.piece_type, 0)

            if piece.color == chess.WHITE:
                score += value + get_piece_square_value(piece, square)
            else:
                score -= value + get_piece_square_value(piece, square)

    return score


def search(board, depth=3, alpha=0, beta=0):
    if (depth == 0):
        return round(evaluate_board(board), 2)

    moves = board.legal_moves
    if (moves.count == 0):
        if (board.is_check()):
            return -9999
        return 0

    for move in moves:
        #print(move) # just to see formatting
        board.push(chess.Move.from_uci(move))
        evaluation = -search(depth - 1, -alpha, -beta)
        board.pop()
        if (evaluation >= beta):
            return beta
        alpha = max(alpha, evaluation)
        
    return alpha

def order_moves(moves):
    for move in moves:
        move_score_guess = 0
        move_piece_type = chess.piece_at(move.to_square)



# Get piece positional scores
def get_piece_square_value(piece, square):
    # Assign values based on piece square tables
    piece_square_tables = {
        chess.PAWN: [
            0,    0,   0,   0,    0,   0,   0,  0,
            .5, .10, .10, -.20, -.20, .10, .10, .5,
            .5, -.5, -.10,  0,  0, -.10, -.5, .5,
            0,    0,   0, .20, .20,  0,   0,  0,
            .5,  .5, .10, .25, .25, .10,  .5, .5,
            .10, .10, .20, .30, .30, .20, .10, .10,
            .50, .50, .50, .50, .50, .50, .50, .50,
            0,    0,   0,   0,    0,  0,   0,   0
        ],
        # Similar tables for other pieces can be added
    }

    index = square if piece.color == chess.WHITE else chess.square_mirror(square)
    try:
        return piece_square_tables.get(piece.piece_type, [0])[index]
    except:
        #print(f"That piece is not added to the table yet!")
        return 0


def demo():
    board = chess.Board(chess.STARTING_FEN)
    board.push(chess.Move.from_uci("e2e4"))
    print("Board Evaluation after white e4:", round(evaluate_board(board), 2))
    #print(f"Board moves list: {search(board)}")
demo()

# main window loop
#app = QtWidgets.QApplication(sys.argv)
#app.exec()
