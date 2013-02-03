# Python Curve class
# Written by Gary S. Worsham
# January 3, 2013
# This code covered by the GPLV3 license.
# See GPLV3.txt for details.

import pygame, sys, os, math, random, ConfigParser
from pygame.locals import *

CURVE = -1
X_FUNC = -1
Y_FUNC = -1
C_FUNC = -1

#----------------------------------------
# Import the android module. If we can't import it, set it to None - this
# lets us test it, and check to see if we want android-specific behavior.
try:
    import android
except ImportError:
    android = None

def randomRange(low, high, granularity=0.001):
    min = int(low/granularity) + 1
    max = int(high/granularity) + 1
    return random.randint(min, max) * granularity
#==========================================================================================================
class Sequence(object):
    def __init__(self, width, height, screen):
        print "==> Sequence init!"
        super(Sequence, self).__init__()
        self.screen = screen
        # print self.screen
        self.centerX = width/2
        self.centerY = height/2
        print "Center:", self.centerX, self.centerY
        # watch "width"!  here it is half width
        self.width = width/2
        self.height = height/2
#        self.curve = HarmonoGraph(self.width, self.height, self.screen)
        self.curve = Lissajous(self.width, self.height, self.screen)
        self.curve.p1 = 0.25
        self.increment = 0
        
    def adjust(self):
        self.incPhase()
        self.incDamping()
        self.curve.time = 0.0
        self.increment += 1

    def incPhase(self):
        self.curve.p1 = self.curve.p1 + 0.02
        self.curve.p4 = self.curve.p4 - 0.03
        self.curve.p2 = self.curve.p2 + 0.04
        self.curve.p3 = self.curve.p3 - 0.05
        print "increment! phase = ", self.curve.p1, self.curve.p2, self.curve.p3, self.curve.p4

    def incDamping(self):
        self.curve.d1 = self.curve.d1 + 0.00015
        self.curve.d4 = self.curve.d4 + 0.00087
        self.curve.d2 = self.curve.d2 + 0.00092
        self.curve.d3 = self.curve.d3 + 0.00074
        print "increment! damping = ", self.curve.d1, self.curve.d2, self.curve.d3, self.curve.d4

    def drawPoint(self):
        self.curve.drawPoint()
        return

#==================================================================================================    
class CurveSet(object):
    def __init__(self, width, height, screen):
        print "CurveSet init!"
        super(CurveSet, self).__init__()
        self.curvy = [(SpiroGraph, Lissajous), (Lissajous, Lissajous), (SpiroGraph, SpiroGraph2), (HarmonoGraph, Null)]
        # debug
#        self.curvy = [(SpiroGraph, Null), (SpiroGraph2, Null), (SpiroGraph, Null), (SpiroGraph2, Null)]
        # self.curvy = [(Lissajous, Lissajous), (Lissajous, Lissajous), (SpiroGraph, SpiroGraph2), (HarmonoGraph, Null)]
#        self.curvy = [(HarmonoGraph, Null), (HarmonoGraph, Null), (HarmonoGraph, Null), (HarmonoGraph, Null)]
        self.curveIndex = 0
        self.screen = screen
        # print self.screen
        self.centerX = width/2
        self.centerY = height/2
        print "Center:", self.centerX, self.centerY
        # watch "width"!  here it is half width
        self.width = width/2
        self.height = height/2

    def selectCurves(self):
        print "-----  New Curve -------------------------"
        print self.curvy[self.curveIndex]

        self.curve0 = self.curvy[self.curveIndex][0](self.width, self.height, self.screen)
        self.curve1 = self.curvy[self.curveIndex][1](self.width, self.height, self.screen)
        self.curve0Stopped = 0
        self.curve1Stopped = 0
        
        self.curveIndex = (self.curveIndex + 1) % 4
        print "Curve index: ", self.curveIndex
        self.time = 0.0

    def drawPoints(self):
        # return
        if self.curve0Stopped == 0:
            if (self.curve0.drawPoint() == -1):
                print "Stopping curve 0"
                self.curve0Stopped = 1
        if self.curve1Stopped == 0:
            if (self.curve1.drawPoint() == -1):
                print "Stopping curve 1"
                self.curve1Stopped = 1
        if (self.curve0Stopped == 1) & (self.curve1Stopped == 1):
            return -1
        else:
            return 0

