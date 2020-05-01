# -*- coding: utf-8 -*-

import PyQt5

WIN_TITLE = 'Myograph - Capture settings'

class UiCaptureSettings:

    def __init__(self, win_capture_settings):
        # window to design ui
        self.win_capture_settings = win_capture_settings
        # window name
        self.win_capture_settings.setWindowTitle(WIN_TITLE)
        # main widget
        self.central_widget = PyQt5.QtWidgets.QWidget()
        self.win_capture_settings.setCentralWidget(self.central_widget)
        # layout inicialization
        self.grid_widget = PyQt5.QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.grid_widget)
        # layout construction
        self.createLabels()
        self.createTextBoxes()
        self.createButtons()
        self.posWidgets()

    def createLabels(self):
        # create bits per sample label
        self.label_bits_sample = PyQt5.QtWidgets.QLabel()
        self.label_bits_sample.setText('Bits per sample:')
        # create sample rate label
        self.label_sample_rate = PyQt5.QtWidgets.QLabel()
        self.label_sample_rate.setText('Sample rate (Hz):')
        # create channels per board label
        self.label_ch_board = PyQt5.QtWidgets.QLabel()
        self.label_ch_board.setText('Channels per board:')
        # create number of boards label
        self.label_num_boards = PyQt5.QtWidgets.QLabel()
        self.label_num_boards.setText('Number of boards:')

    def createTextBoxes(self):
        # create bits per sample text box
        self.text_bits_sample = PyQt5.QtWidgets.QLineEdit()
        self.text_bits_sample.setFixedWidth(100)
        # create sample rate text box
        self.text_sample_rate = PyQt5.QtWidgets.QLineEdit()
        self.text_sample_rate.setFixedWidth(100)
        # create channels per board text box
        self.text_ch_board = PyQt5.QtWidgets.QLineEdit()
        self.text_ch_board.setFixedWidth(100)
        # create number of boards text box
        self.text_num_boards = PyQt5.QtWidgets.QLineEdit()
        self.text_num_boards.setFixedWidth(100)

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
        self.grid_widget.addWidget(self.label_bits_sample, 0, col_labels)
        self.grid_widget.addWidget(self.label_sample_rate, 1, col_labels)
        self.grid_widget.addWidget(self.label_ch_board, 2, col_labels)
        self.grid_widget.addWidget(self.label_num_boards, 3, col_labels)
        # text boxes postion
        col_textbox = 1
        self.grid_widget.addWidget(self.text_bits_sample, 0, col_textbox)
        self.grid_widget.addWidget(self.text_sample_rate, 1, col_textbox)
        self.grid_widget.addWidget(self.text_ch_board, 2, col_textbox)
        self.grid_widget.addWidget(self.text_num_boards, 3, col_textbox)
        # buttons position
        row_buttons = 4
        self.grid_widget.addWidget(self.button_apply, row_buttons, 0, 2, 1)
        self.grid_widget.addWidget(self.button_cancel, row_buttons, 1, 2, 1)