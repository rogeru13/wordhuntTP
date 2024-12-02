from cmu_graphics import *
from cmu_graphics import pygameEvent

# Scroll wheel integration
def handlePygameEvent(event, callUserFn, app):
    if event.type == 1027:  # pygame.MOUSEWHEEL
        callUserFn('onMouseWheel', (event.x, event.y))

pygameEvent.connect(handlePygameEvent)


# def drawGameEndScreen(app):
#     # Background
#     drawImage('images/background.png', app.width / 2, app.height / 2, align='center')

#     # White Box
#     drawRect(app.boxLeftX, app.boxTopY, app.boxWidth, app.boxHeight, borderWidth=15, fill='white')

#     # Words and Scores
#     wordsStartY = app.boxTopY - app.scrollOffset  # Start from the offset position
#     visibleTop = app.boxTopY
#     visibleBottom = app.boxTopY + app.boxHeight

#     y = wordsStartY
#     for word in app.boardWords:
#         if visibleTop <= y <= visibleBottom - app.wordHeight:  # Render only visible words
#             score = len(word) * 100  # Calculate score
#             drawLabel(word, app.boxLeftX + 10, y, size=20, align='left', bold=True)
#             drawLabel(str(score), app.boxLeftX + app.boxWidth - 50, y, size=20, align='right', bold=True)
#         y += app.wordHeight

#     # Scrollbar
#     totalWordHeight = len(app.boardWords) * app.wordHeight
#     scrollbarHeight = min(app.boxHeight, app.boxHeight * app.boxHeight / totalWordHeight)
#     scrollbarY = app.boxTopY + (app.scrollOffset / totalWordHeight) * app.boxHeight
#     scrollbarX = app.boxLeftX + app.boxWidth - 20
#     drawRect(scrollbarX, scrollbarY, 10, scrollbarHeight, fill='black')

# ------- - - -- -- -- ----------

# def drawGameEndScreen(app):
#     # Background
#     drawImage('images/background.png', app.width / 2, app.height / 2, align='center')

#     # White Boxes
#     leftBoxX = 50
#     rightBoxX = app.width - 315
#     boxY = 175
#     boxWidth = app.width / 3
#     boxHeight = app.height / 2.5
#     borderWidth = 15

#     # text info
#     textMarginX = 40  # Left margin for text
#     textMarginY = 40  # Top margin for text
#     textStartX = rightBoxX + textMarginX
#     textStartY = boxY + textMarginY - app.cy  # Adjust with scroll offset
#     textLineHeight = 30  # Line height for words
#     textSize = 20  # Font size for words

#     # Draw white rectangles
#     drawRect(leftBoxX, boxY, boxWidth, boxHeight, borderWidth=borderWidth, fill='white')
#     drawRect(rightBoxX, boxY, boxWidth, boxHeight, borderWidth=borderWidth, fill='white')

#     startY = app.cy
#     for word in app.boardWords:
#         if boxY <= startY <= boxY + boxHeight:
#             drawLabel(word, textStartX, startY, size=textSize, align='left', fill='black')
#         startY += textMarginY

# ----- COPY ------# 

# def drawGameEndScreen(app):

#     # Background
#     drawImage('images/background.png', app.width / 2, app.height / 2, align='center')

#     # White Boxes
#     leftBoxX = 50
#     rightBoxX = app.width - 315
#     boxY = 175
#     boxWidth = app.width / 3
#     boxHeight = app.height / 2.5
#     borderWidth = 15

#     # boxes for word lists
#     drawRect(leftBoxX, boxY, boxWidth, boxHeight, borderWidth=borderWidth, fill='white')
#     drawRect(rightBoxX, boxY, boxWidth, boxHeight, borderWidth=borderWidth, fill='white')


#     textStartY = boxY + 20 - app.scrollOffset  # Start text with offset
#     i = 0
#     for word in app.userFoundWords:
#         currentY = textStartY + i * app.wordHeight  # Spaced words
#         if boxY <= currentY <= boxY + boxHeight - app.wordHeight:  # Only visible words
#             drawLabel(word, leftBoxX + 10, currentY, size=20, align='left', fill='black')
#         i += 1

