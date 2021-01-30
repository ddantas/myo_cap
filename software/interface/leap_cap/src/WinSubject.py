import sys
import os

# obtain the myograph path
myograph_import_path = os.path.split( os.path.split( os.path.split(os.path.abspath(__file__))[0] )[0] )[0]
# adds the myograph path for future inclusions 
sys.path.append(myograph_import_path)

import pygame as pg
import Constants as const

class WinSubject:
    
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        #self.win_size = (1368, 768)
        self.win_size = (800, 600)
        self.win = None
        self.close = False

    def show(self):
        pg.init()
        self.win = pg.display.set_mode(size=self.win_size)                
        self.win.fill(self.white)  
        pg.display.update()

    def close(self):
        pg.quit()

    def getKey(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit(); #sys.exit() if sys is imported
                    self.close = True
                    
                if event.type == pg.KEYDOWN:                                      
                    # left hand
                    if event.key == pg.K_1:
                        return const.PINKY
                    if event.key == pg.K_2:
                        return const.RING
                    if event.key == pg.K_3:
                        return const.MIDDLE
                    if event.key == pg.K_4:
                        return const.INDICATOR
                    if event.key == pg.K_SPACE:
                        return const.THUMB
                    
                    # right hand
                    if event.key == pg.K_SPACE:
                        return const.THUMB 
                    if event.key == pg.K_7:
                        return const.INDICATOR
                    if event.key == pg.K_8:
                        return const.MIDDLE
                    if event.key == pg.K_9:
                        return const.RING
                    if event.key == pg.K_0:
                        return const.PINKY        
                    
                    # Close Window
                    if event.key == pg.K_ESCAPE:
                        return const.CLOSE_SUBJECT_WIN
                    
                    else:
                        return const.NO_KEY_PRESSED
                    
                    
"""

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit(); #sys.exit() if sys is imported
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                print("Mínimo esquerdo")
            if event.key == pg.K_2:
                print("Anular esquerdo")
            if event.key == pg.K_3:
                print("Médio esquerdo")
            if event.key == pg.K_4:
                print("Indicador esquerdo")
"""
