# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

WIN_TITLE = 'Myograph - Display settings'

class UiDisplaySettings:

    def __init__(self, win_display_settings):
        self.win_display_settings = win_display_settings

        # window name
        self.win_display_settings.setWindowTitle(WIN_TITLE)

        # main widget
        self.central_widget = QtWidgets.QWidget()
        self.win_display_settings.setCentralWidget(self.central_widget)

        # layout inicialization
        self.grid_widget = QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.grid_widget)

        # layout construction
        self.createLabels()
        self.createTextBoxes()
        self.createButtons()
        self.posWidgets()

    def createLabels(self):
        self.label_swipe = QtWidgets.QLabel()
        self.label_vmin = QtWidgets.QLabel()
        self.label_vmax = QtWidgets.QLabel()
        self.label_vtick = QtWidgets.QLabel()
        self.label_htick = QtWidgets.QLabel()
        self.label_show_ch = QtWidgets.QLabel()

        self.label_swipe.setText('Swipe:')
        self.label_vmin.setText('Min. voltage (V):')
        self.label_vmax.setText('Max. voltage (V):')
        self.label_vtick.setText('Vertical tick (V):')
        self.label_htick.setText('Horizontal tick (samples):')
        self.label_show_ch.setText('Number of channels:')

    def createTextBoxes(self):
        self.text_swipe = QtWidgets.QLineEdit()
        self.text_vmin = QtWidgets.QLineEdit()
        self.text_vmax = QtWidgets.QLineEdit()
        self.text_vtick = QtWidgets.QLineEdit()
        self.text_htick = QtWidgets.QLineEdit()
        self.text_show_ch = QtWidgets.QLineEdit()

        self.text_swipe.setFixedWidth(100)
        self.text_vmin.setFixedWidth(100)
        self.text_vmax.setFixedWidth(100)
        self.text_vtick.setFixedWidth(100)
        self.text_htick.setFixedWidth(100)
        self.text_show_ch.setFixedWidth(100)

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
        self.grid_widget.addWidget(self.label_swipe, 0, col_labels)
        self.grid_widget.addWidget(self.label_vmin, 1, col_labels)
        self.grid_widget.addWidget(self.label_vmax, 2, col_labels)
        self.grid_widget.addWidget(self.label_vtick, 3, col_labels)
        self.grid_widget.addWidget(self.label_htick, 4, col_labels)
        self.grid_widget.addWidget(self.label_show_ch, 5, col_labels)

        # text boxes postion
        col_textbox = 1
        self.grid_widget.addWidget(self.text_swipe, 0, col_textbox)
        self.grid_widget.addWidget(self.text_vmin, 1, col_textbox)
        self.grid_widget.addWidget(self.text_vmax, 2, col_textbox)
        self.grid_widget.addWidget(self.text_vtick, 3, col_textbox)
        self.grid_widget.addWidget(self.text_htick, 4, col_textbox)
        self.grid_widget.addWidget(self.text_show_ch, 5, col_textbox)

        # buttons position
        row_buttons = 6
        self.grid_widget.addWidget(self.button_apply, row_buttons, 0, 2, 1)
        self.grid_widget.addWidget(self.button_cancel, row_buttons, 1, 2, 1)
