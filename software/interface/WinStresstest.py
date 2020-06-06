# -*- coding: utf-8 -*-

import PyQt5
import UiStresstest

class WinStresstest(PyQt5.QtWidgets.QMainWindow):

    def __init__(self, settings, board, win_main):
        # calling superclass constructor
        super(WinStresstest, self).__init__()
        # global objects
        self.settings = settings
        self.board = board
        self.win_main = win_main
        #settings
        self.freq = self.settings.getFuncGenFreq()
        self.time = self.settings.getStressTime()

        #data
        self.recvData()
        
        # stress test ui
        self.ui_stress_test = UiStresstest.UiStresstest(self)
            # progressBar        
        self.progressBar = self.ui_stress_test.progressBar
            # buttons
        self.btnStart = self.ui_stress_test.button_stop
        self.btnCancel = self.ui_stress_test.button_cancel
            # connect ui buttons to modules
        self.btnStart.clicked.connect(self.startProgress)
        self.btnCancel.clicked.connect(self.cancelTest)
        
        # load settings
        self.loadSettings()
        
        # timer
        self.timer = PyQt5.QtCore.QBasicTimer()
        self.step = 0

        # start
        self.startProgress()
	

    # received data
    def recvData(self):
        try:
            self.received = self.win_main.textfile.getLogLength()
        except:
            self.received = 0

    # progressBar
    def resetBar(self):
        self.step = 0
        self.progressBar.setValue(0)

    def cancelTest(self):
        self.timer.stop()
        self.win_main.stopCapture(False)
        self.close()
        
    def startProgress(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btnStart.setText('Start')
            # reset test midway
            self.resetBar()
        else:
            self.timer.start((1000*self.time)/100, self)
            self.btnStart.setText('Stop/Reset')
            # start capture
            self.win_main.startCapture()

    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            self.btnStart.setText('Done')
            self.btnStart.setEnabled(False)
            # stop capture
            self.logTestData()
            self.win_main.stopCapture(True)
            return

        self.step +=1
        self.progressBar.setValue(self.step)
        
        # refresh window capture information
        self.loadSettings()
        self.recvData()

    #log test
    def logTestData(self):
        self.win_main.textfile.writeHeaderLine('')
        self.win_main.textfile.writeHeaderLine('Stress test results')
        self.win_main.textfile.writeHeaderLine('')
        self.win_main.textfile.writeMetadataLine('testLength',self.time)
        self.win_main.textfile.writeMetadataLine('testFrequency',self.freq)
        self.win_main.textfile.writeMetadataLine('expectedSamples',self.ex_samp)
        self.win_main.textfile.writeMetadataLine('receivedSamples',self.received)
        self.win_main.textfile.writeMetadataLine('droppedSamples',self.dr_samp)
        self.win_main.textfile.writeMetadataLine('dropRate',self.drop)
        pass

    
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

