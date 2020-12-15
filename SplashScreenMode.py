from cmu_112_graphics import *

#Basically the home screen
class SplashScreenMode(Mode):
    #CLASSES
    class Button():
        def __init__(self,x0,y0,x1,y1, text):
            self.text = text
            self.x0 = x0
            self.x1 = x1
            self.y0 = y0
            self.y1 = y1
            self.color = 'black'
            self.textColor = 'white'

        def move(self,x0,y0,x1,y1):
            self.x0 = x0
            self.x1 = x1
            self.y0 = y0
            self.y1 = y1
        
        def hoveredOver(self,x,y):
            return self.x0 < x < self.x1 and self.y0 < y < self.y1
            
    class Model():
        def __init__(self,faces): #takes in a string and a 2d array of coords
            self.faces = faces

    class Face():
        def __init__(self,coords, color, outline):
            self.coords = coords
            self.outline = outline
            self.color = color

    class ScoreBoard():
        pass
    def appStarted(mode):
        mode.gameWidth = 800
        mode.gameHeight = 600
        mode.gameDepth = mode.width*2
        mode.focalOffset = 600
        mode.offsetChange = 5
        mode.tableHeight = 50
        mode.netHeight = 50
        mode.offsetChangeOn = True

        
        mode.startGame = False
        mode.chooseDiff = False
        mode.displayScoreboard = False
        mode.help = False
        mode.settings = False



        mode.room = mode.createRoom()
        mode.net = mode.createNet()

        mode.startButton = mode.Button(mode.width/2 - 90,mode.height/2 - 30 - 100,
                                  mode.width/2 + 90,mode.height/2 + 30 - 100, 'START')

        #Difficulty Buttons

        mode.easyButton = mode.Button(mode.width/2 - 190 - 100,mode.height/2 - 30 - 25,
                            mode.width/2 - 10 - 100,mode.height/2 + 30 - 25, 'EASY')

        mode.mediumButton = mode.Button(mode.width/2 - 90,mode.height/2 - 30 - 25,
                            mode.width/2 + 90,mode.height/2 + 30 - 25, 'MEDIUM')

        mode.hardButton = mode.Button(mode.width/2 + 10 + 100,mode.height/2 - 30 - 25,
                            mode.width/2 + 190 + 100,mode.height/2 + 30 - 25, 'HARD')

            
        mode.arcadeButton = mode.Button(mode.width/2 - 90,mode.height/2 - 30 - 25,
                                  mode.width/2 + 90,mode.height/2 + 30 - 25, 'ARCADE')
        mode.scoreBoardButton = mode.Button(mode.width/2 - 90,mode.height/2 - 30 + 50,
                                  mode.width/2 + 90,mode.height/2 + 30 + 50, 'SCOREBOARD')
        mode.helpButton = mode.Button(mode.width/2 - 90,mode.height/2 - 30 + 125,
                                  mode.width/2 + 90,mode.height/2 + 30 + 125, 'HELP')

        mode.buttonList = [mode.startButton, mode.easyButton, mode.mediumButton, mode.hardButton,
                           mode.arcadeButton, mode.scoreBoardButton, mode.helpButton]
        
        mode.settingsButton = mode.Button(mode.width-75, mode.height-75,
                                          mode.width-75 + 65, mode.height-75 + 65,
                                          '')
        mode.settingsPicInit = mode.loadImage('settings.png')
        mode.settingsPic = mode.scaleImage(mode.settingsPicInit, .12)

    def createRoom(mode):
        floor = mode.Face([[-mode.gameWidth,-100,0], 
                    [mode.gameWidth,-100,0], 
                    [mode.gameWidth,-100,mode.gameDepth], 
                    [-mode.gameWidth,-100,mode.gameDepth]], 
                    "gold3","")
        floor2 = mode.Face([[-mode.gameWidth,-110,0], 
                    [mode.gameWidth,-110,0], 
                    [mode.gameWidth,-110,mode.gameDepth], 
                    [-mode.gameWidth,-110,mode.gameDepth]], 
                    "gold2","")
        
        tableBottom = mode.Face([[-mode.gameWidth/2,mode.tableHeight-5,0], 
                    [mode.gameWidth/2,mode.tableHeight-5,0], 
                    [mode.gameWidth/2,mode.tableHeight-5,mode.gameDepth], 
                    [-mode.gameWidth/2,mode.tableHeight-5,mode.gameDepth]], 
                    "green3", "")

        table = mode.Face([[-mode.gameWidth/2,mode.tableHeight,0], 
                    [mode.gameWidth/2,mode.tableHeight,0], 
                    [mode.gameWidth/2,mode.tableHeight,mode.gameDepth], 
                    [-mode.gameWidth/2,mode.tableHeight,mode.gameDepth]], 
                    "green2", "")
        tableOutline = mode.Face([[-mode.gameWidth/2 + 10,mode.tableHeight,10], 
                    [mode.gameWidth/2 - 10,mode.tableHeight,10], 
                    [mode.gameWidth/2 - 10,mode.tableHeight,mode.gameDepth-10], 
                    [-mode.gameWidth/2 + 10,mode.tableHeight,mode.gameDepth-10]], 
                    "white", "")
        tableOutline2 = mode.Face([[-mode.gameWidth/2 + 20,mode.tableHeight,20], 
                    [mode.gameWidth/2 - 20,mode.tableHeight,20], 
                    [mode.gameWidth/2 - 20,mode.tableHeight,mode.gameDepth-20], 
                    [-mode.gameWidth/2 + 20,mode.tableHeight,mode.gameDepth-20]], 
                    "green2", "")

        leftLeg = mode.Face([[-mode.gameWidth/2 + 100,-100,50], 
                    [-mode.gameWidth/2 + 120,-100,50], 
                    [-mode.gameWidth/2 + 120,mode.tableHeight,50], 
                    [-mode.gameWidth/2 + 100,mode.tableHeight,50]], 
                    "brown", "")
        leftLegShadow = mode.Face([[-mode.gameWidth/2 + 100,-100,100], 
                    [-mode.gameWidth/2 + 120,-100,100], 
                    [-mode.gameWidth/2 + 120,mode.tableHeight,100], 
                    [-mode.gameWidth/2 + 100,mode.tableHeight,100]], 
                    "brown4", "")

        rightLeg = mode.Face([[mode.gameWidth/2 - 100,-100,50], 
                    [mode.gameWidth/2 - 120,-100,50], 
                    [mode.gameWidth/2 - 120,mode.tableHeight,50], 
                    [mode.gameWidth/2 - 100,mode.tableHeight,50]], 
                    "brown", "")

        rightLegShadow = mode.Face([[mode.gameWidth/2 - 100,-100,100], 
                    [mode.gameWidth/2 - 120,-100,100], 
                    [mode.gameWidth/2 - 120,mode.tableHeight,100], 
                    [mode.gameWidth/2 - 100,mode.tableHeight,100]], 
                    "brown4", "")

        
        return mode.Model([floor, floor2,
                    leftLegShadow, leftLeg, rightLegShadow, rightLeg,
                    tableBottom, table, tableOutline, tableOutline2])

    def createNet(mode):
        
        net1 = mode.Face([[-mode.gameWidth/2,mode.tableHeight,mode.gameDepth/2-10], 
                        [-mode.gameWidth/2,mode.tableHeight+mode.netHeight,mode.gameDepth/2-10], 
                        [mode.gameWidth/2,mode.tableHeight+mode.netHeight,mode.gameDepth/2-10], 
                        [mode.gameWidth/2,mode.tableHeight,mode.gameDepth/2-10]],
                        "gainsboro", "")

        net2 = mode.Face([[-mode.gameWidth/2,mode.tableHeight,mode.gameDepth/2+5], 
                        [-mode.gameWidth/2,mode.tableHeight+mode.netHeight,mode.gameDepth/2+5], 
                        [mode.gameWidth/2,mode.tableHeight+mode.netHeight,mode.gameDepth/2+5], 
                        [mode.gameWidth/2,mode.tableHeight,mode.gameDepth/2+5]],
                        "gainsboro", "")
        return mode.Model([net2,net1])

    def keyPressed(mode, event):
        if event.key == "s":
            mode.app.setActiveMode(mode.app.settingsMode)
        if event.key == "h":
            mode.app.setActiveMode(mode.app.helpMode)

    def timerFired(mode):
        if mode.offsetChangeOn:
            if mode.startGame and mode.focalOffset <= 200:
                mode.app.setActiveMode(mode.app.gameMode)
            elif mode.startGame:
                mode.offsetChange = -7
            elif mode.focalOffset <= 500:
                mode.offsetChange = 1
            elif mode.focalOffset >= 600:
                mode.offsetChange = -1
            mode.focalOffset += mode.offsetChange

        if mode.startGame and mode.focalOffset == 200:
            mode.app.setActiveMode(mode.app.gameMode)
        elif mode.chooseDiff:
            #move bottom arround
            mode.arcadeButton.move(mode.width/2 - 90,mode.height/2 - 30 + 50,
                                          mode.width/2 + 90,mode.height/2 + 30 + 50)
            mode.scoreBoardButton.move(mode.width/2 - 90,mode.height/2 - 30 + 125,
                                              mode.width/2 + 90,mode.height/2 + 30 + 125)
            mode.helpButton.move(mode.width/2 - 90,mode.height/2 - 30 + 200,
                                        mode.width/2 + 90,mode.height/2 + 30 + 200)
            #display difficulty buttons

        elif mode.displayScoreboard:
            mode.arcadeButton.move(mode.width/2 - 90,mode.height/2 - 30 - 25,
                                    mode.width/2 + 90,mode.height/2 + 30 - 25)
            mode.scoreBoardButton.move(mode.width/2 - 90,mode.height/2 - 30 + 50,
                                    mode.width/2 + 90,mode.height/2 + 30 + 50)

            mode.helpButton.move(mode.width/2 - 90,mode.height/2 - 30 + 275,
                                    mode.width/2 + 90,mode.height/2 + 30 + 275)
        elif mode.help:
            mode.app.setActiveMode(mode.app.helpMode)
        elif mode.settings:
            mode.app.setActiveMode(mode.app.settingsMode)
        else:
            mode.arcadeButton.move(mode.width/2 - 90,mode.height/2 - 30 - 25,
                                    mode.width/2 + 90,mode.height/2 + 30 - 25)
            mode.scoreBoardButton.move(mode.width/2 - 90,mode.height/2 - 30 + 50,
                                    mode.width/2 + 90,mode.height/2 + 30 + 50)
            mode.helpButton.move(mode.width/2 - 90,mode.height/2 - 30 + 125,
                                    mode.width/2 + 90,mode.height/2 + 30 + 125)

    def mouseMoved(mode,event):
        for button in mode.buttonList:
            if button.hoveredOver(event.x,event.y):
                button.color = 'white'
                button.textColor = 'black'
            else:
                button.color = 'black'
                button.textColor = 'white'



    def mousePressed(mode,event):
        if not mode.startGame:
            if mode.startButton.hoveredOver(event.x,event.y):
                mode.chooseDiff = True
                mode.displayScoreboard = False
                mode.help = False
                mode.settings = False
            elif mode.chooseDiff and mode.easyButton.hoveredOver(event.x,event.y):
                mode.chooseDiff = False
                mode.displayScoreboard = False
                mode.help = False
                mode.settings = False

                mode.app.diff = 0
                mode.startGame = True
            elif mode.chooseDiff and mode.mediumButton.hoveredOver(event.x,event.y):
                mode.chooseDiff = False
                mode.displayScoreboard = False
                mode.help = False
                mode.settings = False

                mode.app.diff = 1
                mode.startGame = True
            elif mode.chooseDiff and mode.hardButton.hoveredOver(event.x,event.y):
                mode.chooseDiff = False
                mode.displayScoreboard = False
                mode.help = False
                mode.settings = False

                mode.app.diff = 2
                mode.startGame = True

            elif mode.arcadeButton.hoveredOver(event.x,event.y):
                mode.chooseDiff = False
                mode.displayScoreboard = False
                mode.help = False
                mode.settings = False

        
                mode.app.diff = 4
                mode.startGame = True
        
            elif mode.scoreBoardButton.hoveredOver(event.x,event.y):
                mode.chooseDiff = False
                mode.displayScoreboard = True
                mode.help = False
                mode.settings = False

            elif mode.helpButton.hoveredOver(event.x,event.y):
                mode.chooseDiff = False
                mode.displayScoreboard = False
                mode.help = True
                mode.settings = False
            
            elif mode.settingsButton.hoveredOver(event.x,event.y):
                mode.chooseDiff = False
                mode.displayScoreboard = False
                mode.help = False
                mode.settings = True



    def drawFace(mode, canvas, face):
        #converts each point in the model to a new 2d list
        points = []
        for coord in face.coords:
            x = coord[0]
            y = coord[1]
            z = coord[2]

            scaleFactor = 1 - (z/mode.gameDepth) * .7
            # = 1 when z is 0
            # = .5 when z is mode.gameDepth

            newX = x * scaleFactor
            newY = y * scaleFactor
            focalX = mode.gameWidth//2
            focalY = mode.gameHeight - (z/mode.gameDepth)*mode.focalOffset

            points.extend([focalX + newX,focalY - newY])
        
        canvas.create_polygon(points, outline=face.outline, fill=face.color, width=2)
        #draws the polygon from that 2d list

    def drawModel(mode, canvas, model):
        for face in model.faces:
            mode.drawFace(canvas, face)

    def drawTitleScreen(mode,canvas):
        canvas.create_text(mode.width/2, 175, text='POG PONG', font = 'Helvetica 125 bold')
        mode.drawButton(canvas,mode.startButton)
        mode.drawButton(canvas,mode.arcadeButton)
        mode.drawButton(canvas,mode.scoreBoardButton)
        mode.drawButton(canvas,mode.helpButton)

        if mode.chooseDiff:
            mode.drawButton(canvas,mode.easyButton)
            mode.drawButton(canvas,mode.mediumButton)
            mode.drawButton(canvas,mode.hardButton)
        if mode.displayScoreboard:
            mode.drawScoreboard(canvas)
        
        canvas.create_image(mode.width-32.5-10, mode.height-32.5-10, image=ImageTk.PhotoImage(mode.settingsPic))



    def drawStartMessage(mode,canvas):
        if 400 <mode.focalOffset <= 500:
            canvas.create_text(mode.width/2, mode.height/2, text='READY', font = 'Helvetica 150 bold')
        elif 300 <mode.focalOffset <= 400:
            canvas.create_text(mode.width/2, mode.height/2, text='SET', font = 'Helvetica 150 bold')
        elif 200 < mode.focalOffset <= 300:
            canvas.create_text(mode.width/2, mode.height/2, text='GO!', font = 'Helvetica 150 bold')

    def drawButton(mode,canvas,button):
        canvas.create_rectangle(button.x0,button.y0,
                                button.x1, button.y1, fill = button.color, outline = "") 
        canvas.create_text((button.x0+button.x1)/2, (button.y0+button.y1)/2, text = button.text, 
                            font = 'Helvetica 20 bold', fill = button.textColor)

    def drawScoreboard(mode,canvas):
        canvas.create_rectangle(mode.width/2 - 200,mode.height/2 - 30 + 125,
                                mode.width/2 + 200,mode.height/2 + 30 + 200, fill = "black")
        canvas.create_rectangle(mode.width/2 - 200 + 5,mode.height/2 - 30 + 125 + 5,
                                mode.width/2 + 200 - 5,mode.height/2 + 30 + 200 - 5, fill = "white")
        index = 0
        for row in mode.app.scores:
            if row[0] != "":
                canvas.create_text(mode.width/2, mode.height/2 - 30 + 145 + 20*index,
                                text=f'{row[0]}.................{row[1]}', font = 'Helvetica 20 bold')
                index += 1


    def redrawAll(mode, canvas):
        canvas.create_rectangle(0,0,mode.width, mode.height, fill = "lavender") 
        mode.drawModel(canvas,mode.room) 
        mode.drawModel(canvas,mode.net)

        if not mode.startGame:
            mode.drawTitleScreen(canvas)
        else:
            mode.drawStartMessage(canvas)
        