#     textMarginX = 40  
#     textMarginY = 40  
#     textStartX = rightBoxX + textMarginX
#     textStartY = boxY + textMarginY - app.scrollOffset  
#     textLineHeight = 30  
#     textSize = 20  

#     i = 0
#     for word in app.boardWords:
#         currentY = textStartY + i * textLineHeight
#         if boxY + 20 < currentY  < boxY + boxHeight - 50:  # Only draw visible text
#             score = len(word) * 100  # Calculate score dynamically
#             drawLabel(word, textStartX, currentY, size=textSize, align='left', fill='black')
#             drawLabel(str(score), textStartX + 150, currentY, size=textSize, align='left', fill='black')
#         i += 1  # Increment the manual counter

#     # Scrollbar
#     scrollbarX = rightBoxX + boxWidth - 10  # Right side of the box
#     scrollbarY = boxY
#     scrollbarWidth = 20
#     scrollbarHeight = boxHeight

#     # These following lines for implementing the scroll bar are from OpenAI (ChatGPT.com)
    
#     totalWordsHeight = len(app.boardWords) * textLineHeight 
#     if totalWordsHeight > boxHeight:
#         thumbHeight = max(30, boxHeight * boxHeight / totalWordsHeight)  # Minimum thumb size
#         thumbY = scrollbarY + (app.scrollOffset / totalWordsHeight) * boxHeight
#         drawRect(scrollbarX, scrollbarY, scrollbarWidth, scrollbarHeight, fill='lightgray')
#         drawRect(scrollbarX, thumbY, scrollbarWidth, thumbHeight, fill='black')

def drawGameEndScreen(app):
    # Background
    drawImage('images/background.png', app.width / 2, app.height / 2, align='center')

    # Define rectangles
    leftBoxX = 50
    rightBoxX = app.width - 315
    boxY = 175
    boxWidth = app.width / 3
    boxHeight = app.height / 2.5
    borderWidth = 15

    # Draw white rectangles
    drawRect(leftBoxX, boxY, boxWidth, boxHeight, borderWidth=borderWidth, fill='white')
    drawRect(rightBoxX, boxY, boxWidth, boxHeight, borderWidth=borderWidth, fill='white')

    # Left Rectangle: User Found Words
    textStartY = boxY + 20 - app.scrollOffset  # Start text with offset
    i = 0
    for word in app.userFoundWords:
        currentY = textStartY + i * app.wordHeight  # Spaced words
        if boxY <= currentY <= boxY + boxHeight - app.wordHeight:  # Only visible words
            drawLabel(word, leftBoxX + 10, currentY, size=20, align='left', fill='black')
        i += 1

    # Right Rectangle: Board Words with Scores
    textStartY = boxY + 20 - app.scrollOffset  # Start text with offset
    i = 0
    for word in app.boardWords:
        currentY = textStartY + i * app.wordHeight  # Spaced words
        if boxY <= currentY <= boxY + boxHeight - app.wordHeight:  # Only visible words
            score = len(word) * 100  # Calculate score dynamically
            drawLabel(word, rightBoxX + 10, currentY, size=20, align='left', fill='black')
            drawLabel(str(score), rightBoxX + boxWidth - 50, currentY, size=20, align='right', fill='black')
        i += 1

    # Draw scrollbars
    drawScrollBar(app, leftBoxX + boxWidth - 10, boxY, boxHeight, len(app.userFoundWords))
    drawScrollBar(app, rightBoxX + boxWidth - 10, boxY, boxHeight, len(app.boardWords))


def drawScrollBar(app, x, y, height, totalItems):
    # Calculate scrollbar dimensions
    totalContentHeight = totalItems * app.wordHeight
    if totalContentHeight > height:  # Only draw scrollbar if content overflows
        scrollbarHeight = max(30, height * height / totalContentHeight)  # Thumb size
        thumbY = y + (app.scrollOffset / totalContentHeight) * height
        drawRect(x, y, 10, height, fill='lightgray')  # Scrollbar background
        drawRect(x, thumbY, 10, scrollbarHeight, fill='black')  # Scrollbar thumb
