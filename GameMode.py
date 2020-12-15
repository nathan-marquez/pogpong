from cmu_112_graphics import *
import math
import random
import time
try:
    import cv2
except:
    print("no cv")
import csv

class GameMode(Mode):
    #CLASSES#

    class Model():
        def __init__(self,faces): #takes in a string and a 2d array of coords
            self.faces = faces

    class Face():
        def __init__(self,coords, color, outline):
            self.coords = coords
            self.outline = outline
            self.color = color

    class Ball():
        def __init__(self, x, y, z , dX = 0, dY = -40, dZ = 100):
            self.x = x
            self.y = y
            self.z = z
            self.r = 10
            self.loss = 1.3
            
            self.dX = dX
            self.dY = dY
            self.dZ = dZ

            self.touchedRedSide = False
            self.touchedBlueSide = False
        
        def move(self,mode):
            self.dY += mode.gravity
            self.x += self.dX
            self.y += self.dY
            self.z += self.dZ
            self.impact = 60 - 60*(self.y/mode.gameHeight)

            #if dot collides with table, check to see if double bounce and redo dY
            if self.y <= mode.tableHeight and mode.gameDepth > self.z >= 0 and -mode.gameWidth/2 < self.x < mode.gameWidth/2:
                if self.z > mode.gameDepth/2 :
                    self.touchedRedSide = False
                    if self.touchedBlueSide and not mode.redToastOn and not mode.blueToastOn and mode.app.diff != 4:
                        mode.redPoint = True
                    self.touchedBlueSide = True

                elif self.z < mode.gameDepth/2:
                    self.touchedBlueSide = False
                    if self.touchedRedSide and not mode.redToastOn and not mode.blueToastOn:
                        mode.bluePoint = True
                    self.touchedRedSide = True

                self.y = mode.tableHeight + self.r
                if mode.app.diff != 4: self.dY = -self.dY//self.loss
                else: self.dY = max(-self.dY//self.loss, 10)
                #friction:
                self.dZ = self.dZ//self.loss
                self.dX = self.dX//self.loss
            
            if mode.app.diff == 4:
                if self.x >= mode. gameWidth//2:
                    self.x = mode.gameWidth//2 - self.r
                    self.dX = -self.dX//self.loss
                if self.x <= -mode.gameWidth//2:
                    self.x = -mode.gameWidth//2 + self.r
                    self.dX = -self.dX//self.loss
            
            
            #if dot collides with opponent or back 
            if self.z >= mode.gameDepth: 
                parityCheck = random.randint(0,1)
                if parityCheck:
                    mode.opponent.parity = -1
                else:
                    mode.opponent.parity = 1
                
                if mode.app.diff == 4: #KINEMATICS FOR ARCADE MODE(DIFFICULTY 4):
                    self.touchedBlueSide = True
                    self.touchedRedSide = False
                    self.z = mode.gameDepth - self.r
                    if self.y <= mode.tableHeight + 20:
                        self.dZ = -60
                    else:
                        self.dZ = -self.dZ - .25
                    depth = -mode.gameDepth * (.80)
                    time = depth/self.dZ
                    height = -(self.y - mode.tableHeight) + mode.netHeight
                    self.dY = (height - (.5)*(mode.gravity)*(time**2))/(time) 
                    
                elif mode.collides(mode.ball, mode.opponent) and self.z < mode.gameDepth +100+ abs(self.dZ):
                    self.touchedBlueSide = True
                    self.touchedRedSide = False
                    self.z = mode.gameDepth - self.r

                    self.dZ = -(self.dZ) - self.impact
                    self.dY += mode.opponent.dY 
                    self.dX += mode.opponent.dX 
                    

                        

                elif self.z > mode.gameDepth + abs(self.dZ) and not mode.redToastOn and not mode.blueToastOn:
                    if(self.touchedBlueSide):
                        mode.redPoint = True
                    elif(self.touchedRedSide):
                        mode.bluePoint = True
                    self.dZ = 0

            #if dot collides with hits your side, check if it hits paddle
            if self.z <= 0:
                if mode.collides(mode.ball, mode.player) and self.z > -200 - abs(self.dZ):
                    if mode.app.diff == 4 and not mode.gameOver:
                        mode.arcadeScore += 1 * mode.pointMultiplier
                    self.touchedRedSide = True
                    self.touchedBlueSide = False
                    self.z = self.r
                    self.dZ = -(self.dZ) + self.impact
                    self.dY += mode.player.dY 
                    self.dX += mode.player.dX
                elif self.z <= -200 - abs(self.dZ) and not mode.redToastOn and not mode.blueToastOn:
                    if(self.touchedBlueSide):
                        mode.redPoint = True
                    elif(self.touchedRedSide):
                        mode.bluePoint = True

            #dot collides with net:
            if (mode.gameDepth/2 + max(10,abs(self.dZ)) >= self.z >= mode.gameDepth/2 - max(10,abs(self.dZ))):
                if (self.y - self.r) <= (mode.netHeight + mode.tableHeight):
                    if mode.app.diff != 4:
                        self.dZ = -(self.dZ/2)
                    else:
                        self.dZ = -abs(self.dZ)

    class BallClones():
        def __init__(self, x, y, z , dX = 0, dY = -40, dZ = -100):
            self.x = x
            self.y = y
            self.z = z
            self.r = 10
            self.loss = 1.3
            
            self.dX = dX
            self.dY = dY
            self.dZ = dZ
            
            self.outOfBounds = False

        
        def move(self,mode):
            self.dY += mode.gravity
            self.x += self.dX
            self.y += self.dY
            self.z += self.dZ
            self.impact = 60 - 60*(self.y/mode.gameHeight)

            #if dot collides with table, check to see if double bounce and redo dY
            if self.y <= mode.tableHeight and mode.gameDepth > self.z >= 0 and -mode.gameWidth/2 < self.x < mode.gameWidth/2:
                self.y = mode.tableHeight + self.r
                self.dY = max(-self.dY//self.loss, 10)
                #friction:
                self.dZ = self.dZ//self.loss
                self.dX = self.dX//self.loss
            
            #collide with sides
            if self.x >= mode. gameWidth//2:
                self.x = mode.gameWidth//2 - self.r
                self.dX = -self.dX//self.loss
            if self.x <= -mode.gameWidth//2:
                self.x = -mode.gameWidth//2 + self.r
                self.dX = -self.dX//self.loss
            
            #if dot collides with opponent or back 
            if self.z >= mode.gameDepth+100: 
                self.outOfBounds = True
                    
            #if dot collides with hits your side, check if it hits paddle
            if self.z <= 0:
                if mode.collides(self, mode.player) and self.z > -200 - abs(self.dZ):
                    if mode.app.diff == 4 and not mode.gameOver:
                        mode.arcadeScore += 1 * mode.pointMultiplier
                    self.touchedRedSide = True
                    self.touchedBlueSide = False
                    self.z = self.r
                    self.dZ = -(self.dZ) + self.impact
                    self.dY += mode.player.dY 
                    self.dX += mode.player.dX
                elif self.z <= -200 - abs(self.dZ):
                    self.outOfBounds = True

            #dot collides with net:
            if (mode.gameDepth/2 + max(10,abs(self.dZ)) >= self.z >= mode.gameDepth/2 - max(10,abs(self.dZ))):
                if (self.y - self.r) <= (mode.netHeight + mode.tableHeight):
                    if mode.app.diff != 4:
                        self.dZ = -(self.dZ/2)
                    else:
                        self.dZ = -abs(self.dZ)
    class Guide():
        def __init__(self, ball):
            self.z = ball.z

    class Paddle():
        def __init__(self,mode, x = 0, y = 0, z = 0, color = 'red'):
            self.x = x
            self.y = y
            self.z = z
            self.r = 50
            self.dX = 0
            self.dY = 0
            self.pastX = []
            self.pastY = []
            self.pastdX = []
            self.pastdY = []
            self.aX = 0
            self.aY = 0
            self.color = color
            #OPPONENT SWIPE DATA
            self.swiping = False
            #This is a parity generator used to randomly choose how the opponent moves
            parityCheck = random.randint(0,1)
            if parityCheck:
                self.parity = -1
            else:
                self.parity = 1
            

        def updatePhysics(self):
            self.pastX.append(self.x)
            self.pastY.append(-self.y)
            if len(self.pastX) > 3: 
                self.pastX.pop(0)
            if len(self.pastY) > 3: 
                self.pastY.pop(0)

            if len(self.pastX) == 3:
                self.pastdX = [(self.pastX[1] - self.pastX[0])/2,
                            (self.pastX[2] - self.pastX[1])/2]
                self.dX = self.pastdX[-1]
            if len(self.pastY) == 3:
                self.pastdY = [(self.pastY[0] - self.pastY[1])/2,
                            (self.pastY[1] - self.pastY[2])/2]
                self.dY = self.pastdY[-1]
            if len(self.pastdX) == len(self.pastdY) == 2:
                self.aX = (self.pastdX[1] - self.pastdX[0])/2
                self.aY = (self.pastdY[1] - self.pastdY[0])/2

        def move(self,mode,x,y):
            self.x = x - mode.gameWidth/2
            self.y = mode.gameHeight - y
            self.updatePhysics()

        #I referenced Stack Overflow for this function: https://stackoverflow.com/questions/19747856/pygame-move-object-towards-position

        def moveTowards(self,thingx,thingy,speed):
            dx, dy = (thingx - self.x, (thingy) - self.y)
            stepx, stepy = (dx / speed, dy / speed)
            self.x = self.x + stepx
            self.y = self.y + stepy
            self.updatePhysics()

        def swipe(self, dX, dY):
            self.x = self.x + dX
            self.y = self.y + dY
            self.updatePhysics()

    class Particle():
        def __init__(self,ball):
            self.x = ball.x
            self.y = ball.y
            self.z = ball.z
            self.r = 2

    class PowerUp():
        def __init__(self,mode,x):
            self.x = x
            self.z = mode.gameDepth * .75
            self.r = 40
            self.y = mode.tableHeight + self.r

            self.onTable = False
            self.activated = False

        def collides(self,mode,otherX,otherY,otherZ):
            if otherY <= mode.tableHeight + self.r*2:
                if self.x - self.r < otherX < self.x + self.r:
                    if self.z - self.r < otherZ < self.z + self.r:
                        return True
            return False
        
    class CircleFace():
        def __init__(self,x,y,z,r):
            self.x = x
            self.y = y
            self.z = z
            self.r = r

    #HELPERS#
    def collides(mode, ob1, ob2):
        maxLength = ob1.r + ob2.r
        distance = math.sqrt((ob1.x - ob2.x)**2 + (ob1.y - ob2.y)**2)
        return distance < maxLength

    #CONTROLLERS#

    def appStarted(mode):
        #INITIALIZERS
        mode.gameWidth = 800
        mode.gameHeight = 600
        mode.gameDepth = mode.width*2
        mode.focalOffset = 200
        mode.offsetChange = 5
        mode.gravity = -5
        mode.tableHeight = 50
        mode.netHeight = 50

        #GAMEPLAY:
        mode.winScore = 11
        mode.pointToastStart = 0
        mode.redToastOn = False
        mode.blueToastOn = False
        mode.redPoint = False
        mode.bluePoint = False
        mode.redScore = 0
        mode.blueScore = 0
        mode.gameOverToastOn = False
        mode.gameOver = False
        
        #ARACDE MODE:
        mode.arcadeScore = 0
        mode.playerName = ""
        #POWERUPS:
        mode.freeze = mode.PowerUp(mode,0)
        mode.freezeModel = mode.createFreezeModel() #[clockFace,hand,hand]
        mode.frenzy = mode.PowerUp(mode,-mode.gameWidth/4)
        mode.frenzyModel = mode.createFrenzyModel() #[ball1,ball2,ball3]
        mode.doublePoints = mode.PowerUp(mode,mode.gameWidth/4)
        mode.doublePointsModel = mode.createDoublePointsModel() #[pillar1,pillar2,roof,floor]
        mode.pointMultiplier = 1
        mode.powerUpStart = 0
        mode.powerUpOn = False
        mode.powerUpList = [mode.freeze,mode.frenzy,mode.doublePoints]
        mode.ballClones = []
        mode.powerUpToastStart = 0
        mode.powerUpToastOn = False

        #MODELS:
        mode.room = mode.createRoom()
        mode.net = mode.createNet()
        
        #BALL:
        mode.resetBall()

        #PLAYER:
        mode.player = mode.Paddle(mode, 0, 5, 0, "red")
        mode.playerShadow = mode.Paddle(mode, 0, 0, -30,'indian red')
        mode.playerHandle = mode.createHandle(mode.player)

        #OPPONENT:
        mode.opponent = mode.Paddle(mode, 0, mode.tableHeight + 100, mode.gameDepth-10, "RoyalBlue3")
        mode.opponentShadow = mode.Paddle(mode, 0, mode.tableHeight + 100, mode.gameDepth,'blue')
        mode.opponentHandle = mode.createHandle(mode.opponent)

        #TRACKER:
        if mode.app.trackerOn:
            mode.createTracker()

    #I learned OpenCV from this Tutorial: https://www.youtube.com/watch?v=1FJWXOO1SRI&ab_channel=Murtaza%27sWorkshop-RoboticsandAI
    #I essentially followed it along, but replaced the majority of th code in order to suit the needs of this project
    def createTracker(mode):
        mode.cap = cv2.VideoCapture(0)
        mode.tracker = cv2.TrackerCSRT_create()

        mode.success, mode.img = mode.cap.read()
        mode.img = cv2.flip(mode.img, 1)
        mode.bbox = cv2.selectROI("Tracking", mode.img, False)
        mode.tracker.init(mode.img,mode.bbox)

    def resetBall(mode):
        dX = (random.random() * 20) - 10
        mode.ball = mode.Ball(0, mode.tableHeight + 400, 0, dX, 0, 80)
        mode.guide = mode.Guide(mode.ball)
        mode.particles = []
        mode.fail = False

    #ROOM MODELS
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
        
        if mode.app.wallsOn:
            wallColor = "gray91"
        else:
            wallColor = ""
        leftWall = mode.Face([[-mode.gameWidth/2,0,0], 
                        [-mode.gameWidth/2,mode.gameHeight*2,0], 
                        [-mode.gameWidth/2,mode.gameHeight*2,mode.gameDepth], 
                        [-mode.gameWidth/2,0,mode.gameDepth]],
                        wallColor, "")

        rightWall = mode.Face([[mode.gameWidth/2,0,0], 
                        [mode.gameWidth/2,mode.gameHeight*2,0], 
                        [mode.gameWidth/2,mode.gameHeight*2,mode.gameDepth], 
                        [mode.gameWidth/2,0,mode.gameDepth]],
                        wallColor, "")
        
        return mode.Model([floor, floor2,
                    leftLegShadow, leftLeg, rightLegShadow, rightLeg,
                    leftWall, rightWall, 
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

    #POWERUP MODELS

    def createFreezeModel(mode):
        clockFace = mode.CircleFace(mode.freeze.x,mode.freeze.y,mode.freeze.z,mode.freeze.r/2)
        hand1 = mode.Face([[mode.freeze.x-2,mode.freeze.y+mode.freeze.r/2,mode.freeze.z],
                      [mode.freeze.x+2,mode.freeze.y+mode.freeze.r/2,mode.freeze.z],
                      [mode.freeze.x+2,mode.freeze.y,mode.freeze.z],
                      [mode.freeze.x-2,mode.freeze.y,mode.freeze.z]],
                      "LightBlue1","") 

        hand2 = mode.Face([[mode.freeze.x,mode.freeze.y+2,mode.freeze.z],
                      [mode.freeze.x+mode.freeze.r/2,mode.freeze.y+2,mode.freeze.z],
                      [mode.freeze.x+mode.freeze.r/2,mode.freeze.y-2,mode.freeze.z],
                      [mode.freeze.x,mode.freeze.y-2,mode.freeze.z]],
                      "LightBlue1","") 

        return [clockFace,hand1,hand2]
    
    def createFrenzyModel(mode):
        ball1 = mode.CircleFace(mode.frenzy.x - 7, mode.frenzy.y,
                                mode.frenzy.z,mode.frenzy.r/3)
        ball2 = mode.CircleFace(mode.frenzy.x + 7, mode.frenzy.y,
                                mode.frenzy.z,mode.frenzy.r/3)
        ball3 = mode.CircleFace(mode.frenzy.x, mode.frenzy.y + 7,
                                mode.frenzy.z,mode.frenzy.r/3)

        return [ball3,ball2,ball1]

    def createDoublePointsModel(mode):
        pillar1 = mode.Face([[mode.doublePoints.x-8*(3/2),mode.doublePoints.y-8*(3/2),mode.doublePoints.z],
                      [mode.doublePoints.x-8*(3/2),mode.doublePoints.y+8*(3/2),mode.doublePoints.z],
                      [mode.doublePoints.x-4*(3/2),mode.doublePoints.y+8*(3/2),mode.doublePoints.z],
                      [mode.doublePoints.x-4*(3/2),mode.doublePoints.y-8*(3/2),mode.doublePoints.z]],
                      "orange3","") 
        pillar2 = mode.Face([[mode.doublePoints.x+8*(3/2),mode.doublePoints.y-8*(3/2),mode.doublePoints.z],
                      [mode.doublePoints.x+8*(3/2),mode.doublePoints.y+8*(3/2),mode.doublePoints.z],
                      [mode.doublePoints.x+4*(3/2),mode.doublePoints.y+8*(3/2),mode.doublePoints.z],
                      [mode.doublePoints.x+4*(3/2),mode.doublePoints.y-8*(3/2),mode.doublePoints.z]],
                      "orange3","") 
        floor = mode.Face([[mode.doublePoints.x+12*(3/2),mode.doublePoints.y-12*(3/2),mode.doublePoints.z],
                      [mode.doublePoints.x+12*(3/2),mode.doublePoints.y-8*(3/2),mode.doublePoints.z],
                      [mode.doublePoints.x-12*(3/2),mode.doublePoints.y-8*(3/2),mode.doublePoints.z],
                      [mode.doublePoints.x-12*(3/2),mode.doublePoints.y-12*(3/2),mode.doublePoints.z]],
                      "orange3","") 
        cieling = mode.Face([[mode.doublePoints.x+12*(3/2),mode.doublePoints.y+12*(3/2),mode.doublePoints.z],
                      [mode.doublePoints.x+12*(3/2),mode.doublePoints.y+8*(3/2),mode.doublePoints.z],
                      [mode.doublePoints.x-12*(3/2),mode.doublePoints.y+8*(3/2),mode.doublePoints.z],
                      [mode.doublePoints.x-12*(3/2),mode.doublePoints.y+12*(3/2),mode.doublePoints.z]],
                      "orange3","")      

        return [pillar1,pillar2,floor,cieling] 

    def createHandle(mode, paddle):
        midX = 0
        midY = mode.tableHeight
        z = paddle.z
        #trianlge = mode.Face()
        handle = mode.Face([[paddle.x + 10,paddle.y,z], 
                    [paddle.x - 10,paddle.y,z], 
                    [paddle.x - 10,paddle.y - 100,z], 
                    [paddle.x + 10,paddle.y - 100,z]],
                        "black", "")
        handleShadow = mode.Face([[paddle.x + 10,paddle.y,z-10], 
                    [paddle.x - 10,paddle.y,z-30], 
                    [paddle.x - 10,paddle.y - 100,z-10], 
                    [paddle.x + 10,paddle.y - 100,z-10]],
                        "gray10", "")
        handleStripe = mode.Face([[paddle.x + 5,paddle.y,z-11], 
                    [paddle.x - 5,paddle.y,z-11], 
                    [paddle.x - 5,paddle.y - 100,z-11], 
                    [paddle.x + 5,paddle.y - 100,z-11]],
                        "goldenrod", "")

        return mode.Model([handle,handleShadow, handleStripe])

    def updateTail(mode):
        particle = mode.Particle(mode.ball)
        mode.particles.append(particle)

        if len(mode.particles) > 10:
            mode.particles.pop(0)
        
    def updateOpponent(mode):
        if mode.app.diff == 0:
            speed = 2
            dY = 60 - 60*(mode.ball.y/mode.gameHeight)
            dX = 0
            swipingRange = 300
            endFollowThrough = mode.gameDepth - 100
        elif mode.app.diff == 1:
            speed = 1.7
            dY = 120 - 60*(mode.ball.y/mode.gameHeight) - 30*(mode.ball.dY/20) - 30*(mode.ball.dZ/40)
            dX = 0
            swipingRange = 400
            endFollowThrough = mode.gameDepth - 50
        elif mode.app.diff == 2:
            speed = 1.3
            dY = 120 - 60*(mode.ball.y/mode.gameHeight) - 30*(mode.ball.dY/20) - 30*(mode.ball.dZ/40)
            dX = (mode.ball.x - mode.opponent.x)
            swipingRange = 400
            endFollowThrough = mode.gameDepth - 50
        elif mode.app.diff == 4:
            speed = 1.3
            dY = 120 - 60*(mode.ball.y/mode.gameHeight) - 30*(mode.ball.dY/20) - 30*(mode.ball.dZ/40)
            dX = (mode.ball.x - mode.opponent.x)
            swipingRange = 400
            endFollowThrough = mode.gameDepth - 50
  

        if mode.opponent.swiping:
            if mode.gameDepth - swipingRange < mode.ball.z < mode.gameDepth - swipingRange/2 \
                and mode.ball.dZ > 0:
                mode.opponent.swipe(-dX,-dY)
                mode.opponentShadow.swipe(-dX,-dY)
            elif (mode.ball.dZ > 0 or mode.gameDepth + 100 > mode.ball.z > mode.gameDepth - swipingRange/2):
                #swipe up
                if not mode.ball.touchedBlueSide and mode.ball.y > mode.tableHeight + 60 and mode.app.diff != 4:
                    mode.opponent.swipe(-dX,-100)
                    mode.opponentShadow.swipe(-dX,-100)
                else:
                    mode.opponent.swipe(dX,dY)
                    mode.opponentShadow.swipe(dX,dY)
                    
            elif(mode.ball.z <= mode.gameDepth + 100):
                mode.opponent.moveTowards(mode.ball.x,mode.ball.y,4)
                mode.opponentShadow.moveTowards(mode.ball.x,mode.ball.y,4)

            if mode.ball.z <= mode.gameDepth/2 or mode.ball.z >= mode.gameDepth + 200: 
                mode.opponent.swiping = False
            
        #approach ball
        elif(mode.gameDepth/2 < mode.ball.z <= mode.gameDepth + 100): #move toward the ball
            mode.opponent.moveTowards(mode.ball.x,mode.ball.y-mode.opponent.r,speed)
            mode.opponentShadow.moveTowards(mode.ball.x,mode.ball.y-mode.opponentShadow.r,speed)
            #check if we are in swiping range
            if mode.ball.z >= mode.gameDepth - swipingRange:
                if mode.app.diff != 4:
                    mode.opponent.swiping = True

        
        else: #mimick player
            mode.opponent.moveTowards(mode.player.x * mode.opponent.parity, mode.tableHeight + 100,speed)
            mode.opponentShadow.moveTowards(mode.player.x * mode.opponent.parity,mode.tableHeight + 100,speed)
                
            
        mode.opponentHandle = mode.createHandle(mode.opponent)

    #OPENCV NON-INIT FUNCTIONS#
    #I learned OpenCV from this Tutorial: https://www.youtube.com/watch?v=1FJWXOO1SRI&ab_channel=Murtaza%27sWorkshop-RoboticsandAI
    #I essentially followed it along, but replaced the majority of th code in order to suit the needs of this project

    def updateTracker(mode):
        timer = cv2.getTickCount()
        success, mode.img = mode.cap.read()
        mode.img = cv2.flip(mode.img, 1)
        success, mode.bbox = mode.tracker.update(mode.img)
        if success:
            mode.drawBox(mode.img,mode.bbox)
            mode.updatePosition()
        else:
            cv2.putText(mode.img,"Lost",(75,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
    

        fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
        cv2.putText(mode.img,str(int(fps)),(75,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        cv2.imshow("Tracking",mode.img)

    def drawBox(mode,img,bbox):
        x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
        cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)
        cv2.putText(img,"Tracking",(75,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

    def updatePosition(mode):
        boxWidth,boxHeight = mode.bbox[2], mode.bbox[3]
        boxX,boxY = mode.bbox[0] + boxWidth//2 ,mode.bbox[1] + boxHeight//2
        vidWidth  = mode.cap.get(3) # float
        vidHeight = mode.cap.get(4) # float
        x = (boxX/vidWidth) * mode.width
        y = (boxY/vidHeight) * mode.height

        mode.player.move(mode,x,y)
        mode.playerShadow.move(mode,x,y)
        mode.playerHandle = mode.createHandle(mode.player)
    #################

    def updateScore(mode):
        if mode.app.diff != 4:
            if(mode.redPoint) and not mode.gameOver:
                mode.redScore += 1
                mode.redPoint = False
                mode.redToastOn = True
                mode.pointToastStart = time.time()

            elif(mode.bluePoint) and not mode.gameOver:
                mode.blueScore += 1
                mode.bluePoint = False
                mode.blueToastOn = True
                mode.pointToastStart = time.time()

            if(mode.redScore == mode.winScore or mode.blueScore == mode.winScore) and not mode.gameOverToastOn:
                mode.gameOverToastOn = True
                mode.gameOver = True
        else:
                if (mode.bluePoint) and not mode.gameOver and not mode.gameOverToastOn:
                    mode.gameOverToastOn = True
                    mode.blueToastOn = True
                    mode.gameOver = True

    def updateToasts(mode):
        #update pointToast
        if mode.app.diff != 4:
            currentTime = time.time()
            if mode.redToastOn and currentTime >= mode.pointToastStart + .5:
                mode.redToastOn = False
                mode.resetBall()
            elif mode.blueToastOn and currentTime >= mode.pointToastStart + .5:
                mode.blueToastOn = False
                mode.resetBall()
    
    def updatePowerUps(mode):
        if mode.powerUpList[0].activated == mode.powerUpList[1].activated == mode.powerUpList[2].activated == False:
            if mode.powerUpList[0].onTable == mode.powerUpList[1].onTable == mode.powerUpList[2].onTable == False:
                choose = random.randint(0,2)
                mode.powerUpList[choose].onTable = True
            else:
                #something is on table      
                #check if that thing on table is hit, and if so activate it
                #and turn mode.powerUpOn
                for powerUp in mode.powerUpList:
                    if powerUp.onTable and powerUp.collides(mode,mode.ball.x,mode.ball.y,mode.ball.z):
                        mode.powerUpToastOn = True
                        mode.powerUpToastStart = time.time()
                        powerUp.activated = True
                        powerUp.onTable = False
                        mode.powerUpOn = True
                        mode.powerUpStart = time.time()

        #go through list of extra balls
        for ball in mode.ballClones:
            ball.move(mode)
            if ball.outOfBounds:
                mode.ballClones.remove(ball)

        mode.activatePowerUps()

    def activatePowerUps(mode):
        currentTime = time.time()
        if currentTime >= mode.powerUpToastStart + 4:
            mode.powerUpToastOn = False
        if mode.powerUpOn:
            if mode.freeze.activated:
                mode.app.timerDelay = 100
                if currentTime >= mode.powerUpStart + 15 or mode.gameOver:
                    mode.app.timerDelay = 50
                    mode.freeze.activated = False
                    mode.app.powerUpOn = False


            elif mode.frenzy.activated:
                mode.activateFrenzy()
                if currentTime >= mode.powerUpStart + 3 or mode.gameOver:
                    mode.app.timerDelay = 50
                    mode.frenzy.activated = False
                    mode.app.powerUpOn = False

            
            elif mode.doublePoints.activated:
                mode.pointMultiplier = 2
                if currentTime >= mode.powerUpStart + 20 or mode.gameOver:
                    mode.pointMultiplier = 1
                    mode.doublePoints.activated = False
                    mode.app.powerUpOn = False


    def activateFrenzy(mode):
        for i in range(1,10):
            dX = (random.random() * 40) - 20
            dZ = -(random.random() * 40 + 80)
            dY = (random.random() * 40) - 20
            x = ((i/10) * mode.gameWidth) - mode.gameWidth/2
            ball = mode.BallClones(x, mode.tableHeight + 400, mode.gameDepth, dX, dY, dZ)
            mode.ballClones.append(ball)

    def timerFired(mode):
        mode.updateScore()
        mode.updateToasts()
        mode.ball.move(mode)
        mode.updateOpponent()
        if mode.app.diff == 4:
            mode.updatePowerUps()

        if mode.app.tailOn:
            mode.updateTail()
        if mode.app.drawGuideOn:
            mode.guide.z = mode.ball.z
        if mode.app.offsetChangeOn and not mode.gameOver:
            mode.focalOffset = 200 + 50*(mode.ball.z/mode.gameDepth)
        elif mode.app.offsetChangeOn and mode.gameOver:
            if mode.focalOffset <= 200:
                mode.offsetChange = 1
            elif mode.focalOffset >= 300:
                mode.offsetChange = -1
            mode.focalOffset += mode.offsetChange
        if mode.app.trackerOn:
            mode.updateTracker()

    def mouseMoved(mode, event):
        if not mode.app.trackerOn:
            mode.player.move(mode,event.x,event.y)
            mode.playerShadow.move(mode,event.x,event.y)
        mode.playerHandle = mode.createHandle(mode.player)

    def keyPressed(mode,event):
        if not (mode.gameOverToastOn and mode.app.diff == 4):
            if event.key == "q":
                mode.app.splashScreenMode.startGame = False
                mode.app.timerDelay = 50
                mode.app.splashScreenMode.focalOffset = 600
                mode.appStarted()
                mode.app.setActiveMode(mode.app.splashScreenMode)
            elif event.key == "r":
                mode.appStarted()

        #gets keyboard input
        else:
            if event.key == "Enter" or event.key == "Return":
                #update the scoreboard
                mode.updateScoreboard(mode.playerName, mode.arcadeScore)
                mode.app.splashScreenMode.startGame = False
                mode.app.splashScreenMode.focalOffset = 600
                mode.appStarted()
                mode.app.setActiveMode(mode.app.splashScreenMode)
            elif event.key == "Delete" or event.key == "Backspace" and mode.playerName != "":
                mode.playerName = mode.playerName[:-1]  #himynamei
            elif len(mode.playerName) < 20 and len(event.key) == 1:
                mode.playerName += event.key.upper()    
        
    def updateScoreboard(mode, newName, newScore):
        for index in range(len(mode.app.scores)):
            if newScore >= mode.app.scores[index][1]:
                mode.app.scores = mode.app.scores[0:index] + [[newName,newScore]] + mode.app.scores[index:]
                if len(mode.app.scores) > 5:
                    mode.app.scores.pop(-1)
                break
        if len(mode.app.scores) < 5:
            mode.app.scores.append([newName,newScore])  

        with open('scoreboard.txt') as inf:
            reader = csv.reader(inf.readlines())

        with open('scoreboard.txt', 'w') as csv_file:
            writer = csv.writer(csv_file)
            index = 0
            for line in reader:
                currentName = mode.app.scores[index][0]
                currentScore = mode.app.scores[index][1]
                writer.writerow([currentName,currentScore])
                index += 1
        
    #VIEW#

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

    def drawCircle(mode, canvas, ball, color = "white", outlineColor = ''):
        z = ball.z
        scaleFactor = 1 - (z/mode.gameDepth) * .7

        x0 = (ball.x - ball.r) * scaleFactor
        y0 = (ball.y - ball.r) * scaleFactor
        x1 = (ball.x + ball.r) * scaleFactor
        y1 = (ball.y + ball.r) * scaleFactor

        focalX = mode.gameWidth//2
        focalY = mode.gameHeight - (z/mode.gameDepth)*mode.focalOffset
        

        canvas.create_oval(focalX + x0, focalY - y0, 
                        focalX + x1, focalY - y1, 
                        outline = outlineColor, fill=color)

    def drawBallShadow(mode, canvas, ball):
        #converts each point in the model to a new 2d list
        x = ball.x
        z = ball.z
        r = ball.r - (ball.r/2)*(ball.y/mode.gameHeight)
        shadowCoords = [[x+r,mode.tableHeight,z+r],
                        [x-r,mode.tableHeight,z-r]]
        points = []
        for coord in shadowCoords:
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
        
        canvas.create_oval(points[0],points[1],points[2],points[3], outline="",fill="gray")
        #draws the polygon from that 2d list

    def drawGuide(mode,canvas,guide, color):
        z = guide.z
        scaleFactor = 1 - (z/mode.gameDepth) * .7

        x0 = (-mode.gameWidth//2) * scaleFactor
        y0 = (mode.gameHeight) * scaleFactor
        x1 = (mode.gameWidth//2) * scaleFactor
        y1 = (mode.tableHeight) * scaleFactor

        focalX = mode.gameWidth//2
        focalY = mode.gameHeight - (z/mode.gameDepth)*mode.focalOffset
        

        canvas.create_rectangle(focalX + x0, focalY - y0, 
                        focalX + x1, focalY - y1, 
                        outline = color)
        
        canvas.create_line(focalX + mode.ball.x * scaleFactor, 
                        focalY - y0, 
                        focalX + mode.ball.x * scaleFactor, 
                        focalY - y1, 
                        fill = color)
        canvas.create_line(focalX + x0,
                        focalY - mode.ball.y * scaleFactor, 
                        focalX + x1, 
                        focalY - mode.ball.y * scaleFactor, 
                        fill = color)
        
    def drawPaddle(mode,canvas,paddle):
        mode.drawCircle(canvas,paddle, paddle.color)

    def drawBehindTrail(mode,canvas):
        for particle in mode.particles:
            if particle.z <= mode.ball.z:
                mode.drawCircle(canvas,particle,"red")

    def drawFrontTrail(mode,canvas):
        for particle in mode.particles:
            if particle.z > mode.ball.z:
                mode.drawCircle(canvas,particle,"blue")

    def displayData(mode,canvas):
        #BALL:

        canvas.create_text(50, 50, text = "BALL:",
                    fill="black", font="Helvetica 26 bold")
        #POSITION
        canvas.create_text(50, 75, text = "X:",
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(100, 75, text = int(mode.ball.x),
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(50, 100, text = "Y:",
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(100, 100, text = int(mode.ball.y),
                        fill="black", font="Helvetica 15 bold")
        #VELOCITY
        canvas.create_text(50, 125, text = "dX:",
                            fill="black", font="Helvetica 15 bold")
        canvas.create_text(100, 125, text = int(mode.ball.dX),
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(50, 150, text = "dY:",
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(100, 150, text = int(mode.ball.dY),
                        fill="black", font="Helvetica 15 bold")


        #PLAYER:
        canvas.create_text(65, 200, text = "PLAYER:",
                    fill="black", font="Helvetica 26 bold")
        
        #POSITION
        canvas.create_text(50, 225, text = "X:",
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(100, 225, text = int(mode.player.x),
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(50, 250, text = "Y:",
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(100, 250, text = int(mode.player.y),
                        fill="black", font="Helvetica 15 bold")
        #VELOCITY
        canvas.create_text(50, 275, text = "dX:",
                            fill="black", font="Helvetica 15 bold")
        canvas.create_text(100, 275, text = int(mode.player.dX),
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(50, 300, text = "dY:",
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(100, 300, text = int(mode.player.dY),
                        fill="black", font="Helvetica 15 bold")
        #ACCELERATION
        canvas.create_text(50, 325, text = "aX:",
                            fill="black", font="Helvetica 15 bold")
        canvas.create_text(100, 325, text = int(mode.player.aX),
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(50, 350, text = "aY:",
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(100, 350, text = int(mode.player.aY),
                        fill="black", font="Helvetica 15 bold")

        #OPPONENT:
        canvas.create_text(65, 400, text = "OPPONENT:",
                    fill="black", font="Helvetica 26 bold")
        
        #POSITION
        canvas.create_text(50, 425, text = "X:",
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(100, 425, text = int(mode.opponent.x),
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(50, 450, text = "Y:",
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(100, 450, text = int(mode.opponent.y),
                        fill="black", font="Helvetica 15 bold")
        #VELOCITY
        canvas.create_text(50, 475, text = "dX:",
                            fill="black", font="Helvetica 15 bold")
        canvas.create_text(100, 475, text = int(mode.opponent.dX),
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(50, 500, text = "dY:",
                        fill="black", font="Helvetica 15 bold")
        canvas.create_text(100, 500, text = int(mode.opponent.dY),
                        fill="black", font="Helvetica 15 bold")

    def displayScoreAndQuit(mode,canvas):
        if not mode.gameOverToastOn:
            if mode.app.diff != 4:
                canvas.create_text(mode.width - 130, 50, text = "PLAYER:",
                            fill="black", font="Helvetica 26 bold")
                canvas.create_text(mode.width - 50, 50, text = mode.redScore,
                            fill="black", font="Helvetica 26 bold")
                canvas.create_text(mode.width - 150, 100, text = "OPPONENT:",
                            fill="black", font="Helvetica 26 bold")
                canvas.create_text(mode.width - 50, 100, text = mode.blueScore,
                            fill="black", font="Helvetica 26 bold")
            else:
                canvas.create_text(mode.width/2, 50, text = f"SCORE: {mode.arcadeScore}",
                            fill="black", font="Helvetica 26 bold")

    def drawWinMessage(mode,canvas):
        if mode.app.diff != 4:
            if (mode.redScore == mode.winScore):
                canvas.create_text(mode.width/2, 100, text='YOU WIN', font = 'Helvetica 150 bold')
            else:
                canvas.create_text(mode.width/2, 100, text='YOU LOSE', font = 'Helvetica 150 bold')
            canvas.create_text(mode.width/2, 200, text='PRESS R TO RESTART OR Q TO QUIT', font = 'Helvetica 30 bold')
        else:
            canvas.create_text(mode.width/2, 100, text='GAME OVER', font = 'Helvetica 125 bold')
            canvas.create_text(mode.width/2, 200, text=f'YOUR SCORE: {mode.arcadeScore}', font = 'Helvetica 40 bold')
            canvas.create_text(mode.width/2, 250, text=f'ENTER YOUR NAME: {mode.playerName}', font = 'Helvetica 30 bold')

    def drawPowerUps(mode,canvas):
        if mode.freeze.onTable:
            mode.drawBallShadow(canvas, mode.freeze)
            clockFace = mode.freezeModel[0]
            mode.drawCircle(canvas,clockFace,color = "RoyalBlue1", outlineColor = "blue2")
            hand1 = mode.freezeModel[1]
            mode.drawFace(canvas,hand1)
            hand2 = mode.freezeModel[2]
            mode.drawFace(canvas,hand2)
            
        if mode.frenzy.onTable:
            for ball in mode.frenzyModel:
                mode.drawBallShadow(canvas, mode.frenzy)
                mode.drawCircle(canvas,ball,color = "indian red", outlineColor = "red")
                
        if mode.doublePoints.onTable:
            for face in mode.doublePointsModel:
                mode.drawBallShadow(canvas, mode.doublePoints)
                mode.drawFace(canvas, face)
                

    def drawBehindClones(mode,canvas):
        for clone in mode.ballClones:
            if clone.z <= mode.ball.z:
                mode.drawCircle(canvas, clone, 'white')

    def drawFrontClones(mode,canvas):
        for clone in mode.ballClones:
            if clone.z > mode.ball.z:
                mode.drawCircle(canvas, clone, 'white')
    
    def drawPowerUpToasts(mode,canvas):
        if mode.freeze.activated:
            canvas.create_text(mode.width//2, mode.height-50, text = "SLO-MO!", 
                                font = "Helvetica 50 bold", fill = "blue")

        if mode.frenzy.activated:
            canvas.create_text(mode.width//2, mode.height-50, text = "FRENZY!", 
                                font = "Helvetica 50 bold", fill = "RED")

        if mode.doublePoints.activated:
            canvas.create_text(mode.width//2, mode.height-50, text = "DOUBLE POINTS!",
                                font = "Helvetica 50 bold", fill = "ORANGE")


    def redrawAll(mode, canvas):
        #drawBackground
        if mode.redToastOn or mode.redScore == mode.winScore:
            backColor = "OliveDrab1"
        elif mode.blueToastOn or mode.blueScore == mode.winScore:
            backColor = "tomato"
        else:
            backColor = "lavender"

        canvas.create_rectangle(0,0,mode.width, mode.height, fill = backColor) 

        #draw ball if behind opponent
        if mode.ball.z > mode.gameDepth - 5:
            if mode.frenzy.activated:
                mode.drawCircle(canvas,mode.ball,'red')
            else:
                mode.drawCircle(canvas,mode.ball)

        #draw opponent
        if mode.app.handleOn: 
            mode.drawModel(canvas, mode.opponentHandle)

        mode.drawPaddle(canvas,mode.opponent)
        mode.drawPaddle(canvas,mode.opponentShadow)

        #draw stage
        mode.drawModel(canvas,mode.room) 

        

        #draw ball (if in front players), net, and tail 
        mode.drawBehindTrail(canvas)
        if mode.ball.z < mode.gameDepth * .75:
            mode.drawPowerUps(canvas)

        if mode.ball.z < mode.gameDepth/2:
            mode.drawModel(canvas,mode.net)
        
        if mode.app.shadowOn and mode.gameDepth - 5 >= mode.ball.z >= 5:
            mode.drawBallShadow(canvas,mode.ball)
        if mode.gameDepth - 5 > mode.ball.z > -200:
            if mode.frenzy.activated:
                mode.drawCircle(canvas,mode.ball,"red")
            else:
                mode.drawCircle(canvas,mode.ball)

        if mode.ball.z >= mode.gameDepth * .75:
            mode.drawPowerUps(canvas)
        
        if mode.ball.z >= mode.gameDepth/2:
            mode.drawModel(canvas,mode.net)
        mode.drawBehindClones(canvas)
        mode.drawFrontTrail(canvas)
        mode.drawFrontClones(canvas)

        #draw optional guide
        if mode.app.drawGuideOn:
            mode.drawGuide(canvas,mode.guide, "yellow")

        #draw player paddle
        mode.drawPaddle(canvas,mode.player)
        if mode.app.handleOn: 
            mode.drawModel(canvas, mode.playerHandle)
        mode.drawPaddle(canvas,mode.playerShadow)

        #draw ball if behind player
        if mode.ball.z < -200:
            mode.drawCircle(canvas,mode.ball)
        #draw optional data
        if mode.app.dataOn:
            mode.displayData(canvas)

        #draw score and quit text
        mode.displayScoreAndQuit(canvas)

        if mode.powerUpToastOn:
            mode.drawPowerUpToasts(canvas)

        #draw win message:
        if mode.gameOverToastOn:
            mode.drawWinMessage(canvas)
