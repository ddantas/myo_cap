import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

import pygame 
from pygame import *


import modules


sys.path.append("../../")

#from tiva import Main

allFingers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


class LeapMotionListener(Leap.Listener):
 #   print modules.tivaGlobal
    #id = modules.tivaGlobal.textfile.init(15, "%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;", "lp")

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

        #allFingers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        #allFingers [:]
        frame = controller.frame()
        output = ""
        for hand in frame.hands:
            del allFingers[:]

            for finger  in hand.fingers:

                bone = finger.bone(3)
                zDistal = str(bone.direction)
                zDistal = zDistal.replace("(","")
                zDistal = zDistal.replace(")","")
                zDistal = zDistal.split(',')
                zPosDis = zDistal[2]
                zPosDis = float(zPosDis)

                if zPosDis >= 0:
                    zPosDis = zPosDis * 50
                    zPosDis += 50
                else:
                    zPosDis = zPosDis * -50
                    zPosDis = 50 - zPosDis
            
                bone = finger.bone(2)
                zMedial = zMedial = str(bone.direction)
                zMedial = zMedial.replace("(","")
                zMedial = zMedial.replace(")","")
                zMedial = zMedial.split(',')
                zPosMed = zMedial[2]
                zPosMed = float(zPosMed)

                if zPosMed >= 0:
                    zPosMed = zPosMed * 50
                    zPosMed += 50
                else:
                    zPosMed = zPosMed * -50
                    zPosMed = 50 - zPosMed
    
                zProximal = zProximal = str(bone.direction)
                zProximal = zProximal.replace("(","")
                zProximal = zProximal.replace(")","")
                zProximal = zProximal.split(',')
                zPosProx = zProximal[2]
                zPosProx = float(zPosProx)

                bone = finger.bone(1)
                if zPosProx >= 0:
                    zPosProx = zPosProx * 50
                    zPosProx += 50
                else:
                    zPosProx = zPosProx * -50
                    zPosProx = 50 - zPosProx                

                white = (255,255,255)
                black = (0,0,0)

                if self.finger_names[finger.type] == 'Polegar':
                    allFingers[0:2] = int(zPosDis),int(zPosMed),int(zPosProx)
                    pygame.draw.rect(modules.gameDisplay,white, [100,600,20,zPosDis])
                    pygame.display.update()

                if self.finger_names[finger.type] == 'Indicador':
                    allFingers[3:5] = int(zPosDis),int(zPosMed),int(zPosProx)
                    pygame.draw.rect(modules.gameDisplay, white, [130,600,20,zPosDis])
                    pygame.display.update()

                if self.finger_names[finger.type] == 'Meio':
                    allFingers[6:8] = int(zPosDis),int(zPosMed),int(zPosProx)
                    pygame.draw.rect(modules.gameDisplay, white, [160,600,20,zPosDis])
                    pygame.display.update()

                if self.finger_names[finger.type] == 'Anular':
                    allFingers[9:11] = int(zPosDis),int(zPosMed),int(zPosProx)
                    pygame.draw.rect(modules.gameDisplay, white, [190,600,20,zPosDis])
                    pygame.display.update()

                if self.finger_names[finger.type] == 'Mindinho':
                    allFingers[12:14] = int(zPosDis),int(zPosMed),int(zPosProx)
                    pygame.draw.rect(modules.gameDisplay, white, [220,600,20,zPosDis])
                    pygame.display.update()

                pygame.display.update()

                #tiva.textfile.log(id, allFingers)
                pygame.draw.rect(modules.gameDisplay, black, [100,600,20,100])
                pygame.draw.rect(modules.gameDisplay, black, [130,600,20,100])
                pygame.draw.rect(modules.gameDisplay, black, [160,600,20,100])
                pygame.draw.rect(modules.gameDisplay, black, [190,600,20,100])
                pygame.draw.rect(modules.gameDisplay, black, [220,600,20,100])

            print "2"+str(allFingers)
            modules.tivaGlobal.textfile.log(id, allFingers)