# Motivation: I want to build a bot that knows how to play chess.
# I'm not good at chess, although I enjoy it. I think it'd
# be to sick to write a bot and put it on Lichess.org to get rated.
# Especially considering it'll probably be rated higher than me!


import chess

board = chess.Board()

# NOTE What is my overarching goal? - To create a competitive bot on Lichess.org
#   How will that be achieved?
#   - Create a self sustaining bot that can play me, or itself in chess
#   - Connect bot to lichess api and play against opponents

# TODO List
#   [ ] - Authenticate
#   [ ] - Main Loop
#       [ ] - Search
#       [ ] - Evaluate
#       [ ] - Execute decisions
#   [ ] - Player interface
#       [ ] - Figure out how to let me play too
#   [ ] - Connect to lichess api
#       [ ] - Search/get matches
#       [ ] - Build a monitoring interface for a current match
#           [ ] - ...
