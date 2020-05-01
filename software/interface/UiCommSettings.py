# -*- coding: utf-8 -*-

import PyQt5

WIN_TITLE = 'Myograph - Communication Settings'

class UiCommSettings:

    def __init__(self, win_comm_settings):
        # window to design ui
        self.win_comm_settings = win_comm_settings
        # window name
        self.win_comm_settings.setWindowTitle(WIN_TITLE)
        # main widget
        self.central_widget = PyQt5.QtWidgets.QWidget()
        self.win_comm_settings.setCentralWidget(self.central_widget)
        # layout inicialization
        self.grid_widget = PyQt5.QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.grid_widget)
        # layout construction
        self.createLabels()
        self.createTextBoxes()
        self.createButtons()
        self.posWidgets()

    def createLabels(self):
        # create packet size label
        self.label_pkt_size = PyQt5.QtWidgets.QLabel()
        self.label_pkt_size.setText('Packet size (bytes):')

    def createTextBoxes(self):
        # create packet size text box
        self.text_pkt_size = PyQt5.QtWidgets.QLineEdit()
        self.text_pkt_size.setFixedWidth(100)

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
        self.grid_widget.addWidget(self.label_pkt_size, 0, col_labels)
        # text boxes postion
        col_textbox = 1
        self.grid_widget.addWidget(self.text_pkt_size, 0, col_textbox)
        # buttons position
        row_buttons = 1
        self.grid_widget.addWidget(self.button_apply, row_buttons, 0, 2, 1)
        self.grid_widget.addWidget(self.button_cancel, row_buttons, 1, 2, 1)