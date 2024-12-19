from cmu_graphics import *


def drawScoreboard(app):
    # designed fully in figma
    drawImage('images/scoreboard.png', app.width / 2, app.height / 2, align='center')
    
    # gets final scores in a list
    finalScores = []
    for name in app.nameDict:
        finalScores.append((name.upper(), app.nameDict[name]))

    # iterating through scores
    for i in range(len(finalScores)):
        for j in range(0, len(finalScores) - i - 1):
            if finalScores[j][1] < finalScores[j + 1][1]:  # compares scores to put them in descending order
                finalScores[j], finalScores[j + 1] = finalScores[j + 1], finalScores[j]  # swap positions
    
    for i in range(min(5, len(finalScores))):
        drawLabel(f'{finalScores[i][0]}', 150, 180 + 132*i, size = 40, bold = True, font = 'Peace Sans', fill = 'white', align = 'left')
        drawLabel(f'{finalScores[i][1][0]}', 548, 180 + 132*i, size = 40, bold = True, font = 'Peace Sans', fill = 'white', align = 'left')
        drawLabel(f'({finalScores[i][1][1]}x{finalScores[i][1][1]})', 548, 215 + 132*i, size = 15, bold = True, font = 'Peace Sans', fill = 'white', align = 'left')

