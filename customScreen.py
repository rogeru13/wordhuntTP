from cmu_graphics import *

def drawCustomScreen(app):
    drawImage('images/customSize.png', app.width/2, app.height/2, align = 'center')

    # input box
    drawRect(app.width / 2 - 150, app.height / 2 - 30, 300, 60, fill="white", border="black")
    drawLabel(app.customSize, app.width / 2, app.height / 2, size=30)

