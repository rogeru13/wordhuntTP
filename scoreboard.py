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
        drawLabel(f'{finalScores[i][1]}', 462, 180 + 132*i, size = 40, bold = True, font = 'Open Sans', fill = 'white', align = 'left')

    
7
        
