from cmu_graphics import *

def drawHome(app):
    # loaded full image instead of separate pngs for efficiency purposes
    # designed in figma
    drawImage('images/board.png', app.width/2, app.height/2, align = "center")

# button class for input
class Button:
    def __init__(self, x1, x2, y1, y2, targetScreen):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.targetScreen = targetScreen

    def isClicked(self, mouseX, mouseY):
        if self.x1 <= mouseX <= self.x2 and self.y1 <= mouseY <= self.y2:
            return True
        return False
    
