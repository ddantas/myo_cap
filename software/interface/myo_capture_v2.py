#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtWidgets

# Serial
# ser = serial.Serial('/dev/ttyACM0', 115200, timeout=3)  # abre porta serial com o baud rate de 115200

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
        text, ok = QtWidgets.QInputDialog.getText(self, 'Luke\'s Hand:', 
            'Número de canais:')
        
        if ok:
            self.len_ch = int(text)
            self.setInterface()
    
    def setInterface(self):      
        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.matplotlibWidget = []
        for i in range(self.len_ch):
            self.matplotlibWidget.append(MatplotlibWidget(self))
            self.layoutVertical.addWidget(self.matplotlibWidget[i])

        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle('Graphs')

        # Set var
        self.len_sig = 1000
        self.data = np.empty(shape=(self.len_ch,self.len_sig)) # len_ch x len_sig
        self.data[:][:] = None #NULL
        self.num_ch, self.num_sig = 0,0

        # Serial
        # ser.close()
        # ser.open()
        # ser.flushInput()
        # self.timer = pg.QtCore.QTimer()
        # self.timer.timeout.connect(self.showSerial)
        # self.timer.start(0)

        self.showSerial()
        self.show()

    def showSerial(self):
        # .txt
        self.file = open('myo_capture.txt','r') # open file

        for line in self.file:
            # add data
            self.data[self.num_ch][self.num_sig] = float(line)
            self.num_ch += 1

            if self.num_ch >= self.len_ch:
                self.num_ch, self.num_sig = 0, self.num_sig + 1

            if self.num_sig >= self.len_sig:
                self.num_sig = 0
                for i in range(self.len_ch):
                    self.matplotlibWidget[i].axis.clear()
                    self.matplotlibWidget[i].axis.plot(self.data[i])
                    self.matplotlibWidget[i].canvas.draw()

        # Serial
        # while (ser.inWaiting() == 0):
        #     pass

        # self.data[self.num_ch][self.num_sig] = float(ser.readline())
        # self.num_ch += 1

        # if self.num_ch >= self.len_ch:
        #     self.num_ch, self.num_sig = 0, self.num_sig + 1

        # if self.num_sig >= self.len_sig:
        #     self.num_sig = 0
        #     for i in range(self.len_ch):
        #         self.matplotlibWidget[i].axis.clear()
        #         self.matplotlibWidget[i].axis.plot(self.data[i])
        #         self.matplotlibWidget[i].canvas.draw()        

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())