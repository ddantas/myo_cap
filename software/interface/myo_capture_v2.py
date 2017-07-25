#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial
import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from PyQt4.QtGui import *

# baudrate
baudrate = 115200

# serial configuration
ser = serial.Serial('/dev/ttyACM0', baudrate, timeout=1)

# amplitude
amplitude_start = 0
amplitude_end = 500

class Main():
    
    def __init__(self): 
        # show interface
        self.showInputs()

    def showInputs(self):

        # window init
        self.app = QtGui.QApplication(sys.argv)
        self.window = QtGui.QMainWindow()

        # window title
        self.window.setWindowTitle('Entrada')
        self.window.resize(200, 160)

        # input channel
        self.label1 = QLabel(self.window)
        self.label1.setText("Canais:")
        self.label1.move(20,10)

        self.input_channel = QLineEdit(self.window)
        self.input_channel.move(20, 35)
        self.input_channel.resize(160,30)

        #input frequency
        self.label1 = QLabel(self.window)
        self.label1.setText("Frequencia:")
        self.label1.move(20,60)

        self.input_freq = QLineEdit(self.window)
        self.input_freq.move(20, 85)
        self.input_freq.resize(160,30)

        # button
        self.button = QPushButton(self.window)
        self.button.setText("Enviar") 
        self.button.move(20, 120)
        self.button.clicked.connect(self.showInterface)
        
        # show window
        self.window.show()
        self.app.exec_()

    def showInterface(self):      

        # set var
        self.len_ch = int(self.input_channel.text())
        self.len_sig = int(self.input_freq.text()) 

        ## window config        
        self.app = QtGui.QApplication(sys.argv)
        self.window = QtGui.QMainWindow()

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('Sinal Mioeletrico')

        # set var 
        self.data = np.empty(shape = (self.len_ch, self.len_sig))
        self.data[:][:] = None
        self.num_ch, self.num_sig = 0, 0
        self.graph = []
        self.curve = []

        # set n graphs in window	
        for i in range(self.len_ch):
            self.layoutVertical = self.win.addLayout(row=i, col=0)		
            self.graph.append(self.layoutVertical.addPlot(title="Channel "+str(i+1)))  
                          
        for i in range(self.len_ch):
            self.graph[i].setXRange(0, self.len_sig)
            self.graph[i].setYRange(amplitude_start, amplitude_end) #Range Amplitude
            self.graph[i].setLabel('left', 'Tensão (V)')
            self.graph[i].setLabel('bottom', 'Nº de amostras')
            self.curve.append(self.graph[i].plot(self.data[i]))

        # serial
        ser.close()
        ser.open()
        ser.flushInput()
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.showSerial)
        self.timer.start(0)
        
        # show window
        self.app.exec_()

    def showSerial(self):

        # serial
        while (ser.inWaiting() == 0):
            pass

        # split string and add data
        self.num_ch = 0 
        
        for sig in ser.readline().rstrip().split(" "):
            self.data[self.num_ch][self.num_sig] = sig
            self.num_ch += 1

        self.num_sig += 1

        # plot n graphs
        if self.num_sig % self.len_sig == 0:
            self.num_sig = 0
	    
	    for i in range(self.len_ch):
            	self.graph[i].clear()
            	self.curve[i] = self.graph[i].plot(self.data[i], pen = 'k')
	
    	self.data[i] = None       
        
        if self.num_sig % 10 == 0:
            for i in range(self.len_ch):
                self.curve[i].setData(self.data[i] * 0.0008,  pen=pg.mkPen('k', width = 2))
        
	    # read .txt
        # self.file = open('myo_capture.txt','r') # open file

        # for line in self.file:
        #    self.num_ch = 0
        #    #add data 
        #    for sig in line.rstrip().split(" "):
        #        self.data[self.num_ch][self.num_sig] = sig
        #        self.num_ch += 1
        #    self.num_sig += 1
        #    #plot n graphs
        #    if self.num_sig >= self.len_sig:
        #        self.num_sig = 0
        #        for i in range(self.len_ch):
        #            self.graph[i].clear()
        #            self.graph[i].plot(self.data[i])


if __name__ == '__main__':
    
    main = Main()
