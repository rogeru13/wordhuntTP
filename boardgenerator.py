from cmu_graphics import *
import random


# BOARD DRAWER

# def generateBoard(boardLen):
#     # creates an empty board that will be filled
#     return [["" for _ in range(boardLen)] for _ in range(boardLen)]

def generateBoard(boardLen):
    # Creates a board and fills it with random letters
    board = [[random.choice('AAAEEEIIOOTTBCDEFGHIJKLMNOPQRSTUVWXYZ') for row in range(boardLen)] for col in range(boardLen)] # added extra vowels for more common word generation
    return board

def generateValidBoard(legalWords, minWords=100):
    while True:
        board = generateBoard(app.boardLen)
        valid, foundWords = isLegalBoard(board, legalWords, minWords)
        if valid:
            return board, foundWords
    
def drawBoard(app):
    totalCells = app.boardLen  # boardLen
    totalBorder = 60  
    border = totalBorder / (totalCells + 1)  # thickness
    cellInnerSize = (app.cellSize * 4 - totalBorder) / totalCells 
    cellCenters = [[None for _ in range(totalCells)] for _ in range(totalCells)] # for the red line

    # draws background 
    drawImage('images/boardbackground.png', app.width/2, app.height/2, align = "center") # designed in figma: https://www.figma.com/design/MdZN6ojTAYLTDaIlLjcJkc/Wordhunt---roger?node-id=0-1&node-type=canvas&t=Hb5hfmV195ld3ymW-0
    
    # draws black board background for border
    drawRect(app.boardLeft, app.boardTop, app.cellSize * 4, app.cellSize * 4, fill='black')

    # drawing full board
    for row in range(totalCells):
        for col in range(totalCells):
            # calculates board coordinates
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
            drawLabel(app.board[row][col], (x0 + x1) / 2, (y0 + y1) / 2, size=45, bold=True, font = 'monospace')

    # draws the red lines when the user selects a cell
    for i in range(len(app.selectedCells) - 1):
        row1, col1 = app.selectedCells[i]
        row2, col2 = app.selectedCells[i + 1]
        x1, y1 = cellCenters[row1][col1]
        x2, y2 = cellCenters[row2][col2]
        drawLine(x1, y1, x2, y2, fill='red', lineWidth=7)

    drawLabel(f'Time Left: {int(app.timer)}s', app.width / 2, 50, size=30, bold=True)

def drawScore(app):
    drawLabel(f'Score: {app.currentScore}', app.width/2, 100, size = 50, bold = True)

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


# BOARD LETTER CREATOR

def searchFromCell(board, word, row, col, seen):
    if word == '':
        return True
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for drow, dcol in directions:
        newRow, newCol = row + drow, col + dcol
        if (0 <= newRow < len(board) and 0 <= newCol < len(board[0]) and
                (newRow, newCol) not in seen and board[newRow][newCol] == word[0]):
            if searchFromCell(board, word[1:], newRow, newCol, seen | {(newRow, newCol)}):
                return True
    return False

def isLegalBoard(board, legalWords, minWords):
    foundWords = set()

    for word in legalWords:
        if searchBoard(board, word):
            foundWords.add(word)
    
    return len(foundWords) >= minWords, foundWords

def searchBoard(board, word):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == word[0]:  
                if searchFromCell(board, word[1:], row, col, {(row, col)}):
                    return True
    return False

def drawHint(app):
    if app.hintGreen:
        if app.hintsRemaining > 1:
            drawLabel(f'Good! {app.hintsRemaining} hints left!', 409, 830, align='center', fill='paleGreen', size=25, bold=True)
        elif app.hintsRemaining == 1:
            drawLabel(f'Good! {app.hintsRemaining} hint left!', 409, 830, align='center', fill='paleGreen', size=25, bold=True)
        else:
            drawLabel(f'Good! Out of hints.', 409, 830, align='center', fill='paleGreen', size=25, bold=True)
            
    elif app.hintsRemaining == 0 and not app.hint:
        drawLabel('Out of hints.', 409, 830, align='center', fill='white', size=40, bold=True)

    elif app.hint:
        hintLabel = app.hint[:app.letters] + "_ " * (len(app.hint) - app.letters)
        drawLabel(hintLabel, 410, 831, align = 'center', size = 30, fill = 'white')

    # elif app.hintsRemaining >= 0:
    #     drawLabel('Press h for hint.', 409, 830, align = 'center', fill = 'white', size = 40)

    else:
        drawLabel('Press h for hint.', 409, 830, align = 'center', size = 40, fill = 'white')



# -------------------------------------------------------   OLD BOARD GENERATION ----------------------------------------------------------- #
 
