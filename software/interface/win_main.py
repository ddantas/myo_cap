# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from tiva import Main

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2560, 1315)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())

        MainWindow.setSizePolicy(sizePolicy)

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())

        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.widget = Main(self.centralwidget)
        self.widget.setObjectName("widget")

        self.horizontalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 2560, 22))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuCapture = QtWidgets.QMenu(self.menubar)
        self.menuCapture.setObjectName("menuCapture")

        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")

        self.menuFuncGen = QtWidgets.QMenu(self.menubar)
        self.menuFuncGen.setObjectName("menuFuncGen")

        MainWindow.setMenuBar(self.menubar)

        self.actionLoad_Capture = QtWidgets.QAction(MainWindow)
        self.actionLoad_Capture.setObjectName("actionLoad_Capture")
        self.actionSave_Capture = QtWidgets.QAction(MainWindow)
        self.actionSave_Capture.setObjectName("actionSave_Capture")

        self.actionStart_Capture = QtWidgets.QAction(MainWindow)
        self.actionStart_Capture.setObjectName("actionStart_Capture")
        self.actionStop_Capture = QtWidgets.QAction(MainWindow)
        self.actionStop_Capture.setObjectName("actionStop_Capture")
        self.actionShow_Capture = QtWidgets.QAction(MainWindow)
        self.actionShow_Capture.setObjectName("actionShow_Capture")

        self.actionLoad_Settings = QtWidgets.QAction(MainWindow)
        self.actionLoad_Settings.setObjectName("actionLoad_Settings")
        self.actionSave_Settings = QtWidgets.QAction(MainWindow)
        self.actionSave_Settings.setObjectName("actionSave_Settings")
        self.actionCapture_Settings = QtWidgets.QAction(MainWindow)
        self.actionCapture_Settings.setObjectName("actionCapture_Settings")
        self.actionDisplay_Settings = QtWidgets.QAction(MainWindow)
        self.actionDisplay_Settings.setObjectName("actionDisplay_Settings")

        self.actionSine_FuncGen = QtWidgets.QAction(MainWindow)
        self.actionSine_FuncGen.setObjectName("actionSine_FuncGen")
        self.actionSquare_FuncGen = QtWidgets.QAction(MainWindow)
        self.actionSquare_FuncGen.setObjectName("actionSquare_FuncGen")
        self.actionSawtooth_FuncGen = QtWidgets.QAction(MainWindow)
        self.actionSawtooth_FuncGen.setObjectName("actionSawtooth_FuncGen")

        self.actionSawtooth_FuncGen = QtWidgets.QAction(MainWindow)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCapture.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuFuncGen.menuAction())

        self.menuFile.addAction(self.actionLoad_Capture)
        self.menuFile.addAction(self.actionSave_Capture)

        self.menuCapture.addAction(self.actionStart_Capture)
        self.menuCapture.addAction(self.actionStop_Capture)
        self.menuCapture.addAction(self.actionShow_Capture)

        self.menuSettings.addAction(self.actionLoad_Settings)
        self.menuSettings.addAction(self.actionSave_Settings)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.actionCapture_Settings)
        self.menuSettings.addAction(self.actionDisplay_Settings)

        self.menuFuncGen.addAction(self.actionSine_FuncGen)
        self.menuFuncGen.addAction(self.actionSquare_FuncGen)
        self.menuFuncGen.addAction(self.actionSawtooth_FuncGen)
        self.menuSettings.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(_translate("MainWindow", "EMG"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuCapture.setTitle(_translate("MainWindow", "Capture"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuFuncGen.setTitle(_translate("MainWindow", "Function Generator"))

        self.actionLoad_Capture.setText(_translate("MainWindow", "Load Capture"))
        self.actionSave_Capture.setText(_translate("MainWindow", "Save Capture"))

        self.actionStart_Capture.setText(_translate("MainWindow", "Start Capture"))
        self.actionStop_Capture.setText(_translate("MainWindow", "Stop Capture"))
        self.actionShow_Capture.setText(_translate("MainWindow", "Show Capture"))

        self.actionLoad_Settings.setText(_translate("MainWindow", "Load Settings"))
        self.actionSave_Settings.setText(_translate("MainWindow", "Save Settings"))
        self.actionCapture_Settings.setText(_translate("MainWindow", "Capture Settings"))
        self.actionDisplay_Settings.setText(_translate("MainWindow", "Display Settings"))

        self.actionSine_FuncGen.setText(_translate("MainWindow", "Sine"))
        self.actionSine_FuncGen.setCheckable(True)
        self.actionSquare_FuncGen.setText(_translate("MainWindow", "Square"))
        self.actionSquare_FuncGen.setCheckable(True)
        self.actionSawtooth_FuncGen.setText(_translate("MainWindow", "Sawtooth"))
        self.actionSawtooth_FuncGen.setCheckable(True)