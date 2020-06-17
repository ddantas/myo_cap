# -*- coding: utf-8 -*-

import PyQt5

WIN_TITLE = 'Myograph - Stress test'

class UiStresstest:

    def __init__(self, win_stress_test):
        # window to design ui
        self.win_stress_test = win_stress_test
        # window name
        self.win_stress_test.setWindowTitle(WIN_TITLE)
        # how make this window modal?
        #self.win_stress_test.setWindowModality(Qt.WindowModal)
        # main widget
        self.central_widget = PyQt5.QtWidgets.QWidget()
        self.win_stress_test.setCentralWidget(self.central_widget)
        # layout inicialization
        self.grid_widget = PyQt5.QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.grid_widget)
        # layout construction
        self.createLabels()
        self.createTextBoxes()
        self.createButtons()
        self.createProgressBar()
        self.posWidgets()

    def createLabels(self):        
        self.label_time = PyQt5.QtWidgets.QLabel()
        self.label_time.setText('Test length (s):')
        self.label_freq = PyQt5.QtWidgets.QLabel()
        self.label_freq.setText('Capture frequency (Hz):')
        self.label_ex_samp = PyQt5.QtWidgets.QLabel()
        self.label_ex_samp.setText('Expected samples:')
        self.label_re_samp = PyQt5.QtWidgets.QLabel()
        self.label_re_samp.setText('Received samples:')
        self.label_dr_samp = PyQt5.QtWidgets.QLabel()
        self.label_dr_samp.setText('Dropped samples:')
        self.label_drop = PyQt5.QtWidgets.QLabel()
        self.label_drop.setText('Drop rate (%):')
        
    def createTextBoxes(self):        
        # create time text box
        self.text_time = PyQt5.QtWidgets.QLabel()
        self.text_time.setFixedWidth(100)
        # create frequency text box
        self.text_freq = PyQt5.QtWidgets.QLabel()
        self.text_freq.setFixedWidth(100)
        # create expected samples text box
        self.text_ex_samp = PyQt5.QtWidgets.QLabel()
        self.text_ex_samp.setFixedWidth(100)
        # create received samples text box
        self.text_re_samp = PyQt5.QtWidgets.QLabel()
        self.text_re_samp.setFixedWidth(100)
        # create dropped samples text box
        self.text_dr_samp = PyQt5.QtWidgets.QLabel()
        self.text_dr_samp.setFixedWidth(100)
        # create drop rate text box
        self.text_drop = PyQt5.QtWidgets.QLabel()
        self.text_drop.setFixedWidth(100)

    def createButtons(self):
        # create apply button
        self.button_stop = PyQt5.QtWidgets.QPushButton()
        self.button_stop.setText('Stop')
        self.button_stop.setFixedWidth(100)
        # create cancel button
        self.button_cancel = PyQt5.QtWidgets.QPushButton()
        self.button_cancel.setText('Cancel')
        self.button_cancel.setFixedWidth(100)

    def createProgressBar(self):
        self.progressBar = PyQt5.QtWidgets.QProgressBar()
##        self.progressBar.setTextVisible(False)
##        self.progressBar.setGeometry(30, 40, 200, 25)
        
    def posWidgets(self):
        #progressbar position
        self.grid_widget.addWidget(self.progressBar, 0, 0)
        ##self.grid_widget.addSeparator()
        # labels position
        col_labels = 0
        self.grid_widget.addWidget(self.label_time, 1, col_labels)
        self.grid_widget.addWidget(self.label_freq, 2, col_labels)
        self.grid_widget.addWidget(self.label_ex_samp, 3, col_labels)
        self.grid_widget.addWidget(self.label_re_samp, 4, col_labels)
        self.grid_widget.addWidget(self.label_dr_samp, 5, col_labels)
        self.grid_widget.addWidget(self.label_drop, 6, col_labels)
        # text boxes postion
        col_boxes = 1
        self.grid_widget.addWidget(self.text_time, 1, col_boxes)
        self.grid_widget.addWidget(self.text_freq, 2, col_boxes)
        self.grid_widget.addWidget(self.text_ex_samp, 3, col_boxes)
        self.grid_widget.addWidget(self.text_re_samp, 4, col_boxes)
        self.grid_widget.addWidget(self.text_dr_samp, 5, col_boxes)
        self.grid_widget.addWidget(self.text_drop, 6, col_boxes)
        # buttons position
        row_buttons = 7
        self.grid_widget.addWidget(self.button_stop, row_buttons, 0, 2, 1)
        self.grid_widget.addWidget(self.button_cancel, row_buttons, 1, 2, 1)
