# Python Curve class
# Written by Gary S. Worsham
# January 3, 2013
# This code covered by the GPLV3 license.
# See GPLV3.txt for details.

import pygame, sys, os, math, random
from pygame.locals import *
# Import the android module. If we can't import it, set it to None - this
# lets us test it, and check to see if we want android-specific behavior.
try:
    import android
except ImportError:
    android = None

class Curve():
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        
        self.radius = self.width/4
        self.radius2 = 80
    
    def x_pos_func(self, time, index):
        i = math.copysign(1,math.sin(time/self.fct_4))
        result = {
            0: lambda time: int(self.width/2 + self.radius * (math.sin(time/self.fct_1)) + self.radius2 * math.sin(time * (self.fct_2 + 3))),
            1: lambda time: int(self.width/2 + (self.radius + self.radius2) * (math.sin((time * self.fct_4)/self.fct_3))),
            2: lambda time: int(self.width/2 + self.radius * (math.sin(time)) + self.radius2 * math.sin(6.283 * math.cos(time/(self.fct_2)))),
            3: lambda time: int(self.width/2 + (self.radius + self.radius2 )* (math.sin(time * self.fct_1/self.fct_1))),
            4: lambda time: int(self.width/2 + self.radius * (math.sin(6.283/self.fct_2 + time/self.fct_1)) + self.radius2 * math.sin(time * self.fct_2)),
            5: lambda time: int(self.width/2 + (self.radius * math.sin(time/self.fct_1) + (self.radius2/2) * (math.sin(time * self.fct_1)))),
            6: lambda time: int(self.width/2 + (self.radius * (math.sin(time/self.fct_1)))),
            7: lambda time: int(self.width/2 + (self.radius * (i * (math.sqrt(abs(math.sin(time/self.fct_4))))) + self.radius2 * (math.sin(time * self.fct_1/self.fct_1))))
            } [index] (time)
        return result
 
    def y_pos_func(self, time, index):
        i = math.copysign(1, self.fct_1 - self.fct_2)
        ii = math.copysign(1, self.fct_3 - self.fct_4)
