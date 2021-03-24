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
JOINT_FALANG_FALANG   = 0
JOINT_METACARP_FALANG = 1

# Fingers parameters
NUM_FINGERS           = 5
NUM_JOINTS            = 2

# Images parameters
NUM_DISPLAYED_IMAGES  = 4
IMAGES_FORMAT         = '.png'
DEFAULT_IMAGES_SIZE   = (310, 370)

class UiSubject:
    
    def __init__(self, win_size, win_title, images_path, displayed_images_names, chosen_hand):
               
        # Store the current hand choice. The choice it's left or right hand.
        self.chosen_hand  = chosen_hand 
        # Subject window size
        self.win_size = win_size                  
 
        # Initialize PyGame
        pg.init()
        # Creates a resizeble PyGame Window for the Subject Window 
        self.win   = pg.display.set_mode(size=win_size, flags = pg.RESIZABLE)  
        # Sets the window title
        pg.display.set_caption(win_title)
           
        ## Layouts size definition                
        # Default vertical spacing used between elements in the window
        vertical_spacing   = self.win_size[PGExt.VERTICAL]   * 0.01                
        # Default horizontal spacing used between elements in the window
        horizontal_spacing = self.win_size[PGExt.HORIZONTAL] * 0.02    
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
        self.default_spacer = PGExt.Spacer( (horizontal_spacing, vertical_spacing) )
        # Load the displayed images
        self.disp_images    = self.LoadDisplayedImages(images_path, displayed_images_names)                
        # Calculates the sizes of the visual Elements inside the Main Panel.
        self.calcSizeOfElements()
        # Calculates the positions of the visual elements inside the Main Panel.
        self.calcPosOfElements()
        self.createElements()
        self.createMainPanel()     
    
    def LoadDisplayedImages(self, images_path, displayed_images_names):        
        disp_images = [None] * NUM_DISPLAYED_IMAGES
        for image_num in range(NUM_DISPLAYED_IMAGES):  
            image_surface          = pg.image.load(images_path + displayed_images_names[image_num] + IMAGES_FORMAT)      
            disp_images[image_num] = PGExt.Image(PGExt.VERTICAL, DEFAULT_IMAGES_SIZE, PGExt.ORIGIN, image_surface, PGExt.GRAY, PGExt.FIXED_ASPECT_RATIO) 
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
        # Default vertical spacing used between elements in the window
        vertical_spacing      = self.win_size[PGExt.VERTICAL]   * 0.002    
        # Default horizontal spacing used between elements in the window
        horizontal_spacing    = self.win_size[PGExt.HORIZONTAL] * 0.016  
        # Creates a spacer for the Joint Angles Layout.
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
    
    def createLetters(self):
        lst_letters = ['T', 'I', 'M', 'R', 'P']
        letters     = [None] * NUM_FINGERS
        font = pg.font.SysFont('Arial', 60)
        for finger_number in range(NUM_FINGERS):            
            letter_size    = font.size( lst_letters[finger_number] )
            letter_surface = font.render( lst_letters[finger_number], True, PGExt.BLACK)    
            letters[finger_number] = PGExt.Image(PGExt.HORIZONTAL, letter_size, PGExt.ORIGIN, letter_surface, PGExt.GRAY, PGExt.FIXED_ASPECT_RATIO) 
        return letters
            
    def createFingersLettersLayout(self):  
        self.finger_letters = self.createLetters()
        
    def createElements(self):                
        self.images_layout = self.createImagesLayout(self.image_layout_size, self.image_layout_pos, self.disp_images, self.default_spacer)        
        self.time_bars_panel       = self.createTimeBarsPanel()        
        self.joint_angles_layout   = self.createJointAnglesLayout()
        #self.fingers_angles_layout = self.createFingersLettersLayout()
        
    def createMainPanel(self):
        # List of Elements that will be added to Main Panel.
        self.lst_elements       = [self.images_layout, self.time_bars_panel, self.joint_angles_layout]
        # List of the sizes of each Element that will be added to Main Panel.
        self.lst_sizes_elements = [self.image_layout_size, self.time_bars_panel_size, self.joint_angles_layout_size]
        # List of the positions for each Element inside of the main panel. 
        self.lst_pos_elements   = [self.image_layout_pos, self.time_bars_panel_pos, self.joint_angles_layout_pos]                
        # Number of Elements in the main panel
        NUM_ELEMENTS = 3
        # Create the Main Panel that holds the Layouts created.
        self.main_panel = PGExt.Panel( self.win_size, PGExt.ORIGIN, NUM_ELEMENTS, self.lst_elements, self.lst_sizes_elements, self.lst_pos_elements)        
    
    def SetDisplayedImages(self, orientation, images_path, displayed_images_names, frame_color, keep_aspect_ratio):    
        for image_num in range(NUM_DISPLAYED_IMAGES):              
            new_image_surface = pg.image.load(images_path + displayed_images_names[image_num] + IMAGES_FORMAT)      
            self.disp_images[image_num].SetNewImage(orientation, new_image_surface, frame_color, keep_aspect_ratio)
    
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
            