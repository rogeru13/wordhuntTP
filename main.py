# Roger You
# 15112 F

from cmu_graphics import *
from boardGenerator import *
from homescreen import *
from scoreboard import *
from gameEndScreen import *
from drawNameInput import *
from customScreen import *
import random

def loadWordSet(filePath): # github citation https://github.com/dwyl/english-words/blob/master/read_english_dictionary.py (loading in a dictionary file) 
    wordSet = set()
    with open(filePath, 'r') as file:
        for line in file:
            word = line.strip()  # removes any extra spaces just in case
            if len(word) > 2 and len(word) < 10:  # Skips words that are less than 3 characters
                wordSet.add(word.upper())  # makes all of them uppercase
    return wordSet

def loadPlayerData():
    pass

def storeData(app):
    # locally update dictionary
    pass
    # add the csv file 

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
    app.game = False

    # buttons
    app.homeButtonList = [Button(250, 550, 350, 460, 'nameInput'), Button(250, 550, 495, 585, 'scoreboard'),
                      Button(250, 550, 625, 720, 'customSize')]
    app.homeButton = Button(216, 596, 678, 816, 'home')
    app.backButton = Button(594, 778, 838, 900, 'home')
    app.backButtonName = Button(27, 215, 22, 82, 'home')

    # timer
    app.timer = 60
    app.timerOn = False
    app.stepsPerSecond = 15

    # board initialization
    app.wordSet = loadWordSet('english.txt')
    app.board, app.boardWords = generateValidBoard(app.wordSet)
    
    # player name input
    app.playerName = ''
    app.nameDict = {}
    app.maxNameLength = 8

    # sizes
    app.cellSize = 145
    app.width = 804 # size of image from figma (self-designed) https://www.figma.com/design/MdZN6ojTAYLTDaIlLjcJkc/Wordhunt---roger?node-id=1-4&node-type=frame&t=1ri7PKyCdNK3MigY-0
    app.height = 943 
    app.boardLeft = app.width/2 - app.cellSize*2
    app.boardTop = app.height/2 - app.cellSize*2 + 100

    # scroll
    app.scrollOffsetRight = 0
    app.scrollOffsetLeft = 0
    app.wordHeight = 30  # word spacing

    # hint
    app.hint = ''
    app.hintsRemaining = 3
    app.letters = 0
    app.hintGreen = False  
    app.hintFlashTime = 0  

    # custom
    app.custom = False
    app.customSize = ''

    # difficulties
    app.mode = ''
    app.easyLower = 100
    app.easyHigher = 200
    app.mediumLower = 50
    app.mediumHigher = 100
    app.hardLower = 5
    app.hardHigher = 50
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
        drawHint(app)

    elif app.screen =='scoreboard':
        drawScoreboard(app)
    elif app.screen == 'gameEndScreen':
        drawGameEndScreen(app)
    elif app.screen == 'customSize':
        drawCustomScreen(app)
    elif app.screen == 'exitScreen':
        drawExitScreen(app)  

