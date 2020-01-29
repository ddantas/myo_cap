# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

WIN_TITLE = 'Myograph - Communication Settings'

class UiCommSettings:

    def setupUi(self, win_comm_settings):
        self.win_comm_settings = win_comm_settings

        # window size
        self.win_comm_settings.setMinimumWidth(300)
        self.win_comm_settings.setMinimumHeight(120)

        # window name
        self.win_comm_settings.setWindowTitle(WIN_TITLE)

        # main widget
        self.central_widget = QtWidgets.QWidget()
        self.win_comm_settings.setCentralWidget(self.central_widget)

        # layout inicialization
        self.grid_widget = QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.grid_widget)

        # layout construction
        self.createLabels()
        self.createTextBoxes()
        self.createButtons()
        self.posWidgets()

    def createLabels(self):
        self.label_pkt_size = QtWidgets.QLabel()
        self.label_baudrate = QtWidgets.QLabel()

        self.label_pkt_size.setText('Packet size (bytes):')
        self.label_baudrate.setText('Baudrate (bps):')

    def createTextBoxes(self):
        self.text_pkt_size = QtWidgets.QLineEdit()
        self.text_baudrate = QtWidgets.QLineEdit()

        self.text_pkt_size.setFixedWidth(100)
        self.text_baudrate.setFixedWidth(100)

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
        self.grid_widget.addWidget(self.label_pkt_size, 0, col_labels)
        self.grid_widget.addWidget(self.label_baudrate, 1, col_labels)

        # text boxes postion
        col_textbox = 1
        self.grid_widget.addWidget(self.text_pkt_size, 0, col_textbox)
        self.grid_widget.addWidget(self.text_baudrate, 1, col_textbox)

        # buttons position
        row_buttons = 4
        self.grid_widget.addWidget(self.button_apply, row_buttons, 0, 2, 1)
        self.grid_widget.addWidget(self.button_cancel, row_buttons, 1, 2, 1)