#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import sys
import glob
import numpy as np
import pyqtgraph as pg

from pyqtgraph.Qt import QtCore, QtGui
from win_capture_settings import Ui_CaptureSettingsWindow
from win_display_settings import Ui_DisplaySettingsWindow
from sys import platform

if platform == "linux" or platform == "linux2":
    from PyQt4.QtGui import *
    ports = glob.glob('/dev/tty[A-Za-z]*')

elif platform == "win32":
    from qtpy.QtGui import *
    ports = ['COM%s' % (i + 1) for i in range(256)]

for port in ports:
    try:
        ser = serial.Serial(port, baudrate=115200, timeout=1)
    except (OSError, serial.SerialException):
        pass

# config 
capture_file = "data/capture.config"
display_file = "data/display.config"
debug_file = "data/debug.txt"

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
        data = self.loadSettings(capture_file, 1)
        self.ui_caps = Ui_CaptureSettingsWindow()
        self.ui_caps.setupUi(self)
        # set data
        self.ui_caps.input_ch.setText(data[0].strip())
        # init actions
        self.ui_caps.button_save.clicked.connect(self.saveCaptureSettings)
        self.ui_caps.button_cancel.clicked.connect(window.close)
        self.stopTimer()
        window.show()

    def saveCaptureSettings(self):
        output = open(capture_file,"w")
        # output.writelines([self.ui_caps.input_sampleR.text()+"\n",self.ui_caps.input_ch.text()+"\n",self.ui_caps.input_numofboards.text()+"\n",self.ui_caps.input_bits.text()])
        output.writelines([self.ui_caps.input_ch.text()])
        output.close()
        window.close()
        self.showGraph()

    # display settings
    def showDisplaySettings(self):
        data = self.loadSettings(display_file, 3)
        self.ui_display = Ui_DisplaySettingsWindow()
        self.ui_display.setupUi(self)
        # set data
        self.ui_display.input_swipe.setText(data[0].strip())
        self.ui_display.input_vtick.setText(data[1].strip())
        self.ui_display.input_htick.setText(data[2].strip())
        # init actions
        self.ui_display.button_save.clicked.connect(self.saveDisplaySettings)
        self.ui_display.button_cancel.clicked.connect(window.close)
        self.stopTimer()
        window.show()

    def saveDisplaySettings(self):
        output = open(display_file,"w")
        output.writelines([self.ui_display.input_swipe.text()+"\n",self.ui_display.input_vtick.text()+"\n", self.ui_display.input_htick.text()])
        output.close()
        window.close()
        self.showGraph()        

    def loadSettings(self, type, num_params):
        try:
            output = open(type, "r")
            data = output.readlines()
            if(len(data) < num_params):
                data = ['0' for i in range(num_params)]
                return data
            else:
                return data
        except IOError:
            data = ['0' for i in range(num_params)]
            return data

    def sendSerial(self):
        ser.close()
        data = self.loadSettings(capture_file, 1)
        ser.write("PC1"+data[0]+"B1"+data[1]+"S9"+data[2])
    
    def saveData(self):
        output = open(debug_file,"w")
        output.writelines(["Channel "+ str(i) +": \n" + str(self.data[i])+"\n" for i in range(self.num_ch)])
        output.close()
        window.close()
    
    # graph settings
    def showGraph(self):   

        # load data
        data_cap = self.loadSettings(capture_file, 1)
        data_display = self.loadSettings(display_file, 3)

        # set capture settings
        self.len_ch = int(data_cap[0])

        # set display settings
        self.swipe = int(data_display[0])

        # swipe ( w = t * r ), sendo r = sample rate e t = tempo
        
        self.vtick = int(data_display[1])
        self.htick = int(data_display[2])
        self.amplitude_start = 0
        self.amplitude_end = 4 * int(data_cap[0])

        self.data = np.empty(shape = (self.len_ch, self.swipe))
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
        label_configs.setText("Swipe: " + str(self.swipe) + " | Zero: 0 | Amplitude: 4V | HTick: " + str(self.htick) + " | VTick " + str(self.vtick) + "V | Channels: " + str(self.len_ch))
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
        self.axis_y.setTickSpacing(4000, self.vtick)

        # graph
        self.graph = self.layout.addPlot(axisItems={'left': self.axis_y},col=0,row=3, colspan = 6)
        self.graph.setYRange(self.amplitude_start, self.amplitude_end)
        self.graph.showGrid(x=True, y=True, alpha=0.25)
        self.graph.setMenuEnabled(False, 'same')

        # config axis x
        self.axis_x = self.graph.getAxis('bottom')
        self.axis_x.setTickSpacing(self.swipe, self.htick)

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
            try:
                self.data[self.num_ch][self.num_sig] = self.strToInt(word) * 0.0008
                self.num_ch += 1
                # debug
                # print (self.strToInt(word))
            except IndexError:
                pass

        self.num_sig += 1

        # clean graph and data
        if self.num_sig % self.swipe == 0:
            self.num_sig = 0
            self.graph.clear()
            #debug
            # self.saveData()

            for i in range(self.len_ch):
                self.curve[i] = self.graph.plot(self.data[i] + (i*4))
                self.data[i] = None       
        
        # set data in graph
        if self.num_sig % int(self.swipe/50) == 0:
            for i in range(self.len_ch):
                self.curve[i].setData((self.data[i] + (i*4)),  pen=pg.mkPen('r', width = 2))

    def strToInt(self, word):
        try:
            return int(((ord(word[0]) - 128) <<     6 ) + (ord(word[1]) - 128))
        except IndexError:
            return 0

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())
