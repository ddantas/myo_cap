# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 12:31:49 2021

@author: Asaphe Magno
"""

import pygame as pg
import PyGameLibExt as PGExt

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

IMAGES_FORMAT         = '.png'
DEFAULT_IMAGES_SIZE   = (310, 370)
FIXED_ASPECT_RATIO    = True

class UiSubject:
    
    def __init__(self, win_size, win_name, images_path, images_names, displayed_images_num, chosen_hand):
        
        # Initialize PyGame
        pg.init()
        
        # Store the current hand choice. The choice it's left or right hand.
        self.chosen_hand = chosen_hand     
        # List with the number of the images that will be displayed
        self.displayed_images_num = displayed_images_num            
        # Subject window size
        self.win_size = win_size          
            
        ## Layouts size definition                
        # Default vertical spacing used between elements in the window
        vertical_spacing  = win_size[PGExt.VERTICAL] * 0.02                
        # Default horizontal spacing used between elements in the window
        horizontal_spacing = win_size[PGExt.HORIZONTAL] * 0.03    
        # Vertical screen percentage for the Layouts in the window. Values between 0 - 1.0 -> 0 - 100% 
        self.vert_perc_images_layout          = 0.45
        self.vert_perc_time_bars_layout       = 0.1
        self.vert_perc_joint_angles_layout    = 0.35
        self.vert_perc_fingers_letters_layout = 0.1
        # Horizontal screen percentage for the Layouts in the window. Values between 0 - 1.0 -> 0 - 100% 
        self.horiz_perc_images_layout          = 1
        self.horiz_perc_time_bars_layout       = 1
        # The width value of the joints angles layout will be setted to the image size as soon as image size be calculated.
        # The width value of the fingers letters layout will be setted to the image size as soon as image size be calculated.        
  
        # Creates a default spacer. Defines the default spacing used to separate elements in this window
        self.default_spacer = PGExt.Spacer( (vertical_spacing, horizontal_spacing) )
        # Load the images
        self.images = self.LoadImages(images_path, images_names)  
        # Load the displayed images
        self.disp_images = self.LoadDisplayedImages(self.displayed_images_num)        
        
        # Calculates the sizes of the Layouts inside the Main Panel.
        self.calcSizeOfLayouts()
        # Calculates the positions of the Layouts inside the Main Panel.
        self.calcPosOfLayouts()
        self.createLayouts()
        self.createMainPanel()
        
    def LoadImages(self, images_path, images_names):
        total_num_images = len(images_names)
        images           = [None] * total_num_images
        for image_num in range(total_num_images):  
            image_surface = pg.image.load(images_path + images_names[image_num] + IMAGES_FORMAT)      
            images[image_num] = PGExt.Image(PGExt.VERTICAL, DEFAULT_IMAGES_SIZE, PGExt.ORIGIN, image_surface, PGExt.GREEN, FIXED_ASPECT_RATIO)            
        return images
    
    def LoadDisplayedImages(self, displayed_images_num):
        num_displayed_images = len(displayed_images_num)
        disp_images          = [None] * num_displayed_images
        for image_num in range(num_displayed_images):  
            disp_images[image_num] = self.images[ displayed_images_num[image_num] ]
        return disp_images
    
    def calcSizeOfLayouts(self):
        self.image_layout_size = ( self.win_size[PGExt.HORIZONTAL], ( self.vert_perc_images_layout * self.win_size[PGExt.VERTICAL] ) )     
    
    # Position of the Layouts inside the Main Panel.
    def calcPosOfLayouts(self):                
        # Image layout above all layouts.
        self.image_layout_pos     = (0, 0)  
        # Time bars layout below the Image layout an above the joint angles layout.
        self.time_bars_layout_pos = (0, 0)          
        
    def createImagesLayout(self, size, image_layout_pos, displayed_images, spacer):  
        NUM_IMAGES_IN_LAYOUT  = 4                
        NUM_LINES_IN_LAYOUT = 1    
        SPACERS_IN_BORDER   = True
        images_layout = PGExt.Layout(size, image_layout_pos, NUM_LINES_IN_LAYOUT, NUM_IMAGES_IN_LAYOUT, displayed_images, spacer, SPACERS_IN_BORDER)
        return images_layout
    
    def createTimeBarsLayout(self):
        # Percentage of the remaining gesture time. Value betweeen 0.0 - 1 -> 0 - 100% 
        self.gesture_time_perc    = 1
        # Percentage of the remaining experiment time. Value betweeen 0.0 - 1 -> 0 - 100% 
        self.experiment_time_perc = 1
    
    def createJointAnglesLayout(self):
        # Number of used fingers 
        self.num_fingers          = 5
        # Number of used joints 
        self.num_joints           = 2
        # Initialise the values for the joint angles bars as zero.
        self.joints_value = [None] * self.num_fingers        
        for finger_number in range(self.num_fingers):
            self.joints_value[finger_number] = [0] * self.num_joints   
    
    def createFingersLettersLayout(self):
        pass
        
    def createLayouts(self):                
        self.images_layout = self.createImagesLayout(self.image_layout_size, self.image_layout_pos, self.disp_images, self.default_spacer)
        # Get the width of the first image of the Images Layout.
        # That width will be used also as the width of Joint Angles and Fingers Letters Layouts. 
        self.images_width = self.images[0].GetImageSize()[PGExt.HORIZONTAL]           
        self.createTimeBarsLayout()        
        self.createJointAnglesLayout()
        self.createFingersLettersLayout()
        
    def createMainPanel(self):
        # List of Layouts that will be added to Main Panel.
        self.lst_layouts = [self.images_layout]
        # List of the sizes of each Layout that will be added to Main Panel.
        self.lst_sizes_layouts = [self.image_layout_size]
        # List of the positions for each Layout inside of the panel. 
        self.lst_pos_layouts = [self.image_layout_pos]                
        # Number of Layouts in the main panel
        NUM_LAYOUTS = 1
        # Create the Main Panel that holds the Layouts created.
        self.main_panel = PGExt.Panel( self.win_size, PGExt.ORIGIN, NUM_LAYOUTS, self.lst_layouts, self.lst_sizes_layouts, self.lst_pos_layouts)        
            
    def resize(self, new_win_size):
        self.win_size = new_win_size
        self.main_panel.Resize(new_win_size)
        
    def draw(self):
        # Creates a resizeble PyGame Window for the Subject Window 
        self.win = pg.display.set_mode(size=self.win_size, flags = pg.RESIZABLE)  
        # Get the draw parameters for each elements inside the main panel in the right order to be drawn.
        draw_param = self.main_panel.GetDrawParam(PGExt.ORIGIN)        
        self.win.fill(PGExt.WHITE) 
        PGExt.Draw(self.win, draw_param)        
        # Update the window with elements redrawed.
        pg.display.flip()
      
    def close(self):
        pg.display.quit()
            