#===============================================================================================================
class Curve(object):
    def __init__(self, width, height, screen):
        print "==> Curve init!"
        super(Curve, self).__init__()
        self.screen = screen
        # print self.screen
        self.centerX = width
        self.centerY = height
        print "Center:", self.centerX, self.centerY
        # watch "width"!  here it is half width
        self.width = width
        self.height = height
        print "Size:", self.width, self.height
        self.increment = 0.05
        self.time = 0.0
        self.maxPoints = 400  # how many points to draw
        self.Point = 0 # current point
        # screen drawing increments, which need to be optimized per curve type
        self.incMin = 2
        self.incMax = 4

        self.radiusScale = 1.0

        self.randomize()
        
    def randomize(self):
        print "Curve randomize!"
        
        self.f1 = randomRange(1.0, 6.0, 0.5)
        self.f2 = randomRange(1.0, 4.0, 0.5)
        self.f3 = randomRange(1.0, 6.0, 0.5)
        self.f4 = randomRange(1.0, 4.0, 0.5)
        self.f5 = randomRange(3.0, 10.0, 1.0)
        self.f6 = randomRange(5.0, 12.0, 1.0)
        print "Freq: ", self.f1, self.f2, self.f3, self.f4, self.f5, self.f6

        self.p1 = randomRange(0.0, 6.2830, 6.283/8)
        self.p2 = randomRange(0.0, 6.283, 6.283/8)
        self.p3 = randomRange(0.0, 6.283, 6.283/8)
        self.p4 = randomRange(0.0, 6.283, 6.283/8)
        print "Phase: ", self.p1, self.p2, self.p3, self.p4
        
        self.d1 = randomRange(0.001, 0.005, 0.0001)
        self.d2 = randomRange(0.001, 0.01)
        self.d3 = randomRange(0.001, 0.005, 0.0001)
        self.d4 = randomRange(0.001, 0.01)
        print "Damping: ", self.d1, self.d2, self.d3, self.d4

        # randomize some colors
        self.c1 = (123, 234, 180)
        self.c2 = (0, 234, 185)
        # print "Color: ", self.c1, self.c2
        
        self.fill = random.randint(0,3)
        # all curves have color funcs
        if C_FUNC == -1:
            self.cFunc = random.randint(0,15)
        else:
            self.cFunc = C_FUNC
            
        self.rFunc = random.randint(0,11)
        print "Curve Funcs c:", self.cFunc, " r:", self.rFunc

    def x_pos_func(self, time):
        return math.sin(time)

    def y_pos_func(self, time):
        return math.cos(time)

    def drawFunc(self, screen, color, start, end, radius, fill):
        # print start
        pygame.draw.circle(screen, color, start, max(1,int(radius * self.radiusScale)), fill)

    def drawPoint(self):
        # print self.curveType
        # get normalized coordinates from drawing functions -1.0 to +1.0
        x = self.x_pos_func(self.time)
        y = self.y_pos_func(self.time)
        # print "X, y:", x, y

        if x == None:
            return
        else:   # no point in it aww hhaaa haaaa haaa
            # first draw for positive time
            screen_x = self.centerX + int(x * self.width)
            screen_y = self.centerY + int(y * self.height)
            now_point = (screen_x, screen_y)

            radius = self.radius_func(self.time, self.rFunc)
            color = self.color_func(self.time, self.cFunc)
            # print color
            if self.time == 0.0:
                self.last = now_point
                self.time += self.increment
                return
            
            # print self.time, self.last, now_point
                
            self.drawFunc(self.screen, color, self.last, now_point, radius, min(radius, self.fill))

            if 1:
                # adjust increment so that sucessive points are drawn not too far and not too close
                # print "Last:", self.last[0], self.last[1], "Now: ", now_point
                delta_x1 = abs(self.last[0] - screen_x)
                delta_y1 = abs(self.last[1] - screen_y)

                if (delta_x1 + delta_y1) < self.incMin:
                    # print "Delta = ", delta_x1 + delta_y1
                    self.increment = self.increment * 1.5
                    # print self.increment

                if (delta_x1 + delta_y1) > self.incMax:
                    # print "Delta = ", delta_x1 + delta_y1
                    self.increment = self.increment / 1.5
                    # print self.increment

        x = self.x_pos_func(-1.0 * self.time)
        if x <> None:   # Harmonograph returns None for negative time
            y = self.y_pos_func(-1.0 * self.time)
            screen_x = self.centerX + int(x * self.width)
            screen_y = self.centerY + int(y * self.height)

            radius = self.radius_func(-self.time, self.rFunc)
            color = self.color_func(-self.time, self.cFunc)
            self.drawFunc(self.screen, color, (screen_x, screen_y), now_point, radius, min(radius, self.fill))

        self.last = now_point
        self.time += self.increment
        self.Point += 1
        if self.Point == self.maxPoints:    # stop drawing this curve
            print "maxPoints reached!", self.maxPoints
            return -1
        
    def makeStripe(self, c1, c2, c3, c4, time, rate, nBands):
        speed = 300
        stripe = abs(int((time * speed) % rate))
        b1 = rate/nBands
        b2 = b1 * 2
        b3 = b1 * 3
        b4 = b1 * 4
        b5 = (b1 * 5) - 1
        if stripe < b1:
            result = c1
            # print "B1", stripe, result
        elif stripe < b2:
            factor = (float(stripe - b1)/(b2 - b1))
            result = (c1[0] + int(factor * (c2[0] - c1[0])),c1[1] + int(factor * (c2[1] - c1[1])), min(255,c1[2] + int(factor * (c2[2] - c1[2]))))
            # print "B2", factor, stripe, result
        elif stripe < b3:
            factor = (float(stripe - b2)/(b3 - b2))
            result = (c2[0] + int(factor * (c3[0] - c2[0])),c2[1] + int(factor * (c3[1] - c2[1])), c2[2] + int(factor * (c3[2] - c2[2])))
            # print "B3", factor, stripe, result
        elif stripe < b4:
            factor = (float(stripe - b3)/(b4 - b3))
            result = ((c3[0] + int(factor * (c4[0] - c3[0]))),(c3[1] + int(factor * (c4[1] - c3[1]))), (c3[2] + int(factor * (c4[2] - c3[2]))))
            # print "B4", factor, stripe, result
        elif stripe < b5:
            factor = (float(stripe - b4)/(b5 - b4))
