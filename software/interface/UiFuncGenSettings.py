# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

WIN_TITLE = 'Myograph - Function generator settings'

class UiFuncGenSettings:

    def setupUi(self, win_capture_settings):
        self.win_funcgen_settings = win_capture_settings

        # window size
        self.win_funcgen_settings.setMinimumWidth(300)
        self.win_funcgen_settings.setMinimumHeight(120)

        # window name
        self.win_funcgen_settings.setWindowTitle(WIN_TITLE)

        # main widget
        self.central_widget = QtWidgets.QWidget()
        self.win_funcgen_settings.setCentralWidget(self.central_widget)

        # layout inicialization
        self.grid_widget = QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.grid_widget)

        # layout construction
        self.createLabels()
        self.createTextBoxes()
        self.createButtons()
        self.posWidgets()

    def createLabels(self):
        self.label_freq = QtWidgets.QLabel()
        self.label_time = QtWidgets.QLabel()

        self.label_freq.setText('Frequency (Hz):')
        self.label_time.setText('Stress test time (s):')

    def createTextBoxes(self):
        self.text_freq = QtWidgets.QLineEdit()
        self.text_time = QtWidgets.QLineEdit()

        self.text_freq.setFixedWidth(100)
        self.text_time.setFixedWidth(100)

    def createButtons(self):
        self.button_apply = QtWidgets.QPushButton()
        self.button_cancel = QtWidgets.QPushButton()

        self.button_apply.setText('Apply')
        self.button_cancel.setText('Cancel')

        self.button_apply.setFixedWidth(100)
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
        row_buttons = 4
        self.grid_widget.addWidget(self.button_apply, row_buttons, 0, 2, 1)
        self.grid_widget.addWidget(self.button_cancel, row_buttons, 1, 2, 1)