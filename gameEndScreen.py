from cmu_graphics import *


def drawGameEndScreen(app):
    # background and text
    drawImage('images/postGameScreen.png', app.width / 2, app.height / 2, align='center')

    # rect bounds
    leftBoxX = 50
    rightBoxX = app.width - 315
    boxY = 175
    boxWidth = app.width / 3
    boxHeight = app.height / 2.5
    borderWidth = 15

    drawRect(leftBoxX, boxY, boxWidth, boxHeight, borderWidth=borderWidth, fill='white')
    drawRect(rightBoxX, boxY, boxWidth, boxHeight, borderWidth=borderWidth, fill='white')

    # left rectangle with words
    textStartY = boxY + 20 - app.scrollOffsetLeft  # start text with offset
    i = 0
    for word in app.userFoundWords:
        currentYLeft = textStartY + i * app.wordHeight  # current word position
        if boxY + 20 <= currentYLeft <= boxY + boxHeight - app.wordHeight:  # only draws the word if it is within the rectangle bounds
            scoreFound = len(word) * 100 
            drawLabel(word, leftBoxX + 10, currentYLeft, size=20, align='left', fill='black') # draws word
            drawLabel(str(scoreFound), leftBoxX + boxWidth - 50, currentYLeft, size=20, align='right', fill='black') # draws score

        i += 1

    # right rectangles with words
    textStartY = boxY + 20 - app.scrollOffsetRight 
    j = 0
    for word in app.boardWords:
        currentY = textStartY + j * app.wordHeight  
        if boxY + 20 <= currentY <= boxY + boxHeight - app.wordHeight:  
            scoreBoard = len(word) * 100  
            drawLabel(word, rightBoxX + 10, currentY, size=20, align='left', fill='black')
            drawLabel(str(scoreBoard), rightBoxX + boxWidth - 50, currentY, size=20, align='right', fill='black')
        j += 1

    # draw actual scrollbar
    drawScrollBar(app, leftBoxX + boxWidth - 10, boxY, boxHeight, len(app.userFoundWords), app.scrollOffsetLeft)
    drawScrollBar(app, rightBoxX + boxWidth - 10, boxY, boxHeight, len(app.boardWords), app.scrollOffsetRight)

# Help from Elena Li (TA) and Austin 
def drawScrollBar(app, x, y, height, totalItems, scrollOffset):
    # scrollbar dimensions
    totalContentHeight = totalItems * app.wordHeight
    if totalContentHeight > height:  # only draws if the words are longer than the box
        scrollbarHeight = max(app.wordHeight, height * height / totalContentHeight)  # size
        thickY = y + (scrollOffset / totalContentHeight) * height
        drawRect(x, y, 17, height, fill='lightgray')  # scrollbar background
        drawRect(x, thickY, 17, scrollbarHeight, fill='black')  # scrollbar thumb
