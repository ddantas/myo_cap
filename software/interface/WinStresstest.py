# -*- coding: utf-8 -*-

import PyQt5
import UiStresstest
from PyQt5.QtCore import QBasicTimer

class WinStresstest(PyQt5.QtWidgets.QMainWindow):

    def __init__(self, settings, board, winMain):
        # calling superclass constructor
        super(WinStresstest, self).__init__()
        # global objects
        self.settings = settings
        
        self.board = board
        self.winMain = winMain 

        #settings
        self.freq = self.settings.getFuncGenFreq()
        self.time = self.settings.getStressTime()
        #data
        self.received = 0
        self.received = self.winMain.textfile.getLogLength()
        
        # stress test ui
        self.ui_stress_test = UiStresstest.UiStresstest(self)
        # connect ui buttons to modules
        self.ui_stress_test.button_stop.clicked.connect(self.startProgress)
        self.ui_stress_test.button_cancel.clicked.connect(self.close)
        # load settings
        self.loadSettings()        
        # progressBar        
        self.progressBar = self.ui_stress_test.progressBar
        # buttons
        self.btnStart = self.ui_stress_test.button_stop
        self.btnReset = self.ui_stress_test.button_cancel

        # timer
        self.timer = QBasicTimer()
        self.step = 0

        #start
        self.startProgress()
	
        # start capture
##        self.winMain.startCapture()

    # progressBar
    def resetBar(self):
        self.step = 0
        self.progressBar.setValue(0)

    def startProgress(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btnStart.setText('Start')
            # start capture
##            self.winMain.startCapture()
        else:
            self.timer.start((1000*self.time)/100, self)
            self.btnStart.setText('Stop')

    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            self.btnStart.setText('Done')
            # stop capture
##            self.winMain.stopCapture()
            return

        self.step +=1
        self.progressBar.setValue(self.step)
        # simulated capture
        self.received +=1
        # refresh window capture information
        self.loadSettings()
            
    # load settings to text boxes
    def loadSettings(self):
        # load stress time
        self.ui_stress_test.text_time.setText(str(self.time))
        #load capture frequency
        self.ui_stress_test.text_freq.setText(str(self.freq))
        #calculate and load expected samples
        self.ex_samp = (self.freq*self.time)
        self.ui_stress_test.text_ex_samp.setText(str(self.ex_samp))
        #read and load received samples
        self.ui_stress_test.text_re_samp.setText(str(self.received))
        #calculate and load dropped samples
        self.dr_samp = self.ex_samp-self.received
        self.ui_stress_test.text_dr_samp.setText(str(self.dr_samp))
        #calculate and load drop rate
        self.drop = 100*self.dr_samp/self.ex_samp
        self.ui_stress_test.text_drop.setText(str(self.drop))

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
