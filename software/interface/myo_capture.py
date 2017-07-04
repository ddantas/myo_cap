# -*- coding: utf-8 -*-

# ubuntu setup:
# sudo apt-get install python-serial python-pyqtgraph

import sys
import serial
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

from PyQt4 import QtGui, QtCore


ser = serial.Serial('/dev/ttyACM0', 115200, timeout=3)

#file = open('myo_cap.txt','a') # open file

class Main():

    def __init__(self):
        ser.close() 
        self.comunicaSerial()

    def comunicaSerial(self):
        ser.open()
        self.armazenamento = []
        ser.flushInput()

        ## interface start ##        

        self.app = QtGui.QApplication(sys.argv)
        self.window = QtGui.QMainWindow()
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('Luke')

        self.stringaxisx = pg.AxisItem(orientation='bottom')
        self.stringaxisy = pg.AxisItem(orientation='left')
        self.stringaxisx.setLabel('Número de Pontos')
        self.stringaxisy.setLabel('Tensão', 'V')

        self.p1 = self.win.addPlot(axisItems={'left': self.stringaxisy, 'bottom': self.stringaxisx})
        self.p1.setXRange(0, 1000)
        self.p1.setYRange(0, 3)

        ## global data1, curve1 ##

        self.tamanho_vetor = 1000
        self.data1 = np.empty(self.tamanho_vetor)
        self.data1[:] = None
        self.curve1 = self.p1.plot(self.data1)

        self.ptr1 = 0

        ## interface end ##

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(0)
        self.app.exec_()

    def update(self):
        self.ptr1 += 1

        while (ser.inWaiting() == 0):
            pass

        package = ser.readline() # get data
        [data, trash1, trash2, trash3] = map(int, package.split(" ", 4))
        data = data  * 0.0008
        
        #file.write(str(package) + "\n") # save data

        ## plot data ##

        if self.ptr1%self.tamanho_vetor == 0:
            self.p1.clear()
            self.curve1 = self.p1.plot(self.data1, pen ='k')
            self.data1[:] = None
        self.data1[self.ptr1%self.tamanho_vetor] = data
        if self.ptr1%10 == 0:
            self.curve1.setData(self.data1, pen=pg.mkPen('k', width = 3))

Main()