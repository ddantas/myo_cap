# -*- coding: utf-8 -*-

import PyQt5
import UiFuncGenSettings
import Board

class WinFuncGenSettings(PyQt5.QtWidgets.QMainWindow):

    def __init__(self, settings):
        # calling superclass constructor
        super(WinFuncGenSettings, self).__init__()
        # global objects
        self.settings = settings
        # function generator ui
        self.ui_funcgen_settings = UiFuncGenSettings.UiFuncGenSettings(self)
        # connect ui buttons to modules
        self.ui_funcgen_settings.button_apply.clicked.connect(self.applyChanges)
        self.ui_funcgen_settings.button_cancel.clicked.connect(self.close)
        # load settings
        self.loadSettings()

    # load settings to text boxes
    def loadSettings(self):
        #load frequency
        self.ui_funcgen_settings.text_freq.setText(str(self.settings.getFuncGenFreq()))
        # load stress time
        self.ui_funcgen_settings.text_time.setText(str(self.settings.getStressTime()))

    # set new values at settings object and board
    def applyChanges(self):
        # set frequency
        self.settings.setFuncGenFreq(self.ui_funcgen_settings.text_freq.text())
        # set stress time
        self.settings.setStressTime(self.ui_funcgen_settings.text_time.text())
        # close window
        self.close()