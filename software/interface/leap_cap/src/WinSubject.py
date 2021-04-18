# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:31:41 2021

@author: Asaphe Magno
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

# Hand options
RIGHT_HAND            = 0
LEFT_HAND             = 1

# Fingers options for keyboard input only
PINKY                 = 0
RING                  = 1
MIDDLE                = 2
INDICATOR             = 3
THUMB                 = 4 

# Fingers Joints options
JOINT_PHALANG_PHALANG = 0
JOINT_METACARP_FALANG = 1
  
# Window parameters
WINDOW_TITLE          = 'Subject'
DEFAULT_WIN_SIZE      = (1024, 576)


class WinSubject:
    
    def __init__(self, routine_name, time_step, chosen_hand):     
        ## Gesture images parameters                   
        images_path                = WinSubject.getImagesDir()
        images_names               = WinSubject.getImagesNames(images_path)
        gesture_routine_path       = WinSubject.getGestureSeqPath()
        gesture_and_duration_seq   = WinSubject.getGestureSequence(gesture_routine_path, routine_name)           
        self.gesture_sequence      = gesture_and_duration_seq[GESTURE]
        self.gesture_duration_seq  = gesture_and_duration_seq[GESTURE_TIME]
        self.routine_img_dict      = {}        
        self.routine_img_surfaces  = WinSubject.loadRoutineImages(self.routine_img_dict, images_path, images_names)        
        self.current_gesture_index = 0
        images_names_to_disp       = WinSubject.createLstImgNamesToDisplay(self.gesture_sequence, self.current_gesture_index)
        lst_imgs_to_disp           = WinSubject.createLstImgsToDisplay(images_names_to_disp, self.routine_img_dict, self.routine_img_surfaces)                
        
        ## Time bars parameters      
        self.time_step             = time_step
        # Current time inside a gesture time 
        self.gesture_time          = 0
        # Current time inside a experiment time
        self.experiment_time       = 0
        self.experiment_duration   = WinSubject.calcExperimentDuration(self.gesture_duration_seq)
        
        ## Joint Angles Bars
        self.chosen_hand           = chosen_hand
        
        ## UI parameters                   
        self.ui_subject            = UiSubject.UiSubject(DEFAULT_WIN_SIZE, WINDOW_TITLE, lst_imgs_to_disp, self.chosen_hand)    
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
                    if event.type == pg.QUIT:      self.close = True;   pg.display.quit(); #sys.exit() if sys is imported
                    
                    if event.type == pg.KEYDOWN:                                      
                        # left hand
                        if event.key == pg.K_1:     self.nextTimeStep(); self.ui_subject.draw();   return 'PINKY'      #return const.PINKY                            
                        if event.key == pg.K_2:     return 'RING'        #return const.RING                            
                        if event.key == pg.K_3:     return 'MIDDLE'      #return const.MIDDLE
                        if event.key == pg.K_4:     return 'INDICATOR'   #return const.INDICATOR                                                    
                        if event.key == pg.K_SPACE: self.nextGesture();  self.ui_subject.draw();   return 'THUMB'  #return const.THUMB                              
                        # right hand
                        if event.key == pg.K_SPACE: return 'THUMB'       #return const.THUMB 
                        if event.key == pg.K_7:     return 'INDICATOR'   #return const.INDICATOR                                                        
                        if event.key == pg.K_8:     return 'MIDDLE'      #return const.MIDDLE
                        if event.key == pg.K_9:     return 'RING'        #return const.RING
                        if event.key == pg.K_0:     return 'PINKY'       #return const.PINKY        
                            
                    if(event.type == pg.VIDEORESIZE):
                        new_win_size = pg.display.get_window_size();    self.ui_subject.resize(new_win_size);   self.tests();   self.ui_subject.draw()                                

            else:  return const.NO_KEY_PRESSED
                       
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
        gesture_seq_file     = open(gesture_routine_path + gesture_seq_name, 'r')
        gestures_lines       = gesture_seq_file.readlines()        
        gesture_sequence     = []
        gesture_duration_seq = []        
        for line in gestures_lines:
            if not ( (line[0] == '#') or (line[0] == ' ') or (line[0] == '\n') ):
                temp = line.replace('\n','').split(';') 
                gesture_sequence.append( temp[0] );     gesture_duration_seq.append( int( temp[1] ) )                
        gesture_seq_file.close()        
        return gesture_sequence, gesture_duration_seq
    
    def calcExperimentDuration(gesture_duration_seq):
        experiment_duration = 0
        for gesture in range( len(gesture_duration_seq) ) :
            experiment_duration = experiment_duration + gesture_duration_seq[gesture]    
        return experiment_duration
    
    def updateGestureTimeBar(self):
        percentage = self.gesture_time / self.gesture_duration_seq[self.current_gesture_index]
        self.ui_subject.SetGestureTimeProgress(1 - percentage)
    
    def updateExperimentTimeBar(self):
        percentage = self.experiment_time / self.experiment_duration
        self.ui_subject.SetExperimentTimeProgress(1 - percentage)
        
    def nextTimeStep(self):                
        # The experiment it's over.
        if (self.current_gesture_index >= len(self.gesture_duration_seq) ): return 0            
        self.gesture_time     = self.gesture_time + self.time_step        
        if(self.gesture_time >= self.gesture_duration_seq[self.current_gesture_index]):
            # Update gesture time
            self.gesture_time = self.gesture_time - self.gesture_duration_seq[self.current_gesture_index]            
            self.updateGestureTimeBar()            
            # Update experiment time
            self.experiment_time = self.experiment_time + self.gesture_duration_seq[self.current_gesture_index]
            self.updateExperimentTimeBar()
            self.nextGesture()            
            # If that was the last gesture, than update the gesture time bar to empty.
            if (self.current_gesture_index >= len(self.gesture_duration_seq) ): self.ui_subject.SetGestureTimeProgress(0);     
        else: self.updateGestureTimeBar()        
            
    # Receives a list with ten values to display in the Joint Angles Bars. Values between 0 - 100.
    # The first five values should be related to the joint between the phalanges bones. 
    # The last five values should be related to the joint between metacarpal and phalange bones.
    # The Exact order should be: 
    # 0 - Thumb-Phalange_Phalange;  1 - Indicator-Phalange_Phalange;  2 - Middle-Phalange_Phalange;  3 - Ring-Phalange_Phalange;  4 - Pinky-Phalange_Phalange;
    # 5 - Thumb-Metacapal-Phalange; 6 - Indicator-Metacapal-Phalange; 7 - Middle-Metacapal-Phalange; 8 - Ring-Metacapal-Phalange; 9 - Pinky-Metacapal-Phalange.  
    # If the chosen hand it's the right hand, than the sequence received it's the same of the sequence displayed except by a factor of 100. 
    # Otherwise it's necessary to also change the order of the fingers in the list. That operation it's made by this module internally.
    def setJointAnglesValues(self, lst_joint_values):
        if(self.chosen_hand == RIGHT_HAND): 
            new_lst_joint_values = [None] * ( UiSubject.NUM_FINGERS * UiSubject.NUM_JOINTS )
            for value_index in range( UiSubject.NUM_FINGERS * UiSubject.NUM_JOINTS ):                 
                new_lst_joint_values[value_index] = lst_joint_values[value_index] / 100
            self.ui_subject.SetJointAnglesProgress(new_lst_joint_values)            
        else:
            # list with the joint values reordered
            new_lst_joint_values      = []
            # Order reversal for metacapal_phalange_values
            metacapal_phalange_values = lst_joint_values[:5]            
            for finger_num in range(UiSubject.NUM_FINGERS): new_lst_joint_values.append( ( metacapal_phalange_values[ (UiSubject.NUM_FINGERS - 1) - finger_num ] ) / 100 )
            # Order reversal for phalange_phalange_values            
            phalange_phalange_values  = lst_joint_values[5:]            
            for finger_num in range(UiSubject.NUM_FINGERS): new_lst_joint_values.append( ( phalange_phalange_values [ (UiSubject.NUM_FINGERS - 1) - finger_num ] ) / 100 )
            # Sends the new list with the joint values reordered to the user interface.
            self.ui_subject.SetJointAnglesProgress(new_lst_joint_values)            
            
    def tests(self):
        self.setJointAnglesValues( [10, 30, 50, 70, 90,  60, 50, 40, 30, 20] )
        #self.ui_subject.SetHand(UiSubject.LEFT_HAND)
        