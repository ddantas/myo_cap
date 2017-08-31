# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_main.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(232, 236)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.button_start = QtGui.QPushButton(self.centralwidget)
        self.button_start.setGeometry(QtCore.QRect(40, 170, 161, 31))
        self.button_start.setObjectName(_fromUtf8("button_start"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 0, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(43, 40, 100, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(43, 70, 100, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(43, 100, 100, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(43, 130, 100, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_ch = QtGui.QLabel(self.centralwidget)
        self.label_ch.setGeometry(QtCore.QRect(150, 40, 81, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_ch.setFont(font)
        self.label_ch.setObjectName(_fromUtf8("label_ch"))
        self.label_ampS = QtGui.QLabel(self.centralwidget)
        self.label_ampS.setGeometry(QtCore.QRect(150, 100, 81, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_ampS.setFont(font)
        self.label_ampS.setObjectName(_fromUtf8("label_ampS"))
        self.label_sampleR = QtGui.QLabel(self.centralwidget)
        self.label_sampleR.setGeometry(QtCore.QRect(150, 70, 81, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_sampleR.setFont(font)
        self.label_sampleR.setObjectName(_fromUtf8("label_sampleR"))
        self.label_ampE = QtGui.QLabel(self.centralwidget)
        self.label_ampE.setGeometry(QtCore.QRect(150, 130, 81, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_ampE.setFont(font)
        self.label_ampE.setObjectName(_fromUtf8("label_ampE"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 232, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.menuFile.addAction(self.actionSettings)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Main", None))
        self.button_start.setText(_translate("MainWindow", "Start", None))
        self.label.setText(_translate("MainWindow", "Graph Info", None))
        self.label_2.setText(_translate("MainWindow", "Channels: ", None))
        self.label_3.setText(_translate("MainWindow", "Sample Rate:", None))
        self.label_4.setText(_translate("MainWindow", "Amp. Start:", None))
        self.label_5.setText(_translate("MainWindow", "Amp. End:", None))
        self.label_ch.setText(_translate("MainWindow", "100", None))
        self.label_ampS.setText(_translate("MainWindow", "100", None))
        self.label_sampleR.setText(_translate("MainWindow", "100", None))
        self.label_ampE.setText(_translate("MainWindow", "100", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionSettings.setText(_translate("MainWindow", "Settings", None))

