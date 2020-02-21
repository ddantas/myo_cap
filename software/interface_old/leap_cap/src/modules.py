from PyQt5 import QtTest
from PyQt5 import QtWidgets
from datetime import datetime
import pygame
from pygame import *
import threading
import datetime
import  time

from pyqtgraph.Qt import QtCore, QtGui
import Leap, sys, thread, time, LeapMotion
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

from LeapMotion import LeapMotionListener
#import StatusFinger
import converter

from StatusFinger import Main

sys.path.append("../../")

#from tiva import Main
# from tiva import lineTiva

#from tiva import Main

tivaGlobal = None

gameDisplay = 0
linesEmg = []
logend = open('../routine/log.txt', 'a')


# outputKey = ""q

def endCapture(self, tiva):
    pygame.quit()
    #sys.exit()
    #tiva.textfile.save('/data/%s.log' % (datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))


def keyCapture(self, tiva, textId, statusFinger):
    global gameDisplay
    global logend

    white = (255, 255, 255)
    black = (0, 0, 0)

    old_k_delay, old_k_interval = pygame.key.get_repeat()
    pygame.key.set_repeat(500, 30)
    i = 0
    p = 8
    gameExit = False

    outputKey = [0,0,0,0,0]

    ini = time.time()
    timeBase = ini - ini
    frame = 0
    frameT = 0
    try:
        while not gameExit:
            for event in pygame.event.get():


                if event.type == pygame.QUIT:
                    gameExit = True

                if pygame.key.get_pressed()[pygame.K_ESCAPE] != 0:
                    endCapture(self, tiva)

                if pygame.key.get_pressed()[pygame.K_SPACE] != 0:
                    outputKey[0] = 100
                else:
                    outputKey[0] = 0

                if pygame.key.get_pressed()[pygame.K_7] != 0:
                    outputKey[1] = 100
                else:
                    outputKey[1] = 0
                if pygame.key.get_pressed()[pygame.K_8] != 0:
                    outputKey[2] = 100
                else:
                    outputKey[2] = 0
                if pygame.key.get_pressed()[pygame.K_9] != 0:
                    outputKey[3] = 100
                else:
                    outputKey[3] = 0

                if pygame.key.get_pressed()[pygame.K_0] != 0:
                    outputKey[4] = 100
                else:
                    outputKey[0] = 0

                fim = time.time()
                timeFim = fim - ini

                n = 10
                if (timeFim - timeBase) >= n:
                    timeBase = timeFim
                    frameT = frame
                    frame = 0

                frame += 1
                #tiva.textfile.log(textId, outputKey)
                statusFinger.display_screen(gameDisplay,outputKey,frameT/n)

                p += 1
                pygame.draw.rect(gameDisplay, black, [100, 700, 20, 2])
                pygame.draw.rect(gameDisplay, black, [130, 700, 20, 2])
                pygame.draw.rect(gameDisplay, black, [160, 700, 20, 2])
                pygame.draw.rect(gameDisplay, black, [190, 700, 20, 2])
                pygame.draw.rect(gameDisplay, black, [220, 700, 20, 2])
                pygame.display.update()


    finally:
        pygame.key.set_repeat(old_k_delay, old_k_interval)


def leapCapture(self, tiva, textId, statusFinger):
    global tivaGlobal
    global gameDisplay

    #pygame.init()

    #old_k_delay, old_k_interval = pygame.key.get_repeat()

    #pygame.key.set_repeat(500, 30)
    gameExit = False
    listener = LeapMotionListener(tiva, textId, statusFinger)
    controller = Leap.Controller()


#time seg e nanoseg
    try:
        while not gameExit:
            for event in pygame.event.get():
                if pygame.key.get_pressed()[pygame.K_ESCAPE] != 0:
                    endCapture(self,tiva)
                    gameExit = True
                    #tiva.textfile.save('/data/%s.log' % (datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))



            controller.add_listener(listener)
            controller.remove_listener(listener)

    except Exception as e:
        print(e)