# def generateValidBoard(wordSet, boardLen=4, minWords=20):
#     # generates a valid board with a minimum number of words
#     board = generateBoard(boardLen)
#     words = random.sample(list(wordSet), min(minWords, len(wordSet)))  # randomly select words from wordSet, from w3: https://www.w3schools.com/python/ref_random_sample.asp
#     print(f"Selected words: {words}")
    
#     if canPlaceWords(board, words, boardLen, 0, minWords):
#         fillEmptyCells(board, boardLen)
#         return board
#     return generateValidBoard(wordSet, boardLen, minWords)  # retry if board fails

# def findWordsOnBoard(board, wordSet):
#     boardLen = len(board)
#     foundWords = set()

#     # Helper function to extract a word in a given direction
#     def extractWord(row, col, drow, dcol):
#         word = ""
#         positions = []
#         while 0 <= row < boardLen and 0 <= col < boardLen:
#             word += board[row][col]
#             positions.append((row, col))
#             if word in wordSet:
#                 foundWords.add(word)  # Add valid word to foundWords
#             row += drow
#             col += dcol

#     # Iterate over each cell and extract words in all directions
#     for row in range(boardLen):
#         for col in range(boardLen):
#             directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
#             for drow, dcol in directions:
#                 extractWord(row, col, drow, dcol)

#     return foundWords

# def canPlaceWords(board, words, boardLen, index, minWords):
#     # if all the words are placed
#     if len(words) == index:
#         return True
    
#     word = words[index]
#     # accounts for words that will not fit on the board
#     if len(word)<=2:
#         return False
#     elif not hasValidStart(board, word, boardLen): 
#         return canPlaceWords(board, words, boardLen, index + 1, minWords)

#     # iterates through every starting point and direction for the word
#     for row in range(boardLen):
#         for col in range(boardLen):
#             locations = []
#             if placeWord(board, word, boardLen, row, col, 0, set(), locations):
#                 print(f"Placed word '{word}' at locations: {locations}")
#                 # recur to place the next word
#                 if canPlaceWords(board, words, boardLen, index + 1, minWords):
#                     return True
#                 # backtrack 
#                 removeWord(board, locations)
#                 print(f"Backtracked on word '{word}'")
#     return False

# def placeWord(board, word, boardLen, row, col, index, visited, locations):
#     # if all letters of word placed
#     if len(word) == index:
#         return True
    
#     # check bounds and constraints
#     if (row < 0 or row >= boardLen or col < 0 or col >= boardLen or
#         (board[row][col] != "" and (board[row][col] != word[index] or (row, col) not in visited)) or
#         (row, col) in visited):
#         return False
    
#     # places current letter
#     board[row][col] = word[index]
#     visited.add((row, col))
#     locations.append((row, col))

#     # randomizes directions for placement
#     directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
#     random.shuffle(directions) # code from w3: https://www.w3schools.com/python/ref_random_shuffle.asp

#     for drow, dcol in directions:
#         if placeWord(board, word, boardLen, row + drow, col + dcol, index + 1, visited, locations):
#             return True
    
#     # backtrack
#     board[row][col] = ""
#     visited.remove((row, col))
#     locations.pop()
#     return False

# def removeWord(board, locations):
#     # removes a word from the board for backtracking
#     for row, col in locations:
#         board[row][col] = ""

# def fillEmptyCells(board, boardLen):
#     # fills remaining empty spaces with random letters
#     for row in range(boardLen):
#         for col in range(boardLen):
#             if board[row][col] == "":
#                 board[row][col] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# # function that determine whether a words even fits initially in the board
# # shortcuts the excessive backtracking
# def hasValidStart(board, word, boardLen):
#     wordLen = len(word)
#     for row in range(boardLen):
#         for col in range(boardLen):
#             if canFit(board, wordLen, boardLen, row, col):
#                 return True
#     return False

# def canFit(board, wordLen, boardLen, row, col):
#     # checks all possible directions
#     directions = [
#         (-1, 0), (1, 0), (0, -1), (0, 1),(-1, -1), (-1, 1), (1, -1), (1, 1)]
#     for drow, dcol in directions:
#         if isSpaceAvailable(board, wordLen, boardLen, row, col, drow, dcol):
#             return True
#     return False

# def isSpaceAvailable(board, wordLen, boardLen, row, col, drow, dcol):
#     for i in range(wordLen):
#         newRow, newCol = row + i * drow, col + i * dcol
#         if newRow < 0 or newRow >= boardLen or newCol < 0 or newCol >= boardLen:
#             return False
#     return True


