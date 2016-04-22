from slackclient import SlackClient
import time  # time for sleep between polls
import json  # json for parse the rtm_read() data
import sys
import random

# create listOfMoves to prevent duplicate moves
listOfMoves = []
listOfMoves.append("")
listOfMoves.append(" ")

# Slack API token
with open('token.json') as api_key:
    api_key = json.load(api_key)
    token = api_key["token"]

# create an instance of a slack client
sc = SlackClient(token)

# send a test messgae
sc.api_call("api.test")
sc.api_call("channels.info", channel="1234567890")


# draw new written board and send
def drawWrittenBoard(board):
    boardString = "               GAMEBOARD\n"
    # This function prints out the board that it was passed. Returns None
    HLINE = '  +---+---+---+---+---+---+---+---+\n'
    VLINE = '  |   |   |   |   |   |   |   |   |\n'

    boardString += '    1   2   3   4   5   6   7   8\n'
    boardString += HLINE
    for y in range(8):
        boardString += (str(y+1) + ' ')
        for x in range(8):
            boardString += '| ' + str(board[x][y]) + ' '
        boardString += '|\n' + HLINE
    # Send the board string.
    sc.api_call(
        "chat.postMessage", channel="#general", text='```'+ boardString+'```',
        username='gamebot', icon_emoji=':robot_face:'
    )

# draw new board and send
def drawBoard(board):
    boardString = "               GAMEBOARD\n"
    # This function prints out the board that it was passed. Returns None

    boardString += ':robot_face::one::two::three::four::five::six::seven::eight:\n'
    for y in range(8):
        if y == 0:
            boardString += ":one:"
        elif y == 1:
            boardString += ":two:"
        elif y == 2:
            boardString += ":three:"
        elif y == 3:
            boardString += ":four:"
        elif y == 4:
            boardString += ":five:"
        elif y == 5:
            boardString += ":six:"
        elif y == 6:
            boardString += ":seven:"
        elif y == 7:
            boardString += ":eight:"
        for x in range(8):
            if board[x][y] == ' ':
                boardString += ':' + 'white_square' + ':'
            elif board[x][y] == '.':
                boardString += ':' + 'wink' + ':'
            else:
                boardString += ':' + str(board[x][y]) + ':'
        boardString += '\n'
    # Send the board string.
    sc.api_call(
        "chat.postMessage", channel="#general", text=boardString,
        username='gamebot', icon_emoji=':robot_face:'
    )

def getSmartComputerMove(board, computerTile, playerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)
    # randomize the order of the possible moves
    random.shuffle(possibleMoves)
    # always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]
    # Go through all the possible moves and remember the best scoring move
    bestScore = -1
    bestMove = [-1,-1]
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        nextMove = getComputerMove(dupeBoard, playerTile)
        makeMove(dupeBoard, playerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove

def resetBoard(board):
    # Blanks out the board it is passed, except for the original starting position.
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '

    # Starting pieces:
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'


def getNewBoard():
    # Creates a brand new, blank board data structure.
    board = []
    for i in range(8):
        board.append([' '] * 8)

    return board


def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if board[xstart][ystart] != ' ':
        return False
    elif not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile  # temporarily set the tile on the board.

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection  # first step in the direction
        y += ydirection  # first step in the direction
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):  # break out of while loop, then continue in for loop
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = ' '  # restore the empty space
    if len(tilesToFlip) == 0:  # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= 7 and y >= 0 and y <= 7


def getBoardWithValidMoves(board, tile):
    # Returns a new board with . marking the valid moves the given player can make.
    dupeBoard = getBoardCopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'
    return dupeBoard


def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves


def getScoreOfBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}


def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    sc.api_call(
        "chat.postMessage", channel="#general",
        text='Do you want to play again? (yes or no)',
        username='gamebot', icon_emoji=':robot_face:'
    )
    # Get the player move from slack.
    data = json.loads(sc.api_call("channels.history", channel="C0N84ELPN", count=1))
    playAgain = data["messages"][0]["text"]
    return playAgain.lower().startswith('y')


def makeMove(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move, True if it is valid.

    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip is False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def getBoardCopy(board):
    # Make a duplicate of the board list and return the duplicate.
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]

    return dupeBoard


def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


