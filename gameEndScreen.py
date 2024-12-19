from cmu_graphics import *


def drawGameEndScreen(app):
    # background and text
    drawImage('images/endGameScreen.png', app.width / 2, app.height / 2, align='center') # loaded full image instead of separate pngs for efficiency purposes
    drawMiniBoard(app)
    
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
    sortedUserWords = sorted(app.userFoundWords)
    for word in sortedUserWords:
        currentYLeft = textStartY + i * app.wordHeight  # current word position
        if boxY + 20 <= currentYLeft <= boxY + boxHeight - app.wordHeight:  # only draws the word if it is within the rectangle bounds
            scoreFound = len(word) * 100 
            drawLabel(word, leftBoxX + 10, currentYLeft, size=20, align='left', fill='black') # draws word
            drawLabel(str(scoreFound), leftBoxX + boxWidth - 50, currentYLeft, size=20, align='right', fill='black') # draws score

        i += 1

    # right rectangles with words
    textStartY = boxY + 20 - app.scrollOffsetRight 
    j = 0
    sortedBoardWords = sorted(app.missingWords)
    for word in sortedBoardWords:
        currentY = textStartY + j * app.wordHeight  
        if boxY + 20 <= currentY <= boxY + boxHeight - app.wordHeight:  
            scoreBoard = len(word) * 100  
            drawLabel(word, rightBoxX + 10, currentY, size=20, align='left', fill='black')
            drawLabel(str(scoreBoard), rightBoxX + boxWidth - 50, currentY, size=20, align='right', fill='black')
        j += 1

    # draw actual scrollbar
    drawScrollBar(app, leftBoxX + boxWidth - 10, boxY, boxHeight, len(app.userFoundWords), app.scrollOffsetLeft)
    drawScrollBar(app, rightBoxX + boxWidth - 10, boxY, boxHeight, len(app.missingWords), app.scrollOffsetRight)

# help from Elena Li (TA) and Austin 
def drawScrollBar(app, x, y, height, totalItems, scrollOffset):
    # scrollbar dimensions
    totalContentHeight = totalItems * app.wordHeight
    if totalContentHeight > height:  # only draws if the words are longer than the box
        scrollbarHeight = max(app.wordHeight, height * height / totalContentHeight)  # size
        thickY = y + (scrollOffset / totalContentHeight) * height
        drawRect(x, y, 17, height, fill='lightgray')  # scrollbar background
        drawRect(x, thickY, 17, scrollbarHeight, fill='black')  # scrollbar thumb


def drawMiniBoard(app):
    miniBoardSize = 275
    miniBorder = 12 - app.boardLen  # adjust border for smaller cells
    miniCellSize = (miniBoardSize - (app.boardLen + 1) * miniBorder) / app.boardLen

    miniLeft = 50
    miniTop = app.height - miniBoardSize - 20 

    # draw black background for mini-board
    drawRect(miniLeft, miniTop, miniBoardSize, miniBoardSize, fill='black')

    # draw the full board
    for row in range(app.boardLen):
        for col in range(app.boardLen):
            x0 = miniLeft + col * (miniCellSize + miniBorder) + miniBorder
            y0 = miniTop + row * (miniCellSize + miniBorder) + miniBorder
            # draw cells
            drawImage("images/cell.png", x0, y0, width=miniCellSize, height=miniCellSize)

            # draw letters
            drawLabel(app.board[row][col], x0 + miniCellSize / 2, y0 + miniCellSize / 2,
                      size=16 - app.boardLen, bold=True, font="Helvetica")

    # iterates through every word
    if app.miniWordIndex < len(app.missingWords):
        word = app.missingWordsList[app.miniWordIndex]
        path = getWordPath(app.board, word)

        # draw cells green along the red line
        for i in range(app.miniLine + 1):
            if i < len(path):
                row, col = path[i]
                #  cell coordinates for  path
                x0 = miniLeft + col * (miniCellSize + miniBorder) + miniBorder
                y0 = miniTop + row * (miniCellSize + miniBorder) + miniBorder
                x1 = x0 + miniCellSize
                y1 = y0 + miniCellSize

                # draw highlighted cell 
                drawImage("images/cellCorrect.png", x0, y0, width=miniCellSize, height=miniCellSize)
                #draws letter on top
                drawLabel(app.board[row][col], (x0 + x1) / 2, (y0 + y1) / 2, size=16 - app.boardLen, bold=True, font='Helvetica')

        # draw the missing word label
        drawLabel(f'Missing: {word}', miniLeft + miniBoardSize / 2, miniTop - 15,
                  size=18, bold=True, align='center', fill='black', font='Peace Sans')
        
        # animate the red line along the full path
        if app.miniLine < len(path):
            for i in range(app.miniLine):
                row1, col1 = path[i]
                row2, col2 = path[i + 1]

                # calculate cell centers for red line
                x1 = miniLeft + col1 * (miniCellSize + miniBorder) + miniBorder + miniCellSize / 2
                y1 = miniTop + row1 * (miniCellSize + miniBorder) + miniBorder + miniCellSize / 2
                x2 = miniLeft + col2 * (miniCellSize + miniBorder) + miniBorder + miniCellSize / 2
                y2 = miniTop + row2 * (miniCellSize + miniBorder) + miniBorder + miniCellSize / 2

                # draws line
                drawLine(x1, y1, x2, y2, fill='red', lineWidth=2)

# validates a real position
def isValid(board, row, col, seen):
    return (0 <= row < len(board) and 0 <= col < len(board[0]) and (row, col) not in seen)

# finds the specific path for the given (row,col)
def searchPath(board, word, row, col, path, seen, directions):
    if not word:  # word is the same 
        return path
    # iterates through every direction recursively
    for drow, dcol in directions:
        newRow, newCol = row + drow, col + dcol # new position
        if (0 <= newRow < len(board) and 0 <= newCol < len(board[0]) and (newRow, newCol) not in seen and board[newRow][newCol] == word[0]):
            seen.add((newRow, newCol))
            path.append((newRow, newCol))
            if searchPath(board, word[1:], newRow, newCol, path, seen, directions):
                return path
            # backtrack
            seen.remove((newRow, newCol))
            path.pop()

    return None # no word

# finds the starting point and returns full path
def getWordPath(board, word):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == word[0]:  # first letter matches
                seen = {(row, col)}
                path = [(row, col)]
                if searchPath(board, word[1:], row, col, path, seen, directions): # check all paths if they match from that position
                    return path # returns first ones that succeed
    return []

