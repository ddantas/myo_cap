# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 12:43:45 2021

@author: asaph
"""

import os
import sys
# obtain the myograph path
myograph_import_path = os.path.split( os.path.split( os.path.split(os.path.abspath(__file__))[0] )[0] )[0]
# adds the myograph path for future inclusions 
sys.path.append(myograph_import_path)

import PyQt5
import UiGestureCapSettings


# Device type index
LEAP_MOTION = 0
kEYBOARD    = 1
NONE        = 2

# Hand side index
LEFT_HAND   = 0
RIGHT_HAND  = 1

class WinGestureCapSettings(PyQt5.QtWidgets.QMainWindow):

    def __init__(self, settings):
        # calling superclass constructor
        super(WinGestureCapSettings, self).__init__()
        # global objects
        self.settings  = settings
        self.file_name = ''
        # capture settings ui
        self.ui_gesture_cap_settings = UiGestureCapSettings.UiGestureCapSettings(self)
        # connect ui buttons to methods
        self.ui_gesture_cap_settings.button_select_routine.clicked.connect(self.openRoutine)
        self.ui_gesture_cap_settings.button_apply.clicked.connect(self.applyChanges)
        self.ui_gesture_cap_settings.button_cancel.clicked.connect(self.close)
        # load settings
        self.loadSettings()
        
        
    # load settings to text boxes
    def loadSettings(self):        
        # Loads the device type from the settings object
        device_type = self.settings.getDeviceType() 
        if   (device_type == 'LeapMotion'): self.ui_gesture_cap_settings.combo_device.setCurrentIndex(LEAP_MOTION)
        elif (device_type == 'Keyboard'):   self.ui_gesture_cap_settings.combo_device.setCurrentIndex(kEYBOARD)
        elif (device_type == 'None'):       self.ui_gesture_cap_settings.combo_device.setCurrentIndex(NONE)        
        
        # Loads the hand side from the settings object
        hand_side = self.settings.getHand()
        if (hand_side == 'Left'):  self.ui_gesture_cap_settings.combo_hand.setCurrentIndex(LEFT_HAND )
        if (hand_side == 'Right'): self.ui_gesture_cap_settings.combo_hand.setCurrentIndex(RIGHT_HAND)        
        

    # set new values at settings object
    def applyChanges(self):        
        # Gets the new device type
        device_type = self.ui_gesture_cap_settings.combo_device.currentIndex()        
        # Saves the new device type in the settings object        
        if  (device_type == LEAP_MOTION): self.settings.setDeviceType('LeapMotion')
        elif(device_type == kEYBOARD):    self.settings.setDeviceType('Keyboard') 
        elif(device_type == NONE):        self.settings.setDeviceType('None') 
        
        # Saves the new routine file in the settings object
        if(len(self.file_name)): self.settings.setCaptureRoutine(self.file_name)
        
        # Gets the new hand side
        hand_side = self.ui_gesture_cap_settings.combo_hand.currentIndex()        
        # Saves the new hand side in the settings object        
        if(hand_side == LEFT_HAND):    self.settings.setHand('Left')   # Left hand side
        elif(hand_side == RIGHT_HAND): self.settings.setHand('Right')  # Right hand side        
        
        # close window
        self.close()
        
    def openRoutine(self):
        FILE_NAME_INDEX = 1
        options = PyQt5.QtWidgets.QFileDialog.Options()
        options |= PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
        self.file_name, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Select capture file', '', 'CSV files (*.csv)', options=options)        
        self.file_name    = os.path.split(self.file_name)[FILE_NAME_INDEX]