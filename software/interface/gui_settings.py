# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_settings.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName(_fromUtf8("SettingsWindow"))
        SettingsWindow.resize(294, 307)
        SettingsWindow.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.centralwidget = QtGui.QWidget(SettingsWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label_11 = QtGui.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(10, 50, 100, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_17 = QtGui.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(70, 0, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.input_ch = QtGui.QLineEdit(self.centralwidget)
        self.input_ch.setGeometry(QtCore.QRect(110, 50, 151, 31))
        self.input_ch.setObjectName(_fromUtf8("input_ch"))
        self.input_sampleR = QtGui.QLineEdit(self.centralwidget)
        self.input_sampleR.setGeometry(QtCore.QRect(110, 90, 151, 31))
        self.input_sampleR.setObjectName(_fromUtf8("input_sampleR"))
        self.label_13 = QtGui.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(10, 90, 100, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.input_ampS = QtGui.QLineEdit(self.centralwidget)
        self.input_ampS.setEnabled(False)
        self.input_ampS.setGeometry(QtCore.QRect(110, 130, 151, 31))
        self.input_ampS.setObjectName(_fromUtf8("input_ampS"))
        self.label_12 = QtGui.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(10, 130, 100, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_14 = QtGui.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(10, 170, 100, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_14.setFont(font)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.input_ampE = QtGui.QLineEdit(self.centralwidget)
        self.input_ampE.setEnabled(False)
        self.input_ampE.setGeometry(QtCore.QRect(110, 170, 151, 31))
        self.input_ampE.setObjectName(_fromUtf8("input_ampE"))
        self.button_save = QtGui.QPushButton(self.centralwidget)
        self.button_save.setGeometry(QtCore.QRect(30, 230, 111, 31))
        self.button_save.setObjectName(_fromUtf8("button_save"))
        self.button_cancel = QtGui.QPushButton(self.centralwidget)
        self.button_cancel.setGeometry(QtCore.QRect(150, 230, 111, 31))
        self.button_cancel.setObjectName(_fromUtf8("button_cancel"))
        SettingsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Settings", None))
        self.label_11.setText(_translate("SettingsWindow", "Channels: ", None))
        self.label_17.setText(_translate("SettingsWindow", "Settings", None))
        self.label_13.setText(_translate("SettingsWindow", "Sample Rate:", None))
        self.input_ampS.setText(_translate("SettingsWindow", "0", None))
        self.label_12.setText(_translate("SettingsWindow", "Amp. Start:", None))
        self.label_14.setText(_translate("SettingsWindow", "Amp. End:", None))
        self.input_ampE.setInputMask(_translate("SettingsWindow", "4; ", None))
        self.button_save.setText(_translate("SettingsWindow", "Save", None))
        self.button_cancel.setText(_translate("SettingsWindow", "Cancel", None))

