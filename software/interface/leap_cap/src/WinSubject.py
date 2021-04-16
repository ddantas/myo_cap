# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:31:41 2021

@author: asaph
"""

import sys
import os
import pygame as pg
import PyGameLibExt as PGExt
import UiSubject

# obtain the myograph path
myograph_path = os.path.split( os.path.split( os.path.split(os.path.abspath(__file__))[0] )[0] )[0]        
# adds the myograph path for future inclusions 
sys.path.append(myograph_path)

import Constants as const


# Image parameters
IMAGES_FORMAT         = '.png'
GRAYSCALE_SUFFIX      = 'EC'
NUM_DISPLAYED_IMAGES  = 4

# Gestures index definitions
GESTURE               = 0
GESTURE_TIME          = 1
  
# Window parameters
WINDOW_TITLE          = 'Subject'
DEFAULT_WIN_SIZE      = (1024, 576)


class WinSubject:
    
    def __init__(self):                        
        images_path                = WinSubject.getImagesDir()
        images_names               = WinSubject.getImagesNames(images_path)
        gesture_routine_path       = WinSubject.getGestureSeqPath()
        gesture_and_time_seq       = WinSubject.getGestureSequence(gesture_routine_path, 'default.txt')           
        self.gesture_sequence      = gesture_and_time_seq[GESTURE]
        self.gesture_time_seq      = gesture_and_time_seq[GESTURE_TIME]
        self.routine_img_dict      = {}        
        self.routine_img_surfaces  = WinSubject.loadRoutineImages(self.routine_img_dict, images_path, images_names)        
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

    
    def getImagesDir():        
        images_path = os.path.join( os.path.join( os.path.join(myograph_path, 'leap_cap') , 'images') , '')    
        return images_path
    
    def getImagesNames(images_path):
        # Gets the file names of the images inside the 'images_path'
        images_file_lst = next(os.walk(images_path))[2] 
        # Removes the file extension
        for image_index in range( len(images_file_lst)):
            images_file_lst[image_index] = images_file_lst[image_index].split('.')[0]
        return images_file_lst    
    
    def getGestureSeqPath():
        gesture_routine_path = os.path.join( os.path.join( os.path.join(myograph_path, 'leap_cap') , 'routine') , '')    
        return gesture_routine_path
    
    def getGestureSequence(gesture_routine_path, gesture_seq_name):
        gesture_seq_file = open(gesture_routine_path + gesture_seq_name, 'r')
        gestures_lines   = gesture_seq_file.readlines()        
        gesture_sequence = []
        gesture_time_seq = []        
        for line in gestures_lines:
            if not ( (line[0] == '#') or (line[0] == ' ') or (line[0] == '\n') ):
                temp = line.replace('\n','').split(';') 
                gesture_sequence.append( temp[0] );     gesture_time_seq.append( temp[1] )                
        gesture_seq_file.close()        
        return gesture_sequence, gesture_time_seq

        