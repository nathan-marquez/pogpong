from cmu_112_graphics import *
#the help screen
class HelpMode(Mode):
    def appStarted(mode):
        mode.image1 = mode.loadImage('help.jpeg')
        mode.image2 = mode.scaleImage(mode.image1, .35)

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image=ImageTk.PhotoImage(mode.image2))
        canvas.create_text(mode.width-150, mode.height-50, text = "PRESS Q TO GO BACK", font = 'Helvetica 20 bold')

    def keyPressed(mode, event):
        mode.app.splashScreenMode.help = False
        mode.app.setActiveMode(mode.app.splashScreenMode)
        
