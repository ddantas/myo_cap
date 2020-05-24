# -*- coding: utf-8 -*-

import PyQt5
import UiFuncGenSettings


class WinFuncGenSettings(PyQt5.QtWidgets.QMainWindow):

    def __init__(self, settings, board, win_main):
        # calling superclass constructor
        super(WinFuncGenSettings, self).__init__()
        # global objects
        self.settings = settings
        self.board = board
        self.win_main = win_main
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
        try:
            # set frequency
            if self.board.setFucGenFreq(self.ui_funcgen_settings.text_freq.text()) == 'ok': 
                self.settings.setFuncGenFreq(self.ui_funcgen_settings.text_freq.text())
        except:
            self.win_main.showMessage('Error','Function generator settings did not apply!\nPlease, connect the board.')
        # set stress time
        self.settings.setStressTime(self.ui_funcgen_settings.text_time.text())
        # close window
        self.close()