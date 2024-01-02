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
import chess
import chess.pgn
import chess.svg
import berserk # lichess api
from PySide6 import QtCore, QtWidgets, QtGui

# main window loop
app = QtWidgets.QApplication(sys.argv)

app.exec()
