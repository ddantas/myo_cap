import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

import pygame 
from pygame import *
import numpy as np
import time
import modules


sys.path.append("../../")


allFingers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


class LeapMotionListener(Leap.Listener):

    def __init__(self, tiva, textId, statusFinger):
        self.statusFinger = statusFinger
        self.tiva = tiva
        self.textId = textId
        self.ini = time.time()
        self.timeBase = self.ini - self.ini
        self.frame = 0
        self.frameT = 0
        self.n = 1
        Leap.Listener.__init__(self)

    finger_names = ['Polegar','Indicador','Meio','Anular','Mindinho']
    bone_names = ['Metacarpo','Proximal','Intermediario','Distal']
    state_names = ['STATE_INVALID','STATE_START','STATE_UPDATE','STATE_END']

    #tiva = Main(self)
    #id = tiva.textfile.init(15, "%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;", "key")

    #def on_init(self, controller):
            #print"Inicializado"

    def on_connect(self, controller):
            #print"Sensor Conectado"
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
            print"Sensor Desconectado"
       # def on_exit(self, controller):
       #     print"Saiu"
    def on_frame(self, controller):

        frame = controller.frame()
        outputLeap = [0,0,0,0,0]
        for hand in frame.hands:
            del allFingers[:]

            for finger  in hand.fingers:

                bone = finger.bone(0)
                bone2 = finger.bone(1)
                bone3 = finger.bone(2)
                bone4 = finger.bone(3)

                proximal_angle =  bone.direction.angle_to(bone2.direction)
                intermediate_angle =  bone2.direction.angle_to(bone3.direction)
                distal_angle =  bone3.direction.angle_to(bone4.direction)

                C = 157.079
                C2 = 100
                try:
                    proximal = (C2*proximal_angle / C)*100

                except ZeroDivisionError:
                    proximal = 0

                try:
                    intermediate = (C2*intermediate_angle / C)*100

                except ZeroDivisionError:
                    intermediate = 0

                try:
                    distal = (C2*distal_angle / C)*100

                except ZeroDivisionError:
                    distal = 0

                # print str(C)+"/"+str(proximal_angle)+"="+str(proximal)
                # print str(C)+"/"+str(intermediate_angle)+"="+str(intermediate)
                # print str(C)+"/"+str(distal_angle)+"="+str(distal)
                # #proximal = np.dot(list(bone.direction), list(bone2.direction))
                #print proximal

                if self.finger_names[finger.type] == 'Polegar':
                    allFingers[0:2] = int(proximal),int(intermediate),int(distal)
                    outputLeap[0]=distal

                if self.finger_names[finger.type] == 'Indicador':
                    allFingers[3:5] = int(proximal),int(intermediate),int(distal)
                    outputLeap[1] = distal

                if self.finger_names[finger.type] == 'Meio':
                    allFingers[6:8] = int(proximal),int(intermediate),int(distal)
                    outputLeap[2] = distal

                if self.finger_names[finger.type] == 'Anular':
                    allFingers[9:11] = int(proximal),int(intermediate),int(distal)
                    outputLeap[3] = distal

                if self.finger_names[finger.type] == 'Mindinho':
                    allFingers[12:14] = int(proximal),int(intermediate),int(distal)
                    outputLeap[4] = distal

            fim = time.time()
            timeFim = fim - self.ini


            if (timeFim - self.timeBase) >=  self.n :
                self.timeBase = timeFim
                self.frameT = self.frame
                self.frame = 0

            self.frame += 1
            self.tiva.textfile.log(self.textId, allFingers)
            self.statusFinger.display_screen(modules.gameDisplay, outputLeap,self.frameT/self.n)
