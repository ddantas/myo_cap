from PyQt5 import QtTest
from datetime import datetime
import pygame
from pygame import *
import time
import threading
import datetime

from pyqtgraph.Qt import QtCore, QtGui
import Leap, sys, thread, time, LeapMotion
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

from LeapMotion import LeapMotionListener

white = (255, 255, 255)
black = (0, 0, 0)
aux = 0
class Main(QtGui.QMainWindow):

    def display_screen(self,gameDisplay,output,frameT):
        aux = 0

        y0 = 600
        x0 = 100
        xStep = 30
        w = 20
        c = 5

        pygame.draw.rect(gameDisplay, black, [x0, y0+100-output[0], 20, output[0]+c])
        pygame.draw.rect(gameDisplay, white, [x0, y0,               20, 100-output[0]])

        pygame.draw.rect(gameDisplay, black, [x0+xStep, y0+x0-output[1], 20, output[1]+c])
        pygame.draw.rect(gameDisplay, white, [x0+xStep, y0,         20, 100-output[1]])

        pygame.draw.rect(gameDisplay, black, [x0+(xStep*2), y0+x0-output[2], 20, output[2]+c])
        pygame.draw.rect(gameDisplay, white, [x0+(xStep*2), y0,     20, 100-output[2]])

        pygame.draw.rect(gameDisplay, black, [x0+(xStep*3), y0+x0-output[3], 20, output[3]+c])
        pygame.draw.rect(gameDisplay, white, [x0+(xStep*3), y0,     20, 100-output[3]])

        pygame.draw.rect(gameDisplay, black, [x0+(xStep*4), y0+x0-output[4], 20, output[4]+c])
        pygame.draw.rect(gameDisplay, white, [x0+(xStep*4), y0,     20, 100-output[4]])

        myfont = pygame.font.SysFont("arial", 15)
        pygame.draw.rect(gameDisplay, white, [300, 650,50,50])

        # render text
        if frameT != aux:
            pygame.draw.rect(gameDisplay, white, [300,650, 50,50])

            label = myfont.render("C/s: "+str(frameT), 1, (0, 0, 0))
            gameDisplay.blit(label, (300, 650))

            aux = frameT

            pygame.display.update()

        pygame.display.update()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.showMainWindow()
    sys.exit(app.exec_())
    window.stopCapture()