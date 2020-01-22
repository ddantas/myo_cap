# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_display_settings.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from sys import platform

if platform == "linux" or platform == "linux2" or platform == "darwin":
    from PyQt5 import QtCore, QtGui

elif platform == "win32":
    from qtpy import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DisplaySettingsWindow(object):
    def setupUi(self, DisplaySettingsWindow):
        DisplaySettingsWindow.setObjectName(_fromUtf8("FuncGenFrequencyWindow"))
        DisplaySettingsWindow.resize(386, 145) #dimensão da janela? sim!
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DisplaySettingsWindow.sizePolicy().hasHeightForWidth())
        DisplaySettingsWindow.setSizePolicy(sizePolicy)
        DisplaySettingsWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtGui.QWidget(DisplaySettingsWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label_17 = QtGui.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(100, 20, 200, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.input_freq = QtGui.QLineEdit(self.centralwidget)
        self.input_freq.setEnabled(True)
        self.input_freq.setGeometry(QtCore.QRect(200, 70, 151, 31))
        self.input_freq.setObjectName(_fromUtf8("input_freq"))
        self.label_13 = QtGui.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(30, 70, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.button_save = QtGui.QPushButton(self.centralwidget)
        self.button_save.setGeometry(QtCore.QRect(20, 110, 151, 31)) #(20, 320, 151, 31)
        self.button_save.setObjectName(_fromUtf8("button_save"))
        self.button_cancel = QtGui.QPushButton(self.centralwidget)
        self.button_cancel.setGeometry(QtCore.QRect(200, 110, 151, 31))
        self.button_cancel.setObjectName(_fromUtf8("button_cancel"))
	   
        DisplaySettingsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(DisplaySettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(DisplaySettingsWindow)

    def retranslateUi(self, DisplaySettingsWindow):
        DisplaySettingsWindow.setWindowTitle(_translate("DisplaySettingsWindow", "Function Generator", None))
        self.label_17.setText(_translate("DisplaySettingsWindow", "Frequency Settings", None))
        self.label_13.setText(_translate("DisplaySettingsWindow", "Frequency:", None))
        self.button_save.setText(_translate("DisplaySettingsWindow", "Save", None))
       #self.button_save.clicked.connect(self.widget.setFrequency)
        self.button_cancel.setText(_translate("DisplaySettingsWindow", "Cancel", None))
