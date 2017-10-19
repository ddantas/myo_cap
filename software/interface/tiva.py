#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import sys
import numpy as np
import pyqtgraph as pg

from pyqtgraph.Qt import QtCore, QtGui
from PyQt4.QtGui import *

from win_main import Ui_MainWindow
from win_settings import Ui_SettingsWindow

# baudrate
baudrate = 115200

# serial configuration
ser = serial.Serial('/dev/ttyACM0', baudrate, timeout=1)

class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        for x in values:
            strns.append(x%4)
        return strns


class Main(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.showInfo()

    def showInfo(self):
        self.ui_m = Ui_MainWindow()
        self.ui_m.setupUi(self)
        self.initActionsMain()
        self.setInfo()

    def setInfo(self):
        self.loadSettings()
        
        self.ui_m.label_ch.setText(self.data[0])
        self.ui_m.label_sampleR.setText(self.data[1])
        self.ui_m.label_ampS.setText(self.data[2])
        self.ui_m.label_ampE.setText(self.data[3])

    def initActionsMain(self):
        self.ui_m.button_start.clicked.connect(self.showGraph)
        self.ui_m.actionSettings.triggered.connect(self.showSettings)
       
    def showSettings(self):
        self.ui_s = Ui_SettingsWindow()
        self.ui_s.setupUi(self)
        self.initActionsSettings()

    def initActionsSettings(self):
        self.ui_s.button_save.clicked.connect(self.saveSettings)
        # self.ui_s.button_cancel.clicked.connect(self.saveSettings)

    def saveSettings(self):
        output = open("settings_myo.txt","w")
        output.writelines([self.ui_s.input_ch.text()+'\n', self.ui_s.input_sampleR.text()+'\n', self.ui_s.input_ampS.text()+'\n', self.ui_s.input_ampE.text()])
        output.close()
        self.showInfo()

    def loadSettings(self):
        output = open("settings_myo.txt", "r")
        self.data = output.readlines()
        if(len(self.data) < 4):
            self.data = ['0','0','0','0']
            self.showSettings()

    def showGraph(self):   

        self.loadSettings()
        
        # set var
        self.len_ch = int(self.data[0])
        self.len_sig = int(self.data[1])
        self.amplitude_start = int(self.data[2])
        self.amplitude_end = int(self.data[3]) * int(self.data[0])

        self.axis = DateAxis(orientation='left')
        self.axis.setScale(scale=2)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')                
        self.pw = pg.PlotWidget(axisItems={'left': self.axis})

        self.pw.setMouseEnabled(x=False, y=False)
        self.pw.setLabel('left', '', units='V')
        self.pw.setLabel('bottom', 'Sample Rate', units='S')
        self.pw.setWindowTitle('EMG')

        # set var 
        self.data = np.empty(shape = (self.len_ch, self.len_sig))
        self.data[:][:] = None
        self.num_ch, self.num_sig = 0, 0
        self.curve = []

        # set n graphs in window	

        self.pw.setYRange(self.amplitude_start, self.amplitude_end) #Range Amplitude
        self.pw.showGrid(x=True, y=True, alpha=0.25)
        self.pw.setMenuEnabled(False, 'same')
        
        for i in range(self.len_ch):
            self.curve.append(self.pw.plot(self.data[i]))


        self.pw.showMaximized()

        ser.close()
        ser.open()
        ser.flushInput()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.showSerial)
        self.timer.start(0)


    def showSerial(self):
        
        # serial
        while (ser.inWaiting() == 0):
            pass

        # split string and add data 
        self.num_ch = 0 
        
        for word in ser.readline().rstrip().split(" "):
            self.data[self.num_ch][self.num_sig] = self.strToInt(word) * 0.0008
            self.num_ch += 1

        self.num_sig += 1

        # plot n graphs
        if self.num_sig % self.len_sig == 0:
            self.num_sig = 0
            self.pw.clear()

            for i in range(self.len_ch):
                self.curve[i] = self.pw.plot(self.data[i] + (i*4))
                self.data[i] = None       
            
        if self.num_sig % 10 == 0:
            for i in range(self.len_ch):
                self.curve[i].setData((self.data[i] + (i*4)),  pen=pg.mkPen('k', width = 2))

    def strToInt(self, word):
        if(len(word) > 1):
            return int(((ord(word[0]) - 128) <<6 ) + (ord(word[1]) - 128))
        else:
            return 0
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    programa = Main()
    programa.show()
    sys.exit(app.exec_())
