#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import sys
import glob
import numpy as np
import pyqtgraph as pg
import datetime
import numbers

from pyqtgraph.Qt import QtCore, QtGui
from win_capture_settings import Ui_CaptureSettingsWindow
from win_display_settings import Ui_DisplaySettingsWindow
from sys import platform

# select platform
if platform == "linux" or platform == "linux2":
    from PyQt4.QtGui import *
    ports = glob.glob('/dev/tty[A-Za-z]*')
elif platform == "win32":
    from qtpy.QtGui import *
    ports = ['COM%s' % (i + 1) for i in range(256)]

# search port
for port in ports:
    try:
        ser = serial.Serial(port, baudrate=115200, timeout=1)
    except (OSError, serial.SerialException):
        pass

# log file
log_file = "data/"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+".log"

# config files
capture_file = "config/capture.config"
display_file = "config/display.config"

# config tiva
t_start = 0
t_end = 3.3
ad = 12
const_board = (t_end - t_start) / (2 ** ad) 

# class to set axis label
class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        data_display = load().settings(display_file, 6)
        amplitude_start = float(data_display[4])
        amplitude_end = float(data_display[5])
        amplitude = amplitude_end - amplitude_start
        for x in values:
            strns.append((x % amplitude) + (amplitude_start))
        return strns

# class to init main window
class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

