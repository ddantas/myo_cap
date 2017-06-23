# ubuntu setup:
# sudo apt-get install python-serial python-pyqtgraph

# -*- coding: utf-8 -*-
import sys
import serial
#import matplotlib.pyplot as plt
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

from PyQt4 import QtGui, QtCore


ser = serial.Serial('/dev/ttyACM0', 115200, timeout=3)  # abre porta serial com o baud rate de 115200
file = open('myo_cap.txt','a') # open file

class Main():

    def __init__(self):
        ser.close() 
        self.comunicaSerial()

    def comunicaSerial(self):
        ser.open()
        self.armazenamento = []
        ser.flushInput()

        ## Interface Start ##        
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
        #Se tirar esse setXRange e esse setYRange, fica automatica a escala
        self.p1.setXRange(0,1000)
        self.p1.setYRange(0,3)

        # global data1, curve1
        self.tamanho_vetor = 1000
        self.data1 = np.empty(self.tamanho_vetor)
        self.data1[:] = None #Prenchendo o vetor com NULL
        self.curve1 = self.p1.plot(self.data1)

        self.ptr1 = 0

        ## Interface End ##

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(0)
        self.app.exec_()

    def update(self):
        self.ptr1 += 1
        #self.data1[:-1] = self.data1[1:]  # shift data in the array one sample left

        while (ser.inWaiting() == 0):
            pass

        data = float(ser.readline()) # get data
        #data = data * 0.0008
        print(data) # print data
        file.write(str(data)+"\n") # save data
        self.armazenamento.append(str(data) + ",") 

        # plot data
        if self.ptr1%self.tamanho_vetor ==0:
            self.p1.clear()
            self.curve1 = self.p1.plot(self.data1, pen='k')
            self.data1[:] = None
        self.data1[self.ptr1%self.tamanho_vetor] = data
        if self.ptr1%10 == 0:
            self.curve1.setData(self.data1, pen=pg.mkPen('k', width=3))

Main()

