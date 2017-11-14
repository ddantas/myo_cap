#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import sys
import numpy as np
import pyqtgraph as pg

from pyqtgraph.Qt import QtCore, QtGui
from PyQt4.QtGui import *

from win_capture_settings import Ui_CaptureSettingsWindow
from win_display_settings import Ui_DisplaySettingsWindow

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

class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

class Main(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.showGraph()

    def showCaptureSettings(self):
        self.loadSettings()
        self.ui_caps = Ui_CaptureSettingsWindow()
        self.ui_caps.setupUi(self)
        self.initActionsSettings()
        self.stopTimer()
        window.show()

    def showDisplaySettings(self):
        self.loadSettings()
        self.ui_disps = Ui_DisplaySettingsWindow()
        self.ui_disps.setupUi(self)
        self.stopTimer()
        window.show()

    def initActionsSettings(self):
        self.ui_caps.button_save.clicked.connect(self.saveSettings)
        self.ui_caps.button_cancel.clicked.connect(window.close)

    def saveSettings(self):
        output = open("settings_myo.txt","w")
        output.writelines([self.ui_caps.input_ch.text()+'\n', self.ui_caps.input_sampleR.text()+'\n', self.ui_caps.input_ampS.text()+'\n', self.ui_caps.input_ampE.text()])
        output.close()
        window.close()
        self.showGraph()

    def loadSettings(self):
        output = open("settings_myo.txt", "r")
        self.data = output.readlines()
        if(len(self.data) < 4):
            self.data = ['0','0','0','0']
            self.showSettings()

    def showGraph(self):   

        self.loadSettings()

        # load and set settings
        self.len_ch = int(self.data[0])
        self.len_sig = int(self.data[1])
        self.amplitude_start = int(self.data[2])
        self.amplitude_end = int(self.data[3]) * int(self.data[0])
        
        self.axis = DateAxis(orientation='left')
        self.axis.setScale(scale=2)
        
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')                
        
        self.pw = pg.GraphicsWindow()

        self.pw.setWindowTitle('EMG')
        
        #  
        self.data = np.empty(shape = (self.len_ch, self.len_sig))
        self.data[:][:] = None
        self.num_ch, self.num_sig = 0, 0
        self.curve = []

        # config layout
        self.layout = self.pw.addLayout()
        
        # config buttons
        proxy_play = QGraphicsProxyWidget()
        button_play = QPushButton('Start Capture')
        button_play.resize(50,50)
        button_play.clicked.connect(self.showGraph)
        proxy_play.setWidget(button_play)
        self.layout.addItem(proxy_play,row=0, colspan = 1)

        proxy_stop = QGraphicsProxyWidget()
        button_stop = QPushButton('Stop Capture')
        button_stop.clicked.connect(self.stopTimer)
        proxy_stop.setWidget(button_stop)
        self.layout.addItem(proxy_stop, row=0, colspan = 1)

        label_configs = pg.LabelItem()
        label_configs.setText("Swipe: " + str(self.len_sig) + " ~ 0.5s | Zero: 0 | Amplitude: 3.3V | HTick: 100 ~ 0.1s | VTick 1.0V | Channels: "+ str(self.len_ch))
        self.layout.addItem(label_configs, row=0, colspan=2)

        proxy_settings = QGraphicsProxyWidget()
        button_settings = QPushButton('Display Settings')
        button_settings.clicked.connect(self.showDisplaySettings)
        proxy_settings.setWidget(button_settings)
        self.layout.addItem(proxy_settings, row=0, colspan = 1)

        proxy_settings2 = QGraphicsProxyWidget()
        button_settings2 = QPushButton('Capture Settings')
        button_settings2.clicked.connect(self.showCaptureSettings)
        proxy_settings2.setWidget(button_settings2)
        self.layout.addItem(proxy_settings2, row=0, colspan = 1)

        self.graph = self.layout.addPlot(axisItems={'left': self.axis},col=0,row=3, colspan = 6)

        self.graph.setYRange(self.amplitude_start, self.amplitude_end) #Range Amplitude
        self.graph.showGrid(x=True, y=True, alpha=0.1)
        self.graph.setMenuEnabled(False, 'same')
        
        for i in range(self.len_ch):
            self.curve.append(self.graph.plot(self.data[i]))

        self.pw.showMaximized()

        self.startTimer()

    def startTimer(self):

        ser.close()
        ser.open()
        ser.flushInput()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.plotSerial)
        self.timer.start(0)

    def stopTimer(self):
        ser.close()
        self.timer.stop()

    def plotSerial(self):
        
        # serial
        while (ser.inWaiting() == 0):
            pass

        # split string and add data 
        self.num_ch = 0             self.data[self.num_ch][self.num_sig] = self.strToInt(word) * 0.0008

        
        for word in ser.readline().rstrip().split(" "):
            self.num_ch += 1

        self.num_sig += 1

        # plot n graphs
        if self.num_sig % self.len_sig == 0:
            self.num_sig = 0
            self.graph.clear()

            for i in range(self.len_ch):
                self.curve[i] = self.graph.plot(self.data[i] + (i*4))
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
    window = Main()
    sys.exit(app.exec_())
