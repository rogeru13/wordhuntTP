from cmu_graphics import *

def drawNameInputScreen(app):
    # loaded full image instead of separate pngs for efficiency purposes
    # designed in figma
    drawImage('images/nameInput.png', app.width/2, app.height/2, align = 'center') 

    # input box
    drawRect(app.width / 2 - 150, app.height / 2 - 30, 300, 60, fill="white", border="black")
    drawLabel(app.playerName, app.width / 2, app.height / 2, size=30, font = 'Peace Sans')

