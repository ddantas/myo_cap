# -*- coding: utf-8 -*-

import PyQt5
import UiStresstest


class WinStresstest(PyQt5.QtWidgets.QMainWindow):

    def __init__(self, settings, board, winMain):
        # calling superclass constructor
        super(WinStresstest, self).__init__()
        # global objects
        self.settings = settings
        
        self.board = board
        self.winMain = winMain 
    
        # stress test ui
        self.ui_stress_test = UiStresstest.UiStresstest(self)
        # connect ui buttons to modules
        self.ui_stress_test.button_apply.clicked.connect(self.applyChanges)
        self.ui_stress_test.button_cancel.clicked.connect(self.close)
        # load settings
        self.loadSettings()

    # load settings to text boxes
    def loadSettings(self):
        #load frequency
        self.ui_stress_test.text_freq.setText(str(self.settings.getFuncGenFreq()))
        # load stress time
        self.ui_stress_test.text_time.setText(str(self.settings.getStressTime()))

    # set new values at settings object and board
    def applyChanges(self):
        
        self.winMain.stopCapture()
        self.board.stop()
        
        if self.board.setFucGenFreq( self.ui_funcgen_settings.text_freq.text() ) == 'ok': 
            # set frequency
            self.settings.setFuncGenFreq(self.ui_funcgen_settings.text_freq.text())
        
        # set stress time
        self.settings.setStressTime(self.ui_funcgen_settings.text_time.text())
        # close window
        self.close()
