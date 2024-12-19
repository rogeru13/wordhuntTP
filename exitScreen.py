from cmu_graphics import *

def drawExitScreen(app):
    # loaded full image instead of separate pngs for efficiency purposes
    # designed in figma
    drawImage('images/exitScreen.png', app.width/2, app.height/2, align = 'center')
