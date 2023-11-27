# Motivation: I want to build a bot that knows how to play chess.
# I'm not good at chess, although I enjoy it. I think it'd
# be to sick to write a bot and put it on Lichess.org to get rated.
# Especially considering it'll probably be rated higher than me!

# NOTE What is my overarching goal? - To create a competitive bot on Lichess.org
#   How will that be achieved?
#   - Create a self sustaining bot that can play me, or itself in chess
#   - Connect bot to lichess api and play against opponents

# NOTE only designed for one match right now

# TODO List
#   [ ] - Authenticate
#   [ ] - Search for opponent
#   [ ] - Main Game Loop
#       [ ] - Search
#       [ ] - Evaluate
#       [ ] - Execute decisions
#   [ ] - Player interface
#       [ ] - Figure out how to let me play too
#   [ ] - Connect to lichess api
#       [ ] - Search/get matches
#       [ ] - Build a monitoring interface for a current match
#           [ ] - ...

import chess
import chess.pgn
import berserk
import json
import random
import time

#board = chess.Board()

session = berserk.TokenSession(json.load(open("token.json"))['token'])
client = berserk.Client(session)

current_match = None


def on_update(event, game_id):
    game_state = client.games.export(game_id, as_pgn=True)


def minimaxRoot(depth, board, isMaximizing):
    possibleMoves = board.legal_moves
    bestMove = -9999
    secondBest = -9999
    thirdBest = -9999
    bestMoveFinal = None
    for x in possibleMoves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        value = max(bestMove, minimax(depth - 1, board, not isMaximizing))
        board.pop()
        if( value > bestMove):
            print("Best score: " ,str(bestMove))
            print("Best move: ",str(bestMoveFinal))
            print("Second best: ", str(secondBest))
            thirdBest = secondBest
            secondBest = bestMove
            bestMove = value
            bestMoveFinal = move

    print(f"Best move final: {bestMoveFinal}")
    return bestMoveFinal


def minimax(depth, board, is_maximizing):
    if (depth == 0):
        return -evaluation(board)
    possibleMoves = board.legal_moves
    if(is_maximizing):
        bestMove = -9999
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = max(bestMove,minimax(depth - 1, board, not is_maximizing))
            board.pop()
        return bestMove
    else:
        bestMove = 9999
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = min(bestMove, minimax(depth - 1, board, not is_maximizing))
            board.pop()
        return bestMove


def evaluation(board):
    i = 0
    evaluation = 0
    x = True
    try:
        x = bool(board.piece_at(i).color)
    except AttributeError as e:
        x = x
    while i < 63:
        i += 1
        evaluation = evaluation + (getPieceValue(str(board.piece_at(i))) if x else -getPieceValue(str(board.piece_at(i))))
    #print(f"Evaluation: {evaluation}")
    return evaluation


def getPieceValue(piece):
    if(piece == None):
        return 0
    value = 0
    if piece == "P" or piece == "p":
        value = 10
    if piece == "N" or piece == "n":
        value = 30
    if piece == "B" or piece == "b":
        value = 30
    if piece == "R" or piece == "r":
        value = 50
    if piece == "Q" or piece == "q":
        value = 90
    if piece == 'K' or piece == 'k':
        value = 900
    #value = value if (board.piece_at(place)).color else -value
    return value


def minmax_move(fen, color):
    board = chess.Board(fen)

    move_number = get_move_number(fen)

    opening_moves_black = ["e7e5", "d7d5"]

    opening_moves_white = ["e2e4", "d2d4"]


    if move_number < 2:
        if color == "white":
            return random.choice(opening_moves_white)
        else:
            return random.choice(opening_moves_black)
    else:

        maximizing = False

        if color == "white":
            maximizing = True

        move = minimaxRoot(3, board, maximizing)
        print(move)
        return move


def get_move_number(fen):
    number = int(fen[-1])

    return number

def random_move(fen):
    board = chess.Board(fen)
    legal_moves = []
    moves = iter(board.legal_moves)
    for i in range(board.legal_moves.count()):
        legal_moves.append(next(moves))

    move = random.choice(legal_moves)
    print(legal_moves)
    print(move)
    return move

def get_ongoing_game():
    try:
        game = client.games.get_ongoing()[0]
        print(f"Game info: {game}")

        return game
    except Exception as e:
        print(f"No ongoing games found")

    return None

def play_lichess_game(token: str):
    # # Creating a session with the Lichess API using the provided token
    # session = berserk.TokenSession(token)
    #
    # # Creating a client object to interact with the Lichess API
    # client = berserk.Client(session)


    # Starting a new game with the Lichess API
    response = client.challenges.create_ai(
        clock_limit=600,  # Time limit for each player's moves (in seconds)
        clock_increment=0,  # Increment added to each player's clock after a move (in seconds)
        color="random",  # Randomly assign the color (white or black) to the player
        level=5  # Level of the AI opponent (ranging from 1 to 8)
    )

    # Extracting the game ID from the API response
    game_id = response["id"]

    # Printing the game ID to the console
    print(f"Game ID: {game_id}")

    game = get_ongoing_game()
    color = game['color']
    # status = client.games.export(game_id)['status']

    time.sleep(5)

    while True:
        time.sleep(2)
        game = get_ongoing_game()
        if game is not None:
            if game['isMyTurn'] == True:
                #move = random_move(game['fen'])
                move = minmax_move(game['fen'], color)
                # TODO Make the engine instead of random move
                try:
                    client.bots.make_move(game_id, move)
                except Exception as e:
                    print(f"Trouble making move: {e}")
            elif game['isMyTurn'] == False:
                time.sleep(2)
        else:
            break

    print("Game Over! (i think)")
    final_pgn = client.games.export(game_id, as_pgn=True)

    f = open("pgn.pgn", "w")
    f.write(final_pgn)
    f.close()

    final = chess.pgn.read_game(open("pgn.pgn"))
    board = final.board()
    print(board)
    print(board.outcome())



# Example usage of the play_lichess_game function
api_token = json.load(open("token.json"))['token']
play_lichess_game(api_token)