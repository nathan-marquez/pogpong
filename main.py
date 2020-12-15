from cmu_112_graphics import *
from SplashScreenMode import *
from GameMode import *
from HelpMode import *
from SettingsMode import *
import csv


#CITATIONS#
'''
Free Gear Icon: https://www.vhv.rs/viewpic/hbxxwRo_settings-gear-settings-gear-icon-free-hd-png/
Designs for Help Screen made in Apple Keynote
CMU MVC: https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
TP Video made with Apple iMovie
Free Lofi Trap Beat for Video: https://www.youtube.com/watch?v=7l9RF7Re4fo&ab_channel=SpoonBeats

I reference this article for the multiple CSV functions throughout the video, along with the CSV python DOcs
https://realpython.com/python-csv/
https://docs.python.org/3/library/csv.html
'''


class MyModalApp(ModalApp):
    def appStarted(mode):
        mode.offsetChangeOn = True
        mode.drawGuideOn = False
        mode.trackerOn = False
        mode.wallsOn = False
        mode.dataOn = False
        mode.tailOn = True 
        mode.shadowOn = True
        mode.handleOn = True
        mode.diff = 2
        mode.scores = []
        with open('scoreboard.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                mode.scores.append([row[0],int(row[1])])

        mode.splashScreenMode = SplashScreenMode()
        mode.gameMode =  GameMode()
        mode.helpMode = HelpMode()
        mode.settingsMode = SettingsMode()
        mode.setActiveMode(mode.splashScreenMode)
        mode.timerDelay = 50

mode = MyModalApp(width=800, height=800)
