#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial
import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

# serial configuration
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

class Main():
    
    def __init__(self):
       
       # set len ch
        self.len_ch = 4

        # show interface
        self.showInterface()
           
    def showInterface(self):      
        
        ## window config        
        self.app = QtGui.QApplication(sys.argv)
        self.window = QtGui.QMainWindow()

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('Sinal mioeletrico')

        # set var
        self.len_sig = 1000
        self.data = np.empty(shape = (self.len_ch, self.len_sig))
        self.data[:][:] = None
        self.num_ch, self.num_sig = 0, 0
        self.graph = []
        self.curve = []

        # set n graphs in window
        self.num_rows = 2
        self.num_cols = 2
	
	for i in range(num_rows):
            for j in range(num_cols):
                self.layoutVertical = self.win.addLayout(row = i, col = j)
                
        for i in ranfe(self.len_ch)
            self.graph.append(self.layoutVertical.addPlot(title = "Canal " + str(i + 1)))
            self.graph[i].setXRange(0, self.len_sig)
            self.graph[i].setYRange(0, 3)
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
        
	#read .txt
        #self.file = open('myo_capture.txt','r') # open file

        #for line in self.file:
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