#            print "factor: ", factor, c1, "->", c1[0], c4, "->", c4[0]
            result = (c4[0] + int(factor * (c1[0] - c4[0])),min(255,c4[1] + int(factor * (c1[1] - c4[1]))), c4[2] + int(factor * (c1[2] - c4[2])))
#            print "B5", factor, stripe, result
        else:
            result = c4
        # print result
        return result
    
    def color_func(self, time, index):
        if (index == 0):
            result = (random.randint(1, 15)+ int(20 + 19 * math.sin(self.f1 * time)), int( 130 + 100 * math.sin(self.f2 * time)), int(20 + 19 * math.sin(self.f3 * time)))
        elif (index == 1):
            c1 = self.c1
            c2 = (0, 255, 0)
            c3 = self.c2
            c4 = (250,250,250)
            return self.makeStripe(c1, c2, c3, c4, time, 1000, 5)
        elif (index == 2):
            green = 100 + int(4 * math.pow(1 + (math.cos(time * self.f1)), 5))
            result = (0, green, int( 127 + 110 * math.sin(time * self.f2)))
            # print result    
        elif (index == 3):
            result = (random.randint(30, 40) + int(20 + 10 * math.sin((self.f3 * time))), int( 121 + 120 * math.sin(time/self.f4)), 228)
        elif (index == 4):
            c1 = self.c1
            c2 = (0, 255, 200)
            c3 = self.c2
            c4 = (200,255,200)
            return self.makeStripe(c1, c2, c3, c4, time, 1000, 5)
        elif (index == 5):  # bluish green
            result = (random.randint(10, 20), int( 147 + 100 * math.sin((self.f1 * time))), int( 130 + 99 * math.cos((time * self.f2))))
        elif (index == 6):  # chartreuse
            result = (random.randint(0, 5) + int(125 + 120 * math.sin(time * self.f1)), int( 227 + 10 * math.sin(time * self.f2)), int( 127 + 110 * math.sin(time * (self.f3))))
        elif (index == 7):  # pink blue green orange
            result = (random.randint(0, 5) + int(125 + 120 * math.sin(time * 7)), int( 67 + 10 * math.sin(time * 3)), int( 127 + 110 * math.sin(time * 9)))
        elif (index == 8):
            c1 = (255, 0 ,0)
            c2 = (0, 255, 0)
            c3 = (0, 0, 255)
            c4 = (255, 255, 255)
            return self.makeStripe(c1, c2, c3, c4, time, 2000, 5)
        elif (index == 9):
            result = (random.randint(0, 4) + int(90 + 60 * math.sin(time * 13)), int( 127 + 110 * math.sin(time * self.f2)), int( 127 + 110 * math.cos(time * self.f3)))
        elif (index == 10):
            c1 = (80 * (self.f1 % 3), 80 * (self.f2 % 3) , 80 * (self.f3 % 3))
            c2 = (0, 255, 0)
            c3 = (80 * (self.f4 % 3), 80 * (self.f5 % 3) , 80 * (self.f6 % 3))
            c4 = (0,0,255)
            return self.makeStripe(c1, c2, c3, c4, time, 1000, 5)
        elif (index == 11):
            result = (random.randint(10, 20), int( 154 + 100 * math.sin(time * self.f1)), int( 154 - 100 * math.sin(time * self.f2)))
        elif (index == 12):
            result = (random.randint(0, 4) + int(100 + (90 * math.sin(time * self.f1))), 20 , int( 127 + (100 * math.cos(time * self.f3))))
        elif (index == 13):
            result = (int(190 + (60 * math.sin(time * 15))), int( 127 + (100 * math.sin(time * 5))), 20)
        elif (index == 14):
            result = ((random.randint(10, 20)), random.randint(10, 20), int( 157 + 90 * math.sin(time * self.f4)))
        elif (index == 15):
            result = (int( 127 + 115 * math.sin(time * self.f4)),int( 127 - 115 * math.sin(time * self.f4/2)) , (random.randint(10, 20))),
        return result
        
    def radius_func(self, time, index):
        result = {
            0: lambda time: int(3 + 2 * math.sin(math.sin((self.f6 * time)/self.f5) * self.f6) + math.cos(time)),
            1: lambda time: int(4 + 3 * math.sin(math.cos((self.f5 * time)/self.f5) * self.f6)),
            2: lambda time: int(4 + 3 * math.sin(math.sin(time * self.f5))),
            3: lambda time: random.randint(3, 6),
            4: lambda time: int(3 + 2 * math.sin(math.sin(time/self.f5) * self.f6)),
            5: lambda time: int (1 + 2 * math.sqrt(abs(math.sin((time * self.f6)/self.f5)))),
            6: lambda time: int(4 + 2 * math.sin(math.sin((self.f6 * time)) * self.f6)),
            7: lambda time: int(3 + 3 * math.sin(math.sin((self.f3 * time)/self.f5) * self.f6) * math.cos((self.f4 * time))),
            8: lambda time: int(3 + 2 * math.sin(math.sin(time/self.f5) * (self.f6 % 5))),
            9: lambda time: random.randint(2, 5),
            10: lambda time: int(4 + 3 * math.sin(math.sin(time/self.f5) * self.f6)),
            11: lambda time: int (1 + 4 * math.sqrt(abs(math.sin((time * self.f5))))),
            11: lambda time: 1 # 1 + (self.f5 % 3)
            } [index] (time)
        return result

