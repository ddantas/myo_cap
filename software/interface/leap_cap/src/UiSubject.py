# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 13:55:35 2021

@author: asaph
"""

import PyQt5

WIN_TITLE = 'LeapCap - Subject'

class UiSubject:

    def __init__(self, win_subject):
        # window to design ui
        self.win_subject = win_subject
        # window name
        self.win_subject.setWindowTitle(WIN_TITLE)
        # main widget
        self.central_widget = PyQt5.QtWidgets.QWidget()
        self.win_subject.setCentralWidget(self.central_widget)
        #window size
        #self.win_main.showMaximized()
        self.win_subject.setMinimumWidth(992)
        self.win_subject.setMinimumHeight(558)

