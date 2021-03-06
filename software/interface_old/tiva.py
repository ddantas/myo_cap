#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import sys
import time
import datetime
import numpy as np
import thread
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QPushButton, QMessageBox, QComboBox, QGraphicsProxyWidget, QLabel,  QInputDialog, QLineEdit, QFileDialog)
from serial.tools import list_ports
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from date_axis_custom import DateAxis
from settings import Settings
from api_tiva import ApiTiva
from display_settings import DisplaySettings
from capture_settings import CaptureSettings
from serial_ports import SerialPorts
from textfile import Textfile

import sys, os

class Main(pg.GraphicsWindow): 
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    def __init__(self, parent=None, **kargs):
        pg.GraphicsWindow.__init__(self, **kargs)
        self.setParent(parent)

        # load data
        self.settings_data = Settings().load()

        # communication serial specifications
        self.ser = serial.Serial()
        self.ser.baudrate = self.settings_data['baudrate']
        self.ser.timeout = 1

        # board TIVA parameters
        vMaxTiva = 3.3
        self.const_ADC = vMaxTiva / (2 ** int(self.settings_data['bitsPerSample']) - 1)

        # time acquisition
        self.t = 0.0

        # init textfile class
        self.textfile = Textfile()

        self.menuFlag = True

        # start
        self.showMainWindow()

    def showDisplaySettings(self):
        self.win_display = DisplaySettings(self)
        self.stopCapture()
        self.win_display.show()

    def showCaptureSettings(self):
        self.win_capture = CaptureSettings(self)
        self.stopCapture()
        self.win_capture.show()

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
        
        self.setWindowTitle('EMG')

        # config layout
        self.layout = self.addLayout()
        
        # config combobox ports
        self.combobox_type = QComboBox()
        self.combobox_type.setEditable(False)
        self.combobox_type.addItem("Serial")      
        self.combobox_type.addItem("File")            
        self.combobox_type.currentIndexChanged.connect(self.onChange)
        proxy_select = QGraphicsProxyWidget()
        proxy_select.setWidget(self.combobox_type)

        # config combobox ports
        self.combobox_serial = QComboBox()
        self.combobox_serial.setEditable(False)
        for port in SerialPorts().list():
            self.combobox_serial.addItem(port)
        proxy_list = QGraphicsProxyWidget()
        proxy_list.setWidget(self.combobox_serial)

        # config file button
        proxy_file = QGraphicsProxyWidget()
        self.button_file = QPushButton("Select File")
        self.button_file.clicked.connect(self.showInputFile)
        proxy_file.setWidget(self.button_file)
        self.button_file.setEnabled(False)

        #config display settings button
        proxy_display_settings = QGraphicsProxyWidget()
        self.button_display_settings = QPushButton('Display Settings')
        self.button_display_settings.clicked.connect(self.showDisplaySettings)
        proxy_display_settings.setWidget(self.button_display_settings)

        # config capture settings button
        proxy_capture_settings = QGraphicsProxyWidget()
        self.button_capture_settings = QPushButton('Capture Settings')
        self.button_capture_settings.clicked.connect(self.showCaptureSettings)
        proxy_capture_settings.setWidget(self.button_capture_settings)

        # config label
        proxy_configs = QGraphicsProxyWidget()
        self.label_configs = QLabel()
        self.label_configs.setText("Swipe: " + str(self.settings_data['swipeSamples']) +
                            " | vMin: " + str(self.settings_data['vMin']) + "V"+
                            " | vMax:  " + str(self.settings_data['vMax']) + "V" +
                            " | HTick: " + str(self.settings_data['horizTick']) +
                            " | VTick " + str(self.settings_data['vertTick']) + "V" + 
                            " | Channels: " + str(self.settings_data['showChannels']))
        self.label_configs.alignment()
        self.label_configs.setAlignment(QtCore.Qt.AlignCenter)
        self.label_configs.setFixedHeight(25)
        self.label_configs.setStyleSheet("background-color:#ffffff;")
        proxy_configs.setWidget(self.label_configs)

        # config start capture button
        proxy_play = QGraphicsProxyWidget()
        self.button_start = QPushButton('Start Capture')
        self.button_start.clicked.connect(self.startCapture)
        self.button_start.setEnabled(True)
        proxy_play.setWidget(self.button_start)

        # config stop capture button
        proxy_show = QGraphicsProxyWidget()
        self.button_show = QPushButton('Show Capture')
        self.button_show.clicked.connect(self.showCapture)
        self.button_show.setEnabled(False)
        proxy_show.setWidget(self.button_show)

        # config stop capture button
        proxy_stop = QGraphicsProxyWidget()
        self.button_stop = QPushButton('Stop Capture')
        self.button_stop.clicked.connect(self.stopCapture)
        self.button_stop.setEnabled(False)
        proxy_stop.setWidget(self.button_stop)

        if(self.menuFlag):
            self.layout.addItem(proxy_select, row=0, colspan=1)
            self.layout.addItem(proxy_list, row=0, colspan=1)
            self.layout.addItem(proxy_file, row=0, colspan=1)
            self.layout.addItem(proxy_display_settings, row=0, colspan=1)
            self.layout.addItem(proxy_capture_settings, row=0, colspan=1)
            self.layout.addItem(proxy_configs, row=0, colspan=4)
            self.layout.addItem(proxy_play, row=0, colspan=1)
            self.layout.addItem(proxy_show, row=0, colspan=1)       
            self.layout.addItem(proxy_stop, row=0, colspan=1)
        else:
            self.layout.addItem(proxy_configs, row=0, colspan=4)
            
        # config axis y 
        self.axis_y = DateAxis(orientation='left')
        self.axis_y.setTickSpacing(4000, self.settings_data['vertTick'])

        # graph
        self.graph = self.addPlot(axisItems={'left': self.axis_y}, col=0,row=3, colspan=12)
        self.graph.setYRange(0, self.amplitude_max)
        self.graph.showGrid(x=True, y=True, alpha=0.2)
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
        self.showMaximized()

    def showInputFile(self):
        self.stopCapture()
        self.timer.stop()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            try:
                self.loadData(fileName)
                self.button_start.setEnabled(False)
                self.button_show.setEnabled(True)
            except:
                self.showMessage("ERROR", "File")

    def startCapture(self):
        if self.combobox_type.currentText() == "Serial":
            try:
                if self.ser.is_open == False:
                    self.ser.port = self.combobox_serial.currentText()
                    self.ser.open()
                self.apiTiva = ApiTiva(self.ser)

                # log file
                self.log_id = self.textfile.init(self.settings_data['showChannels'], "%d;%d;%d;%d", "ch1;ch2;ch3;ch4")
                # self.log_file = "data/" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".log"
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
            self.button_start.setEnabled(True)
            self.button_stop.setEnabled(False)
            if self.combobox_type.currentText() == "Serial" and self.start == True:
                self.apiTiva.stop()
                self.ser.close()
                self.storeLogData()
                self.showMessage("Warning", "Data stored successfully in the file: "+ self.log_file)
                self.start = False
            else:
                self.button_show.setEnabled(True)
                self.timer_plot.stop()
                self.f.close()
        except:
            pass

    def showCapture(self):
        self.control = 0
        self.stopCapture()
        self.num_sig = 0
        # log file
        self.data = np.zeros(shape=(self.settings_data['showChannels'], self.settings_data['swipeSamples']), dtype=float)
        self.timer_plot = QtCore.QTimer()
        self.timer_plot.timeout.connect(self.plotLogData)
        self.timer_plot.start(0)
        self.button_show.setEnabled(False)
        self.button_start.setEnabled(False)
        self.button_stop.setEnabled(True)

    def mainLoop(self):
        try:
            self.captureSerial()
            self.plotSerialData()
        except:
            self.stopCapture()

    def captureSerial(self):
        try:
            self.packet = self.apiTiva.recvPkt(int(self.settings_data['channelsPerBoard']), self.const_ADC)
            self.textfile.log(self.log_id, self.packet)
            self.data_log.append(self.packet)
        except Exception as e:
            print(e)

    def plotSerialData(self):
        try:
            num_ch = 0
            for value in self.packet:
                self.data[num_ch][self.num_sig] = value * self.const_ADC
                num_ch = (num_ch + 1) % self.settings_data['showChannels']
            self.num_sig += 1
            self.plotGraph()
        except:
            self.showMessage("Error!","")
            self.button_show.setEnabled(True)
            self.timer_plot.stop()

    def plotLogData(self):
        try:
            line = self.data_log[self.control]
            # self.textfile.log(self.log_id, line[:-1].split(' '))
            self.control += 1
            num_ch = 0
            time.sleep(1.0/self.settings_data['sampleRate'])

            for word in line:
                self.data[num_ch][self.num_sig] = float(word) * self.const_ADC
                num_ch = (num_ch + 1) % self.settings_data['showChannels']
            self.num_sig += 1
            self.plotGraph()

        except:
            self.control = 0
            self.showMessage("Warning","No more data to plot.")
            self.button_show.setEnabled(True)
            self.button_start.setEnabled(True)
            self.timer_plot.stop()

    def plotGraph(self):
        # update test graph and store data
        if self.num_sig % self.settings_data['swipeSamples'] == 0:
            self.num_sig = 0

        # plot data in graph
        if self.checkSwipe():
            for i in range(self.settings_data['showChannels']):
                self.curve[i].setData(self.data[self.settings_data['showChannels'] - i - 1] - self.settings_data['vMin'] + (self.amplitude * i), pen=pg.mkPen('r', width=0.4))

    def checkSwipe(self):
        return (self.num_sig == 0) or (self.num_sig % 200 == 0) or (self.num_sig + 1 % 200 == 0 and self.num_sig % 200 == self.num_sig % self.settings_data['swipeSamples']) 
        # return (self.num_sig == 0) or (self.num_sig % 200 == 0)

    def storeLogHeader(self):
        self.textfile.message_save("File generated by myo_cap software")
        self.textfile.message_save("Available from github.com/ddantas/myo_cap")
        self.textfile.message_save("Timestamp: "+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        self.textfile.message_save("")
        self.textfile.message_save("EMG capture settings")
        self.textfile.message_save("")
        self.textfile.metadata_save("sampleRate", self.settings_data['sampleRate'])
        self.textfile.metadata_save("channelsPerBoard", self.settings_data['channelsPerBoard'])
        self.textfile.metadata_save("nBoards", self.settings_data['nBoards'])
        self.textfile.metadata_save("bitsPerSample", self.settings_data['bitsPerSample'])

    def storeLogData(self):
        filename = '/data/%s.log' % (datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        self.textfile.save(filename)
        self.showMessage("File stored!", 'File stored at %s' % filename)
        
    def showMessage(self, title, body):
        QMessageBox.about(self, title, body)

    def onChange(self, newIndex):
        if newIndex == 0:
            self.button_start.setEnabled(True)
            self.button_show.setEnabled(False)
            self.button_file.setEnabled(False)
            self.combobox_serial.setEnabled(True)
        elif newIndex == 1:
            self.button_file.setEnabled(True)
            self.combobox_serial.setEnabled(False)

    def loadData(self, file):
        with open(file, 'r') as f:
                for line in f:
                    if line[0] != "#" and line != "":
                        self.data_log.append(line[:-1].replace(";", " ").split(" "))

if __name__ == '__main__':
    w = Main()
    w.show()
    QtGui.QApplication.instance().exec_()
