try:
    from PyQt5 import QtCore, QtWidgets, QtTest, Pyqr, QtGui
    from PyQt5.QtWidgets import *
    from PyQt5.QtWidgets import *

except ImportError:
    from PyQt5 import QtCore, QtWidgets, QtTest, QtGui
    from PyQt5.QtWidgets import *

from datetime import datetime
import threading
import converter, modules
#import EmgEmulation_Ui
import sys
import imp
from GCS import Class_GCS
from EmgEmulation import Class_EMG

sys.path.append("../../")

from settings import Settings
from display_settings import DisplaySettings
from capture_settings import CaptureSettings

from win_display_settings import Ui_DisplaySettingsWindow

from tiva import Main
sequence = []

class Infor(object):
	def set_img(info, img):
    		info.img = img
	def set_temp(info, temp):
		info.temp = temp

class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
	
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 640)
	self.showMaximized()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 25))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)        
	self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
	

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
       
        self.menuCapture = QtWidgets.QMenu(self.menubar)
        self.menuCapture.setObjectName("menuCapture")
        MainWindow.setMenuBar(self.menubar)

        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionLoadcapture = QtWidgets.QAction(MainWindow)
        self.actionLoadcapture.setObjectName("actionLoadcapture")        
        self.actionSavecapture = QtWidgets.QAction(MainWindow)
        self.actionSavecapture.setObjectName("actionSavecapture")        
        self.actionLoademgsignal = QtWidgets.QAction(MainWindow)
        self.actionLoademgsignal.setObjectName("actionLoademgsignal")        

	self.actionStartCapture = QtWidgets.QAction(MainWindow)
        self.actionStartCapture.setObjectName("actionStartCapture")
        self.actionStopCapture = QtWidgets.QAction(MainWindow)
        self.actionStopCapture.setObjectName("actionStopCapture")
	self.actionShowCapture = QtWidgets.QAction(MainWindow)
        self.actionShowCapture.setObjectName("actionShowCapture")	

	self.actionLoadSettings = QtWidgets.QAction(MainWindow)
        self.actionLoadSettings.setObjectName("actionLoadSettings")	
	self.actionSaveSettings = QtWidgets.QAction(MainWindow)
        self.actionSaveSettings.setObjectName("actionSaveSettings")

	self.actionEmgCaptureSettings = QtWidgets.QAction(MainWindow)
        self.actionEmgCaptureSettings.setObjectName("actionEmgCaptureSettings")
	self.actionEmgDisplaySettings = QtWidgets.QAction(MainWindow)
        self.actionEmgDisplaySettings.setObjectName("actionEmgDisplaySettings")	
	self.actionEmgEmulation = QtWidgets.QAction(MainWindow)
        self.actionEmgEmulation.setObjectName("actionEmgEmulation")
	self.actionGestureCaptureSettings = QtWidgets.QAction(MainWindow)
        self.actionGestureCaptureSettings.setObjectName("GestureCaptureSettings")

	
        self.menuFile.addAction(self.actionLoadcapture)	
	self.menuFile.addAction(self.actionSavecapture)	
	self.menuFile.addAction(self.actionLoademgsignal)	

	self.menuCapture.addAction(self.actionStartCapture)	
	self.menuCapture.addAction(self.actionStopCapture)		
	self.menuCapture.addAction(self.actionShowCapture)
	
	self.menuSettings.addAction(self.actionLoadSettings)
	self.menuSettings.addAction(self.actionSaveSettings)
	self.menuSettings.addSeparator()	
	self.menuSettings.addAction(self.actionEmgCaptureSettings)
	self.menuSettings.addAction(self.actionEmgDisplaySettings)
	self.menuSettings.addAction(self.actionEmgEmulation)
	self.menuSettings.addAction(self.actionGestureCaptureSettings)
	


        
        self.menubar.addAction(self.menuFile.menuAction())
        MainWindow.setCentralWidget(self.centralwidget)        

	self.menubar.addAction(self.menuCapture.menuAction())
        MainWindow.setCentralWidget(self.centralwidget)	

	self.menubar.addAction(self.menuSettings.menuAction())
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

	
	self.actionLoadcapture.triggered.connect(self.loadCapture)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)	

	self.actionSavecapture.triggered.connect(self.saveCapture)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)	

	self.actionLoademgsignal.triggered.connect(self.loadEmgsignal)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)	

	self.actionStartCapture.triggered.connect(self.startCapture)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)	

	self.actionStopCapture.triggered.connect(self.stopCapture)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

	self.actionShowCapture.triggered.connect(self.showCapture)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
	
	self.actionLoadSettings.triggered.connect(self.loadSettings)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

	self.actionSaveSettings.triggered.connect(self.saveSettings)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


	self.actionEmgCaptureSettings.triggered.connect(self.emgCaptureSettings)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

	self.actionEmgDisplaySettings.triggered.connect(self.emgDisplaySettings)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


	self.actionEmgEmulation.triggered.connect(self.emgEmulation)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

	self.actionGestureCaptureSettings.triggered.connect(self.gestureCaptureSettings)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

	self.defaultCapPadrao = '../routine/default.txt'
	#self.defaultCapPadrao = routine
		
	f = open(self.defaultCapPadrao,'r')
    	self.linesCap = f.read().splitlines()

	
	self.emgCapPadrao = '../../data/2018-07-11_16-00-00.log' 
	f = open(self.emgCapPadrao,'r')
    	self.linesEmg = f.read().splitlines()

	
    def retranslateUi(self, MainWindow):
	_translate = QtCore.QCoreApplication.translate

	self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionLoadcapture.setText(_translate("MainWindow", "Load capture", None))
	self.actionSavecapture.setText(_translate("MainWindow", "Save capture", None))
	self.actionLoademgsignal.setText(_translate("MainWindow", "Load EMG signal", None))

	self.menuCapture.setTitle(_translate("MainWindow", "Capture", None))
        self.actionStartCapture.setText(_translate("MainWindow", "Start Capture", None))
	self.actionStopCapture.setText(_translate("MainWindow", "Stop Capture", None))
	self.actionShowCapture.setText(_translate("MainWindow", "Show Capture", None))
	
	self.menuSettings.setTitle(_translate("MainWindow", "Settings", None))
        self.actionLoadSettings.setText(_translate("MainWindow", "Load settings", None))
	self.actionSaveSettings.setText(_translate("MainWindow", "Save settings", None))

	self.actionEmgCaptureSettings.setText(_translate("MainWindow", "EMG capture settings", None))
	self.actionEmgDisplaySettings.setText(_translate("MainWindow", "EMG display settings", None))
	self.actionEmgEmulation.setText(_translate("MainWindow", "EMG emulation", None))
	self.actionGestureCaptureSettings.setText(_translate("MainWindow", "Gesture capture settings", None))

	
    def loadCapture(self):
	
	fileNames = QFileDialog.getOpenFileNames(None, 'Open file', '.','Log (*.log)')[0]
	for endfile in fileNames: self.defaultCapPadrao = endfile
	f = open(str(self.defaultCapPadrao),'r')
	self.linesCap = f.read().splitlines()
	f.close()    

    def saveCapture(self):
	print "SalveCapture"

    def loadEmgsignal(self):
	fileNames = QFileDialog.getOpenFileNames(None, 'Open file', '.','Log (*.log)')[0]
	for endfile in fileNames: self.emgCapPadrao = endfile
	f = open(str(self.emgCapPadrao),'r')
	self.linesEmg = f.read().splitlines()
	f.close()    

    def startCapture(self):	
	self.tiva = Main(self)
	self.tiva.showMainWindow()
	self.start()

    def stopCapture(self):
	print "StopCapture"

    def saveSettings(self):
	print "SaveSettings"

    def loadSettings(self):
	print "LoadSettings"

    def emgCaptureSettings(self):
        self.win_capture = CaptureSettings(self)
        self.stopCapture()
        self.win_capture.show()

    def emgDisplaySettings(self):
        self.win_display = DisplaySettings(self)
        self.stopCapture()
        self.win_display.show()
	
    def emgEmulation(self):
	self.win_EMG = Class_EMG(self)
        self.stopCapture()
        self.win_EMG.show()

    def gestureCaptureSettings(self):
	self.win_GCS = Class_GCS(self)
        self.stopCapture()
        self.win_GCS.show()

    def showCapture(self):
	global sequence
	for line in self.linesCap: 
		if len(line) != 0 and line[0]!='#':	
			atributo = line.split(';')
			d = 0
			k = 5			
			while d <= 4:
				deviceDat[d] = int(atributo[d])
				print deviceDar[d]+";"	
			while k <= 9:
				keyDat[k] = int(atributo[k])
				print keyDat[k] + ";"
 		
			self.deviceSequence.append(deviceDat)
			self.keySequence.append(keyDat)

    def readCapture(self):
	global sequence
	for line in self.linesCap: 
		if len(line) != 0 and line[0]!='#':	
			atributo = line.split(';')
			imagem = str(atributo[0])
			temp = int(atributo[1])
			
			l = Infor()
			Infor.set_img(l, imagem)

			#converter.pattern("../images/"+imagem+".png","../images/"+imagem+".png")			
			#converter.gray_scale("../images/"+imagem+".png","../images/"+imagem+"EC.png")

			Infor.set_temp(l, temp)
			sequence.append(l)
    def startLeap(self):
	self.start()

    def startKey(self):		
	self.readCapture()
	global sequence
	modules.main(sequence, self.linesEmg)

    def start(self):
	settingsGCS = open('settingsGCS', 'r')
	setCurrent = settingsGCS.read().splitlines()
	device = setCurrent[0]	
	routine = setCurrent[1]
	hand = setCurrent[2]

	try:
		self.defaultCapPadrao = device		
		self.linesCap = f.read().splitlines()
		f.close()
	except:
		print ("ERRO")
	
###########################################################################

	settingsEE = open('settingsEE', 'r')
	setCurrent = settingsEE.read().splitlines()
	if setCurrent[0] == 'TRUE':
		print setCurrent[1]
		self.tiva.loadData(setCurrent[1])
		self.tiva.showCapture()
	else:
		self.tiva.startCapture()

	if device == 'Keyboard':
		self.startKey()
	if device == 'Leap Motion':
		self.startLeap()
	if device != 'Keyboard' and device != 'Leap Motion':
		print ("Not found")

