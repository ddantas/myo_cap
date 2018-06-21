#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import sys
import time
import datetime
import numpy as np
import thread
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QPushButton, QMessageBox, QComboBox, QGraphicsProxyWidget)
from serial.tools import list_ports
from Tkinter import Tk
from tkFileDialog import askopenfilename
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from date_axis_custom import DateAxis
from settings import Settings
from win_capture_settings import Ui_CaptureSettingsWindow
from win_display_settings import Ui_DisplaySettingsWindow


class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ser = serial.Serial()
        self.ser.baudrate = 115200
        self.ser.timeout = 1

    def showMainWindow(self):

        # load data
        settings_data = Settings().load()

        # set capture settings
        self.sampleR = int(settings_data['sampleRate'])

        # set display settings
        self.swipe = int(settings_data['swipeSamples'])
        self.vtick = float(settings_data['vertTick'])
        self.htick = float(settings_data['horizTick'])
        self.amplitude_start = float(settings_data['vMin'])
        self.amplitude_end = float(settings_data['vMax'])
        self.len_ch = int(settings_data['showChannels'])
        self.amplitude = self.amplitude_end - self.amplitude_start
        self.amplitude_max = self.amplitude * self.len_ch
        self.zero = (self.amplitude_end - self.amplitude_start) / (2 ** 12)

        self.start = False
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
        self.button_file.clicked.connect(self.showInputFile)
        proxy_file.setWidget(self.button_file)
        self.button_file.setEnabled(False)
        self.layout.addItem(proxy_file, row=0, colspan=1)

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

        # config label
        label_configs = pg.LabelItem()
        label_configs.setText("Swipe: " + str(self.swipe) + " | Amplitude: " +
                              str(self.amplitude) + "V | HTick: " + str(self.htick) + " | VTick " + str(self.vtick) +
                              "V | Channels: " + str(self.len_ch))
        self.layout.addItem(label_configs, row=0, colspan=4)

        # config start capture button
        proxy_play = QGraphicsProxyWidget()
        self.button_start = QPushButton('Start Capture')
        self.button_start.clicked.connect(self.startCapture)
        self.button_start.setEnabled(True)
        proxy_play.setWidget(self.button_start)
        self.layout.addItem(proxy_play, row=0, colspan=1)

        # config stop capture button
        proxy_stop = QGraphicsProxyWidget()
        self.button_show = QPushButton('Show Capture')
        self.button_show.clicked.connect(self.showCapture)
        self.button_show.setEnabled(False)
        proxy_stop.setWidget(self.button_show)
        self.layout.addItem(proxy_stop, row=0, colspan=1)

        # config stop capture button
        proxy_stop = QGraphicsProxyWidget()
        self.button_stop = QPushButton('Stop Capture')
        self.button_stop.clicked.connect(self.stopCapture)
        self.button_stop.setEnabled(False)
        proxy_stop.setWidget(self.button_stop)
        self.layout.addItem(proxy_stop, row=0, colspan=1)

        # config axis y 
        self.axis_y = DateAxis(orientation='left')
        self.axis_y.setTickSpacing(4000, self.vtick)

        # graph
        self.graph = self.layout.addPlot(axisItems={'left': self.axis_y}, col=0,row=3, colspan=12)
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

        self.data_log = []

        for i in range(self.len_ch):
            self.curve.append(self.graph.plot(self.data[i]))
        self.pw.showMaximized()
        self.num_sig = 0

    def startCapture(self):
        if(self.combobox_type.currentText() == "Serial"):
            try:
                if self.ser.is_open == False:
                    self.ser.port = self.combobox_serial.currentText()
                    self.ser.open()

                # log file
                self.log_file = "data/" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".log"
                self.storeLogHeader()
                self.ser.write("start\n")
                self.start = True
                self.button_start.setEnabled(False)
                self.button_stop.setEnabled(True)
                self.button_show.setEnabled(True)
                self.timer.start(0)
            except (OSError, serial.SerialException) as err:
                self.showMessage("Error!", str(err))

    def stopCapture(self):
        self.timer.stop()
        try:
            if(self.combobox_type.currentText() == "Serial" and self.start == True):
                self.ser.write("stop\n")
                self.ser.close()
                self.storeLogData()
                self.showMessage("Warning", "Data stored successfully in the file: "+ self.log_file)
                self.start = False
            else:
                self.f.close()
            self.button_start.setEnabled(True)
            self.button_stop.setEnabled(False)
        except:
            pass

    def mainLoop(self):
        try:
            self.captureSerial()
        except:
            pass

    def captureSerial(self):
        # waiting serial data
        while self.ser.inWaiting() == 0:
            pass

        self.data_log.append(self.ser.readline())
           
    def showCapture(self):
        self.control = 0
        self.timer_plot = QtCore.QTimer()
        self.timer_plot.timeout.connect(self.plot)
        self.timer_plot.start(0)
        self.button_show.setEnabled(False)

    def plot(self):
        try:
            line = self.data_log[self.control]
            self.control += 1
            num_ch = 0
            time.sleep(1.0/self.sampleR)
            for word in line.rstrip().split():
                self.data[num_ch][self.num_sig] = float(word) 
                num_ch = (num_ch + 1) % self.len_ch
            self.num_sig += 1
            # update test graph and store data
            if self.num_sig % self.swipe == 0:
                self.num_sig = 0
            # plot data in graph
            if self.num_sig % int(self.swipe / 10) == 0:
                for i in range(self.len_ch):
                    self.curve[i].setData((self.data[self.len_ch - i - 1] * self.zero) - self.amplitude_start + (self.amplitude * i), pen=pg.mkPen('r', width=2))       
        except:
            self.showMessage("Warning","No more data to plot.")
            self.button_show.setEnabled(True)
            self.timer_plot.stop()

    def showCaptureSettings(self):
        self.ui_caps = Ui_CaptureSettingsWindow()
        self.ui_caps.setupUi(self)
        self.settings_data = Settings().load()
        # set capture data
        self.ui_caps.input_sampleR.setText(str(self.settings_data['sampleRate']))
        self.ui_caps.input_ch.setText(str(self.settings_data['channelsPerBoard']))
        self.ui_caps.input_numofboards.setText(str(self.settings_data['nBoards']))
        self.ui_caps.input_bits.setText(str(self.settings_data['bitsPerSample']))
        # init actions
        self.ui_caps.button_save.clicked.connect(self.storeCaptureSettings)
        self.ui_caps.button_cancel.clicked.connect(window.close)
        self.stopCapture()
        window.show()

    def showDisplaySettings(self):

        self.ui_display = Ui_DisplaySettingsWindow()
        self.ui_display.setupUi(self)
        self.settings_data = Settings().load()

        # set data
        self.ui_display.input_swipe.setText(str(self.settings_data['swipeSamples']).replace(".0", ""))
        self.ui_display.input_vtick.setText(str(self.settings_data['vertTick']))
        self.ui_display.input_htick.setText(str(self.settings_data['horizTick']))
        self.ui_display.input_ch.setText(str(self.settings_data['showChannels']).replace(".0", ""))
        self.ui_display.input_voltMin.setText(str(self.settings_data['vMin']))
        self.ui_display.input_voltMax.setText(str(self.settings_data['vMax']))
        # init actions
        self.ui_display.button_save.clicked.connect(self.storeDisplaySettings)
        self.ui_display.button_cancel.clicked.connect(window.close)
        self.stopCapture()
        window.show()

    def storeDisplaySettings(self):
        try:
            self.settings_data['swipeSamples'] = int(self.ui_display.input_swipe.text())
            check = 1 / self.swipe
        except:
            self.settings_data['swipeSamples'] = 1000
            print("ERROR swipeSamples!")
        try:
            self.settings_data['vertTick'] = float(self.ui_display.input_vtick.text())
            check = 1 / self.vtick
        except:
            self.settings_data['vertTick'] = 1.0
            print("ERROR vtick!")
        try:
            self.settings_data['horizTick'] = float(self.ui_display.input_htick.text())
            check = 1 / self.htick
        except:
            self.settings_data['horizTick'] = 100.0
            print("ERROR htick!")
        try:
            self.settings_data['showChannels'] = int(self.ui_display.input_ch.text())
            check = 1 / self.htick
        except:
            self.settings_data['showChannels'] = 4
            print("ERROR showChannels!")
        try:
            self.settings_data['vMin'] = float(self.ui_display.input_voltMin.text())
        except:
            self.settings_data['vMin'] = -2.0
            print("ERROR vMin!")
        try:
            self.settings_data['vMax'] = float(self.ui_display.input_voltMax.text())
        except:
            self.settings_data['vMax'] = 2.0
            print("ERROR vMax!")

        if(Settings().store(self.settings_data)):
            self.showMainWindow()
            window.close()

    def storeCaptureSettings(self):
        try:
            self.settings_data['sampleRate'] = int(self.ui_caps.input_sampleR.text())
        except:
            print("ERROR sample rate!")
        try:
            self.settings_data['channelsPerBoard'] = int(self.ui_caps.input_ch.text())
        except:
            print("ERROR channelsPerBoard!")
        try:
            self.settings_data['nBoards'] = int(self.ui_caps.input_numofboards.text())
        except:
            print("ERROR nBoards!")
        try:
            self.settings_data['bitsPerSample'] = int(self.ui_caps.input_bits.text())
        except:
            print("ERROR bitsPerSample!")
            
        if(Settings().store(self.settings_data)):
            self.showMainWindow()
            window.close()

    def showMessage(self, title, body):
        QMessageBox.about(self, title, body)
 
    def showInputFile(self):
        self.stopCapture()
        self.timer.stop()
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        self.file = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        try:
            with open(self.file, 'r') as f:
                for line in f:
                    if line[0] != "#" and line != "":
                        self.data_log.append(line)
            self.button_start.setEnabled(False)
            self.button_show.setEnabled(True)
        except:
            self.showMessage("ERROR", "File")
    
    def storeLogHeader(self):
        output = open(self.log_file, "a")
        self.settings_data = Settings().load()
        output.write("## File generated by myo_cap software\n"+
                    "## Available from github.com/ddantas/myo_cap\n"+
                    "## Timestamp: 2018-05-23_20-57-32\n"+
                    "##\n"+
                    "## EMG capture settings"+
                    "##\n"+
                    "# sampleRate: "+str(self.settings_data['sampleRate'])+"\n"+
                    "# channelsPerBoard: "+str(self.settings_data['channelsPerBoard'])+"\n"+
                    "# nBoards: "+str(self.settings_data['nBoards'])+"\n"+
                    "# bitsPerSample: "+str(self.settings_data['bitsPerSample'])+"\n"+
                    "##\n"+
                    "## Data\n"+
                    "## t; ch0; ch1; ch2; ch3\n")
        output.close()

    def storeLogData(self):
        output = open(self.log_file, "a")
        for line in self.data_log:
            output.write(str(line))
        output.close()

    def onChange(self, newIndex):
        if newIndex == 0:
            self.button_start.setEnabled(True)
            self.button_show.setEnabled(False)
            self.button_file.setEnabled(False)
            self.combobox_serial.setEnabled(True)
        elif newIndex == 1:
            self.button_file.setEnabled(True)
            self.combobox_serial.setEnabled(False)

    def clearGraph(self):
        self.data = np.zeros(shape=(self.len_ch, self.swipe), dtype=float)
        self.num_sig = 0

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.showMainWindow()
    sys.exit(app.exec_())
    window.stopCapture()