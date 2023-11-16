# Based off the tutorial: https://healeycodes.com/building-my-own-chess-engine

import chess

piece_values = {
    chess.PAWN: 100,
    chess.ROOK: 500,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.QUEEN: 900,
    chess.KING: 20000
}

board = chess.Board(chess.STARTING_FEN)
white_material = 0
black_material = 0

for square in chess.SQUARES:
    piece = board.piece_at(square)
    if not piece:
        continue
    if piece.color == chess.WHITE:
        white_material += piece_values[piece.piece_type]
    else:
        black_material += piece_values[piece.piece_type]
