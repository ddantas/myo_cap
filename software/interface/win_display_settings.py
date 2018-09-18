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
        DisplaySettingsWindow.setObjectName(_fromUtf8("DisplaySettingsWindow"))
        DisplaySettingsWindow.resize(386, 375)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DisplaySettingsWindow.sizePolicy().hasHeightForWidth())
        DisplaySettingsWindow.setSizePolicy(sizePolicy)
        DisplaySettingsWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtGui.QWidget(DisplaySettingsWindow)
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
        self.input_ch.setEnabled(True)
        self.input_ch.setGeometry(QtCore.QRect(200, 110, 151, 31))
        self.input_ch.setObjectName(_fromUtf8("input_voltMin"))
        self.input_swipe = QtGui.QLineEdit(self.centralwidget)
        self.input_swipe.setEnabled(True)
        self.input_swipe.setGeometry(QtCore.QRect(200, 70, 151, 31))
        self.input_swipe.setObjectName(_fromUtf8("input_swipe"))
        self.label_13 = QtGui.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(30, 70, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.input_voltMax = QtGui.QLineEdit(self.centralwidget)
        self.input_voltMax.setEnabled(True)
        self.input_voltMax.setGeometry(QtCore.QRect(200, 270, 151, 31))
        self.input_voltMax.setText(_fromUtf8(""))
        self.input_voltMax.setObjectName(_fromUtf8("input_voltMax"))
        self.label_12 = QtGui.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(30, 190, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_14 = QtGui.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(30, 270, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_14.setFont(font)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.button_save = QtGui.QPushButton(self.centralwidget)
        self.button_save.setGeometry(QtCore.QRect(20, 320, 151, 31))
        self.button_save.setObjectName(_fromUtf8("button_save"))
        self.button_cancel = QtGui.QPushButton(self.centralwidget)
        self.button_cancel.setGeometry(QtCore.QRect(200, 320, 151, 31))
        self.button_cancel.setObjectName(_fromUtf8("button_cancel"))
        self.input_htick = QtGui.QLineEdit(self.centralwidget)
        self.input_htick.setEnabled(True)
        self.input_htick.setGeometry(QtCore.QRect(200, 190, 151, 31))
        self.input_htick.setObjectName(_fromUtf8("input_htick"))
        self.label_15 = QtGui.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(30, 150, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_15.setFont(font)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.input_vtick = QtGui.QLineEdit(self.centralwidget)
        self.input_vtick.setEnabled(True)
        self.input_vtick.setGeometry(QtCore.QRect(200, 150, 151, 31))
        self.input_vtick.setObjectName(_fromUtf8("input_vtick"))
        self.label_16 = QtGui.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(30, 230, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_16.setFont(font)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.input_voltMin = QtGui.QLineEdit(self.centralwidget)
        self.input_voltMin.setEnabled(True)
        self.input_voltMin.setGeometry(QtCore.QRect(200, 230, 151, 31))
        self.input_voltMin.setObjectName(_fromUtf8("input_voltMin"))
        DisplaySettingsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(DisplaySettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(DisplaySettingsWindow)

    def retranslateUi(self, DisplaySettingsWindow):
        DisplaySettingsWindow.setWindowTitle(_translate("DisplaySettingsWindow", "Settings", None))
        self.label_11.setText(_translate("DisplaySettingsWindow", "Channels:", None))
        self.label_17.setText(_translate("DisplaySettingsWindow", "Display Settings", None))
        self.input_ch.setPlaceholderText(_translate("DisplaySettingsWindow", "0", None))
        self.label_13.setText(_translate("DisplaySettingsWindow", "Swipe:", None))
        self.input_voltMax.setPlaceholderText(_translate("DisplaySettingsWindow", "0", None))
        self.label_12.setText(_translate("DisplaySettingsWindow", "Horizontal Tick:", None))
        self.label_14.setText(_translate("DisplaySettingsWindow", "Maximum Voltage:", None))
        self.button_save.setText(_translate("DisplaySettingsWindow", "Save", None))
        self.button_cancel.setText(_translate("DisplaySettingsWindow", "Cancel", None))
        self.label_15.setText(_translate("DisplaySettingsWindow", "Vertical Tick:", None))
        self.label_16.setText(_translate("DisplaySettingsWindow", "Minimum Voltage", None))
        self.input_voltMin.setPlaceholderText(_translate("DisplaySettingsWindow", "4", None))
