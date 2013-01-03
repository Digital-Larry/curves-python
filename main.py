# Main file for Python curve generator.
# Requires Python Curve class (curve.py)
# Written by Gary S. Worsham
# January 3, 2013
# This code covered by the GPLV3 license.
# See GPLV3.txt for details.

import pygame, sys, os, math, random
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
        self.width = 800
        self.height = 600 
        self.xmax = 0;
        self.ymax = 0;
        
        pygame.init()
        pygame.display.set_caption("Python Curve Generator")   
        error = pygame.display.set_mode((self.width, self.height))
        print error
        self.screen = pygame.display.get_surface()

        self.Curve1 = curve.Curve(self.width, self.height, self.screen)
        self.Curve2 = curve.Curve(self.width, self.height, self.screen)

        # Map the back button to the escape key.
        if android:
         android.init()
         android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

        if android: 
            self.delay = 5
        else:
            self.delay = 50

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
               self.randomize()
                 
         if event.type == KEYDOWN:
            if event.key == K_1:
               print ("Key 1")
            if event.key == K_t:
               print ("Key t")
               self.testAll()
            if event.key == K_x:
               print ("Key x")
               self.testX()
            if event.key == K_y:
               print ("Key y")
               self.testY()
            if event.key == K_s:
               print ("Key s")
               self.saveScreen()
            if event.key == K_SPACE:
               print ("Key Space!")
               self.time = 0.0
               self.clearScreen()
               self.Curve1.randomize()
               self.Curve2.randomize()
            if event.key == K_ESCAPE:
               print ("Escape")
               sys.exit(0)
         else:
            x = 1
            # print event

    def saveScreen(self):
        print "Saving screen!"
        font = pygame.font.Font(None, 20)
        name_fg = (220, 250, 235)
        # factors = 'Factors-{}{}{}{}-{}{}={}{}{}{}-{}{}.jpg'.format(self.fct1_1, self.fct1_2, self.fct1_3, self.fct1_4, self.fct1_5, self.fct1_6,self.fct2_1, self.fct2_2, self.fct2_3, self.fct2_4, self.fct2_5, self.fct2_6)
        filename = 'Circle1-x-{}-y-{}.jpg'.format(self.Curve1.xFunc, self.Curve1.yFunc)
        print filename
        text = font.render(filename, 1, name_fg, (0, 0, 0))
        textpos = text.get_rect()
        # print self.name, textpos, textpos.centerx
        textpos.centerx = self.width/2
        textpos.centery = self.height - 20
        # print self.name, textpos, textpos.centerx, textpos.centery
        self.screen.blit(text, textpos)
        pygame.image.save(self.screen, filename)

    def testAll(self):
       self.radFunc1 = 0
       self.colorFunc1 = 0
       self.randomize()

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
                self.randomize()

    def testX(self):
        self.radFunc1 = 1
        self.colorFunc1 = 1
        self.randomize()

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
            self.randomize()

    def testY(self):
        self.radFunc1 = 0
        self.colorFunc1 = 0
        self.randomize()

        self.clearScreen()

        for j in (0, 1, 2, 3, 4, 5, 6):
            self.xFunc1 = 8
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
            self.randomize()
                             
    def run(self):
       self.time = 0.0
       self.speed = 500
       increment = 6.283/self.speed 

       self.clearScreen()
       self.Curve1.randomize()
       self.Curve2.randomize()
       seconds = 0.0
      
      # print "Lehho:"
       while True: 
         self.input(pygame.event.get()) 
         self.Curve1.drawFunc(self.time)
         self.Curve2.drawFunc(self.time)
         if (seconds >= 20000.0):
            print "Seconds: ", seconds
            self.clearScreen()
            self.Curve1.randomize()
            self.Curve2.randomize()
            delay = random.randint(35, 50)
            seconds = 0.0
         self.time = self.time + increment
         pygame.time.wait(self.delay)
         seconds = seconds + 1000.0/self.delay
         pygame.display.flip()
         
       pygame.quit()   
       pygame.exit()

#-----------------------------------------------------------------     
def main(param):
   app = App()
   i = param
   app.run()

# This isn't run on Android.
if __name__ == "__main__":
    main(1)
