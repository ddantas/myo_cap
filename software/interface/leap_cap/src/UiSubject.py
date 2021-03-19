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

# Fingers Joints options
JOINT_METACARP_FALANG = 0
JOINT_FALANG_FALANG   = 1

# Fingers parameters
NUM_FINGERS           = 5
NUM_JOINTS            = 2

# Images parameters
NUM_DISPLAYED_IMAGES  = 4
IMAGES_FORMAT         = '.png'
DEFAULT_IMAGES_SIZE   = (310, 370)
FIXED_ASPECT_RATIO    = True

class UiSubject:
    
    def __init__(self, win_size, win_name, images_path, images_names, indexes_displayed_images, chosen_hand):
        
        # Initialize PyGame
        pg.init()
        
        # Store the current hand choice. The choice it's left or right hand.
        self.chosen_hand = chosen_hand     
        # List with the number of the images that will be displayed
        self.indexes_displayed_images = indexes_displayed_images            
        # Subject window size
        self.win_size = win_size          
            
        ## Layouts size definition                
        # Default vertical spacing used between elements in the window
        vertical_spacing   = win_size[PGExt.VERTICAL]   * 0.02                
        # Default horizontal spacing used between elements in the window
        horizontal_spacing = win_size[PGExt.HORIZONTAL] * 0.01    
        # Vertical screen percentage for the Layouts in the window. Values between 0 - 1.0 -> 0 - 100% 
        self.vert_perc_images_layout          = 0.45
        self.vert_perc_time_bars_panel        = 0.07
        self.vert_perc_joint_angles_layout    = 0.38
        self.vert_perc_fingers_letters_layout = 0.1
        # Horizontal screen percentage for the Layouts in the window. Values between 0 - 1.0 -> 0 - 100% 
        self.horiz_perc_images_paenl          = 1
        self.horiz_perc_time_bars_layout      = 1
        # The width value of the joints angles layout will be setted to the image size as soon as image size be calculated.
        # The width value of the fingers letters layout will be setted to the image size as soon as image size be calculated.        
  
        # Creates a default spacer. Defines the default spacing used to separate elements in this window
        self.default_spacer = PGExt.Spacer( (vertical_spacing, horizontal_spacing) )
        # Load the images
        self.images         = self.LoadImages(images_path, images_names)  
        # Load the displayed images
        self.disp_images    = self.LoadDisplayedImages(self.indexes_displayed_images)        
        
        # Calculates the sizes of the Elements inside the Main Panel.
        self.calcSizeOfElements()
        # Calculates the positions of the Elements inside the Main Panel.
        self.calcPosOfElements()
        self.createLayouts()
        self.createMainPanel()
        
    def LoadImages(self, images_path, images_names):
        total_num_images = len(images_names)
        images           = [None] * total_num_images
        for image_num in range(total_num_images):  
            image_surface = pg.image.load(images_path + images_names[image_num] + IMAGES_FORMAT)      
            images[image_num] = PGExt.Image(PGExt.VERTICAL, DEFAULT_IMAGES_SIZE, PGExt.ORIGIN, image_surface, PGExt.GRAY, FIXED_ASPECT_RATIO)            
        return images
    
    def LoadDisplayedImages(self, indexes_displayed_images):        
        disp_images          = [None] * NUM_DISPLAYED_IMAGES
        for image_num in range(NUM_DISPLAYED_IMAGES):  
            disp_images[image_num] = self.images[ indexes_displayed_images[image_num] ]
        return disp_images
    
    # Calculates the sizes of the Elements inside the Main Panel.
    def calcSizeOfElements(self):        
        self.image_layout_size           = ( self.win_size[PGExt.HORIZONTAL], ( self.vert_perc_images_layout          * self.win_size[PGExt.VERTICAL] ) )            
        self.time_bars_panel_size        = ( self.win_size[PGExt.HORIZONTAL], ( self.vert_perc_time_bars_panel        * self.win_size[PGExt.VERTICAL] ) )                 

        # Calculates the width of the first image of the Images Layout.
        # That width will be used also as the width of Joint Angles and Fingers Letters Layouts. 
        NUM_LINES         = 1
        SPACERS_IN_BORDER = True
        images_size       = PGExt.Layout.CalSizeElements(self.image_layout_size, NUM_LINES, NUM_DISPLAYED_IMAGES, self.default_spacer, SPACERS_IN_BORDER)

        self.images_width = images_size[PGExt.HORIZONTAL]
        self.joint_angles_layout_size    = ( self.images_width              , ( self.vert_perc_joint_angles_layout    * self.win_size[PGExt.VERTICAL] ) ) 
        self.fingers_letters_layout_size = ( self.images_width              , ( self.vert_perc_fingers_letters_layout * self.win_size[PGExt.VERTICAL] ) ) 
        
    # Calculates the positions of the Elements inside the Main Panel.
    def calcPosOfElements(self):                
        # Image layout above all layouts. 
        self.image_layout_pos     = PGExt.ORIGIN 
        # Time bars layout it's below the Image layout and above the Joint Angles Layout.
        self.time_bars_panel_pos        = (0, self.image_layout_size[PGExt.VERTICAL])                  
        # Time bars layout it's below the Time Bars Panel and above the Fingers Letters Layout.
        self.joint_angles_layout_pos    = (self.default_spacer.GetSize()[PGExt.HORIZONTAL] , self.time_bars_panel_pos[PGExt.VERTICAL]     + 
                                           self.time_bars_panel_size[PGExt.VERTICAL]       + self.default_spacer.GetSize()[PGExt.VERTICAL])
        # Fingers Letters Layout it's below the Joint Angles Layout.
        self.fingers_letters_layout_pos = (0, self.joint_angles_layout_pos[PGExt.VERTICAL] + self.joint_angles_layout_size[PGExt.VERTICAL]                                         
                                                                                           + self.default_spacer.GetSize()[PGExt.VERTICAL])        
    def createImagesLayout(self, size, image_layout_pos, displayed_images, spacer):  
        NUM_COLUMNS_IN_LAYOUT  = NUM_DISPLAYED_IMAGES                
        NUM_LINES_IN_LAYOUT    = 1    
        SPACERS_IN_BORDER      = True
        images_layout = PGExt.Layout(size, image_layout_pos, NUM_LINES_IN_LAYOUT, NUM_COLUMNS_IN_LAYOUT, displayed_images, spacer, SPACERS_IN_BORDER)
        return images_layout
    
    # Do not make convert float pixels values into int values that will reduce the final size and positions precision.
    def createTimeBarsPanel(self):
        # Percentage of the remaining gesture time. Value betweeen 0.0 - 1 -> 0 - 100% 
        gesture_time_perc    = 1
        # Percentage of the remaining experiment time. Value betweeen 0.0 - 1 -> 0 - 100% 
        experiment_time_perc = 1        
        gesture_progress_bar_size    = ( self.images_width, 
                                       ( self.time_bars_panel_size[PGExt.VERTICAL]   - 1 * self.default_spacer.GetSize()[PGExt.VERTICAL] ) / 2  )       
        
        experiment_progress_bar_size = ( self.time_bars_panel_size[PGExt.HORIZONTAL] - 2 * self.default_spacer.GetSize()[PGExt.HORIZONTAL] , 
                                       ( self.time_bars_panel_size[PGExt.VERTICAL]   - 1 * self.default_spacer.GetSize()[PGExt.VERTICAL] ) / 2  )      
        # This positions are local positions inside the Time Bars Panel
        gesture_progress_bar_pos     = ( self.default_spacer.GetSize()[PGExt.HORIZONTAL], 0 )
        experiment_progress_bar_pos  = ( self.default_spacer.GetSize()[PGExt.HORIZONTAL], gesture_progress_bar_size[PGExt.VERTICAL] +  
                                                                                          self.default_spacer.GetSize()[PGExt.VERTICAL] )        
        # Progress Bars Creation
        gesture_progress_bar         = PGExt.ProgressBar(PGExt.VERTICAL, experiment_progress_bar_size, gesture_progress_bar_pos,
                                                    gesture_time_perc, PGExt.BLACK, PGExt.BLUE)
        experiment_progress_bar      = PGExt.ProgressBar(PGExt.VERTICAL, experiment_progress_bar_size, experiment_progress_bar_pos, 
                                                    experiment_time_perc, PGExt.BLACK, PGExt.BLUE)
        
        lst_time_bars      = [gesture_progress_bar, experiment_progress_bar]
        lst_sizes_bars     = [gesture_progress_bar_size, experiment_progress_bar_size]
        lst_pos_bars       = [gesture_progress_bar_pos, experiment_progress_bar_pos]
        NUM_ELEM_IN_PANEL  = 2                        
        time_bars_panel    = PGExt.Panel( self.time_bars_panel_size, self.time_bars_panel_pos, NUM_ELEM_IN_PANEL, lst_time_bars, 
                                          lst_sizes_bars, lst_pos_bars )        
        return time_bars_panel
    
    def createJointAnglesLayout(self):                           
        ## Create the Progress Bars for the Joint Angles.
        # Arbitrary size and position for the progress bars. This values will serve to instanciate the bars. 
        # But will be overwritten by the new values automatically calculated by the Joint Angles Layout. 
        arb_value = (50, 50)      
        # Initial value of the joint angles bars.
        progress_perc = 1
        # Joint angles bars creation.
        self.joints_prog_bars = [None] * NUM_FINGERS    
        for finger_number in range(NUM_FINGERS):
            self.joints_prog_bars[finger_number] = [None] * NUM_JOINTS       
            for joint_number in range(NUM_JOINTS):
                self.joints_prog_bars[finger_number][joint_number] = PGExt.ProgressBar(PGExt.HORIZONTAL, arb_value, arb_value, 
                                                                                       progress_perc, PGExt.BLACK, PGExt.BLUE)    
        SPACERS_IN_BORDER    = False
        
        # Create a list of references to the joint progress bar objects. That list will be used to add this bars into the Layout. 
        lst_joints_prog_bars = []
        for finger_number in range(NUM_FINGERS):            
            for joint_number in range(NUM_JOINTS):                
                lst_joints_prog_bars.append( self.joints_prog_bars[finger_number][joint_number] )
        joint_angles_layout  = PGExt.Layout(self.joint_angles_layout_size, self.joint_angles_layout_pos, NUM_JOINTS, NUM_FINGERS, 
                                            lst_joints_prog_bars, self.default_spacer, SPACERS_IN_BORDER)
        return joint_angles_layout
    
    def createFingersLettersLayout(self):
        pass
        
    def createLayouts(self):                
        self.images_layout = self.createImagesLayout(self.image_layout_size, self.image_layout_pos, self.disp_images, self.default_spacer)        
        self.time_bars_panel       = self.createTimeBarsPanel()        
        self.joint_angles_layout   = self.createJointAnglesLayout()
        #self.fingers_angles_layout = self.createFingersLettersLayout()
        
    def createMainPanel(self):
        # List of Layouts that will be added to Main Panel.
        self.lst_elements       = [self.images_layout, self.time_bars_panel, self.joint_angles_layout]
        # List of the sizes of each Layout that will be added to Main Panel.
        self.lst_sizes_elements = [self.image_layout_size, self.time_bars_panel_size, self.joint_angles_layout_size]
        # List of the positions for each Layout inside of the panel. 
        self.lst_pos_elements   = [self.image_layout_pos, self.time_bars_panel_pos, self.joint_angles_layout_pos]                
        # Number of Elements in the main panel
        NUM_ELEMENTS = 3
        # Create the Main Panel that holds the Layouts created.
        self.main_panel = PGExt.Panel( self.win_size, PGExt.ORIGIN, NUM_ELEMENTS, self.lst_elements, self.lst_sizes_elements, self.lst_pos_elements)        
            
    def resize(self, new_win_size):
        self.win_size = new_win_size
        self.main_panel.Resize(new_win_size)
        
    def draw(self):
        # Creates a resizeble PyGame Window for the Subject Window 
        self.win   = pg.display.set_mode(size=self.win_size, flags = pg.RESIZABLE)  
        # Get the draw parameters for each elements inside the main panel in the right order to be drawn.
        draw_param = self.main_panel.GetDrawParam(PGExt.ORIGIN)        
        self.win.fill(PGExt.WHITE) 
        PGExt.Draw(self.win, draw_param)        
        # Update the window with elements redrawed.
        pg.display.flip()
      
    def close(self):
        pg.display.quit()
            