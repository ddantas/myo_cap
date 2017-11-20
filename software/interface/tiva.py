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

# config 
capture_file = "data/capture.config"
display_file = "data/display.config"

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

    # capture settings
    def showCaptureSettings(self):
        data = self.loadSettings(capture_file, 2)
        self.ui_caps = Ui_CaptureSettingsWindow()
        self.ui_caps.setupUi(self)
        # set data
        self.ui_caps.input_ch.setText(data[0].strip())
        self.ui_caps.input_sampleR.setText(data[1].strip())
        # init actions
        self.ui_caps.button_save.clicked.connect(self.saveCaptureSettings)
        self.ui_caps.button_cancel.clicked.connect(window.close)
        self.stopTimer()
        window.show()

    def saveCaptureSettings(self):
        output = open(capture_file,"w")
        output.writelines([self.ui_caps.input_ch.text()+"\n", self.ui_caps.input_sampleR.text()])
        output.close()
        window.close()
        self.showGraph()

    # display settings
    def showDisplaySettings(self):
        data = self.loadSettings(display_file, 2)
        self.ui_display = Ui_DisplaySettingsWindow()
        self.ui_display.setupUi(self)
        # set data
        self.ui_display.input_vtick.setText(data[0].strip())
        self.ui_display.input_htick.setText(data[1].strip())
        # init actions
        self.ui_display.button_save.clicked.connect(self.saveDisplaySettings)
        self.ui_display.button_cancel.clicked.connect(window.close)
        self.stopTimer()
        window.show()

    def saveDisplaySettings(self):
        output = open(display_file,"w")
        output.writelines([self.ui_display.input_vtick.text()+"\n", self.ui_display.input_htick.text()])
        output.close()
        window.close()
        self.showGraph()        

    def loadSettings(self, type, num_params):
        try:
            output = open(type, "r")
            data = output.readlines()
            if(len(data) < num_params):
                data = [0 for i in range(num_params)]
                return data
            else:
                return data
        except IOError:
            data = [0 for i in range(num_params)]
            return data

    # graph settings
    def showGraph(self):   

        # load data
        data_cap = self.loadSettings(capture_file, 2)
        data_display = self.loadSettings(display_file, 2)

        # set capture settings
        self.len_ch = int(data_cap[0])
        self.len_sig = int(data_cap[1])
        self.amplitude_start = 0
        self.amplitude_end = 4 * int(data_cap[0])
        
        # set display settings
        self.vtick =  int(data_display[0])
        self.htick = int(data_display[1])

        self.data = np.empty(shape = (self.len_ch, self.len_sig))
        self.data[:][:] = None
        self.num_ch, self.num_sig = 0, 0
        self.curve = []

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')                
        
        self.pw = pg.GraphicsWindow()
        self.pw.setWindowTitle('EMG')

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
        label_configs.setText("Swipe: " + str(self.len_sig) + " ~ 0.5s | Zero: 0 | Amplitude: 3.3V | HTick: "+ str(self.htick) + " | VTick " + str(self.vtick) + "V | Channels: "+ str(self.len_ch))
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

        # config axis y 
        self.axis_y = DateAxis(orientation='left')
        self.axis_y.setTickSpacing(4, self.vtick)

        # graph
        self.graph = self.layout.addPlot(axisItems={'left': self.axis_y},col=0,row=3, colspan = 6)
        self.graph.setYRange(self.amplitude_start, self.amplitude_end)
        self.graph.showGrid(x=True, y=True, alpha=0.25)
        self.graph.setMenuEnabled(False, 'same')

        # config axis x
        self.axis_x = self.graph.getAxis('bottom')
        self.axis_x.setTickSpacing(100, self.htick)

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

        self.num_ch = 0

        # split string and add data         
        for word in ser.readline().rstrip().split(" "):
            self.data[self.num_ch][self.num_sig] = self.strToInt(word) * 0.0008
            self.num_ch += 1
            # debug
            # print (self.strToInt(word))

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