# class main
class Main(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.showGraph()

    # show capture settings
    def showCaptureSettings(self):
        data = load().settings(capture_file, 1)
        self.ui_caps = Ui_CaptureSettingsWindow()
        self.ui_caps.setupUi(self)
        # set data
        self.ui_caps.input_ch.setText(data[0].strip())
        # init actions
        self.ui_caps.button_save.clicked.connect(self.saveCaptureSettings)
        self.ui_caps.button_cancel.clicked.connect(window.close)
        self.stopTimer()
        window.show()

    # store capture settings
    def saveCaptureSettings(self):
        output = open(capture_file,"w")
        # output.writelines([self.ui_caps.input_sampleR.text()+"\n",self.ui_caps.input_ch.text()+"\n",self.ui_caps.input_numofboards.text()+"\n",self.ui_caps.input_bits.text()])
        output.writelines([self.ui_caps.input_ch.text()])
        output.close()
        window.close()
        self.showGraph()

    # show display settings
    def showDisplaySettings(self):
        data = load().settings(display_file, 3)
        self.ui_display = Ui_DisplaySettingsWindow()
        self.ui_display.setupUi(self)
        # set data
        try:
            self.ui_display.input_swipe.setText(data[0].strip())
            self.ui_display.input_zero.setText(data[1].strip())
            self.ui_display.input_vtick.setText(data[2].strip())
            self.ui_display.input_htick.setText(data[3].strip())
            self.ui_display.input_ampS.setText(data[4].strip())
            self.ui_display.input_ampE.setText(data[5].strip())
        except:
            pass

        # init actions
        self.ui_display.button_save.clicked.connect(self.saveDisplaySettings)
        self.ui_display.button_cancel.clicked.connect(window.close)
        self.stopTimer()
        window.show()

    # store display settings
    def saveDisplaySettings(self):
        try:
            self.swipe = int(self.ui_display.input_swipe.text())
            check = 1 / self.swipe
        except:
            self.swipe = 1000
            print("ERROR swipe!")
        try:
            self.zero = float(self.ui_display.input_zero.text())
        except:
            self.zero = 0.0
            print("ERROR zero!")
        try:
            self.vtick = float(self.ui_display.input_vtick.text())
            check = 1 / self.vtick
        except:
            self.vtick = 1.0
            print("ERROR vtick!")
        try:
            self.htick = float(self.ui_display.input_htick.text())
            check = 1 / self.htick
        except:
            self.htick = 100.0
            print("ERROR htick!")                
        try:
            self.ampS = float(self.ui_display.input_ampS.text())
        except:
            self.ampS = -2.0
            print("ERROR ampS!")
        try:
            self.ampE = float(self.ui_display.input_ampE.text())
        except:
            self.ampE = 2.0
            print("ERROR ampE!")
        output = open(display_file,"w")
        output.writelines([str(self.swipe)+"\n",str(self.zero)+"\n",str(self.vtick)+"\n", str(self.htick)+"\n",str(self.ampS)+"\n",str(self.ampE)])
        output.close()
        window.close()
        self.showGraph()        

    # send config to tiva
    def sendSerial(self):
        ser.close()
        data = load().settings(capture_file, 1)
        ser.write("PC1"+data[0]+"B1"+data[1]+"S9"+data[2])
    
    # save data log emg
    def saveLog(self):
        output = open(log_file,"a")
        # print (range(self.len_ch))
        for j in range(self.swipe):
            for i in range(self.len_ch):
                if (i < self.len_ch - 1):
                    output.write(str(self.data[i][j])+", ")
                else:
                    output.write(str(self.data[i][j])+"\n")
        output.close()
        window.close()
    
    # graph settings
    def showGraph(self):   

        # load data
        data_cap = load().settings(capture_file, 1)
        data_display = load().settings(display_file, 6)

        # set capture settings
        self.len_ch = int(data_cap[0])

        # set display settings
        self.swipe = int(data_display[0])
        # swipe ( w = t * r ), sendo r = sample rate e t = tempo
        self.zero = float(data_display[1])
        self.vtick = float(data_display[2])
        self.htick = float(data_display[3])
        self.amplitude_start = float(data_display[4])
        self.amplitude_end = float(data_display[5])
        self.amplitude = self.amplitude_end - self.amplitude_start
        self.amplitude_max = self.amplitude * self.len_ch

        self.timer = QtCore.QTimer()

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
        button_play.clicked.connect(self.startTimer)
        proxy_play.setWidget(button_play)
        self.layout.addItem(proxy_play,row=0, colspan = 1)

        proxy_stop = QGraphicsProxyWidget()
        button_stop = QPushButton('Stop Capture')
        button_stop.clicked.connect(self.stopTimer)
        proxy_stop.setWidget(button_stop)
        self.layout.addItem(proxy_stop, row=0, colspan = 1)

        label_configs = pg.LabelItem()
        label_configs.setText("Swipe: " + str(self.swipe) + " | Zero: "+ str(self.zero) + " | Amplitude: "+ str(self.amplitude) +"V | HTick: " + str(self.htick) + " | VTick " + str(self.vtick) + "V | Channels: " + str(self.len_ch))
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
        self.graph.setYRange(0, self.amplitude_max)
        self.graph.showGrid(x=True, y=True, alpha=0.5)
        self.graph.setMenuEnabled(False, 'same')

        # config axis x
        self.axis_x = self.graph.getAxis('bottom')
        self.axis_x.setTickSpacing(self.swipe, self.htick)

        for i in range(self.len_ch):
            self.curve.append(self.graph.plot(self.data[i]))
       
        self.pw.showMaximized()
        # self.startTimer()

    def startTimer(self):
        ser.close()
        ser.open()
        ser.write("start\n")
        ser.flushInput()
        self.num_sig = 0
        self.timer.timeout.connect(self.mainLoop)
        self.timer.start(0)

    def stopTimer(self):
        ser.write("stop\n")
        self.timer.stop()

    def mainLoop(self):
        self.capture()
        self.num_sig += 1
        if (self.num_sig % self.swipe == 0):
            self.curvePlot()
            self.num_sig = 0
        if self.num_sig % int(self.swipe/25) == 0:
            self.plot()

    def capture(self):
        # init serial
        while (ser.inWaiting() == 0):
            pass
        self.num_ch = self.len_ch - 1
        # split string and add data         
        for word in ser.readline().rstrip().split(" "):
            try:
                self.data[self.num_ch][self.num_sig] = (int(word) * const_board) + self.zero
                self.num_ch -= 1
                # debug
                # print (word)
            except:
                pass

        # end

        # init read .txt
        # self.file = open('data/input.txt','r') # open file		

        # for line in self.file:		
        #     self.num_ch = self.len_ch - 1		
        #     #add data 		
        #     for word in line.rstrip().split(" "):		
        #         self.data[self.num_ch][self.num_sig] = (int(word) * const_board) + self.zero
        #         self.num_ch -= 1		

        # end

    def curvePlot(self):
        # clean graph
        self.graph.clear()
        # self.saveLog()
        for i in range(self.len_ch):
            self.curve[i] = self.graph.plot(self.data[i] + ( i * (self.amplitude)))
    
    def plot(self):
        for i in range(self.len_ch):
            self.curve[i].setData((self.data[i] + (i * (self.amplitude))),  pen=pg.mkPen('r', width = 2))

    # decode serial code
    def strToInt(self, word):
        try:
            return int(((ord(word[0]) - 128) << 6 ) + (ord(word[1]) - 128))
        except IndexError:
            return 0

class load():
     # load settings
    def settings(self, type, num_params):
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

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())