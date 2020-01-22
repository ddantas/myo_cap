# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

WIN_TITLE = 'Myograph - Capture settings'

class UiCaptureSettings:

    def setupUi(self, win_capture_settings):
        self.win_capture_settings = win_capture_settings

        # window size
        self.win_capture_settings.setMinimumWidth(300)
        self.win_capture_settings.setMinimumHeight(180)

        # window name
        self.win_capture_settings.setWindowTitle(WIN_TITLE)

        # main widget
        self.central_widget = QtWidgets.QWidget()
        self.win_capture_settings.setCentralWidget(self.central_widget)

        # layout inicialization
        self.grid_widget = QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.grid_widget)

        # layout construction
        self.createLabels()
        self.createTextBoxes()
        self.createButtons()
        self.posWidgets()

    def createLabels(self):
        self.label_bits_sample = QtWidgets.QLabel()
        self.label_sample_rate = QtWidgets.QLabel()
        self.label_ch_board = QtWidgets.QLabel()
        self.label_num_boards = QtWidgets.QLabel()

        self.label_bits_sample.setText('Bits per sample:')
        self.label_sample_rate.setText('Sample rate (Hz):')
        self.label_ch_board.setText('Channels per board:')
        self.label_num_boards.setText('Number of boards:')

    def createTextBoxes(self):
        self.text_bits_sample = QtWidgets.QLineEdit()
        self.text_sample_rate = QtWidgets.QLineEdit()
        self.text_ch_board = QtWidgets.QLineEdit()
        self.text_num_boards = QtWidgets.QLineEdit()

        self.text_bits_sample.setFixedWidth(100)
        self.text_sample_rate.setFixedWidth(100)
        self.text_ch_board.setFixedWidth(100)
        self.text_num_boards.setFixedWidth(100)

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