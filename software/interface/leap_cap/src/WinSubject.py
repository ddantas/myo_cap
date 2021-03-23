# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:31:41 2021

@author: asaph
"""

import sys
import os

# obtain the myograph path
myograph_import_path = os.path.split( os.path.split( os.path.split(os.path.abspath(__file__))[0] )[0] )[0]
# adds the myograph path for future inclusions 
sys.path.append(myograph_import_path)
images_path = os.path.join( os.path.join( os.path.join(myograph_import_path, 'leap_cap') , 'images') , '')    

import pygame as pg
import UiSubject
import Constants as const

# Window parameters
WINDOW_TITLE     = 'Subject'
#DEFAULT_WIN_SIZE = (800, 600)
DEFAULT_WIN_SIZE = (1024, 576)
#DEFAULT_WIN_SIZE = (1280, 720)

# Images names for the hand gesstures. It's a dictionary for indexes.
images_names = {'1th_flex':  0, '1th_flexEC':  1, '1th_flex_curl':  2, '1th_flex_curlEC':  3, 
                '2in_flex':  4, '2in_flexEC':  5, '2in_flex_curl':  6, '2in_flex_curlEC':  7,
                '3md_flex':  8, '3md_flexEC':  9, '3md_flex_curl': 10, '3md_flex_curlEC': 11, 
                '4an_flex': 12, '4an_flexEC': 13, '4an_flex_curl': 14, '4an_flex_curlEC': 15, 
                '5mn_flex': 16, '5mn_flexEC': 17, '5mn_flex_curl': 18, '5mn_flex_curlEC': 19, 
                'hand_close': 20, 'hand_closeEC': 21, 'hand_open': 22, 'hand_openEC'    : 23} 


class WinSubject:
    
    def __init__(self):        
        lst_images_names     = list(images_names.keys())
        displayed_images_num = [0, 3, 5, 7]
        self.ui_subject      = UiSubject.UiSubject(DEFAULT_WIN_SIZE, WINDOW_TITLE, images_path, lst_images_names, 
                                                       displayed_images_num, UiSubject.LEFT_HAND)    
        self.close = False
        '''
        # Initialise the values for the joint angles bars as zero.
        self.joints_value = [None] * NUM_FINGERS    
        for finger_number in range(NUM_FINGERS):
            self.joints_value[finger_number] = [0] * NUM_JOINTS               
        '''    
    def show(self):        
        self.ui_subject.draw()
        
    def close(self):
        self.ui_subject.close()

    def getKey(self):
        
        if not(self.close):
            
            # Redraw the images            
            #self.drawImages()    
            
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.display.quit(); #sys.exit() if sys is imported
                        self.close = True
                        
                    if event.type == pg.KEYDOWN:                                      
                        # left hand
                        if event.key == pg.K_1:
                            #return const.PINKY
                            return 'PINKY'
                        if event.key == pg.K_2:
                            #return const.RING
                            return 'RING'
                        if event.key == pg.K_3:
                            #return const.MIDDLE
                            return 'MIDDLE'
                        if event.key == pg.K_4:
                            #return const.INDICATOR
                            return 'INDICATOR'
                        if event.key == pg.K_SPACE:
                            #return const.THUMB
                            return 'THUMB'
                        
                        # right hand
                        if event.key == pg.K_SPACE:
                            #return const.THUMB 
                            return 'THUMB'
                        if event.key == pg.K_7:
                            #return const.INDICATOR
                            return 'INDICATOR'
                        if event.key == pg.K_8:
                            #return const.MIDDLE
                            return 'MIDDLE'
                        if event.key == pg.K_9:
                            #return const.RING
                            return 'RING'
                        if event.key == pg.K_0:
                            #return const.PINKY        
                            return 'PINKY'
                        
                    if(event.type == pg.VIDEORESIZE):
                        new_win_size = pg.display.get_window_size()
                        self.ui_subject.resize(new_win_size)
                        self.ui_subject.draw()                        
                        
            else:   
                    return const.NO_KEY_PRESSED
                           
                
        return const.CLOSE_SUBJECT_WIN                               