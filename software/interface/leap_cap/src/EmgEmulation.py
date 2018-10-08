import sys
try:
    from PyQt5 import QtCore, QtWidgets, QtTest, Pyqr, QtGui
    from PyQt5.QtWidgets import *
    from PyQt5.QtWidgets import *

except ImportError:
    from PyQt5 import QtCore, QtWidgets, QtTest, QtGui
    from PyQt5.QtWidgets import *
from Ui_EEmulation import Ui_Dialog
from pyqtgraph.Qt import QtCore, QtGui

settings = open('settingsEE', 'r')
setCurrent = settings.read().splitlines()
check = setCurrent[0]

class Class_EMG(QtGui.QMainWindow): 
    def __init__(self, parent=None):
        super(Class_EMG, self).__init__(parent)
	self.ui_caps = Ui_Dialog()
        self.ui_caps.setupUi(self)
	self.defaultEmgPadrao = '../../data/2018-07-11_16-00-00.log'
	
	if check == 'True':
		self.ui_caps.checkBox.setChecked(True)
	self.ui_caps.checkBox.stateChanged.connect(self.clickBox)
	#self.ui_caps.pushButton.clicked.connect(self.loadRoutine)
	self.ui_caps.buttonBox.accepted.connect(self.save)
        self.ui_caps.buttonBox.rejected.connect(self.close)

    def save(self):
	settings = open('settingsEE', 'w')
	setCurrent = []
	if self.ui_caps.checkBox.isChecked():
		setCurrent.append('True\n')
		setCurrent.append(self.defaultCapPadrao)
	else :
		setCurrent.append('False')

	settings.writelines(setCurrent)
	settings.close()
	self.close()

    def clickBox(self, state):
        if state == QtCore.Qt.Checked:
		fileNames = QFileDialog.getOpenFileNames(None, 'Open file', '.','Log (*.log)')[0]
		for endfile in fileNames: self.defaultCapPadrao = endfile
		 
   


