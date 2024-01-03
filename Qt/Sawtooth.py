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
from PySide6 import QtCore, QtWidgets, QtGui


# Get board evaluation
def evaluate_board(board):
    score = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if piece is not None:
            value = {
                chess.PAWN: 1,
                chess.KNIGHT: 3,
                chess.BISHOP: 3,
                chess.ROOK: 5,
                chess.QUEEN: 9,
                chess.KING: 0  # Assuming kings have no material value for basic evaluation
            }.get(piece.piece_type, 0)

            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value

    return score

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
board = chess.Board(fen)
print("Board Evaluation:", evaluate_board(board))

# main window loop
#app = QtWidgets.QApplication(sys.argv)
#app.exec()
