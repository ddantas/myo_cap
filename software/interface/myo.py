#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import sys
import numpy as np
import pyqtgraph as pg

from pyqtgraph.Qt import QtCore, QtGui
from PyQt4.QtGui import *

from gui_main import Ui_MainWindow
from gui_settings import Ui_SettingsWindow

# baudrate
baudrate = 115200

# serial configuration
ser = serial.Serial('/dev/ttyACM0', baudrate, timeout=1)

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
        self.amplitude_end = int(self.data[3])

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('EMG')

        # set var 
        self.data = np.empty(shape = (self.len_ch, self.len_sig))
        self.data[:][:] = None
        self.num_ch, self.num_sig = 0, 0
        self.graph = []
        self.curve = []

        # set n graphs in window	
        for i in range(self.len_ch):
            self.layoutVertical = self.win.addLayout(row=i, col=0)		
            self.graph.append(self.layoutVertical.addPlot())  
                          
        for i in range(self.len_ch):
            self.graph[i].setXRange(0, self.len_sig)
            self.graph[i].setYRange(self.amplitude_start, self.amplitude_end) #Range Amplitude
            # self.graph[i].setLabel('left', 'Tensão (V)')
            # self.graph[i].setLabel('bottom', 'Nº de amostras')
            self.curve.append(self.graph[i].plot(self.data[i]))

        # serial
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
            self.data[self.num_ch][self.num_sig] = self.strToInt(word)
            self.num_ch += 1

        self.num_sig += 1

        # plot n graphs
        if self.num_sig % self.len_sig == 0:
            self.num_sig = 0
	    
	        for i in range(self.len_ch):
                self.graph[i].clear()
                self.curve[i] = self.graph[i].plot(self.data[i] * 0.0008, pen=pg.mkPen('k', width = 2))
                self.data[i] = None       
        
        # if self.num_sig % 10 == 0:
        #     for i in range(self.len_ch):
        #         self.curve[i].setData(self.data[i] * 0.0008,  pen=pg.mkPen('k', width = 2))
        
	    # read .txt
        # self.file = open('output.txt','r') # open file

        # for line in self.file:
        #     self.num_ch = 0
        #     #add data 
        #     for word in line.rstrip().split(" "):
        #         self.data[self.num_ch][self.num_sig] = self.strToInt(word)
        #         self.num_ch += 1
        #     self.num_sig += 1
        #     #plot n graphs
        #     if self.num_sig >= self.len_sig:
        #        self.num_sig = 0
        #        for i in range(self.len_ch):
        #            self.graph[i].clear()
        #            self.graph[i].plot(self.data[i] * 0.0008, pen=pg.mkPen('k', width = 2))
        #            self.data[i] = None

    def strToInt(self, word):
        return int(((ord(word[0]) - 128) <<6) + (ord(word[1]) - 128))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    programa = Main()
    programa.show()
    sys.exit(app.exec_())
