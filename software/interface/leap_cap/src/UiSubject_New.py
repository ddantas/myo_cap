# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 12:31:49 2021

@author: Asaphe Magno
"""

import sys
import os
import pygame as pg
import PyGameLibExt as PGExt

# Obtain the myograph path
myograph_import_path = os.path.split( os.path.split( os.path.split(os.path.abspath(__file__))[0] )[0] )[0]
# Adds the myograph path for future inclusions 
sys.path.append(myograph_import_path)
# Generates the folder path to the images of the project
images_path = os.path.join( os.path.join( os.path.join(myograph_import_path, 'leap_cap') , 'images') , '')    

# Window parameters
WINDOW_TITLE     = 'Subject'
DEFAULT_WIN_SIZE = (800, 600)

# Hand options
LEFT_HAND  = 0
RIGHT_HAND = 1

# Fingers options
PINKY     = 0
RING      = 1
MIDDLE    = 2
INDICATOR = 3
THUMB     = 4

# Fingers joints
JOINT_METACARP_FALANG = 0
JOINT_FALANG_FALANG   = 1


# Images names for the hand gesstures. It's a dictionary for indexes.
images_names = {'1th_flex':  0, '1th_flexEC':  1, '1th_flex_curl':  2, '1th_flex_curlEC':  3, 
                '2in_flex':  4, '2in_flexEC':  5, '2in_flex_curl':  6, '2in_flex_curlEC':  7,
                '3th_flex':  8, '3th_flexEC':  9, '3th_flex_curl': 10, '3th_flex_curlEC': 11, 
                '4th_flex': 12, '4th_flexEC': 13, '4th_flex_curl': 14, '4th_flex_curlEC': 15, 
                '5th_flex': 16, '5th_flexEC': 17, '5th_flex_curl': 18, '5th_flex_curlEC': 19, 
                'hand_close': 20, 'hand_closeEC': 21, 'hand_open': 22, 'hand_openEC'    : 23} 

class UiSubject:
    
    def __init__(self, win_size, win_name, images_path, images_names, images_displayed, chosen_hand):
        
        # Percentage of the remaining gesture time. Value betweeen 0.0 - 1 -> 0 - 100% 
        self.gesture_time_perc = 1
        # Percentage of the remaining experiment time. Value betweeen 0.0 - 1 -> 0 - 100% 
        self.experiment_time_perc = 1
        # Number of used fingers 
        self.num_fingers          = 5
        # Number of used joints 
        self.num_joints           = 2
        # Store the current hand choice. The choice it's left or right hand.
        self.chosen_hand = chosen_hand     
            
        ## Elements size definition
        # Subject window size
        self.win_size = win_size                        
        # Default vertical spacing used between elements in the window
        vertical_spacing  = win_size[PGExt.VERTICAL] * 0.02                
        # Default horizontal spacing used between elements in the window
        horizontal_spacing = win_size[PGExt.HORIZONTAL] * 0.03    
        # Vertical screen percentage for the Layouts in the window. Values between 0 - 1.0 -> 0 - 100% 
        vert_perc_images_panel          = 0.4
        vert_perc_time_bars_panel       = 0.1
        vert_perc_joint_angles_panel    = 0.4
        vert_perc_fingers_letters_panel = 0.1
                        
        # Initialize PyGame
        pg.init()
        # Creates a resizeble PyGame Window for the Subject Window 
        self.subj_win = pg.display.set_mode(size=self.win_size, flags = pg.RESIZABLE)                  
        # Creates a default spacer. Defines the default spacing used to separate elements in this window
        self.default_spacer = PGExt.Spacer( (vertical_spacing, horizontal_spacing) )
        # Load the images
        self.images = self.LoadImages(images_path, images_names)                    
        # Initialise the values for the joint angles bars as zero.
        self.joints_value = [None] * self.num_fingers        
        for finger_number in range(self.num_fingers):
            self.joints_value[finger_number] = [0] * self.num_joints                            
       
        self.createImagesPanel()
        self.createTimeBarsPanel()
        self.createJointAnglesPanel()
        self.createFingersLettersPanel()
        self.createMainPanel()
        
    def LoadImages(images_path, images_names):
        total_num_images = len(images_names)
        for image_num in range(total_num_images):  
            images = pg.image.load(images_path + images_names)      
        return images
    
    def createImagesPanel():
        pass
    
    def createTimeBarsPanel():
        pass
    
    def createJointAnglesPanel():
        pass
    
    def createFingersLettersPanel():
        pass
    
    def createMainPanel():
        pass
            