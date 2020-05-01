# -*- coding: utf-8 -*-

import PyQt5

WIN_TITLE = 'Myograph - Function generator settings'

class UiFuncGenSettings:

    def __init__(self, win_funcgen_settings):
        # window to design ui
        self.win_funcgen_settings = win_funcgen_settings
        # window name
        self.win_funcgen_settings.setWindowTitle(WIN_TITLE)
        # main widget
        self.central_widget = PyQt5.QtWidgets.QWidget()
        self.win_funcgen_settings.setCentralWidget(self.central_widget)
        # layout inicialization
        self.grid_widget = PyQt5.QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.grid_widget)
        # layout construction
        self.createLabels()
        self.createTextBoxes()
        self.createButtons()
        self.posWidgets()

    def createLabels(self):
        # create frequency label
        self.label_freq = PyQt5.QtWidgets.QLabel()
        self.label_freq.setText('Frequency (Hz):')
        # create time label
        self.label_time = PyQt5.QtWidgets.QLabel()
        self.label_time.setText('Stress test time (s):')

    def createTextBoxes(self):
        # create frequency text box
        self.text_freq = PyQt5.QtWidgets.QLineEdit()
        self.text_freq.setFixedWidth(100)
        # create time text box
        self.text_time = PyQt5.QtWidgets.QLineEdit()
        self.text_time.setFixedWidth(100)

    def createButtons(self):
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
        self.grid_widget.addWidget(self.label_freq, 0, col_labels)
        self.grid_widget.addWidget(self.label_time, 1, col_labels)
        # text boxes postion
        col_textbox = 1
        self.grid_widget.addWidget(self.text_freq, 0, col_textbox)
        self.grid_widget.addWidget(self.text_time, 1, col_textbox)
        # buttons position
        row_buttons = 2
        self.grid_widget.addWidget(self.button_apply, row_buttons, 0, 2, 1)
        self.grid_widget.addWidget(self.button_cancel, row_buttons, 1, 2, 1)