##=========================================================================================
class Null(Curve):
    def __init__(self, width, height, screen):
        print "==> Null init!"
        super(Null, self).__init__(width, height, screen)
        self.maxPoints = 1
        return
    
    def x_pos_func(self, time):
        return None

    def y_pos_func(self, time):
        return None

    def drawPoint(self):
        return -1

##=========================================================================================
class SpiroGraph(Curve):
    def __init__(self, width, height, screen):
        print "==> SpiroGraph init!"
        super(SpiroGraph, self).__init__(width, height, screen)
        self.maxPoints = 800 + random.randint(20, 1800)

        self.ell = randomRange(0.10, 0.95, 0.035) # ell and kay are l and k from Spirograph functions
        self.kay = randomRange(0.05, 0.85, 0.045)

        print "ell and kay: " , self.ell, self.kay
        
        self.radiusX = randomRange(0.85, 0.99, 0.01)
        print "Radius X:", self.radiusX

        self.radiusY = randomRange(0.75, 0.99, 0.01)

        print "Radius Y:", self.radiusY

        self.fill = 0 # random.randint(0,1)
        self.radiusScale = 0.5

        if self.f1 > self.f2:
            self.direction = 1.0
        else:
            self.direction = -1.0

    def x_pos_func(self, time):
        return (self.direction * (self.radiusX) * ((1.0 - self.kay) * math.cos(time) + ((self.ell * self.kay) * math.cos(time * (1.0 - self.kay)/self.kay))))

    def y_pos_func(self, time):
         return ((self.radiusY)* ((1.0 - self.kay) * math.sin(time) - ((self.ell * self.kay) * math.sin(time * (1.0 - self.kay)/self.kay))))


##=========================================================================================        
class SpiroGraph2(SpiroGraph):
    def __init__(self, width, height, screen):
        print "==> SpiroGraph2 init!"
        super(SpiroGraph2, self).__init__(width, height, screen)

    def y_pos_func(self, time):
         return ((self.radiusY)* ((1.0 - self.kay) * math.sin(time) + ((self.ell * self.kay) * math.sin(time * (1.0 - self.kay)/self.kay))))
        
##=========================================================================================
class HarmonoGraph(Curve):
    def __init__(self, width, height, screen):
        print "==> HarmonoGraph init!"
        super(HarmonoGraph, self).__init__(width, height, screen)

    def randomize(self):
        super(HarmonoGraph, self).randomize()
        print "Harmonograph randomize!"
            
        self.radiusX = randomRange(0.1, 0.5, 0.05)
        self.radiusX2 = 1.0 - self.radiusX
        self.radiusY = randomRange(0.1, 0.5, 0.05)
        self.radiusY2 = 1.0 - self.radiusY

        print "Radius X:", self.radiusX, self.radiusX2
        print "Radius Y:", self.radiusY, self.radiusY2
        self.maxPoints = 3600 + random.randint(20, 1000)

        self.fill = 0 # random.randint(0,1)
        self.rFunc = 11  # needed for consistency, not used...

        self.incMin = 4
        self.incMax = 8

    def x_pos_func(self, time):
        if time < 0.0:
            return None
        try:
            value = ((self.radiusX) * (math.sin((self.f1 * time) + self.p1) * math.exp(-time * self.d1)) + (self.radiusX2) * (math.sin((self.f2 * time) + self.p2)) * math.exp(-time * self.d2))
