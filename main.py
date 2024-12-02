# Roger You
# 15112 F

from cmu_graphics import *
from boardGenerator import *
from homescreen import *
from scoreboard import *
from gameEndScreen import *
from drawNameInput import *

def loadWordSet(filePath): # github citation https://github.com/dwyl/english-words/blob/master/read_english_dictionary.py (loading in a dictionary file)
    wordSet = set()
    with open(filePath, 'r') as file:
        for line in file:
            word = line.strip()  # removes any extra spaces
            if len(word) > 2 and len(word) < 10:  # Skips words that are less than 3 characters
                wordSet.add(word.upper())  # makes all of them uppercase
    return wordSet

def onAppStart(app):
    # initializes random board with at least 20 words
    app.screen = "home"

    #USER ADJUSTABLE
    app.boardLen = 4
    app.minWords = 3
    app.selectedCells= []
    app.currentWord = ''
    app.userFoundWords = set()
    app.currentScore = 0
    app.overallScores = []
    app.game = False

    # timer
    app.timer = 60
    app.timerOn = False
    app.stepsPerSecond = 15

    # board initialization
    app.wordSet = loadWordSet('english.txt')
    app.board, app.boardWords = generateValidBoard(app.wordSet)
    
    # player names
    app.playerName = ""
    app.nameDict = {}
    app.maxNameLength = 10

    # sizes
    app.cellSize = 145
    app.width = 804 # size of image from figma (self-designed) https://www.figma.com/design/MdZN6ojTAYLTDaIlLjcJkc/Wordhunt---roger?node-id=1-4&node-type=frame&t=1ri7PKyCdNK3MigY-0
    app.height = 943 
    app.boardLeft = app.width/2 - app.cellSize*2
    app.boardTop = app.height/2 - app.cellSize*2 + 100

    # scroll
    app.scrollOffset = 0
    app.scrollOffset2 = 0

    app.scrollSpeed = 20

    app.boxLeftX = app.width - 315
    app.boxTopY = 175
    app.boxWidth = app.width / 3
    app.boxHeight = app.height / 2.5
    app.wordHeight = 30  # Word spacing

# ------------------------------------------------------- SIZE ADJUSTMENT -------------------------------------------------------- #

def updateBoardPosition(app):
    # in case of resize 
    app.boardLeft = app.width / 2 - (app.cellSize * 2)
    app.boardTop = app.height / 2 - (app.cellSize * 2)
    
def onResize(app):
    updateBoardPosition(app)

# ---------------------------------------------------------- USER INPUT -------------------------------------------------------- #

def redrawAll(app):
    # print(f"Current screen: {app.screen}") 
    if app.screen == 'home':
        drawHome(app)
    elif app.screen == 'nameInput':
        drawNameInputScreen(app)
    elif app.screen == 'board':
        drawBoard(app)
        drawScore(app)
    elif app.screen =='scoreboard':
        drawScoreboard(app)
    elif app.screen == 'gameEndScreen':
        drawGameEndScreen(app)

def onMousePress(app, mouseX, mouseY):
    print(mouseX,mouseY)
    # pressing the start button
    if app.screen == 'home':
        if 250 <= mouseX <= 550 and 350 <= mouseY <= 460 and app.screen:
            app.screen = 'nameInput'
        elif 250 <= mouseX <= 550 and 495 <= mouseY <= 585:
            app.screen = 'scoreboard'
   
    # elif app.screen == 'board':
    #     app.screen = 'board'
    #     app.game = True
    #     app.timerOn = True
    #     app.timer = 60
    #     app.currentScore = 0
    #     app.scrollOffset = 0  # Reset scroll offset for new game
    #     app.currentWord = ''
    #     app.userFoundWords = set()
    #     app.board, app.boardWords = generateValidBoard(app.wordSet)

    # reset the selected cells and word
    if app.game:
        app.currentWord = ''
        app.selectedCells = []
        # add the first cell clicked
        cell = getCell(app, mouseX, mouseY)
        if cell != None:
            app.selectedCells.append(cell)
            row, col = cell
            app.currentWord += app.board[row][col]

