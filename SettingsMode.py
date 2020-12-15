from cmu_112_graphics import *

#the settings
class SettingsMode(Mode):
    class ToggleButton():
        def __init__(self,x,y,text,value = True):
            self.x0 = x - 50
            self.x1 = x + 50
            self.y0 = y - 25
            self.y1 = y + 25
            self.x = x
            self.y = y
            self.value = value
            self.color = 'black'
            self.textColor = 'white'
            self.text = text
        
        def hoveredOver(self,mode,x,y):
            newx0 = self.x0 - mode.setingsOffset
            newx1 = self.x1 - mode.setingsOffset

            return newx0 < x < newx1 and self.y0 < y < self.y1

    def appStarted(mode):
        mode.setingsOffset = 100
    
        mode.tableTiltButton = mode.ToggleButton(mode.width-100, 140,
                                                 "TABLE TILT", True)
        mode.guideButton = mode.ToggleButton(mode.width-100, 200,
                                             "CROSSHAIR GUIDE", False)
        mode.trackerButton = mode.ToggleButton(mode.width-100, 260,
                                             "CAMERA CONTROLS", False)
        mode.wallsButton = mode.ToggleButton(mode.width-100, 320,
                                             "SIDE WALLS", False)
        mode.dataButton = mode.ToggleButton(mode.width-100, 380,
                                             "PHYSICS DATA", False)
        mode.tailButton = mode.ToggleButton(mode.width-100, 440,
                                             "BALL TAIL", True)
        mode.shadowButton = mode.ToggleButton(mode.width-100, 500,
                                             "BALL SHADOW", True)
        mode.handleButton = mode.ToggleButton(mode.width-100, 560,
                                             "PADDLE HANDLE", True)

        mode.buttonList = [mode.tableTiltButton, mode.guideButton,
                           mode.trackerButton, mode.wallsButton,
                           mode.dataButton, mode.tailButton,
                           mode.shadowButton, mode.handleButton]

    def mousePressed(mode, event):
        for button in mode.buttonList:
            if(button.hoveredOver(mode,event.x,event.y)):
                button.value = not button.value

    def timerFired(mode):
        mode.app.offsetChangeOn = mode.tableTiltButton.value
        mode.app.drawGuideOn = mode.guideButton.value
        mode.app.trackerOn = mode.trackerButton.value
        mode.app.wallsOn = mode.wallsButton.value
        mode.app.dataOn = mode.dataButton.value
        mode.app.tailOn = mode.tailButton.value
        mode.app.shadowOn = mode.shadowButton.value
        mode.app.handleOn = mode.handleButton.value


    def keyPressed(mode, event):
        if event.key == "q":
            mode.app.splashScreenMode.settings = False
            mode.app.setActiveMode(mode.app.splashScreenMode)


    def drawToggleButton(mode,canvas,button):
        if button.value == True:
            color = "black"
            textColor = "white"
            text = "ON"
        else:
            color = "gray69"
            textColor = "black"
            text = "OFF"
        
        canvas.create_rectangle(button.x0 - mode.setingsOffset,button.y0,
                                button.x1 - mode.setingsOffset, button.y1, fill = color, outline = "") 
        canvas.create_text(button.x - mode.setingsOffset, button.y, text = text, 
                            font = 'Helvetica 20 bold', fill = textColor)
    
    def redrawAll(mode, canvas):
        for button in mode.buttonList:
            canvas.create_text(mode.width/2 - mode.setingsOffset,button.y, 
                            text = button.text, 
                            font = 'Helvetica 30 bold')
            mode.drawToggleButton(canvas,button)

            canvas.create_text(mode.width//2-mode.setingsOffset, 285, 
                               text = "(RECOMENDED FOR FAST COMPUTERS WITH OPEN CV)", 
                               font = 'Helvetica 15 bold')
        
            canvas.create_text(mode.width//2, mode.height-100, 
                               text = "PRESS Q TO RETURN TO HOMESCREEN", 
                               font = 'Helvetica 20 bold')