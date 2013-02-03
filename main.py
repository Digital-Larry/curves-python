# Main file for Python curve generator.
# Requires Python Curve class (curve.py)
# Written by Gary S. Worsham
# January 3, 2013
# Revision February 3, 2013
# - Added Spirograph and Harmonograph classes.
# - previous main curve is now "Lissajous" class.
# -------------------------------------------------
# This code covered by the GPLV3 license.
# See GPLV3.txt for details.

import pygame, sys, os, math, random, time
from pygame.locals import *
import curve

# Import the android module. If we can't import it, set it to None - this
# lets us test it, and check to see if we want android-specific behavior.
try:
    import android
except ImportError:
    android = None

class App():
    def __init__(self):
        self.width = 640
        self.height = 480
        
        pygame.init()
        pygame.display.set_caption("Python Curve Generator")   
        error = pygame.display.set_mode((self.width, self.height))
        print error
        self.screen = pygame.display.get_surface()
        # define 2 curves and select their functions intially
        self.curveSet = curve.CurveSet(self.width, self.height, self.screen)
        self.curveSet.selectCurves() 

        # Map the back button to the escape key.
        if android:
         android.init()
         android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

        if android: 
            self.delay = 5
        else:
            self.delay = 2

    def clearScreen(self):
        # self.screen.fill((random.randint(1,15), random.randint(2, 10), random.randint(1,50)))
        self.screen.fill((0, 0, 0))
        pygame.display.flip()   

    def input(self, events): 
      for event in events: 
         if event.type == QUIT:
            sys.exit(0)
         if android:
             if event.type == pygame.MOUSEBUTTONDOWN:
               print ("Android key down!")
               self.clearScreen()
               self.selectCurve()
                 
         if event.type == KEYDOWN:
            if event.key == K_1:
               print ("Key 1")
            if event.key == K_t:
               print ("Key t")
               curve.testAll()
            if event.key == K_x:
               print ("Key x")
               self.testX()
            if event.key == K_y:
               print ("Key y")
               self.testY()
            if event.key == K_s:
               print ("Key s")
               self.saveScreen()
            if event.key == K_q:
               print ("Key q")
               self.sequence()
            if event.key == K_SPACE:
               print ("Key Space!")
               self.time = 0.0
               self.seconds = 0.0
               self.clearScreen()
               # self.saveScreen()
               self.curveSet.selectCurves()
            if event.key == K_ESCAPE:
               print ("Escape")
               sys.exit(0)
         else:
            x = 1
            # print event
            
    def saveScreen(self, filename, foldername="curvedata-01"):
        print "Saving screen!", foldername, filename
        font = pygame.font.Font(None, 20)
        name_fg = (220, 250, 235)
        fileName = '{}\\{:03d}.jpg'.format(foldername, filename)
        pygame.image.save(self.screen, fileName)

    def run(self):
        self.seconds = 0.0
        self.clearScreen()
        self.delay = 10
        folderName = "random"
        fileIndex = 0

        # print "Hello:"
        while True: 
            self.input(pygame.event.get())
            i = self.curveSet.drawPoints()
            if (self.seconds >= 20000.0) | (i == -1):
                print "Seconds: ", self.seconds
                self.saveScreen(fileIndex, folderName)
                self.clearScreen()
                self.curveSet.selectCurves()
                self.seconds = 0.0
                fileIndex += 1

            pygame.time.wait(self.delay)
            self.seconds = self.seconds + 1.0
            pygame.display.flip()
         
        pygame.quit()   
        pygame.exit()

    def sequence(self):
        seconds = 0
        self.clearScreen()
        self.delay = 1
        curveSequence = curve.Sequence(self.width, self.height, self.screen)
        folderName = "curvedata"
        fileIndex = 0
        
        # print "Hello:"
        for i in range (0, 400):
            print "Sequence step ", i
            while seconds < 2000:
                key = self.input(pygame.event.get())
                if (key == K_SPACE):
                    self.fileIndex = 0
                    self.clearscreen()
                    curveSequence.randomize()
                    curveSequence.time = 0.0
                    seconds = 0                 

                curveSequence.drawPoint()
                pygame.time.wait(1)
                seconds = seconds + 1
                pygame.display.flip()

            # print "Seconds: ", self.seconds
            self.saveScreen(fileIndex, folderName)
            fileIndex += 1
            self.clearScreen()
            curveSequence.adjust()
            seconds = 0

         
#-----------------------------------------------------------------     
def main(param):
   app = App()
   i = param
   app.run()

# This isn't run on Android.
if __name__ == "__main__":
    main(1)

"""
    def testAll(self):
       self.radFunc1 = 0
       self.colorFunc1 = 0
       self.selectCurve()

       self.clearScreen()
       
       for i in (0, 1, 2, 3, 4, 5, 6):
            for j in (0, 1, 2, 3, 4, 5, 6):
                self.xFunc1 = i
                self.yFunc1 = j
                time = 0.0
                speed = 500
                increment = 6.283/speed 

                while (time < 2000.0):
                    self.drawFunc(time)
                    time = time + increment
                    # seconds = seconds + 1000.0/self.delay
                    pygame.display.flip()
                self.saveScreen()
                self.clearScreen()
                self.selectCurve()

    def testX(self):
        self.radFunc1 = 1
        self.colorFunc1 = 1
        self.selectCurve()

        self.clearScreen()
        self.yFunc1 = 8
        self.yFunc2 = 8

        for i in (0, 1, 2, 3, 4, 5, 6, 7):
            self.xFunc1 = i
            self.xFunc2 = i
            self.yFunc1 = 8
            self.yFunc2 = 8
            time = 0.0
            speed = 500
            increment = 6.283/speed 

            while (time < float(self.height * 6.283 /speed)):
                self.input(pygame.event.get())
                print time, self.height
                self.drawFunc(time)
                time = time + increment
                # seconds = seconds + 1000.0/self.delay
                pygame.display.flip()
            self.saveScreen()
            self.clearScreen()
            self.selectCurve()

    def testY(self):
        self.radFunc1 = 0
        self.colorFunc1 = 0
        self.selectCurve()

        self.clearScreen()

        for j in (0, 1, 2, 3, 4, 5, 6):
            self.xFunc1 = 8
            self.yFunc1 = j
            time = 0.0
            speed = 1000
            increment = 6.283/speed 

            while (time < 2000.0):
                self.drawFunc(time)
                time = time + increment
                # seconds = seconds + 1000.0/self.delay
                pygame.display.flip()
            self.saveScreen()
            self.clearScreen()
            self.selectCurve()
                             
"""
