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
import sys, imp, thread, time
from GCS import Class_GCS


import datetime
sys.path.append("../../")

from serial_ports import SerialPorts
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
		#self.showMaximized()

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


        self.viewStatAct = QAction('Emg Emulation', self, checkable=True)
        self.viewStatAct.setStatusTip('Emg Emulation')
        self.viewStatAct.setChecked(self.checkableStatus())
        self.viewStatAct.triggered.connect(self.toggleMenu)

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
        self.menuSettings.addAction(self.viewStatAct)
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

        self.actionGestureCaptureSettings.triggered.connect(self.gestureCaptureSettings)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.defaultCapPadrao = '../routine/default.txt'
		#self.defaultCapPadrao = routine
		
        f = open(self.defaultCapPadrao,'r')
        self.linesCap = f.read().splitlines()

	
        self.emgCapPadrao = '../../data/2018-07-11_16-00-00.log'
        f = open(self.emgCapPadrao,'r')
        self.linesEmg = f.read().splitlines()

    def checkableStatus(self):
        settings = open('settingsEE', 'r')
        setCurrent = settings.read().splitlines()
        if setCurrent[0] == "True":
            return True
        else:
            return False

    def toggleMenu(self, state):

        self.defaultEmgPadrao = '../../data/2018-07-11_16-00-00.log'
        if state:
            #fileNames = QFileDialog.getOpenFileNames(None, 'Open file', '.', 'Log (*.log)')[0]
            #for endfile in fileNames: self.defaultCapPadrao = endfile
            settings = open('settingsEE', 'w')
            settings.writelines("True")
            ##MENSAGEM SE ARQUIOVO N CARREGADO
            self.statusbar.show()
        else:
            settings = open('settingsEE', 'w')
            settings.writelines("False")
            self.statusbar.hide()

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
		self.actionGestureCaptureSettings.setText(_translate("MainWindow", "Gesture capture settings", None))

	
    def loadCapture(self):
		fileNames = QFileDialog.getOpenFileNames(None, 'Open file', '.','Log (*.log)')[0]
		for endfile in fileNames: self.defaultCapPadrao = endfile
		f = open(str(self.defaultCapPadrao),'r')
		self.linesCap = f.read().splitlines()
		f.close()

    def saveCapture(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '.','CSV (*.csv)')[0]
        self.tiva.textfile.save(str(fileName))
        #file = open(self.fileName, 'w')
        # text = self.textEdit.toPlainText()
        # file.write(text)
        # file.close()

    def loadEmgsignal(self):
		fileNames = QFileDialog.getOpenFileNames(None, 'Open file', '.','Log (*.log)')[0]
		for endfile in fileNames: self.emgCapPadrao = endfile
		f = open(str(self.emgCapPadrao),'r')
		self.linesEmg = f.read().splitlines()
		f.close()

    def startCapture(self):

        self.tiva = Main(self)

        settingsGCS = open('settingsGCS', 'r')
        setCurrent = settingsGCS.read().splitlines()
        self.device = setCurrent[0]
        self.routine = setCurrent[1]
        self.hand = setCurrent[2]

        try:
            self.defaultCapPadrao = self.routine
            f = open(self.defaultCapPadrao, 'r')
            self.linesCap = f.read().splitlines()
        except:
            print ("ERRO")

        ##########################################################

        settingsEE = open('settingsEE', 'r')
        setCurrent = settingsEE.read().splitlines()
        enable = setCurrent[0]

        # self.tiva = Main(self)
        #self.tiva.showMainWindow()

        self.serialPorts = SerialPorts()

        if setCurrent[0] == 'True':

            self.tiva.showMainWindow()
            try:
                self.tiva.loadData(setCurrent[1])
                tk = tTiva(self.tiva, 'show')
                tk.start()
                self.startDevice()
            except:
                self.tiva.loadData('../../data/2018-07-11_16-00-00.log')
                tk = tTiva(self.tiva, 'show')
                tk.start()
                self.startDevice()
        else:
            if self.serialPorts.list():  # CHECA A PORTA SERIAL

                self.tiva.showMainWindow()
                tk = tTiva(self.tiva, 'start')
                tk.start()
                self.startDevice()
            else:
                self.startDevice()

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
					self.deviceDat[d] = int(atributo[d])
				while k <= 9:
					keyDat[k] = int(atributo[k])

				self.deviceSequence.append(self.deviceDat)
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

    def startDevice(self):
		if (self.device != 'None'):
			self.readCapture()
			global sequence
			modules.start(self, self.tiva, sequence, self.linesEmg, self.device)
		else:
			self.tiva = Main(self)
			self.tiva.showMainWindow()


class tTiva(threading.Thread):
    def __init__(self, tiva, op):
        if op == 'show':
            tiva.showCapture()
        if op == 'start':
            tiva.startCapture()
        threading.Thread.__init__(self)