def printScreen(self, routine):
    global gameDisplay

    filename = "../images/" + routine[0].img + ".png"
    try:
        img1 = pygame.image.load(filename)
    except:
        print("Error loading image from " + filename)
        sys.exit()

    img_w = img1.get_width()
    img_h = img1.get_height()

    tamMin = 50
    tamMax = 1200

    routine_size = len(routine)
    j = 0
    black = (0, 0, 0)

    white = (255, 255, 255)
    jump = (tamMax / routine_size)
    porcent = 0
    gameExit = False

    try:
        pygame.draw.rect(gameDisplay, black, [10, 430, 1270, 20])
        pygame.draw.rect(gameDisplay, white, [12, 432, 1266, 16])
        pygame.display.update()

        pygame.draw.rect(gameDisplay, black, [15, 410, 300, 17])
        pygame.display.update()
        pygame.draw.rect(gameDisplay, white, [17, 412, 296, 13])
        pygame.display.update()

        while (j < routine_size and gameExit == False):
            if pygame.key.get_pressed()[pygame.K_ESCAPE] != 0:
                gameExit = True

            x = 10; y = 30
            img1 = pygame.image.load("../images/" + routine[j].img + ".png")
            gameDisplay.blit(img1, (10, 30))

            x = 330; y = 30
            if (j+1 < routine_size):
                img2 = pygame.image.load("../images/" + routine[j + 1].img + "EC.png")
                gameDisplay.blit(img2, (x, y))
            else:
                pygame.draw.rect(gameDisplay, white, [x, y, img_w, img_h])

            x = 660; y = 30
            if (j+2 < routine_size):
                img3 = pygame.image.load("../images/" + routine[j + 2].img + "EC.png")
                gameDisplay.blit(img3, (660, 30))
            else:
                pygame.draw.rect(gameDisplay, white, [x, y, img_w, img_h])

            x = 990; y = 30
            if (j+3 < routine_size):
                img4 = pygame.image.load("../images/" + routine[j + 3].img + "EC.png")
                gameDisplay.blit(img4, (990, 30))
            else:
                pygame.draw.rect(gameDisplay, white, [x, y, img_w, img_h])

            pygame.display.update()

            j = j + 1

            c = 0
            por = 0
            qtdframes = 20
            aux = (300 - 15) / qtdframes
            while c < qtdframes:
                # print por
                pygame.draw.rect(gameDisplay, black, [19, 413, por, 11])
                pygame.display.update()

                por = por + aux
                QtTest.QTest.qWait(100)
                c = c + 1

            pygame.draw.rect(gameDisplay, white, [19, 413, 294, 11])
            pygame.display.update()

            pygame.draw.rect(gameDisplay, black, [14, 433, porcent, 14])
            pygame.display.update()

            porcent += jump

    except:
        sys.exit()


def start(self, tiva, sequencia, lineEmg, device):
    global gameDisplay
    global linesEmg

    pygame.init()
    white = (255, 255, 255)
    black = (0, 0, 0)
    gameDisplay = pygame.display.set_mode((1600, 740))

    gameDisplay.fill(white)
    pygame.display.update()


    statusFinger = Main(self)

    if device == 'Keyboard':
        textId = tiva.textfile.init(5, "%d;%d;%d;%d;%d;", "key")
        tk = tKey(tiva, textId, statusFinger)
        tk.start()
    if device == 'Leap Motion':
        textId = tiva.textfile.init(15, "%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;", "lp")
        tL = tLeap(tiva, textId, statusFinger)
        tL.start()
    if device == 'None':
        print ("Not found")

    tPS = tPrintS(sequencia)
    tPS.start()
    #printScreen(sequencia)

class tPrintS(threading.Thread):
    def __init__(self, sequencia):
        self.sequencia = sequencia
        threading.Thread.__init__(self)

    def getSequencia(self):
        return self.sequencia

    def run(self):
        printScreen(self=None, routine=self.getSequencia())


class tKey(threading.Thread):
    def __init__(self, tiva, textId, statusFinger):
        self.tiva = tiva
        self.textId = textId
        self.statusFinger = statusFinger
        threading.Thread.__init__(self)

    def getTiva(self):
        return self.tiva

    def getId(self):
        return self.textId

    def getStatusFinger(self):
        return self.statusFinger

    def run(self):
        keyCapture(self=None, tiva=self.getTiva(), textId=self.getId(), statusFinger=self.getStatusFinger())


class tLeap(threading.Thread):
    def __init__(self, tiva, textId, statusFinger):
        self.tiva = tiva
        self.textId = textId
        self.statusFinger = statusFinger
        threading.Thread.__init__(self)

    def getTiva(self):
        return self.tiva

    def getId(self):
        return self.textId

    def getStatusFinger(self):
        return self.statusFinger

    def run(self):
        leapCapture(self=None, tiva=self.getTiva(), textId=self.getId(), statusFinger=self.getStatusFinger())