#            break
        except ValueError:
            print ">", time
            value = 0
        return value

    def y_pos_func(self, time):
        if time < 0.0:
            return None
        try:
            value = ((self.radiusY) * (math.sin((self.f3 * time) + self.p3) * math.exp(-time * self.d3)) + (self.radiusY2) * (math.sin((self.f4 * time) + self.p4)) * math.exp(-time * self.d4))
#            break
        except ValueError:
            print ">", time
            value = 0
        return value

    def drawFunc(self, screen, color, start, end, dummy1, dummy2):
        # print (start,end)
        # print color
        pygame.draw.aaline(screen, color, start, end)

##=========================================================================================
class Lissajous(Curve):
    global x_func, y_func
    def __init__(self, width, height, screen):
        print "==> Lissajous init!"
        super(Lissajous, self).__init__(width, height, screen)
        # function and data overrides
        if X_FUNC >= 0:
            self.xFunc = X_FUNC
        else:
            self.xFunc = random.randint(0,3)

        if Y_FUNC >= 0:
            self.yFunc = Y_FUNC
        else:
            self.yFunc = random.randint(0,10)
        self.maxPoints = 600 + random.randint(20, 300)

        # new data for this derived class
        self.radiusX = random.randint(10, 50)/100.0
        self.radiusX2 = 0.8 - self.radiusX
        self.radiusX3 = 0.95 - (self.radiusX + self.radiusX2)
        print "Radius X:", self.radiusX, self.radiusX2, self.radiusX3, " = ", self.radiusX + self.radiusX2 + self.radiusX3

        self.radiusY = random.randint(10, 50)/100.0
        self.radiusY2 = 0.8 - self.radiusY
        self.radiusY3 = 0.95 - (self.radiusY + self.radiusY2)

        print "Radius Y:", self.radiusY, self.radiusY2, self.radiusY3, " = ", self.radiusY + self.radiusY2 + self.radiusY3

        self.fill = random.randint(0,3)
        return
    
    def x_pos_func(self, time):
        i = math.copysign(1,math.sin(time/self.f4))
        result = {
            0: lambda time: ((self.radiusX )* math.sin((time * self.f4/self.f1) + self.p1) + (self.radiusX2)* (math.pow(math.sin((time * self.f2/self.f3) + self.p2), 3))),
            1: lambda time: ((self.radiusX * (i * (math.sqrt(abs(math.sin(time/self.f4 + self.p1))))) + self.radiusX2 * (math.sin(time * self.f3/self.f1 + self.p2)))  + self.radiusX3 * (math.cos(time * self.f2/self.f1 + self.p3))),
            2: lambda time: (self.radiusX * (math.sin(6.283 * math.sin(time/self.f1 + self.p1) + self.p2)) + (self.radiusX2 * math.sin(time * self.f2 + self.p3))  + self.radiusX3 * math.pow(math.sin(time * self.f2 + self.p4), 3)),
            3: lambda time: ((self.radiusX * math.sin(time + (6.283 * math.cos(time/(1 + (self.f3 % 3)) + self.p1))) + (self.radiusX2 * math.cos((time/self.f1) + self.p2))  + (self.radiusX3 * math.sin(time * self.f2))))
            } [self.xFunc] (time)
        return result
 
    def y_pos_func(self,time):
        i = math.copysign(1, self.f1 - self.f2)
        ii = math.copysign(1, self.f3 - self.f4)
