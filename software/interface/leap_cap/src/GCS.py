import sys
try:
    from PyQt5 import QtCore, QtWidgets, QtTest, Pyqr, QtGui
    from PyQt5.QtWidgets import *
    from PyQt5.QtWidgets import *

except ImportError:
    from PyQt5 import QtCore, QtWidgets, QtTest, QtGui
    from PyQt5.QtWidgets import *
from win_GCS import Ui_Dialog
from pyqtgraph.Qt import QtCore, QtGui

settings = open('settingsGCS', 'r')
setCurrent = settings.read().splitlines()
device = setCurrent[0]
routine = setCurrent[1]
hand = setCurrent[2]


class Class_GCS(QtGui.QMainWindow): 
    def __init__(self, parent=None):
		super(Class_GCS, self).__init__(parent)
		self.ui_caps = Ui_Dialog()
		self.ui_caps.setupUi(self)
		self.ui_caps.comboBox.setEditable(False)

		if device == 'None':
			self.ui_caps.comboBox.addItem("None")
			self.ui_caps.comboBox.addItem("Leap Motion")
			self.ui_caps.comboBox.addItem("Keyboard")
		if device == 'Leap Motion':
			self.ui_caps.comboBox.addItem("Leap Motion")
			self.ui_caps.comboBox.addItem("Keyboard")
			self.ui_caps.comboBox.addItem("None")
		if device == 'Keyboard':
			self.ui_caps.comboBox.addItem("Keyboard")
			self.ui_caps.comboBox.addItem("Leap Motion")
			self.ui_caps.comboBox.addItem("None")

		self.defaultCapPadrao = '../routine/default.txt'
	
		if hand == 'Left':
			self.ui_caps.radioButton.setChecked(True)
		if hand == 'Right':
			self.ui_caps.radioButton_2.setChecked(True)

	#self.ui_caps.comboBox.currentIndexChanged.connect()
		self.ui_caps.pushButton.clicked.connect(self.loadRoutine)
		self.ui_caps.buttonBox.accepted.connect(self.storeGCS)
		self.ui_caps.buttonBox.rejected.connect(self.close)

    def storeGCS(self):
		settings = open('settingsGCS', 'w')
		setCurrent = []

		print self.ui_caps.comboBox.currentText()
		setCurrent.append(self.ui_caps.comboBox.currentText()+'\n')

		setCurrent.append(self.defaultCapPadrao+'\n')
		if self.ui_caps.radioButton.isChecked():
			setCurrent.append("Left\n")
			print ("Left")
		elif self.ui_caps.radioButton_2.isChecked():
			setCurrent.append("Right\n")
			print ("Right")

		#setCurrent.append(self.routine)
		settings.writelines(setCurrent)
		settings.close()
		self.close()

    def loadRoutine(self):
		fileNames = QFileDialog.getOpenFileNames(None, 'Open file', '.','TXT (*.txt)')[0]
		for endfile in fileNames: self.defaultCapPadrao = endfile
		endfile = endfile.split('/')
		nameroutine = endfile[len(endfile) - 1]
		nameroutine = nameroutine[0:len(nameroutine)-4]
		self.ui_caps.label_4.setText(nameroutine)


