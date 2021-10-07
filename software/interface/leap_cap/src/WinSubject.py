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
import PyQt5

## Makes the Myograph directory visible to inclusions of classes and modules shared between the Myograph and Leapcap.
# Obtain the myograph path
myograph_path = os.path.split( os.path.split( os.path.split(os.path.abspath(__file__))[0] )[0] )[0]        
# Adds the myograph path for future inclusions 
sys.path.append(myograph_path)

import Constants as const

# Image parameters
IMAGES_FORMAT         = '.png'
GRAYSCALE_SUFFIX      = 'EC'
NUM_DISPLAYED_IMAGES  = 4

# Gestures index definitions
GESTURE               = 0
GESTURE_DURATION      = 1

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


## WinSubject Class ############################################################################################################################
## This class is responsible to manage the window subject behavior, it instantiates the user interface of the window and load the gestures images.
## Besides to provide automations used in the signals capture process. And to capture keys pressed in this window. 
## One extra feature of this class it's to load gesture sequences in a routine file. That file contains the gestures sequence and duration for 
## each gesture that will be showed in this window.
class WinSubject:
    
    # Method: Constructor for the WinSubject class.
    #
    # Input : routine_name      -> Routine name that will be used to inform the gestures sequence. That name should came from the settings file.
    #         time_step         -> Amount of milliseconds counted each time that "nextTimeStep()" method its called.
    #         chosen_hand       -> Chosen hand for the capture. That choice should came from the settings file.
    #
    # Output: Object of the type WinSubject constructed.
    def __init__(self, routine_name, time_step, chosen_hand):     
        ## Gesture images parameters                   
        # Path to the gesture images folder. This path includes the myograph path.
        images_path                = WinSubject.getImagesDir()
        # List with all the images names located in the images_path.
        images_names               = WinSubject.getImagesNames(images_path)
        # Path to the gesture routines folder. This path includes the myograph path.
        gesture_routine_path       = WinSubject.getGestureSeqPath()
        # Tuple of gestures sequences and gestures duration sequence
        gesture_and_duration_seq   = WinSubject.getGestureSequence(gesture_routine_path, routine_name)                   
        self.gesture_sequence      = gesture_and_duration_seq[GESTURE]
        self.gesture_duration_seq  = gesture_and_duration_seq[GESTURE_DURATION]
        # Dictionary to map image names to loaded image indexes.  
        self.imgs_dictionary       = {}        
        # Stores surfaces of all color images in the images_path and grayscale versions of this images. Surface it's a common Pygame class.
        self.imgs_surfaces  = WinSubject.loadImages(self.imgs_dictionary, images_path, images_names)        
        # Index to the current more left gesture displayed. The gesture to be executed by the subject.
        self.current_gesture_index = 0
        # List with the names to the four gesture images to be displayed. 
        images_names_to_disp       = WinSubject.createLstImgNamesToDisplay(self.gesture_sequence, self.current_gesture_index)
        # List with references to the four current displayed gesture images. 
        lst_imgs_to_disp           = WinSubject.createLstImgsToDisplay(images_names_to_disp, self.imgs_dictionary, self.imgs_surfaces)                
        
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
        # User Interface for this Window.
        self.ui_subject            = UiSubject.UiSubject(DEFAULT_WIN_SIZE, WINDOW_TITLE, lst_imgs_to_disp, self.chosen_hand)    
        # Flag to avoid code execution after this window being closed. 
        self.close = False
 
        ## Timer
        self.timer = PyQt5.QtCore.QTimer()
        self.timer.timeout.connect(self.nextTimeStep)        
 
    
    # Method: Starts the Winsubject timer.
    #
    # Input : None
    #
    # Output: None
    def startTimer(self):        
        self.timer.start(self.time_step)
    
    # Method: Stops the WinSubject timer.
    #
    # Input : None
    #
    # Output: None
    def stopTimer(self):        
        self.timer.stop()        
        
    # Method: Draws and show the User Interface of this Window.
    #
    # Input : None
    #
    # Output: None
    def show(self):        
        self.ui_subject.draw()

    # Method: Closes the User Interface of this Window.        
    #
    # Input : None
    #
    # Output: None
    def close(self):
        self.ui_subject.close()
        
    # Method: Loads the color images located in images_path and creates grayscale versions of this images also as surfaces. Surface it's a common Pygame class.
    #         In the process of images loading, it constructs a dictionary that maps image names to loaded image indexes. 
    #         This dictionary will be used to locate images inside the variable "imgs_surfaces" when surfaces of gestures need to be displayed in the window.
    #         Note: The grayscale surfaces have the same name of the original color image but with a "EC" sulfix. Example: "hand_open" -> "hand_openEC".    
    #
    # Input : imgs_dictionary -> Dictionary to map image names to loaded image indexes.
    #         images_path     -> Path to the gesture images folder. This path includes the myograph path.
    #         images_names    -> List with the names of the images inside the images routine path. 
    #
    # Output: imgs_surfaces   -> Surfaces of all images in the images_path and grayscale versions of this images. Besides a blank Surface for situations
    #                            when there are no more gesture images to fill all four images spaces reserved to gestures. 
    def loadImages(imgs_dictionary, images_path, images_names):
        num_images           = len(images_names)
        imgs_surfaces = [None] * (num_images * 2 + 1)  # +1 because of the blank surface at the end of the list    
        for image_num in range(num_images):  
            # Adds the new color image into the dictionary
            imgs_dictionary[ images_names[image_num] ] = image_num * 2
            # Loads the current image as a Pygame Surface
            imgs_surfaces[image_num * 2] = pg.image.load(images_path + images_names[image_num] + IMAGES_FORMAT)                  
            
            # Copy the current color image
            temp_surface = imgs_surfaces[image_num * 2].copy()
            # Converts the current color image into a grayscale image
            PGExt.rgb2GrayScale(temp_surface)
            # Stores the grayscale of the current image in the next position of the list
            imgs_surfaces[image_num * 2 + 1] = temp_surface
            # Adds the current grayscale image into the dictionary
            imgs_dictionary[ images_names[image_num] + GRAYSCALE_SUFFIX ] = image_num * 2 + 1
        # Copies the last surface
        blank_surface = imgs_surfaces[num_images - 1].copy()
        # Fills the surface with gray
        blank_surface.fill(PGExt.GRAY)
        # Stores the blank surface at the end of the list    
        imgs_surfaces[num_images * 2] = blank_surface
        # Adds the blank surface index into the dictionary
        imgs_dictionary['Blank']   = num_images * 2 
        imgs_dictionary['BlankEC'] = num_images * 2 
            
        return imgs_surfaces    

    # Method: This method creates a list with references to the four surfaces of the gestures that will be displayed in the window.
    #         For the three rightmost images the surfaces referenced are grayscale versions. 
    #         A blank Surface it's referenced when there are no more gesture images to fill all four images spaces reserved to    
    #         gestures.                         
    #
    # Input : gesture_sequence      -> List with the gesture sequence loaded with the routine file.
    #         current_gesture_index -> Index to the current more left gesture displayed. The gesture to be executed by the subject.   
    #
    # Output: lst_img_names         -> List with names to the four gesture images that will be displayed in the Subject window. 
    def createLstImgNamesToDisplay(gesture_sequence, current_gesture_index):
        lst_img_names = [None] * NUM_DISPLAYED_IMAGES
        for image_num in range(NUM_DISPLAYED_IMAGES):
            if( (image_num + current_gesture_index) < len(gesture_sequence) ): # Still there are images to be loaded.
                lst_img_names[image_num] = gesture_sequence[image_num + current_gesture_index]
            else: # There are no images to be loaded. Loads a blank surface in place.
                lst_img_names[image_num] = 'Blank'
        return lst_img_names
                
    # Method: This method creates a list with the names to the four surfaces of the gestures that will be displayed in the window.
    #         For the three left most images the surfaces names end with th "EC" sulfix. And so referece to grayscale surfaces.
    #         A blank Surface it's used when there are no more gesture images to fill all four images spaces reserved to gestures.                            
    #
    # Input : images_names          -> List with all the images names located in the images_path.
    #         imgs_dictionary       -> Dictionary to map image names to loaded image indexes.
    #         imgs_surfaces         -> Surfaces of all color images in the images_path and grayscale versions of this images. 
    #                                  Besides a blank Surface for situations when there are no more gesture images to fill all 
    #                                  four images spaces reserved to gestures. 
    #
    # Output: imgs_to_disp          -> List with references to the four gesture images that will be displayed in the Subject window. 
    def createLstImgsToDisplay(images_names, imgs_dictionary, imgs_surfaces):        
        imgs_to_disp          = [None] * NUM_DISPLAYED_IMAGES
        for image_num in range(NUM_DISPLAYED_IMAGES):  
            if(image_num == 0): # Colored image
                # Finds out the index of the image in the list of routine surfaces using the dictionary
                index = imgs_dictionary[ images_names[image_num] ]                
            else: # Grayscale image
                # Finds out the index of the image in the list of routine surfaces using the dictionary
                index = imgs_dictionary[ images_names[image_num] + GRAYSCALE_SUFFIX ]        
            # Stores the reference of the current image into the list of images to be displayed.    
            imgs_to_disp[image_num] = imgs_surfaces[index]                 
        return imgs_to_disp            
    
    # Method: Automation used in the signals capture process. It updates the gesture index and figures out the next four gesture surfaces 
    #         that will be displayed in the Subject window. Displays the new gestures surfaces. And checks if the gesture sequence it's over.
    #
    # Input : None
    #
    # Output: None
    def nextGesture(self):
        if(self.current_gesture_index < len(self.gesture_sequence)):
            self.current_gesture_index = self.current_gesture_index + 1
            images_names_to_disp       = WinSubject.createLstImgNamesToDisplay(self.gesture_sequence, self.current_gesture_index)
            lst_imgs_to_disp           = WinSubject.createLstImgsToDisplay(images_names_to_disp, self.imgs_dictionary, self.imgs_surfaces)        
            self.ui_subject.SetDisplayedImages(PGExt.VERTICAL, lst_imgs_to_disp, PGExt.GRAY, PGExt.ASPECT_RATIO_FIXED)                           
        else: print('End of the gesture sequence.')
        
    # That method probably will be placed in a different file.    
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
        
    # Method: Obtains the full path to the images gesture folder. That path includes the myograph path.
    #
    # Input : None
    #
    # Output: images_path       ->  String with the path to the gesture images folder.
    def getImagesDir():        
        images_path = os.path.join( os.path.join( os.path.join(myograph_path, 'leap_cap') , 'images') , '')    
        return images_path


    # Method: Obtains the full path to the images gesture folder. That path includes the myograph path.
    #
    # Input : images_path           ->  String with the path to the gesture images folder.
    #
    # Output: images_file_lst       ->  List of Strings. List with the images names inside the images gesture folder.
    #                               The names do not contain the file extension ".PNG".
    def getImagesNames(images_path):
        # Gets the file names of the images inside the 'images_path'
        images_file_lst = next(os.walk(images_path))[2] 
        # Removes the file extension
        for image_index in range( len(images_file_lst)):
            images_file_lst[image_index] = images_file_lst[image_index].split('.')[0]
        return images_file_lst    
    
    # Method: Obtains the full path to the gestures sequences folder. That path includes the myograph path.
    #
    # Input : None
    #
    # Output: gesture_routine_path  ->  String with the path to the gesture images folder.
    def getGestureSeqPath():
        gesture_routine_path = os.path.join( os.path.join( os.path.join(myograph_path, 'leap_cap') , 'routine') , '')    
        return gesture_routine_path
    
    # Method: Generates a list of the gestures sequence and other list with gestures sequence duration contained 
    #         in a gestures sequence file. The name of the gestures sequence file needs to be passed to this method,
    #         as well as the path to the gestures routines folder.          
    #
    # Input : None
    #
    # Output: gesture_sequence      -> List with the gestures sequence. The elements in this list are strigs.
    #         gesture_duration_seq  -> List with the gestures sequence duration. The elements in this list are strigs.
    def getGestureSequence(gesture_routine_path, gesture_seq_name):
        gesture_seq_file     = open(gesture_routine_path + gesture_seq_name, 'r')
        gestures_lines       = gesture_seq_file.readlines()        
        gesture_sequence     = []
        gesture_duration_seq = []        
        gesture_seq_file.close()        
        for line in gestures_lines:
            if not ( (line[0] == '#') or (line[0] == ' ') or (line[0] == '\n') ):
                temp = line.replace('\n','').split(';') 
                gesture_sequence.append( temp[0] );     gesture_duration_seq.append( int( temp[1] ) )                        
        return gesture_sequence, gesture_duration_seq
    
    # Method: Calculates the experiment duration by summing the individual durations of the gestures of the current gesture sequence.
    #
    # Input : gesture_duration_seq  ->  List with one sequence of gestures durations in miliseconds.
    #
    # Output: experiment_duration   ->  Experiment duration in miliseconds.
    def calcExperimentDuration(gesture_duration_seq):
        experiment_duration = 0
        for gesture in range( len(gesture_duration_seq) ) :
            experiment_duration = experiment_duration + gesture_duration_seq[gesture]    
        return experiment_duration
    
    # Method: Updates the gesture time bar progress with the value of the remaining time of the current gesture being executed.  
    #
    # Input : None.
    #
    # Output: None.
    def updateGestureTimeBar(self):
        percentage = self.gesture_time / self.gesture_duration_seq[self.current_gesture_index]
        self.ui_subject.SetGestureTimeProgress(1 - percentage)
    
    # Method: Updates the experiment time bar progress with the value of the remaining time of the current experiment.  
    #
    # Input : None.
    #
    # Output: None.
    def updateExperimentTimeBar(self):
        percentage = self.experiment_time / self.experiment_duration
        self.ui_subject.SetExperimentTimeProgress(1 - percentage)
        
    # Method: Method that automates the steps that need to be taken in each time step inside a experiment period.
    #         That steps include: To verify if the experiment it's over;
    #                             To update the current time inside a experiment(capture).  
    #                             To update the the progress of the time bars.    
    #                             To trigger the update of the gesture images.
    #
    # Input : None.
    #
    # Output: None.
    def nextTimeStep(self):                
        # The experiment it's over.
        if (self.current_gesture_index >= len(self.gesture_duration_seq) ): return 0            
        
        # The experiment continues.
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
        # Updates the UI  
        self.ui_subject.draw();
         
    # Method: Receives a list with ten values of joint opening and send than to UI to display in the Joint Angles Bars. Values between 0 - 100.
    #         This method standardizes the order of reception of the joints and finger values in this method and standardizes the order of 
    #         transmission of the joints and finger values related to the current hand chosen to the UI method that updates the visual feedback. 
    #         The first five values should be related to the joint between the phalanges bones. 
    #         The last five values should be related to the joint between metacarpal and phalange bones.
    #         The Exact order should be: 
    #         0 - Thumb-Phalange_Phalange;  1 - Indicator-Phalange_Phalange;  2 - Middle-Phalange_Phalange;  3 - Ring-Phalange_Phalange;  4 - Pinky-Phalange_Phalange;
    #         5 - Thumb-Metacapal-Phalange; 6 - Indicator-Metacapal-Phalange; 7 - Middle-Metacapal-Phalange; 8 - Ring-Metacapal-Phalange; 9 - Pinky-Metacapal-Phalange.  
    #         If the chosen hand it's the right hand, than the sequence received it's the same of the sequence displayed except by a factor of 100. 
    #         Otherwise it's necessary to also change the order of the fingers in the list. That operation it's made by this module internally.
    #
    # Input : lst_joint_values      -> List with ten joit angles openning to be displayed. The values need to be in the right order. That order it's
    #                                  defined in the method documentation.
    #
    # Output: None.
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
            
    # That method will be removed when the capture code be completed.
    def tests(self):
        self.setJointAnglesValues( [10, 30, 50, 70, 90,  60, 50, 40, 30, 20] )
        #self.ui_subject.SetHand(UiSubject.LEFT_HAND)
        