#            print i, ii
        if (self.yFunc == 0): # sqrt(abs(cos(time))) with sign restored
            i = math.copysign(1,math.cos(time))
            result = (((self.radiusY + self.radiusY2 + self.radiusY3) * i * (math.sqrt(abs(math.cos(time))))))
        elif (self.yFunc == 1):
            y1 = i * (self.radiusY * math.cos(self.f1 * time + self.p1))
            y2 = ii * ((self.radiusY2 + self.radiusY3) * math.sin((time * self.f1/2) + self.p2))
            result =  y1 + y2
            # print result
        elif (self.yFunc == 2): # (cos(sin(f1 * t + p1)))^5 + sin ^3
            y1 = (i * (self.radiusY  + self.radiusY3)* (pow(math.cos(6.283 * math.sin(time/(1 + (self.f3)) + self.p3)), 4.0)))
            y2 = ii * self.radiusY2 * pow(math.sin((time/(0.5 + self.f1)) + self.p2), 3.0)                                             
            result =  y1 + y2
        elif (self.yFunc == 3): # cosine + sine
            y1 = (i * self.radiusY * (math.cos((time * self.f2) + self.p1)))
            y2 = ii * (self.radiusY2  + self.radiusY3) * math.sin((time * self.f3) + self.p2)
            result =  y1 + y2
        elif (self.yFunc == 4):
            result = (i * self.radiusY * (math.sin(time * self.f3)) + ii * (self.radiusY2) * math.sqrt(abs(math.sin(time * self.f4))))
        elif (self.yFunc == 5):
            freq = 1.0/(1 + (self.f3 % 5))
            result = (i * ((self.radiusY + self.radiusY3) * (math.cos(time * freq))) + ii * (self.radiusY2 * math.cos(time * 3 * freq)))
        elif (self.yFunc == 6):
            result = (i * self.radiusY * (math.pow(math.cos((self.f4 * time)/self.f3), 3)) + ii * (self.radiusY2  + self.radiusY3) * math.sqrt(abs(math.sin(time  * self.f4))))
        elif (self.yFunc == 7):
            result = (i * self.radiusY * math.pow((math.cos(time * self.f3)), 3) + ii * self.radiusY2 * (math.pow(math.cos(time * self.f4), 2)) + (i * ii) * self.radiusY3 * (math.pow(math.cos(time * self.f2), 5)))
        elif (self.yFunc == 8):
            y1 = i * self.radiusY * (math.pow(math.cos((self.f4 * time) + self.p4), (1 + int(self.p3))))
            y2 = ii * (self.radiusY2 + self.radiusY3) * (math.pow(math.cos((time * self.f3) + self.p3),(1 + int(self.f2))))
            result =  y1 + y2
        elif (self.yFunc == 9):
            result = ((self.radiusY + self.radiusY2 + self.radiusY3) * math.cos(time))     # for test drawing of X functions
        elif (self.yFunc == 10):
            result = ((i * self.radiusY * math.cos(time)) + (ii * self.radiusY2 * math.sin(time * self.f3))  + (self.radiusY3 * math.cos(time * self.f4)))    
        elif (self.yFunc == 11):
            result = ((i * self.radiusY * (0.66 * math.cos(time)) + (0.22 * math.cos(3 * time)) + (0.11 * math.cos(5 * time))) + (ii * self.radiusY2 * math.sin(time * self.f3))  + (self.radiusY3 * math.cos(time * self.f_4)))    
        return result

    def color_func(self, time, index):
        if (index == 0):
            result = (random.randint(1, 15)+ int(20 + 19 * math.sin(self.f2 * time)), int( 130 + 100 * math.sin(time)), int(20 + 19 * math.sin(self.f2 * time)))
        elif (index == 1):
            c1 = (25, int(60 * (min(self.f2,3.0))) , min(255, int(80 * (self.f3 % 4))))
            c2 = (0, 255, 0)
            c3 = (min (254, int(80 * (self.f4))), min (254, int(50 * (self.f5))) , min (254, int(20 * (self.f6))))
            c4 = (255,255,255)
            return self.makeStripe(c1, c2, c3, c4, time, 1000, 5)
        elif (index == 2):
            freq = self.f2/2
            green = 100 + int(4 * math.pow(1 + (math.cos(time * freq)), 5))
            result = (0, green, int( 127 + 110 * math.sin(time * freq * self.f3)))
            # print result    
        elif (index == 3):
            result = (random.randint(30, 40) + int(20 + 10 * math.sin((self.f4 * time)/self.f5 )), int( 121 + 120 * math.sin(time/(1 + (self.f6 % 4)))), 228)
        elif (index == 4):
            c1 = (min(255,int(60 * (self.f1))), min(255, int(10 * (self.f2))) , min(255, int(60 * (self.f3))))
            c2 = (0, 255, 0)
            c3 = (min(255,int(60 * (self.f3))), min(255, int(60 * (self.f2))) , min(255, int(10 * (self.f4))))
            c4 = (255,255,255)
            return self.makeStripe(c1, c2, c3, c4, time, 1000, 5)
        elif (index == 5):  # bluish green
            result = (random.randint(10, 20), int( 147 + 100 * math.sin((self.f1 * time))), int( 130 + 99 * math.cos((time * self.f2 % 4))))
        elif (index == 6):  # chartreuse
            result = (random.randint(0, 5) + int(125 + 120 * math.sin(time * self.f2)), int( 227 + 10 * math.sin(time * self.f1)), int( 127 + 110 * math.sin(time * (self.f4))))
        elif (index == 7):  # pink blue green orange
            result = (random.randint(0, 5) + int(125 + 120 * math.sin(time * 7)), int( 67 + 10 * math.sin(time * 3)), int( 127 + 110 * math.sin(time * 9)))
        elif (index == 8):
            c1 = (255, 0 ,0)
            c2 = (0, 255, 0)
            c3 = (0, 0, 255)
            c4 = (255, 255, 255)
            return self.makeStripe(c1, c2, c3, c4, time, 2000, 5)
        elif (index == 9):
            result = (random.randint(0, 4) + int(90 + 60 * math.sin(time * 13)), int( 127 + 110 * math.sin(time * self.f2)), int( 127 + 110 * math.cos(time * self.f3)))
        elif (index == 10):
            c1 = (80 * (self.f1 % 3), 80 * (self.f2 % 3) , 80 * (self.f3 % 3))
            c2 = (0, 255, 0)
            c3 = (80 * (self.f4 % 3), 80 * (self.f5 % 3) , 80 * (self.f6 % 3))
            c4 = (0,0,255)
            return self.makeStripe(c1, c2, c3, c4, time, 1000, 5)
        elif (index == 11):
            result = (random.randint(10, 20), int( 154 + 100 * math.sin(time * 7)), int( 154 - 100 * math.sin(time * 7)))
        elif (index == 12):
            result = (random.randint(0, 4) + int(100 + (90 * math.sin(time * 9))), 20 , int( 127 + (100 * math.cos(time * self.f3))))
        elif (index == 13):
            result = (int(190 + (60 * math.sin(time * 15))), int( 127 + (100 * math.sin(time * 5))), 20)
        elif (index == 14):
            result = ((random.randint(10, 20)), random.randint(10, 20), int( 157 + 90 * math.sin(time * self.f4)))
        elif (index == 15):
            result = (int( 127 + 115 * math.sin(time * self.f4)),int( 127 - 115 * math.sin(time * self.f4/2)) , (random.randint(10, 20))),
        return result
        
    def radius_func(self, time, index):
        result = {
            0: lambda time: int(3 + 2 * math.sin(math.sin((self.f1 * time)/self.f3) * self.f4) + math.cos(time)),
            1: lambda time: int(4 + 3 * math.sin(math.cos((self.f4 * time)))),
            2: lambda time: int(4 + 3 * math.sin(math.sin(time * self.f3))),
            3: lambda time: random.randint(3, 6),
            4: lambda time: int(3 + 2 * math.sin(math.sin(time/self.f3))),
            5: lambda time: int (1 + 2 * math.sqrt(abs(math.sin((time * self.f2)/self.f3)))),
            6: lambda time: int(4 + 2 * math.sin(math.sin((self.f4 * time)))),
            7: lambda time: int(3 + 3 * math.sin(math.sin((self.f3 * time)/self.f4) * self.f2) * math.cos((self.f4 * time))),
            8: lambda time: int(3 + 2 * math.sin(math.sin(time/self.f1) * (self.f2 % 5))),
            9: lambda time: random.randint(2, 5),
            10: lambda time: int(4 + 3 * math.sin(math.sin(time/self.f3))),
            11: lambda time: int (1 + 4 * math.sqrt(abs(math.sin((time * self.f3))))),
            11: lambda time: 1 # 1 + (self.f5 % 3)
            } [index] (time)
        return result

