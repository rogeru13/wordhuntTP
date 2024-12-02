from cmu_graphics import *

def drawNameInputScreen(app):
    # Background
    drawRect(0, 0, app.width, app.height, fill="lightblue")

    # Title
    drawLabel("Enter Your Name:", app.width / 2, app.height / 3, size=40, bold=True)

    # Name Input Box
    drawRect(app.width / 2 - 150, app.height / 2 - 30, 300, 60, fill="white", border="black")
    drawLabel(app.playerName, app.width / 2, app.height / 2, size=30)

    # Instruction
    drawLabel("Press Enter to Start", app.width / 2, app.height / 2 + 60, size=20, fill="gray")
