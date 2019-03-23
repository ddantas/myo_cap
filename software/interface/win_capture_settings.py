# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_capture_settings.ui'
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

class Ui_CaptureSettingsWindow(object):
    def setupUi(self, CaptureSettingsWindow):
        CaptureSettingsWindow.setObjectName(_fromUtf8("CaptureSettingsWindow"))
        CaptureSettingsWindow.resize(381, 320)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CaptureSettingsWindow.sizePolicy().hasHeightForWidth())
        CaptureSettingsWindow.setSizePolicy(sizePolicy)
        CaptureSettingsWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtGui.QWidget(CaptureSettingsWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label_11 = QtGui.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(30, 110, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_17 = QtGui.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(100, 20, 200, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.input_ch = QtGui.QLineEdit(self.centralwidget)
        self.input_ch.setGeometry(QtCore.QRect(200, 110, 151, 31))
        self.input_ch.setEnabled(True)
        self.input_ch.setObjectName(_fromUtf8("input_ch"))
        self.input_sampleR = QtGui.QLineEdit(self.centralwidget)
        self.input_sampleR.setEnabled(True)
        self.input_sampleR.setGeometry(QtCore.QRect(200, 70, 151, 31))
        self.input_sampleR.setObjectName(_fromUtf8("input_sampleR"))
        self.label_13 = QtGui.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(30, 70, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.label_12 = QtGui.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(30, 190, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.button_save = QtGui.QPushButton(self.centralwidget)
        self.button_save.setGeometry(QtCore.QRect(20, 270, 151, 31))
        self.button_save.setObjectName(_fromUtf8("button_save"))
        self.button_cancel = QtGui.QPushButton(self.centralwidget)
        self.button_cancel.setGeometry(QtCore.QRect(200, 270, 151, 31))
        self.button_cancel.setObjectName(_fromUtf8("button_cancel"))
        self.input_bits = QtGui.QLineEdit(self.centralwidget)
        self.input_bits.setEnabled(True)
        self.input_bits.setGeometry(QtCore.QRect(200, 190, 151, 31))
        self.input_bits.setObjectName(_fromUtf8("input_bits"))
        self.label_15 = QtGui.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(30, 150, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_15.setFont(font)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.input_numofboards = QtGui.QLineEdit(self.centralwidget)
        self.input_numofboards.setEnabled(True)
        self.input_numofboards.setGeometry(QtCore.QRect(200, 150, 151, 31))
        self.input_numofboards.setObjectName(_fromUtf8("input_numofboards"))

        self.input_baudrate = QtGui.QLineEdit(self.centralwidget)
        self.input_baudrate.setEnabled(True)
        self.input_baudrate.setGeometry(QtCore.QRect(200, 230, 151, 31))
        self.input_baudrate.setObjectName(_fromUtf8("input_baudrate"))

        self.label_18 = QtGui.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(30, 230, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_18.setFont(font)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        
        CaptureSettingsWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(CaptureSettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(CaptureSettingsWindow)

    def retranslateUi(self, CaptureSettingsWindow):
        CaptureSettingsWindow.setWindowTitle(_translate("CaptureSettingsWindow", "Settings", None))
        self.label_11.setText(_translate("CaptureSettingsWindow", "Ch per board: ", None))
        self.label_17.setText(_translate("CaptureSettingsWindow", "Capture Settings", None))
        self.label_13.setText(_translate("CaptureSettingsWindow", "Sample rate:", None))
        self.label_12.setText(_translate("CaptureSettingsWindow", "Bits per sample:", None))
        self.label_15.setText(_translate("CaptureSettingsWindow", "Num of boards:", None))
        self.label_18.setText(_translate("CaptureSettingsWindow", "Baudrate:", None))

        self.button_save.setText(_translate("CaptureSettingsWindow", "Save", None))
        self.button_cancel.setText(_translate("CaptureSettingsWindow", "Cancel", None))