##=========================================================================================
class oldLissajous(Curve):
    global x_func, y_func
    def __init__(self, width, height, screen):
        print "==> Old Lissajous init!"
        super(oldLissajous, self).__init__(width, height, screen)
        if X_FUNC >= 0:
            self.xFunc = X_FUNC
        else:
            self.xFunc = random.randint(0,3)

        if Y_FUNC >= 0:
            self.yFunc = Y_FUNC
        else:
            self.yFunc = random.randint(0,10)
            
        self.radiusX = random.randint(10, 50)/100.0
        self.radiusX2 = 0.8 - self.radiusX
        self.radiusX3 = 0.95 - (self.radiusX + self.radiusX2)
        print "Radius X:", self.radiusX, self.radiusX2, self.radiusX3, " = ", self.radiusX + self.radiusX2 + self.radiusX3

        self.radiusY = random.randint(10, 50)/100.0
        self.radiusY2 = 0.8 - self.radiusY
        self.radiusY3 = 0.95 - (self.radiusY + self.radiusY2)

        print "Radius Y:", self.radiusY, self.radiusY2, self.radiusY3, " = ", self.radiusY + self.radiusY2 + self.radiusY3

        self.fill = random.randint(0,3)
        return

    def randomize(self):
        self.fct_1 = random.randint(3,6)
        self.fct_2 = random.randint(3,9)
        self.fct_3 = random.randint(4,8)
        self.fct_4 = random.randint(4,12)
        self.fct_5 = random.randint(5,15)
        self.fct_6 = random.randint(5,20)
        print "Curve Randoms: ", self.fct_1, self.fct_2, self.fct_3, self.fct_4, self.fct_5, self.fct_6
    
    def x_pos_func(self, time):
        i = math.copysign(1,math.sin(time/self.fct_4))
        result = {
            0: lambda time: ((self.radiusX )* (math.sin(time * self.fct_5/self.fct_1)) + (self.radiusX2)* (math.pow(math.sin(time * self.fct_6/self.fct_4), (self.fct_5 % 4)))),
            1: lambda time: ((self.radiusX * (i * (math.sqrt(abs(math.sin(time/self.fct_4))))) + self.radiusX2 * (math.sin(time * self.fct_3/self.fct_1)))  + self.radiusX3 * (math.cos(time * self.fct_6/self.fct_1))),
            2: lambda time: (self.radiusX * (math.sin(6.283 * math.sin(time/self.fct_1))) + (self.radiusX2 * math.sin(time * self.fct_2))  + self.radiusX3 * math.pow(math.sin(time * self.fct_2), (self.fct_5 % 4))),
            3: lambda time: ((self.radiusX * math.sin(time + (6.283 * math.cos(time/(1 + (self.fct_3 % 3))))) + (self.radiusX2 * math.cos(time/self.fct_1))  + (self.radiusX3 * math.sin(time * self.fct_2))))
            } [self.xFunc] (time)
        return result
 
    def y_pos_func(self,time):
        i = math.copysign(1, self.fct_1 - self.fct_2)
        ii = math.copysign(1, self.fct_3 - self.fct_4)
