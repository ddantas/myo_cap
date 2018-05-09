#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import sys
import time
import datetime
import numpy as np
import pyqtgraph as pg

from pyqtgraph.Qt import QtCore, QtGui
from win_capture_settings import Ui_CaptureSettingsWindow
from win_display_settings import Ui_DisplaySettingsWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import *
from serial.tools import list_ports
from Tkinter import Tk
from tkFileDialog import askopenfilename

# config files
capture_file = "config/capture.config"
display_file = "config/display.config"

# config tiva
t_start = 0
t_end = 3.3
ad = 12
const_board = (t_end - t_start) / (2 ** ad)

# config serial
ser = serial.Serial()
ser.baudrate = 115200
ser.timeout = 1

# class to set axis label
class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        disp_data = load().settings(display_file)
        amplitude_start = float(disp_data[4])
        amplitude_end = float(disp_data[5])
        amplitude = amplitude_end - amplitude_start
        for x in values:
            strns.append((x % amplitude) + (amplitude_start))
        return strns

# class main
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.showMainWindow()

    # show capture settings
    def showCaptureSettings(self):
        self.ui_caps = Ui_CaptureSettingsWindow()
        self.ui_caps.setupUi(self)
        # load capture data
        cap_data = load().settings(capture_file)
        # set capture data
        self.ui_caps.input_sampleR.setText(cap_data[0].strip())
        self.ui_caps.input_ch.setText(cap_data[1].strip())
        self.ui_caps.input_numofboards.setText(cap_data[2].strip())
        self.ui_caps.input_bits.setText(cap_data[3].strip())
        # init actions
        self.ui_caps.button_save.clicked.connect(self.storeCaptureSettings)
        self.ui_caps.button_cancel.clicked.connect(window.close)
        self.stopTimer()
        window.show()

    # store capture settings
    def storeCaptureSettings(self):
        try:
            self.sampleR = int(self.ui_caps.input_sampleR.text())
        except:
            print("ERROR sample rate!")

        cap_file = open(capture_file, "w")
        cap_file.writelines([str(self.sampleR) + "\n", self.ui_caps.input_ch.text() + "\n",
                             self.ui_caps.input_numofboards.text() + "\n", self.ui_caps.input_bits.text()])
        cap_file.close()
        window.close()
        self.data = np.zeros(shape=(self.len_ch, self.swipe), dtype=float)

    # show display settings
    def showDisplaySettings(self):
        #load display data
        disp_data = load().settings(display_file)
        self.ui_display = Ui_DisplaySettingsWindow()
        self.ui_display.setupUi(self)
        # set data
        self.ui_display.input_swipe.setText(disp_data[0].strip())
        self.ui_display.input_zero.setText(disp_data[1].strip())
        self.ui_display.input_vtick.setText(disp_data[2].strip())
        self.ui_display.input_htick.setText(disp_data[3].strip())
        self.ui_display.input_ampS.setText(disp_data[4].strip())
        self.ui_display.input_ampE.setText(disp_data[5].strip())
        # init actions
        self.ui_display.button_save.clicked.connect(self.storeDisplaySettings)
        self.ui_display.button_cancel.clicked.connect(window.close)
        self.stopTimer()
        window.show()

    # store display settings
    def storeDisplaySettings(self):
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

        disp_file = open(display_file,"w")
        disp_file.writelines([str(self.swipe) + "\n", str(self.zero) + "\n", str(self.vtick) +
                           "\n", str(self.htick) +"\n", str(self.ampS) + "\n", str(self.ampE)])
        disp_file.close()
        window.close()
        self.data = np.zeros(shape=(self.len_ch, self.swipe), dtype=float)

    # show message
    def showMessage(self, title, body):
        QMessageBox.about(self, title, body)
 
    # show input file
    def inputFile(self):
        self.timer.stop()
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        self.file = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    
    # store header log emg
    def writeHeader(self):

        output = open(self.log_file, "a")
        output.write("#---------- INFO ----------#\n"+
                    "#\n# Sample Rate: 2000\n"+
                    "# Channel per Board: "+str(self.len_ch)+"\n"+
                    "# Number of Boards: 1\n"+
                    "# Bit per sample: "+str(ad)+"\n#\n"+
                    "#---------- DATA ----------#\n")

        output.close()
        window.close()

    # store data log emg
    def writeData(self):
        output = open(self.log_file, "a")
        for j in range(self.swipe):
            for i in range(self.len_ch):
                if (i < self.len_ch - 1):
                    output.write(str(self.data[i][j] - (self.zero - self.amplitude_start)) + ", ")
                else:
                    output.write(str(self.data[i][j] - (self.zero - self.amplitude_start)) + "\n")
        output.close()
        window.close()
    
    # show main window
    def showMainWindow(self):   

        # load data
        data_cap = load().settings(capture_file)
        data_display = load().settings(display_file)

        # set capture settings
        self.sampleR = int(data_cap[0])
        self.len_ch = int(data_cap[1])

        # set display settings
        self.swipe = int(data_display[0])
        self.zero = float(data_display[1])
        self.vtick = float(data_display[2])
        self.htick = float(data_display[3])
        self.amplitude_start = float(data_display[4])
        self.amplitude_end = float(data_display[5])
        self.amplitude = self.amplitude_end - self.amplitude_start
        self.amplitude_max = self.amplitude * self.len_ch

        self.start = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.mainLoop)

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')                
        
        self.pw = pg.GraphicsWindow()
        self.pw.setWindowTitle('EMG')

        # config layout
        self.layout = self.pw.addLayout()

        # config combobox ports
        self.combobox_type = QComboBox()
        self.combobox_type.setEditable(False)
        self.combobox_type.addItem("Serial")      
        self.combobox_type.addItem("File")            
        self.combobox_type.currentIndexChanged.connect(self.onChange)
        proxy_list = QGraphicsProxyWidget()
        proxy_list.setWidget(self.combobox_type)
        self.layout.addItem(proxy_list, row=0, colspan=1)

        # config combobox ports
        self.combobox_serial = QComboBox()
        self.combobox_serial.setEditable(False)
        for port in list_ports.comports():
            self.combobox_serial.addItem(port[0])
        proxy_list = QGraphicsProxyWidget()
        proxy_list.setWidget(self.combobox_serial)
        self.layout.addItem(proxy_list, row=0, colspan=1)

        # config file button
        proxy_file = QGraphicsProxyWidget()
        self.button_file = QPushButton("Select File")
        self.button_file.clicked.connect(self.inputFile)
        proxy_file.setWidget(self.button_file)
        self.button_file.setEnabled(False)
        self.layout.addItem(proxy_file, row=0, colspan=1)

        # config start capture button
        proxy_play = QGraphicsProxyWidget()
        self.button_play = QPushButton('Start Capture')
        self.button_play.clicked.connect(self.startTimer)
        proxy_play.setWidget(self.button_play)
        self.layout.addItem(proxy_play, row=0, colspan=1)

        # config stop capture button
        proxy_stop = QGraphicsProxyWidget()
        self.button_stop = QPushButton('Stop Capture')
        self.button_stop.clicked.connect(self.stopTimer)
        self.button_stop.setEnabled(False)
        proxy_stop.setWidget(self.button_stop)
        self.layout.addItem(proxy_stop, row=0, colspan=1)

        # config label
        label_configs = pg.LabelItem()
        label_configs.setText("Swipe: " + str(self.swipe) + " | Zero: " + str(self.zero) + " | Amplitude: " +
                              str(self.amplitude) + "V | HTick: " + str(self.htick) + " | VTick " + str(self.vtick) +
                              "V | Channels: " + str(self.len_ch))
        self.layout.addItem(label_configs, row=0, colspan=2)

        #config display settings button
        proxy_settings = QGraphicsProxyWidget()
        button_settings = QPushButton('Display Settings')
        button_settings.clicked.connect(self.showDisplaySettings)
        proxy_settings.setWidget(button_settings)
        self.layout.addItem(proxy_settings, row=0, colspan=1)

        # config capture settings button
        proxy_settings2 = QGraphicsProxyWidget()
        button_settings2 = QPushButton('Capture Settings')
        button_settings2.clicked.connect(self.showCaptureSettings)
        proxy_settings2.setWidget(button_settings2)
        self.layout.addItem(proxy_settings2, row=0, colspan=1)

        # config axis y 
        self.axis_y = DateAxis(orientation='left')
        self.axis_y.setTickSpacing(4000, self.vtick)

        # graph
        self.graph = self.layout.addPlot(axisItems={'left': self.axis_y}, col=0,row=3, colspan=9)
        self.graph.setYRange(0, self.amplitude_max)
        self.graph.showGrid(x=True, y=True, alpha=0.5)
        self.graph.setMenuEnabled(False, 'same')
        self.graph.hideButtons()
        self.graph.setMouseEnabled(False, False)

        # config axis x
        self.axis_x = self.graph.getAxis('bottom')
        self.axis_x.setTickSpacing(self.swipe, self.htick)

        # creating curves
        self.curve = []
        self.data = np.zeros(shape=(self.len_ch, self.swipe), dtype=float)
        for i in range(self.len_ch):
            self.curve.append(self.graph.plot(self.data[i]))
        self.pw.showMaximized()
        self.num_sig = 0

    # on change combo box type
    def onChange(self, newIndex):
        if newIndex == 0:
            self.button_file.setEnabled(False)
            self.combobox_serial.setEnabled(True)
        elif newIndex == 1:
            self.button_file.setEnabled(True)
            self.combobox_serial.setEnabled(False)

    # start capture
    def startTimer(self):
        if(self.combobox_type.currentText() == "Serial"):
            try:
                if ser.is_open == False:
                    ser.port = self.combobox_serial.currentText()
                    ser.open()

                # log file
                self.log_file = "data/" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".log"
                self.writeHeader()
                ser.write("start\n")
                self.start = 1
            except (OSError, serial.SerialException):
                self.showMessage("ERROR", "Serial")
        else:
            self.f = open(self.file, 'r')

        self.button_play.setEnabled(False)
        self.button_stop.setEnabled(True)
        self.timer.start(0)

    # stop capture
    def stopTimer(self):
        self.timer.stop()
        try:
            if(self.combobox_type.currentText() == "Serial" and self.start):
                ser.write("stop\n")
                ser.close()
                self.showMessage("Log", "Stored data.\nfile: "+ self.log_file)
                self.start = 0
            else:
                self.f.close()
            self.button_play.setEnabled(True)
            self.button_stop.setEnabled(False)
        except:
            pass

    # plot data emg 
    def mainLoop(self):
        try:
            if(self.combobox_type.currentText() == "Serial"):
                self.captureSerial()
            else:
                self.captureLog()
            self.plot()
        except:
            pass

    # capture serial data
    def captureSerial(self):
        # waiting serial data
        while ser.inWaiting() == 0:
            pass

        # split string and add data
        packet = ser.readline()
        num_ch = 0
        for word in packet[:-1].split():
            self.data[num_ch][self.num_sig] = (int(word) * const_board) + self.zero - self.amplitude_start
            num_ch = (num_ch + 1) % self.len_ch

        self.num_sig += 1

    # capture log data
    def captureLog(self):
        time.sleep(1.0/self.sampleR)
        line = self.f.readline()
        if line == '':
            self.f.seek(0)

        if(line[0] != "#"):
            #add data
            num_ch = 0
            for word in line.rstrip().split(","):
                self.data[num_ch][self.num_sig] = float(word) + self.zero - self.amplitude_start
                num_ch = (num_ch + 1) % self.len_ch
            self.num_sig += 1

    # plot data on graph
    def plot(self):
        # update test graph and store data
        if self.num_sig % self.swipe == 0:
            self.num_sig = 0
            if(self.combobox_type.currentText() == "Serial"):
                self.writeData()

        # plot data in graph
        if self.num_sig % int(self.swipe / 10) == 0:
            for i in range(self.len_ch):
                self.curve[i].setData(self.data[i] + (self.amplitude * i), pen=pg.mkPen('r', width=2))

# class to load settings
class load():
    def settings(self, type):
        try:
            output = open(type, "r")
            data = output.readlines()
            return data
        except IOError:
            if(type == capture_file): data = [2000, 4, 1, 12]
            else: data = [1000, 0.0, 1.0, 100.0, -2.0, 2.0]
            return data

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())
    self.stopTimer()