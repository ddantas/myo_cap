# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 12:31:49 2021

@author: Asaphe Magno
"""

import pygame as pg
import PyGameLibExt as PGExt

# Hand options
RIGHT_HAND = 0
LEFT_HAND  = 1

# Fingers options
PINKY     = 0
RING      = 1
MIDDLE    = 2
INDICATOR = 3
THUMB     = 4

# Fingers Joints options
JOINT_FALANG_FALANG   = 0
JOINT_METACARP_FALANG = 1

# Fingers parameters
NUM_FINGERS           = 5
NUM_JOINTS            = 2

# Images parameters
NUM_DISPLAYED_IMAGES  = 4
DEFAULT_IMAGES_SIZE   = (310, 370)
IMAGES_FORMAT         = '.png'

class UiSubject:
    
    def __init__(self, win_size, win_title, lst_displayed_imgs, chosen_hand):
                       
        # Subject window size
        self.win_size           = win_size                  
        self.lst_displayed_imgs = lst_displayed_imgs
        # Store the current hand choice. The choice it's left or right hand.
        self.chosen_hand        = chosen_hand 
 
        # Initialize PyGame
        pg.init()
        # Creates a resizeble PyGame Window for the Subject Window 
        self.win   = pg.display.set_mode(size=win_size, flags = pg.RESIZABLE)  
        # Sets the window title
        pg.display.set_caption(win_title)
           
        ## Layouts size definition                
        # Default vertical spacing used between elements in the window
        self.vertical_spacing   = self.win_size[PGExt.VERTICAL]   * 0.01                
        # Default horizontal spacing used between elements in the window
        self.horizontal_spacing = self.win_size[PGExt.HORIZONTAL] * 0.02    
        # Vertical screen percentage for the Layouts in the window. Values between 0 - 1.0 -> 0 - 100% 
        self.vert_perc_images_layout          = 0.495
        self.vert_perc_time_bars_panel        = 0.065
        self.vert_perc_joint_angles_layout    = 0.38
        self.vert_perc_fingers_letters_layout = 0.041
        # One Vertical spacing between the panels are been used too.
        # Horizontal screen percentage for the Layouts in the window. Values between 0 - 1.0 -> 0 - 100% 
        self.horiz_perc_images_paenl          = 1
        self.horiz_perc_time_bars_layout      = 1
        # The width value of the joints angles layout will be setted to the image size as soon as image size be calculated.
        # The width value of the fingers letters layout will be setted to the image size as soon as image size be calculated.      
        
        # Creates a default spacer. Defines the default spacing used to separate elements in this window
        self.default_spacer = PGExt.Spacer( (self.horizontal_spacing, self.vertical_spacing) )
          
        # Calculates the sizes of the visual Elements inside the Main Panel.
        self.calcSizeOfElements()
        # Calculates the positions of the visual elements inside the Main Panel.
        self.calcPosOfElements()
        
        self.createElements()
        self.createMainPanel()     
    
    def LoadDisplayedImages(self, lst_displayed_imgs):        
        disp_images = [None] * NUM_DISPLAYED_IMAGES
        for image_num in range(NUM_DISPLAYED_IMAGES):              
            disp_images[image_num] = PGExt.Image(PGExt.VERTICAL, DEFAULT_IMAGES_SIZE, PGExt.ORIGIN, lst_displayed_imgs[image_num], PGExt.GRAY, PGExt.ASPECT_RATIO_FIXED) 
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
        self.time_bars_panel_pos        = (PGExt.ORIGIN[PGExt.HORIZONTAL], self.image_layout_size[PGExt.VERTICAL])                  
        # Time bars layout it's below the Time Bars Panel and above the Fingers Letters Layout.
        self.joint_angles_layout_pos    = (self.default_spacer.GetSize()[PGExt.HORIZONTAL] , self.time_bars_panel_pos[PGExt.VERTICAL]     + 
                                           self.time_bars_panel_size[PGExt.VERTICAL]       + self.default_spacer.GetSize()[PGExt.VERTICAL])
        # Fingers Letters Layout it's below the Joint Angles Layout.
        self.fingers_letters_layout_pos = (self.default_spacer.GetSize()[PGExt.HORIZONTAL] , self.joint_angles_layout_pos[PGExt.VERTICAL] + 
                                           self.joint_angles_layout_size[PGExt.VERTICAL]                                                  )        
        
    def createImagesLayout(self, size, image_layout_pos, displayed_images, spacer):  
        NUM_COLUMNS_IN_LAYOUT  = NUM_DISPLAYED_IMAGES                
        NUM_LINES_IN_LAYOUT    = 1    
        SPACERS_IN_BORDER      = True
        images_layout = PGExt.Layout(size, image_layout_pos, NUM_LINES_IN_LAYOUT, NUM_COLUMNS_IN_LAYOUT, displayed_images, spacer, SPACERS_IN_BORDER)
        return images_layout
    
    # Do not convert float pixels values into int values because that will reduce the final size and positions precision.
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
        self.gesture_progress_bar         = PGExt.ProgressBar(PGExt.HORIZONTAL, gesture_progress_bar_size, gesture_progress_bar_pos,
                                                    gesture_time_perc, PGExt.BLACK, PGExt.BLUE)
        self.experiment_progress_bar      = PGExt.ProgressBar(PGExt.HORIZONTAL, experiment_progress_bar_size, experiment_progress_bar_pos, 
                                                    experiment_time_perc, PGExt.BLACK, PGExt.BLUE)
        
        lst_time_bars      = [self.gesture_progress_bar, self.experiment_progress_bar]
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
        # Spacer for the Joint Angles Layout
        # Vertical spacing used between elements in this layout.
        vertical_spacing      = self.win_size[PGExt.VERTICAL]   * 0.002    
        # Horizontal spacing used between elements in this layout.
        horizontal_spacing    = self.win_size[PGExt.HORIZONTAL] * 0.022  
        # Creates a spacer for the Joint Angles and Figers Letters Layouts.
        self.joint_ang_spacer = PGExt.Spacer( (horizontal_spacing, vertical_spacing) )
        SPACERS_IN_BORDER    = True      
        # Joint angles bars creation.
        self.joints_prog_bars = [None] * NUM_JOINTS    
        for joint_number in range(NUM_JOINTS):
            self.joints_prog_bars[joint_number] = [None] * NUM_FINGERS       
            for finger_number in range(NUM_FINGERS):
                self.joints_prog_bars[joint_number][finger_number] = PGExt.ProgressBar(PGExt.VERTICAL, arb_value, arb_value, 
                                                                                       progress_perc, PGExt.BLACK, PGExt.BLUE)          
        # Create a list of references to the joint progress bar objects. That list will be used to add this bars into the Layout. 
        lst_joints_prog_bars = []
        for joint_number in range(NUM_JOINTS):
            for finger_number in range(NUM_FINGERS):                                        
                lst_joints_prog_bars.append( self.joints_prog_bars[joint_number][finger_number] )
        joint_angles_layout  = PGExt.Layout(self.joint_angles_layout_size, self.joint_angles_layout_pos, NUM_JOINTS, NUM_FINGERS, 
                                            lst_joints_prog_bars, self.joint_ang_spacer, SPACERS_IN_BORDER)
        return joint_angles_layout
    
    # Creates a list of Image objects(PyGameLibExt). Each element is one of five letters that represents each finger.
    def createLetters(self):
        # Default: Right Hand. 
        lst_letters = ['T', 'I', 'M', 'R', 'P'];   font_size = 150
        # Left Hand.
        if (self.chosen_hand):  lst_letters = ['P', 'R', 'M', 'I', 'T']
        font = pg.font.SysFont('Arial', font_size)
        
        # Gets the biggest dimensions of the letters.        
        width_max  = 0; height_max = 0
        for finger_number in range(NUM_FINGERS):            
            letter_size    = font.size( lst_letters[finger_number] )
            # Bigger width
            if( letter_size[PGExt.HORIZONTAL] > width_max  ):
                width_max = letter_size[PGExt.HORIZONTAL]
            # Bigger height
            if( letter_size[PGExt.VERTICAL]   > height_max ):
                height_max = letter_size[PGExt.VERTICAL]
        
        # Creates a background surface with the same dimensions for each letter.
        flags = 0; depth = 24 
        bg_surface = [None] * NUM_FINGERS
        for finger_number in range(NUM_FINGERS):                   
            bg_surface[finger_number] = pg.Surface((width_max, height_max), flags, depth)
            bg_surface[finger_number].fill(PGExt.WHITE)    
      
        # Creates a surface for each letter.
        ANTI_ALIASING = True;  font_color = PGExt.BLACK;  font_bg_color = PGExt.WHITE
        letter_surface = [None] * NUM_FINGERS
        for finger_number in range(NUM_FINGERS):                        
            letter_surface[finger_number] = font.render( lst_letters[finger_number], ANTI_ALIASING, font_color, font_bg_color)    

        # Fuses the background surface with the letter surface. For each letter. The letter it's in the center of the background.        
        for finger_number in range(NUM_FINGERS):   
            horizontal_offset = ( width_max  - letter_surface[finger_number].get_width()  ) / 2
            vertical_offset   = ( height_max - letter_surface[finger_number].get_height() ) / 2
            offset            = ( horizontal_offset, vertical_offset ) 
            # Fuse the surfaces into the bg_surface 
            bg_surface[finger_number].blit(letter_surface[finger_number], offset)            
            
        # Creates a list of Image objects(PyGameLibExt) for each of five letters.        
        letters_imgs = [None] * NUM_FINGERS
        letter_size  = (width_max, height_max)
        for finger_number in range(NUM_FINGERS):                        
            letters_imgs[finger_number] = PGExt.Image(PGExt.VERTICAL, letter_size, PGExt.ORIGIN, bg_surface[finger_number], 
                                                      PGExt.WHITE, PGExt.ASPECT_RATIO_FIXED)                             
        return letters_imgs    
            
    def createFingersLettersLayout(self):  
        self.finger_letters_imgs = self.createLetters()
        NUM_COLUMNS_IN_LAYOUT    = NUM_FINGERS
        NUM_LINES_IN_LAYOUT      = 1    
        SPACERS_IN_BORDER        = True
        fingers_letters_layout   = PGExt.Layout(self.fingers_letters_layout_size, self.fingers_letters_layout_pos, NUM_LINES_IN_LAYOUT, 
                                              NUM_COLUMNS_IN_LAYOUT, self.finger_letters_imgs, self.joint_ang_spacer, SPACERS_IN_BORDER)
        return fingers_letters_layout
        
    def createElements(self):                        
        self.disp_images   = self.LoadDisplayedImages(self.lst_displayed_imgs)                
        self.images_layout = self.createImagesLayout(self.image_layout_size, self.image_layout_pos, self.disp_images, self.default_spacer)        
        self.time_bars_panel       = self.createTimeBarsPanel()        
        self.joint_angles_layout   = self.createJointAnglesLayout()
        self.fingers_angles_layout = self.createFingersLettersLayout()
        
    def createMainPanel(self):
        # List of Elements that will be added to Main Panel.
        self.lst_elements       = [self.images_layout, self.time_bars_panel, self.joint_angles_layout, self.fingers_angles_layout]
        # List of the sizes of each Element that will be added to Main Panel.
        self.lst_sizes_elements = [self.image_layout_size, self.time_bars_panel_size, self.joint_angles_layout_size, self.fingers_letters_layout_size]
        # List of the positions for each Element inside of the main panel. 
        self.lst_pos_elements   = [self.image_layout_pos, self.time_bars_panel_pos, self.joint_angles_layout_pos, self.fingers_letters_layout_pos]                
        # Number of Elements in the main panel
        NUM_ELEMENTS = 4
        # Create the Main Panel that holds the Layouts created.
        self.main_panel = PGExt.Panel( self.win_size, PGExt.ORIGIN, NUM_ELEMENTS, self.lst_elements, self.lst_sizes_elements, self.lst_pos_elements)        
    
    def SetDisplayedImages(self, orientation, lst_displayed_imgs, frame_color, keep_aspect_ratio):    
        for image_num in range(NUM_DISPLAYED_IMAGES):                          
            self.disp_images[image_num].SetNewImage(orientation, lst_displayed_imgs[image_num], frame_color, keep_aspect_ratio)
    
    def SetHand(self, chosen_hand):
        if not(self.chosen_hand == chosen_hand):            
            # Get the current letters images inverting the order of ther letter images.
            new_order_letters_imgs = [None] * NUM_FINGERS
            for finger_number in range(NUM_FINGERS):   
                new_order_letters_imgs[finger_number] = self.finger_letters_imgs[ (NUM_FINGERS - 1) - finger_number ].GetOrigImage()
            # Updates the Letters Images.
            for finger_number in range(NUM_FINGERS):   
                orientation = PGExt.VERTICAL;   frame_color = PGExt.WHITE;  keep_aspect_ratio =  PGExt.ASPECT_RATIO_FIXED                
                self.finger_letters_imgs[finger_number].SetNewImage(orientation, new_order_letters_imgs[finger_number], frame_color, keep_aspect_ratio)            
            self.chosen_hand = chosen_hand
            
    def SetGestureTimeProgress(self, percentage):
        self.gesture_progress_bar.SetProgress(percentage) 
        
    def GetGestureTimeProgress(self):        
        return self.gesture_progress_bar.GetProgress() 
    
    def SetExperimentTimeProgress(self, percentage):
        self.experiment_progress_bar.SetProgress(percentage) 
        
    def GetExperimentTimeProgress(self):        
        return self.experiment_progress_bar.GetProgress() 
    
    def SetJointAnglesProgress(self, lst_percentages):
        for joint_number in range(NUM_JOINTS):
            for finger_number in range(NUM_FINGERS):      
                self.joints_prog_bars[joint_number][finger_number].SetProgress( lst_percentages[ joint_number * NUM_FINGERS + finger_number] )                   
    
    def GetJointAnglesProgress(self):        
        lst_percentages = []
        for joint_number in range(NUM_JOINTS):
            for finger_number in range(NUM_FINGERS): 
                lst_percentages.append( self.joints_prog_bars[joint_number][finger_number].GetProgress() )
        return lst_percentages
    
    def resize(self, new_win_size):
        self.win_size = new_win_size
        self.main_panel.Resize(new_win_size)
                        
    def drawVisualElements(self):        
        # Get the draw parameters for each elements inside the main panel in the right order to be drawn.
        draw_param = self.main_panel.GetDrawParam(PGExt.ORIGIN)                  
        PGExt.Draw(self.win, draw_param)                
        
    def drawContainersBorders(self):    
        # Get the border draw parameters for each Panel or Layout inside the main panel including itself.
        border_draw_param = self.main_panel.GetContainersBorders(PGExt.ORIGIN)    
        # Draw the borders of each Panel or Layout inside the main panel including itself.        
        PGExt.DrawContainersBorders(self.win, border_draw_param, PGExt.GREEN)                
                    
    def draw(self):            
        self.win.fill(PGExt.WHITE)       
        self.drawVisualElements()
        # Comment the next line to don't draw the borders of the panels and layouts.
        #self.drawContainersBorders()
        # Update the window with elements redrawed.        
        pg.display.flip()                
            
    def close(self):
        pg.display.quit()
            