#            print i, ii
        if (self.yFunc == 0):
            i = math.copysign(1,math.cos(time))
            result = (((self.radiusY + self.radiusY2 + self.radiusY3) * i * (math.sqrt(abs(math.cos(time))))))
        elif (self.yFunc == 1):
            result = (i * (self.radiusY * math.cos(time)) + ii * ((self.radiusY2 + self.radiusY3) * math.sin(time * (self.fct_5))/2))
        elif (self.yFunc == 2):
            result = (i * (self.radiusY  + self.radiusY3)* (math.cos(6.283 * math.sin(time/(1 + (self.fct_3 % 2))))) + ii * self.radiusY2 * math.sin(time/(1 + (self.fct_1 % 3))))
        elif (self.yFunc == 3):
            result = (i * self.radiusY * (math.cos(time * self.fct_2)) + ii * (self.radiusY2  + self.radiusY3) * math.sin(time * self.fct_3))
        elif (self.yFunc == 4):
            result = (i * self.radiusY * (math.sin(time * self.fct_3)) + ii * (self.radiusY2) * math.sqrt(abs(math.sin(time  * self.fct_4))))
        elif (self.yFunc == 5):
            freq = 1.0/(1 + (self.fct_3 % 5))
            result = (i * ((self.radiusY + self.radiusY3) * (math.cos(time * freq))) + ii * (self.radiusY2 * math.cos(time * 3 * freq)))
        elif (self.yFunc == 6):
            result = (i * self.radiusY * (math.pow(math.cos((self.fct_4 * time)/self.fct_3), 3)) + ii * (self.radiusY2  + self.radiusY3) * math.sqrt(abs(math.sin(time  * self.fct_4))))
        elif (self.yFunc == 7):
            result = (i * self.radiusY * (math.pow((math.cos(time * self.fct_3)), (1 + (self.fct_2 % 3)))) + ii * self.radiusY2 * (math.pow(math.cos(time * self.fct_5),(1 + (self.fct_2 % 3)))) + (i * ii) * self.radiusY3 * (math.pow(math.cos(time * self.fct_2),(1 + (self.fct_2 % 3)))))
        elif (self.yFunc == 8):
            result = (i * self.radiusY * (math.pow(math.cos((self.fct_4 * time)), 3)) + ii * (self.radiusY2 + self.radiusY3) * (math.pow(math.cos(time * self.fct_3),(1 + (self.fct_2 % 4)))))
        elif (self.yFunc == 9):
            result = ((self.radiusY + self.radiusY2 + self.radiusY3) * math.cos(time))     # for test drawing of X functions
        elif (self.yFunc == 10):
            result = ((i * self.radiusY * math.cos(time)) + (ii * self.radiusY2 * math.sin(time * self.fct_3))  + (self.radiusY3 * math.cos(time * self.fct_4)))    
        elif (self.yFunc == 11):
            result = ((i * self.radiusY * (0.66 * math.cos(time)) + (0.22 * math.cos(3 * time)) + (0.11 * math.cos(5 * time))) + (ii * self.radiusY2 * math.sin(time * self.fct_3))  + (self.radiusY3 * math.cos(time * self.fct_4)))    
        return result                          
  
    def drawFunc(self, screen, color, start, end, radius, fill):
        # print start
        pygame.draw.circle(screen, color, start, radius, fill)

##=========================================================================================
class curveTest():
    def __init__(self):
        self.c = Lissajous()
        print"curveTest!"       
    def x_pos_func(self, time):
        if X_FUNC == -1:
            return (time/80.0) - 1.0
        else:
            return self.c.x_pos_func((time /800) * (400/8))
        
    def y_pos_func(self, time):
        if Y_FUNC == -1:
            return (time/80.0) - 1.0
        else:
            return self.c.y_pos_func((time /800) * (600/8))

    def drawFunc(self, screen, color, start, end, radius, fill):
        # print start
        pygame.draw.circle(screen, color, start, 1, 1)
