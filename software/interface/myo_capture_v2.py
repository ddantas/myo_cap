#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtWidgets

# serial
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=3)

class MatplotlibWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        self.axis = self.figure.add_subplot(111)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)#QVBoxLayout
        self.layoutVertical.addWidget(self.canvas)

class Main(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.showDialog()
        
    def showDialog(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Luke\'s Hand:', 'Número de canais:')
        
        if ok:
            self.len_ch = int(text)
            self.setInterface()
    
    def setInterface(self):      
        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.matplotlibWidget = []
        
        # set n graphs in window
        for i in range(self.len_ch):
            self.matplotlibWidget.append(MatplotlibWidget(self))
            self.layoutVertical.addWidget(self.matplotlibWidget[i])

        # window config
        self.showMaximized()
        self.setWindowTitle('Graphs')

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

        # .txt
        # self.showSerial()
        
        # show window
        self.show()

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
                self.matplotlibWidget[i].axis.clear()
                self.matplotlibWidget[i].axis.plot(self.data[i])
                self.matplotlibWidget[i].canvas.draw()        

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
        #             self.matplotlibWidget[i].axis.clear()
        #             self.matplotlibWidget[i].axis.plot(self.data[i])
        #             self.matplotlibWidget[i].canvas.draw()


if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())