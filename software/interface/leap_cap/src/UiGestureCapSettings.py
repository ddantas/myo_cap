# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 12:45:39 2021

@author: asaph
"""

import PyQt5

WIN_TITLE = 'LeapCap - Gesture capture settings'

class UiGestureCapSettings:

    def __init__(self, win_gesture_cap_settings):
        # window to design ui
        self.win_gesture_cap_settings = win_gesture_cap_settings
        # window name
        self.win_gesture_cap_settings.setWindowTitle(WIN_TITLE)
        # main widget
        self.central_widget = PyQt5.QtWidgets.QWidget()
        self.win_gesture_cap_settings.setCentralWidget(self.central_widget)
        # layout inicialization
        self.grid_widget = PyQt5.QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.grid_widget)
        # layout construction
        self.createLabels()
        self.createComboBoxes()
        self.createButtons()
        self.posWidgets()

    def createLabels(self):
        # create "Device" label
        self.label_device = PyQt5.QtWidgets.QLabel()
        self.label_device.setText('Device:')
        #self.label_device.setFixedWidth(100)
        # create "Routine" rate label
        self.label_routine = PyQt5.QtWidgets.QLabel()
        self.label_routine.setText('Routine:')
        # create "Hand side" label
        self.label_hand = PyQt5.QtWidgets.QLabel()
        self.label_hand.setText('Hand side:')


    def createComboBoxes(self):
        # create device combo box
        self.combo_device = PyQt5.QtWidgets.QComboBox()
        self.combo_device.setEditable(False)
        self.combo_device.setFixedWidth(80)
        self.combo_device.addItem('LeapMotion')
        self.combo_device.addItem('Keyboard')
        self.combo_device.addItem('None')        
        # create hand combo box
        self.combo_hand = PyQt5.QtWidgets.QComboBox()        
        self.combo_hand.setEditable(False)
        self.combo_hand.setFixedWidth(80)
        self.combo_hand.addItem('Left')
        self.combo_hand.addItem('Right')        

    def createButtons(self):
        # create select routine button
        self.button_select_routine = PyQt5.QtWidgets.QPushButton()
        self.button_select_routine.setText('Select Routine')
        self.button_select_routine.setFixedWidth(80)
        # create apply button
        self.button_apply = PyQt5.QtWidgets.QPushButton()
        self.button_apply.setText('Apply')
        self.button_apply.setFixedWidth(100)
        # create cancel button
        self.button_cancel = PyQt5.QtWidgets.QPushButton()
        self.button_cancel.setText('Cancel')
        self.button_cancel.setFixedWidth(100)

    def posWidgets(self):
        # labels position
        col_labels = 0
        self.grid_widget.addWidget(self.label_device, 0, col_labels)
        self.grid_widget.addWidget(self.label_routine, 1, col_labels)
        self.grid_widget.addWidget(self.label_hand, 2, col_labels)
        # combo boxes postion
        col_combobox = 1
        self.grid_widget.addWidget(self.combo_device, 0, col_combobox)
        self.grid_widget.addWidget(self.button_select_routine, 1, col_combobox)
        self.grid_widget.addWidget(self.combo_hand, 2, col_combobox)
        # buttons position
        row_buttons = 3
        self.grid_widget.addWidget(self.button_apply, row_buttons, 0, 2, 1)
        self.grid_widget.addWidget(self.button_cancel, row_buttons, 1, 2, 1)