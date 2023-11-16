# Based off the tutorial: https://medium.com/dscvitpune/lets-create-a-chess-ai-8542a12afef

import chess

board = chess.board()


# Check for shit
if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
if board.is_stalemate():
        return 0
if board.is_insufficient_material():
        return 0
