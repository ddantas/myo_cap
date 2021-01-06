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

import AuxFunctions as AuxFunc
import PyQt5
import UiGestureCapSettings

class WinGestureCapSettings(PyQt5.QtWidgets.QMainWindow):

    def __init__(self):
        # calling superclass constructor
        super(WinGestureCapSettings, self).__init__()
        # global objects

        # capture settings ui
        self.ui_gesture_cap_settings = UiGestureCapSettings.UiGestureCapSettings(self)
        # connect ui buttons to modules
        self.ui_gesture_cap_settings.button_select_routine.clicked.connect(self.openRoutine)
        
        self.ui_gesture_cap_settings.button_apply.clicked.connect(self.applyChanges)
        self.ui_gesture_cap_settings.button_cancel.clicked.connect(self.close)
        # load settings
        self.loadSettings()
        
        
    # load settings to text boxes
    def loadSettings(self):
        pass

    # set new values at settings object
    def applyChanges(self):        
        pass
            
        # update graph
        #self.graph.configureGraph()
        # close window
        self.close()
        
    def openRoutine(self):
        options = PyQt5.QtWidgets.QFileDialog.Options()
        options |= PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
        self.file_name, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Select capture file', '', 'CSV files (*.csv)', options=options)
        #self.openCSV(self.file_name)
        AuxFunc.showMessage('warning!', 'Function in development!')