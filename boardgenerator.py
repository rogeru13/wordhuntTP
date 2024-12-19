from cmu_graphics import *
import random


# creates a board and fills it with random letters
def generateBoard(boardLen):
    board = [[random.choice('AAAEEEIIOOTTBCDEFGHIJKLMNOPQRSTUVWXYZ') for row in range(boardLen)] for col in range(boardLen)] # added extra vowels for more common word generation
    return board

# checks if the board is valid
def generateValidBoard(legalWords, minWords=80):
    if app.boardLen == 2:
        minWords = 5
    if app.boardLen == 3:
        minWords = 30
    while True:
        board = generateBoard(app.boardLen)
        valid, foundWords = isLegalBoard(board, legalWords, minWords) # verifies board based on number of words
        if valid:
            return board, foundWords
    
def drawBoard(app):
    totalCells = app.boardLen  
    totalBorder = 60  
    border = totalBorder / (totalCells + 1)  # thickness
    cellInnerSize = (app.cellSize * 4 - totalBorder) / totalCells 
    cellCenters = [[None for _ in range(totalCells)] for _ in range(totalCells)] # for the red line

    # draws background 
    # loaded full image instead of separate assets in CMU graphics for efficiency purposes
    drawImage('images/boardbackground.png', app.width/2, app.height/2, align = "center") # designed in figma: https://www.figma.com/design/MdZN6ojTAYLTDaIlLjcJkc/Wordhunt---roger?node-id=0-1&node-type=canvas&t=Hb5hfmV195ld3ymW-0
    
    # draws black board background for border
    drawRect(app.boardLeft, app.boardTop, app.cellSize * 4, app.cellSize * 4, fill='black')

    # drawing full board
    for row in range(totalCells):
        for col in range(totalCells):
            # board coordinates
            x0 = app.boardLeft + col * (cellInnerSize + border) + border
            y0 = app.boardTop + row * (cellInnerSize + border) + border
            x1 = x0 + cellInnerSize
            y1 = y0 + cellInnerSize
            cellCenters[row][col] = ((x0 + x1)/2, (y0+y1)/2)
            
            # draws image cell
            drawImage("images/cell.png", x0, y0, width = x1-x0, height = y1-y0)

            # cell selection
            if (row, col) in app.selectedCells:
                drawImage("images/cellSelected.png", x0, y0, width = x1-x0, height = y1-y0)

            # if cell is a word
            if ((row, col) in app.selectedCells) and (app.currentWord in app.wordSet):
                if (app.currentWord not in app.userFoundWords):
                    # if it is a new one
                    drawImage("images/cellCorrect.png", x0, y0, width = x1-x0, height = y1-y0)
                else:
                    # if the word has already been added
                    drawImage("images/cellAlready.png", x0, y0, width = x1-x0, height = y1-y0)

            # draws letter on top of cells
            drawLabel(app.board[row][col], (x0 + x1) / 2, (y0 + y1) / 2, size=45, bold=True, font = 'Helvetica')

    # draws the red lines when the user selects a cell
    for i in range(len(app.selectedCells) - 1):
        row1, col1 = app.selectedCells[i]
        row2, col2 = app.selectedCells[i + 1]
        x1, y1 = cellCenters[row1][col1]
        x2, y2 = cellCenters[row2][col2]
        drawLine(x1, y1, x2, y2, fill='red', lineWidth=7)

    drawLabel(f'Time Left: {int(app.timer)}s', app.width / 2, 50, size=30, font = 'Peace Sans')

def drawScore(app):
    drawLabel(f'Score: {app.currentScore}', app.width/2, 100, size = 50, bold = True, font = 'Peace Sans')

def getCell(app, mouseX, mouseY):
    border = 40 # less than drawBoard border to make it easier to drag diagonally
    totalCells = app.boardLen
    cellSize = (app.cellSize * 4 - border * (totalCells + 1)) / totalCells

    # gets cell sizes for user to select
    for row in range(totalCells):
        for col in range(totalCells):
            x0 = app.boardLeft + col * (cellSize + border) + border
            y0 = app.boardTop + row * (cellSize + border) + border
            x1 = x0 + cellSize
            y1 = y0 + cellSize

            if x0 <= mouseX <= x1 and y0 <= mouseY <= y1:
                return row, col
    return None


# draws hint based on user inout
def drawHint(app):
    if app.hintGreen: # notifies user they have completed the hint
        if app.hintsRemaining > 1: 
            drawLabel(f'Good! {app.hintsRemaining} hints left!', 409, 830, align='center', fill='paleGreen', size=25, bold=True, font = 'Peace Sans')
        elif app.hintsRemaining == 1:
            drawLabel(f'Good! {app.hintsRemaining} hint left!', 409, 830, align='center', fill='paleGreen', size=25, bold=True, font = 'Peace Sans')
        else:
            drawLabel(f'Good! Out of hints.', 409, 830, align='center', fill='paleGreen', size=25, bold=True, font = 'Peace Sans')
            
    elif app.hintsRemaining == 0 and not app.hint:
        drawLabel('Out of hints.', 409, 830, align='center', fill='white', size=40, bold=True, font = 'Peace Sans')

    elif app.hint:
        hintLabel = app.hint[:app.letters] + "_ " * (len(app.hint) - app.letters)
        drawLabel(hintLabel, 410, 831, align = 'center', size = 30, fill = 'white', font = 'Peace Sans')

    else:
        drawLabel('Press h for hint.', 409, 830, align = 'center', size = 40, fill = 'white', font = 'Peace Sans')


# RECURSIVE BACKTRACKING

def isLegalBoard(board, legalWords, minWords):
    foundWords = set()

    for word in legalWords:
        if searchBoard(board, word):
            foundWords.add(word)
    
    return len(foundWords) >= minWords, foundWords

# searches full board
def searchBoard(board, word):
    for row in range(len(board)): # iterates through board
        for col in range(len(board[0])):
            if board[row][col] == word[0]: # checks to see if there is a word
                # calls recursive function
                if searchFromCell(board, word[1:], row, col, {(row, col)}):
                    return True
    return False

# searches from specific cell to see if there is a possible word
def searchFromCell(board, word, row, col, seen):
    if word == '':
        return True
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for drow, dcol in directions:
        # tests the cell
        newRow, newCol = row + drow, col + dcol
        if (0 <= newRow < len(board) and 0 <= newCol < len(board[0]) and
                (newRow, newCol) not in seen and board[newRow][newCol] == word[0]):
            # recursion
            if searchFromCell(board, word[1:], newRow, newCol, seen | {(newRow, newCol)}):
                return True
    return False




