from cmu_graphics import *


def drawScoreboard(app):
    drawImage('images/scoreboard.png', app.width / 2, app.height / 2, align='center')

    finalScores = []
    for name in app.nameDict:
        finalScores.append((name.upper(), app.nameDict[name]))

    for i in range(len(finalScores)):
        for j in range(0, len(finalScores) - i - 1):
            if finalScores[j][1] < finalScores[j + 1][1]:  # Compare scores (descending order)
                finalScores[j], finalScores[j + 1] = finalScores[j + 1], finalScores[j]
    
    for i in range(min(5, len(finalScores))):
        drawLabel(f'{finalScores[i][0]}', 150, 180 + 132*i, size = 40, bold = True, font = 'Open Sans', fill = 'white', align = 'left')
        drawLabel(f'{finalScores[i][1]}', 548, 180 + 132*i, size = 40, bold = True, font = 'Open Sans', fill = 'white', align = 'left')
        drawLabel(f'({app.boardLen}x{app.boardLen})', 548, 215 + 132*i, size = 15, bold = True, font = 'Open Sans', fill = 'white', align = 'left')


     
def addNameScore(filePath):
    with open(filePath, 'r') as file:
        for line in file:
            word = line.strip()  # removes any extra spaces just in case
            if len(word) > 2 and len(word) < 10:  # Skips words that are less than 3 characters
                wordSet.add(word.upper())  # makes all of them uppercase
    return wordSet
