# New chess bot with GUI

# Minimum viable product can:
# 0. Possess a working calculation function lmao [x]
# 1. Handle challenges from LiChess [~]
# 2. Display the board of the current match being played
# 3. Display data about search and eval

# Macro steps
# 1. Build a Qt gui window
# 2. Get the calculation/best-move functions working (instead of just repeating moves) [x]
# 3. Display current board state (including opponent -- would be cool)
# 4. Display calculation data

# TODO for bot improvement
# - Pawns need to be used more
# - Need to not move rook(s) so it can castle
# - Capture with the weaker piece
# - Check king to get move advantage
# - Use an opening
# - End/middlegame strats

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


def search(board, depth=6, alpha=-9999, beta=9999):
    if depth == 0:
        return round(evaluate_board(board), 2)

    moves = list(board.legal_moves)
    if not moves:
        if board.is_check():
            return -9999
        return 0

    best_move = None  # Introduce a variable to track the best move

    for move in moves:
        board.push(move)
        evaluation = -search(board, depth - 1, -beta, -alpha)
        board.pop()

        if evaluation >= beta:
            return beta

        if evaluation > alpha:
            alpha = evaluation
            if depth == 6:  # Only update the best move at the root level
                best_move = move

    if depth == 6:
        return str(best_move)  # Return the best move at the root level
    else:
        return alpha


# 15:31 in Seb Lague video
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
        chess.KNIGHT: [
            -.50, -.40, -.30, -.30, -.30, -.30, -.40, -.50,
            -.40, -.20, 0, .5, .5, 0, -.20, -.40,
            -.30, .5, .10, .15, .15, .10, .5, -.30,
            -.30, 0, .15, .20, .20, .15, 0, -.30,
            -.30, .5, .15, .20, .20, .15, .5, -.30,
            -.30, 0, .10, .15, .15, .10, 0, -.30,
            -.40, -.20, 0, 0, 0, 0, -.20, -.40,
            -.50, -.40, -.30, -.30, -.30, -.30, -.40, -.50
        ],
        chess.QUEEN: [
            -1.0, -0.5, -0.5, -0.25, -0.25, -0.5, -0.5, -1.0,
            -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
            -0.5, 0.0, 0.25, 0.25, 0.25, 0.25, 0.0, -0.5,
            -0.25, 0.0, 0.25, 0.5, 0.5, 0.25, 0.0, -0.25,
            0.0, 0.0, 0.25, 0.5, 0.5, 0.25, 0.0, 0.0,
            -0.5, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, -0.5,
            -0.5, 0.0, 0.25, 0.25, 0.25, 0.25, 0.0, -0.5,
            -1.0, -0.5, -0.5, -0.25, -0.25, -0.5, -0.5, -1.0
        ],
        chess.ROOK: [
            -1.0, -0.5, 0.0, 0.25, 0.25, 0.0, -0.5, -1.0,
            -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
            0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0,
            0.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, 0.0,
            0.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, 0.0,
            0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0,
            -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
            -1.0, -0.5, 0.0, 0.25, 0.25, 0.0, -0.5, -1.0
        ],
        chess.BISHOP: [
            -1.0, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -1.0,
            -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
            -0.5, 0.0, 0.25, 0.5, 0.5, 0.25, 0.0, -0.5,
            -0.5, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -0.5,
            -0.5, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -0.5,
            -0.5, 0.0, 0.25, 0.5, 0.5, 0.25, 0.0, -0.5,
            -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
            -1.0, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -1.0
        ]
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
    print(f"Best move: {search(board)}")
#demo()

def demo_match():
    board = chess.Board(chess.STARTING_FEN)

    # player == white
    while(not board.is_game_over()):
        if (board.turn):
            try:
                player_move = chess.Move.from_uci(input("> "))
                if player_move not in board.legal_moves:
                    raise Exception("Move not legal!")
                else:
                    board.push(player_move)
            except Exception as e:
                print(f"{e}")

        else:
            move = search(board)
            print(f"Best move: {move}")
            board.push(chess.Move.from_uci(move))
demo_match()

# main window loop
#app = QtWidgets.QApplication(sys.argv)
#app.exec()
