# -*- coding: utf-8 -*-

import PyQt5

WIN_TITLE = 'Myograph - Display settings'

class UiDisplaySettings:

    def __init__(self, win_display_settings):
        # window to design ui
        self.win_display_settings = win_display_settings
        # window name
        self.win_display_settings.setWindowTitle(WIN_TITLE)
        # main widget
        self.central_widget = PyQt5.QtWidgets.QWidget()
        self.win_display_settings.setCentralWidget(self.central_widget)
        # layout inicialization
        self.grid_widget = PyQt5.QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.grid_widget)
        # layout construction
        self.createLabels()
        self.createTextBoxes()
        self.createButtons()
        self.posWidgets()

    def createLabels(self):
        # create swipe label
        self.label_swipe = PyQt5.QtWidgets.QLabel()
        self.label_swipe.setText('Swipe:')
        # create vmin label
        self.label_vmin = PyQt5.QtWidgets.QLabel()
        self.label_vmin.setText('Min. voltage (V):')
        # create vmax label
        self.label_vmax = PyQt5.QtWidgets.QLabel()
        self.label_vmax.setText('Max. voltage (V):')
        # create vtick label
        self.label_vtick = PyQt5.QtWidgets.QLabel()
        self.label_vtick.setText('Vertical tick (V):')
        # create htick label
        self.label_htick = PyQt5.QtWidgets.QLabel()
        self.label_htick.setText('Horizontal tick (samples):')

    def createTextBoxes(self):
        # create swipe text box
        self.text_swipe = PyQt5.QtWidgets.QLineEdit()
        self.text_swipe.setFixedWidth(100)
        # create vmin text box
        self.text_vmin = PyQt5.QtWidgets.QLineEdit()
        self.text_vmin.setFixedWidth(100)
        # create vmax text box
        self.text_vmax = PyQt5.QtWidgets.QLineEdit()
        self.text_vmax.setFixedWidth(100)
        # create vtick text box
        self.text_vtick = PyQt5.QtWidgets.QLineEdit()
        self.text_vtick.setFixedWidth(100)
        # create htick text box
        self.text_htick = PyQt5.QtWidgets.QLineEdit()
        self.text_htick.setFixedWidth(100)

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
        self.grid_widget.addWidget(self.label_swipe, 0, col_labels)
        self.grid_widget.addWidget(self.label_vmin, 1, col_labels)
        self.grid_widget.addWidget(self.label_vmax, 2, col_labels)
        self.grid_widget.addWidget(self.label_vtick, 3, col_labels)
        self.grid_widget.addWidget(self.label_htick, 4, col_labels)
        # text boxes postion
        col_textbox = 1
        self.grid_widget.addWidget(self.text_swipe, 0, col_textbox)
        self.grid_widget.addWidget(self.text_vmin, 1, col_textbox)
        self.grid_widget.addWidget(self.text_vmax, 2, col_textbox)
        self.grid_widget.addWidget(self.text_vtick, 3, col_textbox)
        self.grid_widget.addWidget(self.text_htick, 4, col_textbox)
        # buttons position
        row_buttons = 5
        self.grid_widget.addWidget(self.button_apply, row_buttons, 0, 2, 1)
        self.grid_widget.addWidget(self.button_cancel, row_buttons, 1, 2, 1)