def onMousePress(app, mouseX, mouseY):
    print(mouseX,mouseY)
    # pressing the start button
    if app.screen == 'home':
        for Button in app.homeButtonList:
            if Button.isClicked(mouseX, mouseY):
                app.screen = Button.targetScreen
                # if app.screen == 'customSize':
                #     app.custom = True
                # else:
                #     app.custom = False
                print(app.screen)

        # if 250 <= mouseX <= 550 and 350 <= mouseY <= 460 and app.screen:
        #     app.screen = 'nameInput'
        # elif 250 <= mouseX <= 550 and 495 <= mouseY <= 585:
        #     app.screen = 'scoreboard'
        # elif 250 <= mouseX <= 550: and 314 <= mouse Y <= 457:
        #     app.screen = 'customSize'

    elif app.screen == 'gameEndScreen':
        if app.homeButton.isClicked(mouseX, mouseY):
            app.screen = app.homeButton.targetScreen

        # if 216 <= mouseX <= 596 and 678 <= mouseY <= 816:
        #     app.screen = 'home'

    elif app.screen == 'scoreboard':
        if app.backButton.isClicked(mouseX, mouseY):
            
            app.screen = 'home'
    
    elif app.screen == 'nameInput':
        if app.backButtonName.isClicked(mouseX, mouseY):
            app.screen = 'home'
    
    elif app.screen == 'customSize':
        if app.backButtonName.isClicked(mouseX, mouseY):
            app.screen = 'home'

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

    # define rectangle bounds for clarity
    leftBoxX = 50
    rightBoxX = app.width - 315
    boxY = 175
    boxWidth = app.width / 3
    boxHeight = app.height / 2.5
    rightScrollX = rightBoxX + boxWidth - 10
    leftScrollX = leftBoxX + boxWidth - 10
    scrollbarWidth = 10

    # help from Elena Li (TA) and Austin 

    # if the mouse in right scrollbar
    if rightScrollX <= mouseX <= rightScrollX + scrollbarWidth and boxY <= mouseY <= boxY + boxHeight:
        totalWordsHeightRight = len(app.boardWords) * app.wordHeight  # total height of all words
        relativePositionRight = (mouseY - boxY) / boxHeight #
        app.scrollOffsetRight = relativePositionRight * (totalWordsHeightRight - boxHeight)
        app.scrollOffsetRight = max(0, min(app.scrollOffsetRight, totalWordsHeightRight - boxHeight)) # hard sets height if you scroll too much

    # if the mouse in  left scrollbar
    elif leftScrollX <= mouseX <= leftScrollX + scrollbarWidth and boxY <= mouseY <= boxY + boxHeight:
        totalWordsHeightLeft = len(app.userFoundWords) * app.wordHeight  # Total height of all words
        relativePositionLeft = (mouseY - boxY) / boxHeight
        app.scrollOffsetLeft = relativePositionLeft * (totalWordsHeightLeft - boxHeight)
        app.scrollOffsetLeft = max(0, min(app.scrollOffsetLeft, totalWordsHeightLeft - boxHeight)) # hard sets height if you scroll too much 


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

    if app.screen == 'nameInput':
        if key == 'enter':
            if len(app.playerName) > 0:  # ensures the name is not empty
                if app.playerName not in app.nameDict:
                    app.nameDict[app.playerName] = 0  # initialize score for the player
                # game starts and board is created and reset
                if not app.custom:
                    app.boardLen = 4
                app.screen = 'board'
                app.game = True
                app.timerOn = True
                app.timer = 60
                app.hintsRemaining = 3
                app.currentScore = 0
                app.scrollOffsetRight = 0  
                app.scrollOffsetLeft = 0 
                app.currentWord = ''
                app.selectedCells= []
                app.userFoundWords = set()
                app.board, app.boardWords = generateValidBoard(app.wordSet)
                app.hint = ''
                app.letters = 0
        elif key == 'backspace':
            app.playerName = app.playerName[:-1]
        elif len(app.playerName) < app.maxNameLength:
            if len(key) == 1 and (key.isalpha()):
                app.playerName += key
    
    elif app.screen == 'board':
        if key == 'h' and not app.hintGreen:
            if app.hintsRemaining > 0:
                remainingWords = [word for word in app.boardWords if word not in app.userFoundWords]
                app.hint = random.choice(remainingWords) # CITE THIS BOI
                app.hintsRemaining -=1 
                app.letters = 0
            else:
                app.hint = ''
                
        elif key == 'e':
            app.timer = 1

    elif app.screen == 'customSize':
        if key == 'enter':
            if len(app.customSize) > 0:  # ensures the input is not empty
                if app.customSize.isdigit() and 2 <= int(app.customSize) <= 8:
                    # game starts and board is created and reset
                    # KEY CHANGE
                    app.boardLen = int(app.customSize)
                    app.customSize = ''
                    app.custom = True
                    app.screen = 'nameInput'
                    # app.game = True
                    # app.timerOn = True
                    # app.timer = 60
                    # app.hintsRemaining = 3
                    # app.currentScore = 0
                    # app.scrollOffsetRight = 0  
                    # app.scrollOffsetLeft = 0 
                    # app.currentWord = ''
                    # app.selectedCells= []
                    # app.userFoundWords = set()
                    # app.board, app.boardWords = generateValidBoard(app.wordSet)
                    # app.hint = ''
                    # app.letters = 0
        elif key == 'backspace':
            app.customSize = app.customSize[:-1]
        elif app.customSize == '':
            if key.isdigit():
                app.customSize += key

# timer functions, resets when hits 0
def onStep(app):
    if app.timerOn and app.timer > 0 and app.screen == 'board':
        app.timer -= 1/app.stepsPerSecond

        # check if enough time has passed to reveal another letter in the hint
        if app.hint and app.timer % 3 < (1 / app.stepsPerSecond) and not app.hintGreen:  # every 3 seconds
            app.letters = min(app.letters + 1, len(app.hint))  # increment revealed letters, capped at the hint length

        if app.hint != '' and app.hint in app.userFoundWords and not app.hintGreen:
            app.hintGreen = True
            app.hintFlashTime = 20
        
        if app.hintGreen:
            app.hintFlashTime -= 1
            if app.hintFlashTime <= 0:
                app.hintGreen = False
                app.hint = '' # check to see if '' works too
                app.letters = 0

        if app.timer <= 0:
            app.timer = 0
            app.timerOn = False
            app.game = False
            app.nameDict[app.playerName] = app.currentScore
            app.screen = 'gameEndScreen'
            app.playerName = ''
            app.hint = ''
            app.hintsRemaining = 3
            app.letters = 0
            app.custom = False
            print(app.nameDict)
        
def appReset(app):
    app.screen = 'board'
    app.game = True
    app.timerOn = True
    app.timer = 60
    app.hintsRemaining = 3
    app.currentScore = 0
    app.scrollOffsetRight = 0  
    app.scrollOffsetLeft = 0 
    app.currentWord = ''
    app.selectedCells= []
    app.userFoundWords = set()
    app.board, app.boardWords = generateValidBoard(app.wordSet)
    app.hint = ''
    app.letters = 0
    


def main():
    runApp()

main()
