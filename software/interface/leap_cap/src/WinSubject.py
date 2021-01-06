# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 13:53:55 2021

@author: asaph
"""

import PyQt5
import UiSubject

class WinSubject(PyQt5.QtWidgets.QMainWindow):

    def __init__(self):
        # calling superclass constructor
        super(WinSubject, self).__init__()
        # global objects
        
        # Subject ui
        self.ui_subject = UiSubject.UiSubject(self)

        
        