def getPlayerMove(board, playerTile):

    sc.api_call(
        "chat.postMessage", channel="#general", text='Enter your move, or type quit to end the game, or hints to turn off/on hints.',
        username='gamebot', icon_emoji=':robot_face:'
    )

    # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()

    validMove = False
    
    while not validMove:

        # Get the player move from slack.
        data = json.loads(sc.api_call("channels.history", channel="C0N84ELPN", count=1))
        move = data["messages"][0]["text"]

        if move not in listOfMoves and len(move) <= 5:
            listOfMoves.append(move)

            if move == 'quit':
                return 'quit'
            if move == 'hints':
                listOfMoves.remove('hints')
                return 'hints'

            if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
                y = int(move[0]) - 1
                x = int(move[1]) - 1
                if isValidMove(board, playerTile, x, y) == False:
                    sc.api_call(
                        "chat.postMessage", channel="#general",
                        text='That is not a valid move. Type the x digit (1-8), then the y digit (1-8).',
                        username='gamebot', icon_emoji=':robot_face:'
                    )
                    sc.api_call(
                        "chat.postMessage", channel="#general",
                        text='For example, 81 will be the bottom-right corner.',
                        username='gamebot', icon_emoji=':robot_face:'
                    )
                    listOfMoves.remove(move)
                else:
                    validMove = True
            

    return [x, y]


def getComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)

    # randomize the order of the possible moves
    random.shuffle(possibleMoves)

    # always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    # Go through all the possible moves and remember the best scoring move
    bestScore = -1
    bestMove = [-1,-1]
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score

    return bestMove


def showPoints(playerTile, computerTile, mainBoard):
    # Prints out the current score.
    scores = getScoreOfBoard(mainBoard)
    output = 'You have ' + str(scores[playerTile]) + ' points. The computer has ' + str(scores[computerTile]) + ' points.'

    sc.api_call(
        "chat.postMessage", channel="#general", text=output,
        username='gamebot', icon_emoji=':robot_face:'
    )


# PLAY GAME
def playReversi():
    while True:

        # Reset the board and game.
        mainBoard = getNewBoard()
        resetBoard(mainBoard)
        playerTile = 'X'
        computerTile = 'O'
        showHints = False

        # choose who goes first
        turn = whoGoesFirst()
        output = 'The ' + turn + ' will go first.'
        sc.api_call(
            "chat.postMessage", channel="#general", text=output,
            username='gamebot', icon_emoji=':robot_face:'
        )

        while True:
            # Player's turn
            if turn == 'player':

                # display hints or not
                if showHints:
                    validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(mainBoard)

                showPoints(playerTile, computerTile, mainBoard)

                # get player move
                move = getPlayerMove(mainBoard, playerTile)
                if move == 'quit':
                    sc.api_call(
                        "chat.postMessage", channel="#general", text = 'Thanks for playing!',
                        username='gamebot', icon_emoji=':robot_face:'
                    )
                    sys.exit()
                elif move == 'hints':
                    showHints = not showHints
                    continue
                else:
                    makeMove(mainBoard, playerTile, move[0], move[1])

                # end game or change to computer's turn
                if getValidMoves(mainBoard, computerTile) == []:
                    break
                else:
                    turn = 'computer'

            # Computer's turn
            else:
                drawBoard(mainBoard)
                showPoints(playerTile, computerTile, mainBoard)
                x, y = getComputerMove(mainBoard, computerTile)
                makeMove(mainBoard, computerTile, x, y)

                # end game or change to player's turn
                if getValidMoves(mainBoard, playerTile) == []:
                    break
                else:
                    turn = 'player'

        # Display the final scores
        drawBoard(mainBoard)
        scores = getScoreOfBoard(mainBoard)
        output = 'X scored ' + str(scores['X']) + ' points. O scored ' + str(scores['O']) + ' points.'
        sc.api_call(
            "chat.postMessage", channel="#general", text = output,
            username='gamebot', icon_emoji=':robot_face:'
        )
        # Player won 
        if scores[playerTile] > scores[computerTile]:
            output = 'You beat the computer by ' + str(scores[playerTile] - scores[computerTile]) + ' points! Congratulations!'
            sc.api_call(
                "chat.postMessage", channel="#general", text = output,
                username='gamebot', icon_emoji=':robot_face:'
            )
        # Computer won
        elif scores[playerTile] < scores[computerTile]:
            output = 'The computer beat you by ' + str(scores[computerTile] - scores[playerTile]) + ' points.'
            sc.api_call(
                "chat.postMessage", channel="#general", text = output,
                username='gamebot', icon_emoji=':robot_face:'
            )
        # Tie
        else:
            sc.api_call(
                "chat.postMessage", channel="#general", text = 'The game was a tie!',
                username='gamebot', icon_emoji=':robot_face:'
            )

        if not playAgain():
            break


def print_menu():
    '''print menu to channel'''

    menu = "Hi and welcome to Slackbot Games! The first game is Reversi! \n"
    menu += "You are player X.\n"

    sc.api_call(
        "chat.postMessage", channel="#general", text = menu,
        username='gamebot', icon_emoji=':robot_face:'
    )


def main():
    # print the menu
    print_menu()
    # play reversi
    playReversi()

main()
