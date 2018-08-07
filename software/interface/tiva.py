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
from api_tiva import ApiTiva
from win_capture_settings import Ui_CaptureSettingsWindow
from win_display_settings import Ui_DisplaySettingsWindow


class Main(QtGui.QMainWindow): 
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # load data
        self.settings_data = Settings().load()

        # communication serial specifications
        self.ser = serial.Serial()
        self.ser.baudrate = 921600
        self.ser.timeout = 1

        # board TIVA parameters
        vMaxTiva = 3.3
        self.const_ADC = vMaxTiva / (2 ** int(self.settings_data['bitsPerSample']) - 1)

        # time acquisition
        self.t = 0.0

    def showMainWindow(self):

        # set display settings
        self.settings_data['vMin'] = ( int(self.settings_data['vMin'] / self.settings_data['vertTick']) - 1 ) * self.settings_data['vertTick']
        self.settings_data['vMax'] = ( int(self.settings_data['vMax'] / self.settings_data['vertTick']) + 1 ) * self.settings_data['vertTick']
        self.amplitude = self.settings_data['vMax'] - self.settings_data['vMin']
        
        self.amplitude_max = self.amplitude * self.settings_data['showChannels']

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
        label_configs.setText("Swipe: " + str(self.settings_data['swipeSamples']) +
                            " | vMin: "+ str(self.settings_data['vMin']) + "V"+ 
                            " | vMax:  "+ str(self.settings_data['vMax']) + "V" +
                            " | Amplitude: " + str(self.amplitude) + "V" + 
                            " | HTick: " + str(self.settings_data['horizTick']) +
                            " | VTick " + str(self.settings_data['vertTick']) + "V" + 
                            " | Channels: " + str(self.settings_data['showChannels']))
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
        self.axis_y.setTickSpacing(4000, self.settings_data['vertTick'])

        # graph
        self.graph = self.layout.addPlot(axisItems={'left': self.axis_y}, col=0,row=3, colspan=12)
        self.graph.setYRange(0, self.amplitude_max)
        self.graph.showGrid(x=True, y=True, alpha=0.5)
        self.graph.setMenuEnabled(False, 'same')
        self.graph.hideButtons()
        self.graph.setMouseEnabled(False, False)

        # config axis x
        self.axis_x = self.graph.getAxis('bottom')
        self.axis_x.setTickSpacing(self.settings_data['swipeSamples'], self.settings_data['horizTick'])

        # creating curves
        self.curve = []
        self.data_log = []
        self.data = np.zeros(shape=(self.settings_data['showChannels'], self.settings_data['swipeSamples']), dtype=float)
        self.num_sig = 0

        for i in range(self.settings_data['showChannels']):
            self.curve.append(self.graph.plot(self.data[i]))
        self.pw.showMaximized()

    def showCaptureSettings(self):
        self.ui_caps = Ui_CaptureSettingsWindow()
        self.ui_caps.setupUi(self)

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
        self.settings_data = Settings().load()

        self.ui_display = Ui_DisplaySettingsWindow()
        self.ui_display.setupUi(self)

        # set data
        self.ui_display.input_swipe.setText(str(self.settings_data['swipeSamples']))
        self.ui_display.input_vtick.setText(str(self.settings_data['vertTick']))
        self.ui_display.input_htick.setText(str(self.settings_data['horizTick']))
        self.ui_display.input_ch.setText(str(self.settings_data['showChannels']))
        self.ui_display.input_voltMin.setText(str(self.settings_data['vMin']))
        self.ui_display.input_voltMax.setText(str(self.settings_data['vMax']))
        # init actions
        self.ui_display.button_save.clicked.connect(self.storeDisplaySettings)
        self.ui_display.button_cancel.clicked.connect(window.close)
        self.stopCapture()
        window.show()

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

    def onChange(self, newIndex):
        if newIndex == 0:
            self.button_start.setEnabled(True)
            self.button_show.setEnabled(False)
            self.button_file.setEnabled(False)
            self.combobox_serial.setEnabled(True)
        elif newIndex == 1:
            self.button_file.setEnabled(True)
            self.combobox_serial.setEnabled(False)

    def startCapture(self):
        if self.combobox_type.currentText() == "Serial":
            try:
                if self.ser.is_open == False:
                    self.ser.port = self.combobox_serial.currentText()
                    self.ser.open()
                self.apiTiva = ApiTiva(self.ser)
                # log file
                self.log_file = "data/" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".log"
                self.storeLogHeader()
                self.start = True
                self.button_start.setEnabled(False)
                self.button_stop.setEnabled(True)
                self.button_show.setEnabled(True)
                self.data_log = []
                self.apiTiva.start()
                self.timer.start(0)
            except (OSError, serial.SerialException) as err:
                self.showMessage("Error!", str(err))

    def stopCapture(self):
        self.timer.stop()
        try:
            if self.combobox_type.currentText() == "Serial" and self.start == True:
                self.apiTiva.stop()
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

    def showCapture(self):
        self.control = 0
        self.stopCapture()
        self.timer_plot = QtCore.QTimer()
        self.timer_plot.timeout.connect(self.plotLogData)
        self.timer_plot.start(0)
        self.button_show.setEnabled(False)

    def mainLoop(self):
        try:
            self.captureSerial()
            self.plotSerialData()
        except:
            self.stopCapture()

    def captureSerial(self):
        self.packet = self.apiTiva.recvPkt()
        self.data_log.append(self.packet.replace(" ", ";"))

    def plotSerialData(self):
        try:
            num_ch = 0
            for word in self.packet.split(' '):
                self.data[num_ch][self.num_sig] = int(word) * self.const_ADC
                num_ch = (num_ch + 1) % self.settings_data['showChannels']
            self.num_sig += 1

            # update test graph and store data
            if self.num_sig % self.settings_data['swipeSamples'] == 0:
                self.num_sig = 0

            # plot data in graph
            if self.num_sig % int(self.settings_data['swipeSamples'] / 10) == 0:
                for i in range(self.settings_data['showChannels']):
                    self.curve[i].setData(self.data[self.settings_data['showChannels'] - i - 1] - self.settings_data['vMin'] + (self.amplitude * i), pen=pg.mkPen('r', width=1.3))
        except:
            self.showMessage("Error!","")
            self.button_show.setEnabled(True)
            self.timer_plot.stop()

    def plotLogData(self):
        try:
            line = self.data_log[self.control]
            self.control += 1
            num_ch = 0
            time.sleep(1.0/self.settings_data['sampleRate'])
            for word in line.replace(';', ' ').split(' '):
                self.data[num_ch][self.num_sig] = int(word) * self.const_ADC
                num_ch = (num_ch + 1) % self.settings_data['showChannels']
            self.num_sig += 1
            # update test graph and store data
            if self.num_sig % self.settings_data['swipeSamples'] == 0:
                self.num_sig = 0
            # plot data in graph
            if self.num_sig % int(self.settings_data['swipeSamples'] / 10) == 0:
                for i in range(self.settings_data['showChannels']):
                    self.curve[i].setData(self.data[self.settings_data['showChannels'] - i - 1] - self.settings_data['vMin'] +
                                          (self.amplitude * i), pen=pg.mkPen('r', width=1.3))
        except:
            self.showMessage("Warning","No more data to plot.")
            self.button_show.setEnabled(True)
            self.timer_plot.stop()

    def storeDisplaySettings(self):
        flag_err = 1
        try:
            self.settings_data['swipeSamples'] = int(self.ui_display.input_swipe.text())
            check = 1 / self.settings_data['swipeSamples']
        except:
            self.showMessage("Error", "swipeSamples!")
            flag_err = 0
        try:
            self.settings_data['vertTick'] = float(self.ui_display.input_vtick.text())
            check = 1 / self.settings_data['vertTick']
        except:
            self.showMessage("Error", "vertTick!")
            flag_err = 0
        try:
            self.settings_data['horizTick'] = int(self.ui_display.input_htick.text())
            check = 1 / self.settings_data['horizTick']
        except:
            self.showMessage("Error", "horizTick!")
            flag_err = 0
        try:
            self.settings_data['showChannels'] = int(self.ui_display.input_ch.text())
            check = 1 / self.settings_data['horizTick']
        except:
            self.showMessage("Error", "showChannels!")
            flag_err = 0
        try:
            self.settings_data['vMin'] = float(self.ui_display.input_voltMin.text())
        except:
            self.showMessage("Error", "vMin!")
            flag_err = 0
        try:
            self.settings_data['vMax'] = float(self.ui_display.input_voltMax.text())
        except:
            self.showMessage("Error", "vMax!")
            flag_err = 0
        if (self.settings_data['vMax'] < self.settings_data['vMin']):
            self.showMessage("Error", "vMin > vMax!")
            flag_err = 0
        if (flag_err):
            if Settings().store(self.settings_data):
                self.showMainWindow()
                window.close()

    def storeCaptureSettings(self):
        flag_err = 1
        try:
            self.settings_data['sampleRate'] = int(self.ui_caps.input_sampleR.text())
        except:
            self.showMessage("Error", "Sample Rate!")
            flag_err = 0
        try:
            self.settings_data['channelsPerBoard'] = int(self.ui_caps.input_ch.text())
        except:
            self.showMessage("Error", "channelsPerBoard!")
            flag_err = 0
        try:
            self.settings_data['nBoards'] = int(self.ui_caps.input_numofboards.text())
        except:
            self.showMessage("Error", "nBoards!")
            flag_err = 0
        try:
            self.settings_data['bitsPerSample'] = int(self.ui_caps.input_bits.text())
        except:
            self.showMessage("Error", "bitsPerSample!")
            flag_err = 0
        if(flag_err):
            self.settings_data['showChannels'] = int(self.settings_data['channelsPerBoard']) * int(self.settings_data['nBoards'])

            if Settings().store(self.settings_data):
                self.showMainWindow()
                window.close()
    
    def storeLogHeader(self):
        output = open(self.log_file, "a")
        self.settings_data = Settings().load()
        output.write("## File generated by myo_cap software\n" +
                    "## Available from github.com/ddantas/myo_cap\n" +
                    "## Timestamp: 2018-05-23_20-57-32\n" +
                    "##\n" +
                    "## EMG capture settings" +
                    "##\n" +
                    "# sampleRate: "+str(self.settings_data['sampleRate']) + "\n" +
                    "# channelsPerBoard: " + str(self.settings_data['channelsPerBoard']) + "\n"+
                    "# nBoards: " + str(self.settings_data['nBoards']) + "\n" +
                    "# bitsPerSample: " + str(self.settings_data['bitsPerSample']) + "\n" +
                    "##\n" +
                    "## Data\n" +
                    "## t;ch0;ch1;...;ch(channelsPerBoard * nBoards - 1)\n")
        output.close()

    def storeLogData(self):
        output = open(self.log_file, "a")

        for line in self.data_log:
            output.write(str(line))
        output.close()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.showMainWindow()
    sys.exit(app.exec_())
    window.stopCapture()