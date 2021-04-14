# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:31:41 2021

@author: asaph
"""

import sys
import os
import PyGameLibExt as PGExt

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


IMAGES_FORMAT         = '.png'
GRAYSCALE_SUFFIX      = 'EC'
NUM_DISPLAYED_IMAGES  = 4

# Images names for the hand gesstures. It's a dictionary for indexes.
images_names  = {'1th_flex':  0, '1th_flexEC':  1, '1th_flex_curl':  2, '1th_flex_curlEC':  3, 
                 '2in_flex':  4, '2in_flexEC':  5, '2in_flex_curl':  6, '2in_flex_curlEC':  7,
                 '3md_flex':  8, '3md_flexEC':  9, '3md_flex_curl': 10, '3md_flex_curlEC': 11, 
                 '4an_flex': 12, '4an_flexEC': 13, '4an_flex_curl': 14, '4an_flex_curlEC': 15, 
                 '5mn_flex': 16, '5mn_flexEC': 17, '5mn_flex_curl': 18, '5mn_flex_curlEC': 19, 
                 'hand_close': 20, 'hand_closeEC': 21, 'hand_open': 22, 'hand_openEC'    : 23} 


class WinSubject:
    
    def __init__(self):                
        self.routine_img_dict      = {}
        # Will receive the list of gesture image names by a variable in the settings object. After the Routine loader be constructed.    
        routine_img_names          = ['1th_flex', '1th_flex_curl', '2in_flex', '2in_flex_curl', '3md_flex', '3md_flex_curl',
                                      '4an_flex', '4an_flex_curl', '5mn_flex', '5mn_flex_curl', 'hand_close', 'hand_open'  ]
        self.routine_img_surfaces  = WinSubject.loadRoutineImages(self.routine_img_dict, images_path, routine_img_names)
        # Will receive the list of gesture sequence by a variable in the settings object. After the Routine loader be constructed.    
        self.gesture_sequence      = ['1th_flex', '1th_flex_curl', '2in_flex', '2in_flex_curl', '3md_flex', '3md_flex_curl',
                                      '4an_flex', '4an_flex_curl', '5mn_flex', '5mn_flex_curl', 'hand_close', 'hand_open'  ]
        self.current_gesture_index = 0
        images_names_to_disp       = WinSubject.createLstImgNamesToDisplay(self.gesture_sequence, self.current_gesture_index)
        lst_imgs_to_disp           = WinSubject.createLstImgsToDisplay(images_names_to_disp, self.routine_img_dict, self.routine_img_surfaces)                
        self.ui_subject            = UiSubject.UiSubject(DEFAULT_WIN_SIZE, WINDOW_TITLE, lst_imgs_to_disp, UiSubject.RIGHT_HAND)    
        self.close = False
 
    def show(self):        
        self.ui_subject.draw()
        
    def close(self):
        self.ui_subject.close()
                
    def loadRoutineImages(routine_img_dict, images_path, routine_img_names):
        num_images           = len(routine_img_names)
        routine_img_surfaces = [None] * (num_images * 2 + 1)  # +1 because of the blank surface at the end of the list    
        for image_num in range(num_images):  
            # Adds the new color image into the dictionary
            routine_img_dict[ routine_img_names[image_num] ] = image_num * 2
            # Loads the current image as a Pygame Surface
            routine_img_surfaces[image_num * 2] = pg.image.load(images_path + routine_img_names[image_num] + IMAGES_FORMAT)                  
            
            # Copy the current color image
            temp_surface = routine_img_surfaces[image_num * 2].copy()
            # Converts the current color image into a grayscale image
            PGExt.rgb2GrayScale(temp_surface)
            # Stores the grayscale of the current image in the next position of the list
            routine_img_surfaces[image_num * 2 + 1] = temp_surface
            # Adds the current grayscale image into the dictionary
            routine_img_dict[ routine_img_names[image_num] + GRAYSCALE_SUFFIX ] = image_num * 2 + 1
        # Copies the last surface
        blank_surface = routine_img_surfaces[num_images - 1].copy()
        # Fills the surface with white
        blank_surface.fill(PGExt.GRAY)
        # Stores the blank surface at the end of the list    
        routine_img_surfaces[num_images * 2] = blank_surface
        # Adds the blank surface index into the dictionary
        routine_img_dict['Blank']   = num_images * 2 
        routine_img_dict['BlankEC'] = num_images * 2 
            
        return routine_img_surfaces
                
    def createLstImgsToDisplay(images_names, routine_img_dict, routine_img_surfaces):        
        imgs_to_disp          = [None] * NUM_DISPLAYED_IMAGES
        for image_num in range(NUM_DISPLAYED_IMAGES):  
            if(image_num == 0): # Colored image
                # Finds out the index of the image in the list of routine surfaces using the dictionary
                index = routine_img_dict[ images_names[image_num] ]                
            else: # Grayscale image
                # Finds out the index of the image in the list of routine surfaces using the dictionary
                index = routine_img_dict[ images_names[image_num] + GRAYSCALE_SUFFIX ]        
            # Stores the reference of the current image into the list of images to be displayed.    
            imgs_to_disp[image_num] = routine_img_surfaces[index]                 
        return imgs_to_disp    
    
    def createLstImgNamesToDisplay(gesture_sequence, current_gesture_index):
        lst_img_names = [None] * NUM_DISPLAYED_IMAGES
        for image_num in range(NUM_DISPLAYED_IMAGES):
            if( (image_num + current_gesture_index) < len(gesture_sequence) ): # Still there are images to be loaded.
                lst_img_names[image_num] = gesture_sequence[image_num + current_gesture_index]
            else: # There are no images to be loaded. Loads a blank surface in place.
                lst_img_names[image_num] = 'Blank'
        return lst_img_names
    
    def nextGesture(self):
        if(self.current_gesture_index < len(self.gesture_sequence)):
            self.current_gesture_index = self.current_gesture_index + 1
            images_names_to_disp       = WinSubject.createLstImgNamesToDisplay(self.gesture_sequence, self.current_gesture_index)
            lst_imgs_to_disp           = WinSubject.createLstImgsToDisplay(images_names_to_disp, self.routine_img_dict, self.routine_img_surfaces)        
            self.ui_subject.SetDisplayedImages(PGExt.VERTICAL, lst_imgs_to_disp, PGExt.GRAY, PGExt.ASPECT_RATIO_FIXED)                           
        else: print('End of the gesture sequence.')
        
    def getKey(self):
        
        if not(self.close):
            
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
                            self.nextGesture()       
                            self.ui_subject.draw()
                            return 'THUMB'
                        
                        # right hand
                        if event.key == pg.K_SPACE:
                            #return const.THUMB 
                            self.nextGesture()       
                            self.ui_subject.draw()      
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
                        
                        # Some Tests
                        self.ui_subject.SetGestureTimeProgress(0.95)
                        self.ui_subject.SetExperimentTimeProgress(0.5)
                        self.ui_subject.SetJointAnglesProgress( [0.2, 0.3, 0.4, 0.5, 0.6,
                                                                 0.6, 0.5, 0.4, 0.3, 0.2] )                                                
                        self.ui_subject.SetHand(UiSubject.LEFT_HAND)
                        
                        self.ui_subject.draw()      
                        
            else:   
                    return const.NO_KEY_PRESSED
                           
                
        return const.CLOSE_SUBJECT_WIN                               