from cmu_graphics import *


def drawGameEndScreen(app):
    # background and text
    drawImage('images/endGameScreen.png', app.width / 2, app.height / 2, align='center')
    if app.miniBoardActive:
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


# def drawMiniBoard(app):
#     # Dimensions for the mini board
#     miniCellSize = app.cellSize / 4
#     miniBorder = 15
#     miniLeft = app.width - (miniCellSize * app.boardLen + miniBorder * (app.boardLen + 1)) - 50
#     miniTop = app.height - (miniCellSize * app.boardLen + miniBorder * (app.boardLen + 1)) - 50

#     # Draw mini board background
#     drawRect(miniLeft, miniTop, miniCellSize * app.boardLen + miniBorder * (app.boardLen + 1),
#              miniCellSize * app.boardLen + miniBorder * (app.boardLen + 1), fill='black')

#     # Draw cells
#     for row in range(app.boardLen):
#         for col in range(app.boardLen):
#             x0 = miniLeft + col * (miniCellSize + miniBorder) + miniBorder
#             y0 = miniTop + row * (miniCellSize + miniBorder) + miniBorder
#             drawImage("images/cell.png", x0, y0, width=miniCellSize, height=miniCellSize)

#             # Draw letters
#             drawLabel(app.board[row][col], x0 + miniCellSize / 2, y0 + miniCellSize / 2,
#                       size=15, bold=True, font="Helvetica")

#     # Animate the missed word with red lines
#     if app.miniWordIndex < len(app.missedWords):
#         word = app.missedWords[app.miniWordIndex]
#         path = getWordPath(app.board, word)

#         # Draw red lines incrementally
#         for i in range(min(len(path) - 1, app.miniLineProgress)):
#             row1, col1 = path[i]
#             row2, col2 = path[i + 1]
#             x1 = miniLeft + col1 * (miniCellSize + miniBorder) + miniBorder + miniCellSize / 2
#             y1 = miniTop + row1 * (miniCellSize + miniBorder) + miniBorder + miniCellSize / 2
#             x2 = miniLeft + col2 * (miniCellSize + miniBorder) + miniBorder + miniCellSize / 2
#             y2 = miniTop + row2 * (miniCellSize + miniBorder) + miniBorder + miniCellSize / 2
#             drawLine(x1, y1, x2, y2, fill="red", lineWidth=2)

def drawMiniBoard(app):
    # Mini board properties
    miniBoardSize = 250  # Fixed size for the mini-board
    # cellSize = miniBoardSize / app.boardLen
    border = 12 - app.boardLen  # Adjust border for smaller cells
    cellSize = (miniBoardSize - (app.boardLen + 1) * border) / app.boardLen    # Bottom-left position

    boardLeft = 50
    boardTop = app.height - miniBoardSize - 50  # Slight padding from bottom

    # Draw black background for mini-board
    drawRect(boardLeft, boardTop, miniBoardSize, miniBoardSize, fill='black')

    # Draw the cells
    
    for row in range(app.boardLen):
        for col in range(app.boardLen):
            # Calculate cell coordinates
            x0 = boardLeft + col * (cellSize + border) + border
            y0 = boardTop + row * (cellSize + border) + border
            x1 = x0 + cellSize
            y1 = y0 + cellSize

            # Draw cell background using the same images as the original board
            drawImage("images/cell.png", x0, y0, width=cellSize, height=cellSize)

            # Draw letter in the cell
            drawLabel(app.board[row][col], (x0 + x1) / 2, (y0 + y1) / 2, size=12, bold=True, font='Helvetica')

    # Draw red line for missed words animation
    if app.miniWordIndex < len(app.missingWords):
        word = app.missingWordsList[app.miniWordIndex]
        path = getWordPath(app.board, word)
        drawLabel(f"Word: {word}", boardLeft + miniBoardSize + 30, boardTop + miniBoardSize / 2,
                  size=15, bold=True, align="left", fill="black", font = 'Peace Sans')
        
        # Animate the red line along the full path
        if app.miniLineProgress < len(path):
            for i in range(app.miniLineProgress):
                row1, col1 = path[i]
                row2, col2 = path[i + 1]
                


                # calculate cell centers for red line
                x1 = boardLeft + col1 * (cellSize + border) + border + cellSize / 2
                y1 = boardTop + row1 * (cellSize + border) + border + cellSize / 2
                x2 = boardLeft + col2 * (cellSize + border) + border + cellSize / 2
                y2 = boardTop + row2 * (cellSize + border) + border + cellSize / 2

                drawLine(x1, y1, x2, y2, fill='red', lineWidth=2)


def isValidCell(board, row, col, seen):
    return (
        0 <= row < len(board) and
        0 <= col < len(board[0]) and
        (row, col) not in seen
    )

# def searchPath(board, row, col, word, seen, directions):
#     stack = [(row, col, word, [(row, col)])]
#     while stack:
#         currRow, currCol, currWord, path = stack.pop()
#         if not currWord:  # If all letters in the word are matched
#             return path
#         for drow, dcol in directions:
#             newRow, newCol = currRow + drow, currCol + dcol
#             if (
#                 isValidCell(board, newRow, newCol, seen | set(path)) and
#                 board[newRow][newCol] == currWord[0]
#             ):
#                 stack.append((newRow, newCol, currWord[1:], path + [(newRow, newCol)]))
#     return None
def searchPath(board, word, row, col, path, seen, directions):
    if not word:  # All letters matched
        return path
    for drow, dcol in directions:
        newRow, newCol = row + drow, col + dcol
        if (
            0 <= newRow < len(board) and
            0 <= newCol < len(board[0]) and
            (newRow, newCol) not in seen and
            board[newRow][newCol] == word[0]
        ):
            seen.add((newRow, newCol))
            path.append((newRow, newCol))
            if searchPath(board, word[1:], newRow, newCol, path, seen, directions):
                return path
            # Backtrack
            seen.remove((newRow, newCol))
            path.pop()
    return None

# def getWordPath(board, word):
#     directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
#     for row in range(len(board)):
#         for col in range(len(board[0])):
#             if board[row][col] == word[0]:
#                 path = searchPath(board, row, col, word[1:], {(row, col)}, directions)
#                 if path:
#                     # print(f"Word: {word}, Path: {path}")
#                     return path
def getWordPath(board, word):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == word[0]:  # First letter matches
                seen = {(row, col)}
                path = [(row, col)]
                if searchPath(board, word[1:], row, col, path, seen, directions):
                    return path
    return []

