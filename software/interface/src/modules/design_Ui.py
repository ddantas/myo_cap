

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
import EmgCS_Ui, EmgDS_Ui, EmgEmulation_Ui, GCS_Ui
import sys

import imp

from settings import Settings
from display_settings import DisplaySettings
from capture_settings import CaptureSettings
from tiva import Main

sequence = []
"""
try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig)
"""
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
        
	self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(300, 400, 131, 51))
        self.pushButton.setObjectName("pushButton")
        
	self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(900, 400, 131, 51))
        self.pushButton_2.setObjectName("pushButton")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 200, 1000, 70))

	self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(600, 60, 20, 600))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

	self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(450, 500, 400, 100))

        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
	
	self.label_3.setFont(font)
        self.label_3.setObjectName("label")
	self.label_3.hide()
	self.label_3.setScaledContents(True)

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

	self.defaultCapPadrao = 'routine/default.txt'
	f = open(self.defaultCapPadrao,'r')
    	self.linesCap = f.read().splitlines()

	
	self.emgCapPadrao = 'data/2018-07-11_16-00-00.log' 
	f = open(self.emgCapPadrao,'r')
    	self.linesEmg = f.read().splitlines()
	
    def retranslateUi(self, MainWindow):
	_translate = QtCore.QCoreApplication.translate


        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(_translate("MainWindow", "Iniciar", None))	
	
	self.pushButton_2.setText(_translate("MainWindow", "Iniciar", None))
	self.pushButton_2.clicked.connect(self.startKey)      
	
	self.label.setText(_translate("MainWindow", "Captura via LeapMotion			    Captura via Teclado", None))
        self.label_3.setText(_translate("MainWindow", "", None))
	
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
	print "StartCapture"
    def stopCapture(self):
	print "StopCapture"
    def saveSettings(self):
	print "SaveSettings"
    def loadSettings(self):
	print "LoadSettings"
    def emgCaptureSettings(self):
        self.win_capture = CaptureSettings(self)
        self.win_capture.show()

    def emgDisplaySettings(self):
        self.win_display = DisplaySettings(self)
        self.win_display.show()
	
    def emgEmulation(self):
	self.tiva = Main(self)
	self.tiva.showMainWindow()

    def gestureCaptureSettings(self):
	"""
	t = CaptureSettings()			
	t.show()
	t.exe_()
	"""
    def showCapture(self, ):
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
	self.start()

    def start(self):
	self.readCapture()
	global sequence
	modules.main(sequence, self.linesEmg)

class EmgCaptureSettings(QtWidgets.QMainWindow, EmgCS_Ui.Ui_Dialog):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
"""
class EmgDisplaySettings(QtWidgets.QMainWindow, Ui_DisplaySettingsWindow):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)


    self.settings_data = Settings().load()
    def storeDisplaySettings(self):
		flag_err = 1
		try:
		    self.settings_data['swipeSamples'] = int(self.input_swipe.text())
		    check = 1 / self.settings_data['swipeSamples']
		except:
		    self.showMessage("Error", "swipeSamples!")
		    flag_err = 0
		try:
		    self.settings_data['vertTick'] = int(self.input_vtick.text())
		    check = 1 / self.settings_data['vertTick']
		except:
		    self.showMessage("Error", "vertTick!")
		    flag_err = 0
		try:
		    self.settings_data['horizTick'] = int(self.input_htick.text())
		    check = 1 / self.settings_data['horizTick']
		except:
		    self.showMessage("Error", "horizTick!")
		    flag_err = 0
		try:
		    self.settings_data['showChannels'] = int(self.input_ch.text())
		    check = 1 / self.settings_data['horizTick']
		except:
		    self.showMessage("Error", "showChannels!")
		    flag_err = 0
		try:
		    self.settings_data['vMin'] = float(self.input_voltMin.text())
		except:
		    self.showMessage("Error", "vMin!")
		    flag_err = 0
		try:
		    self.settings_data['vMax'] = float(self.input_voltMax.text())
		except:
		    self.showMessage("Error", "vMax!")
		    flag_err = 0
		if (self.settings_data['vMax'] < self.settings_data['vMin']):
		    self.showMessage("Error", "vMin > vMax!")
		    flag_err = 0
		if (flag_err):
		    if Settings().store(self.settings_data):
		        self.showMainWindow()
		        Ui_DisplaySettingsWindow.close()
    def close (self):
	Ui_DisplaySettingsWindow

    def showMessage(self, title, body):
        QMessageBox.about(self, title, body)

    def showMainWindow(self):

        # set display settings
        self.amplitude = self.settings_data['vMax'] - self.settings_data['vMin']
        self.amplitude_max = self.amplitude * self.settings_data['showChannels']

        self.start = False
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.mainLoop)

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')                
        
        self.pw = pg.GraphicsWindow()
        self.pw.setWindowTitle('EMG')"""    

class EmgEmulation(QtWidgets.QMainWindow, EmgEmulation_Ui.Ui_Dialog):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)


"""
	self.t = EmgDisplaySettings()			


	self.t.input_swipe.setText(str(self.settings_data['swipeSamples']))
        self.t.input_vtick.setText(str(self.settings_data['vertTick']))
        self.t.input_htick.setText(str(self.settings_data['horizTick']))
        self.t.input_ch.setText(str(self.settings_data['showChannels']))
        self.t.input_voltMin.setText(str(self.settings_data['vMin']))
        self.t.input_voltMax.setText(str(self.settings_data['vMax']))
	
        # init actions
        self.t.button_save.clicked.connect(self.t.storeDisplaySettings)
	self.t.button_cancel.clicked.connect(self.t.close)
	self.t.show()
        #QtCore.QObject.connect(self.button_save, QtCore.SIGNAL(_fromUtf8("accepted()")), self.storeDisplaySettings) """       