#            print i, ii
        if (index == 0):
            i = math.copysign(1,math.cos(time))
            result = int(self.height/2 + (self.radius * i * (math.sqrt(abs(math.cos(time))))))
        if (index == 1):
            result = int(self.height/2 + i * (self.radius * math.cos(time)) + ii * (self.radius2 * math.sin(time * (self.fct_5))/2))
        if (index == 2):
            result = int(self.height/2 + i * self.radius * (math.cos(6.283 * math.sin(time/self.fct_3))) + ii * self.radius2 * math.sin(time/self.fct_1))
        if (index == 3):
            result = int(self.height/2 + i * self.radius * (math.cos(time * self.fct_4)) + ii * self.radius2 * math.sin(time * (self.fct_3)))
        if (index == 4):
            result = int(self.height/2 + i * self.radius * (math.sin(time/self.fct_3)) + ii * self.radius2 * math.sqrt(abs(math.sin(time  * self.fct_4))))
        if (index == 5):
            result = int(self.height/2 + i * ((self.radius + self.radius2) * (math.cos(time/(1 + (self.fct_3 % 3))))))
        if (index == 6):
            result = int(self.height/2 + i * self.radius * (math.pow(math.cos((self.fct_4 * time)/self.fct_3), 3)))
        if (index == 7):
            result = int(self.height/2 + i * self.radius * (math.pow((math.cos(time/3)), (1 + (self.fct_2 % 3)))) + ii * self.radius2 * (math.pow(math.cos(time/5),(1 + (self.fct_2 % 3)))))
        if (index == 8):
            result = int(self.height/2 + i * self.radius * (math.pow(math.cos((self.fct_4 * time)/self.fct_3), 3))) + ii * self.radius2 * (math.pow(math.cos(time/self_fct3),(1 + (self.fct_2 % 4))))
        if (index == 9):
            result = int(time * self.speed/6.283)    # for test drawing of X functions
        return result

    def color_func(self, time, index):
        speed = 300
        if (index == 0):
            result = (random.randint(10, 15)+ int( 139 + 100 * math.cos(self.fct_1 * time)), int( 130 + 100 * math.sin(time/self.fct_4)), int(50 + 39 * math.sin(self.fct_2 * time)))
        elif (index == 1):
            result = (random.randint(0, 4) + int(190 + 60 * math.sin(time * (self.fct_1 + self.fct_4))), int( 27 + 10 * math.sin(time * 2)), int( 127 + 100 * math.cos(time * self.fct_3)))
        elif (index == 2):
            result = (random.randint(12, 15)+ int( 107 + 60 * math.cos(3 * time)), int( 127 + 100 * math.sin(time * 3)), int( 100 + 90 * math.sin(2 * time)))
        elif (index == 3):
            result = (random.randint(30, 40) + int(20 + 10 * math.sin((self.fct_4 * time)/self.fct_5 )), int( 147 + 100 * math.sin(time/self.fct_6)), 228)
        elif (index == 4):
            result = (random.randint(0, 7)+ int( 147 + 100 * math.cos(time * self.fct_4)), int( 107 + 25 * math.sin(time /self.fct_6)), int( 100 + 99 * math.sin(time/2)))
        elif (index == 5):
            result = (random.randint(10, 20), int( 147 + 100 * math.sin((self.fct_5 * time))), int( 130 + 99 * math.cos((time * self.fct_2 % 4))))
        elif (index == 6):
            result = (random.randint(0, 5) + int(125 + 120 * math.sin(time * 11)), int( 67 + 10 * math.sin(time * 5)), int( 127 + 110 * math.sin(time * 3)))
        elif (index == 7):
            result = (random.randint(0, 5) + int(125 + 120 * math.sin(time * 7)), int( 67 + 10 * math.sin(time * 3)), int( 127 + 110 * math.sin(time * 9)))
        elif (index == 8):
            stripe = (time * speed) % 100
            if stripe < 33:
                result = (200, 0, 0)
            elif stripe < 66:
                result = (0,200,0)
            else:
                 result = (0,0,200)
        elif (index == 9):
            result = (random.randint(0, 4) + int(90 + 60 * math.sin(time * 13)), int( 127 + 110 * math.sin(time * self.fct_2)), int( 127 + 110 * math.cos(time * self.fct_3)))
        elif (index == 10):
            stripe = (time * speed) % 200
            if stripe < 40:
                result = (100, 100, 100)
            elif stripe < 80:
                result = (0,255,0)
            elif stripe < 120:
                result = (250,255,250)
            elif stripe < 160:
                result = (0,0,255)
            else:
                result = (200,200,200)
        elif (index == 11):
            result = (random.randint(10, 40), int( 127 + 100 * math.sin(time * 7)), (random.randint(10, 20)))
        elif (index == 12):
            result = (random.randint(0, 4) + int(90 + 60 * math.sin(time * 9)), 20 , int( 127 + 100 * math.cos(time * self.fct_3)))
        elif (index == 13):
            result = (random.randint(0, 4) + int(190 + 60 * math.sin(time * 15)), int( 127 + 100 * math.sin(time * 5)), 20)
        elif (index == 14):
            result = ((random.randint(10, 20)), random.randint(10, 20), int( 147 + 100 * math.sin(time * 7)))
        elif (index == 15):
            result = (int( 147 + 100 * math.sin(time * self.fct_4)), random.randint(10, 20), (random.randint(10, 20))),
        return result
        
    def radius_func(self, time, index):
        result = {
            0: lambda time: int(4 + 2 * math.sin(math.sin((self.fct_6 * time)/self.fct_5) * self.fct_6)),
            1: lambda time: int(5 + 3 * math.sin(math.sin((self.fct_5 * time)/self.fct_5) * self.fct_6)),
            2: lambda time: int(6 + 4 * math.sin(math.sin(time * self.fct_5))),
            3: lambda time: random.randint(3, 6),
            4: lambda time: int(6 + 2 * math.sin(math.sin(time/self.fct_5) * self.fct_6)),
            5: lambda time: int (1 + 5 * math.sqrt(abs(math.sin((time * self.fct_6)/self.fct_5)))),
            6: lambda time: int(4 + 2 * math.sin(math.sin((self.fct_6 * time)) * self.fct_6)),
            7: lambda time: int(5 + 3 * math.sin(math.sin((self.fct_5 * time)/self.fct_5) * self.fct_6) * math.sin((self.fct_4 * time))),
            8: lambda time: int(6 + math.sin(math.sin(time/self.fct_5) * self.fct_6)),
            9: lambda time: random.randint(2, 5),
            10: lambda time: int(6 + 3* math.sin(math.sin(time/self.fct_5) * self.fct_6)),
            11: lambda time: int (1 + 5 * math.sqrt(abs(math.sin((time * self.fct_5)))))
            } [index] (time)
        return result
                             
    def randomize(self):
        self.fct_1 = random.randint(3,5)
        self.fct_2 = random.randint(3,5)
        self.fct_3 = random.randint(3,7)
        self.fct_4 = random.randint(3,7)
        self.fct_5 = random.randint(3,19)
        self.fct_6 = random.randint(7,15)

        print "Fcts 1: ", self.fct_1, self.fct_2, self.fct_3, self.fct_4, self.fct_5, self.fct_6

        self.xFunc = random.randint(0,7)
        self.yFunc = random.randint(0,7)
        self.cFunc = random.randint(0,15)
        self.rFunc = random.randint(0,11)

        print "Funcs 1 x:", self.xFunc, " y:", self.yFunc, " c:", self.cFunc, " r:", self.rFunc

        self.fill = random.randint(0,3)

    def drawFunc(self, time): 
       x = self.x_pos_func(time, self.xFunc)
       y = self.y_pos_func(time, self.yFunc)
       radius = self.radius_func(time, self.rFunc)
       color = self.color_func(time, self.cFunc)
       pygame.draw.circle(self.screen, color, (x, y), radius, min(radius, self.fill))
       
       x = self.x_pos_func(-time, self.xFunc)
       y = self.y_pos_func(-time, self.yFunc)
       radius = self.radius_func(-time, self.rFunc)
       color = self.color_func(-time, self.cFunc)
       pygame.draw.circle(self.screen, color, (x, y), radius, min(radius, self.fill))