def onMouseDrag(app, mouseX, mouseY):
    if app.game:
        # grabs row and col of cell
        cell = getCell(app, mouseX, mouseY) 
        if len(app.selectedCells) >= 1:
            # Get the last selected cell
            lastRow, lastCol = app.selectedCells[-1]
        # checking if the mouse is on an actual cell
        
        if cell is not None:
            # if the cell is in selectedCells
            if len(app.selectedCells) > 1 and cell == app.selectedCells[-2]:
                # removes the last cell to allow going backwards
                app.selectedCells.pop()
                app.currentWord = app.currentWord[:-1]  # removes last letter from the word

            # if the cell has not been selected
            elif cell not in app.selectedCells:
                currentRow, currentCol = cell

                # add cell if it is adjacent 
                if len(app.selectedCells) == 0 or (
                    abs(currentRow - lastRow) <= 1 and abs(currentCol - lastCol) <= 1):
                    app.selectedCells.append(cell)
                    app.currentWord += app.board[currentRow][currentCol]


    leftBoxX = 50
    rightBoxX = app.width - 315
    boxY = 175
    boxWidth = app.width / 3
    boxHeight = app.height / 2.5
    rightScrollbarX = rightBoxX + boxWidth - 10
    leftScrollbarX = leftBoxX + boxWidth - 10
    scrollbarWidth = 10

# -------- READ OVER THIS BOI ---------- #
    if rightScrollbarX <= mouseX <= rightScrollbarX + scrollbarWidth and boxY <= mouseY <= boxY + boxHeight:
        # Calculate new scroll offset based on mouse position
        totalWordsHeight = len(app.boardWords) * 30  # Total height of all words
        relativePosition = (mouseY - boxY) / boxHeight
        app.scrollOffset = relativePosition * (totalWordsHeight - boxHeight)
        app.scrollOffset = max(0, min(app.scrollOffset, totalWordsHeight - boxHeight))  # Clamp value


    elif leftScrollbarX <= mouseX <= (leftScrollbarX + scrollbarWidth) and boxY <= mouseY <= boxY + boxHeight:
        # Calculate new scroll offset based on mouse position
        totalWordsHeight2 = len(app.userFoundWords) * 30  # Total height of all words
        relativePosition2 = (mouseY - boxY) / boxHeight
        app.scrollOffset2 = relativePosition2 * (totalWordsHeight2 - boxHeight)
        app.scrollOffset2 = max(0, min(app.scrollOffset2, totalWordsHeight2 - boxHeight))  # Clamp value


def onMouseRelease(app, mouseX, mouseY):
    # adds word to userFoundWords and score 
    if app.game:
        if ((app.currentWord in app.wordSet) and (app.currentWord not in app.userFoundWords)):
            app.userFoundWords.add(app.currentWord)
            app.currentScore += len(app.currentWord) * 100
            print(f"Word found: {app.currentWord} | Score: {app.currentScore}")
        else:
            print(f"Invalid word: {app.currentWord}")
        # resets selections
        app.selectedCells = []
        app.currentWord = ''

def onKeyPress(app, key):
    if app.screen == "nameInput":
        if key == "enter":
                # Transition to the game screen and reset the board
                app.screen = "board"
                app.game = True
                app.timerOn = True
                app.timer = 60
                app.currentScore = 0
                app.scrollOffset = 0  # Reset scroll offset for new game
                app.currentWord = ''
                app.userFoundWords = set()
                app.board, app.boardWords = generateValidBoard(app.wordSet)

    if key == "space":
        app.screen = "board"
    elif key == "l":
        app.screen = "home"
    elif key == 'e':
        app.timer = 1

def onStep(app):
    if app.timerOn and app.timer > 0 and app.screen == 'board':
        app.timer -= 1/app.stepsPerSecond
        if app.timer <= 0:
            app.timer = 0
            app.timerOn = False
            app.overallScores.append(app.currentScore)
            app.screen = 'gameEndScreen'
        

def main():
    runApp()

main()
