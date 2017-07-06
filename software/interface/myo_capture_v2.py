#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial
import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

# serial
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=3)

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
        self.win.setWindowTitle('Luke\'s Hand')

        self.graph = []

        # set n graphs in window
        for i in range(self.len_ch):
            self.layoutVertical = self.win.addLayout(row=i, col=0)
            self.graph.append(self.layoutVertical.addPlot(title="Channel "+str(i)))

        # set var
        self.len_sig = 1000
        self.data = np.empty(shape=(self.len_ch, self.len_sig)) # len_ch x len_sig
        self.data[:][:] = None #NULL
        self.num_ch, self.num_sig = 0, 0

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
        if self.num_sig >= self.len_sig:
            self.num_sig = 0
            for i in range(self.len_ch):
                self.graph[i].clear()
                self.graph[i].plot(self.data[i])       

        # .txt
        # self.file = open('myo_capture.txt','r') # open file

        # for line in self.file:
        #     self.num_ch = 0
        #     # add data 
        #     for sig in line.rstrip().split(" "):
        #         self.data[self.num_ch][self.num_sig] = sig
        #         self.num_ch += 1
        #     self.num_sig += 1

        #     # plot n graphs
        #     if self.num_sig >= self.len_sig:
        #         self.num_sig = 0
        #         for i in range(self.len_ch):
        #             self.graph[i].clear()
        #             self.graph[i].plot(self.data[i])


if __name__ == '__main__':
    
    main = Main()
