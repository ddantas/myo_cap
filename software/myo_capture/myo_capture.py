# -*- coding: utf-8 -*-
import sys
import serial
import time
import threading
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

from PyQt4 import QtGui, QtCore

ser = serial.Serial('COM3', 115200, timeout=3)  # abre porta serial COM3 com o baud rate de 115200

class Main():
    def __init__(self):
       self.exibeSerial()

    #exibe os dados da porta serial
    def exibeSerial(self):
        ser.open()

        self.armazenamento = []  # armazenar os valores recebidos

        ##--------------------------------------------------
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

        ##--------------------------------------------------
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(0)        

    def update(self):

        self.ptr1 += 1
        while (ser.inWaiting() == 0):
            pass
        data = float(ser.readline())
        ##atenção multiplicaç~]ao duplicada com o firmware tirar
        #data = data * 0.0008
        print(data)
        self.armazenamento.append(str(data) + ",")
        if self.ptr1%self.tamanho_vetor ==0:
            self.p1.clear()
            self.curve1 = self.p1.plot(self.data1, pen='k')
            self.data1[:] = None
        self.data1[self.ptr1%self.tamanho_vetor] = data
        if self.ptr1%10 == 0:
            self.curve1.setData(self.data1, pen=pg.mkPen('k', width=3))

programa = Main()

