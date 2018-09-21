# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EmgDS.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(224, 285)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 220, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 30, 51, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.spinBox = QtGui.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(140, 30, 47, 21))
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.spinBox_2 = QtGui.QSpinBox(Dialog)
        self.spinBox_2.setGeometry(QtCore.QRect(140, 60, 47, 21))
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 51, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.spinBox_3 = QtGui.QSpinBox(Dialog)
        self.spinBox_3.setGeometry(QtCore.QRect(140, 90, 47, 21))
        self.spinBox_3.setObjectName(_fromUtf8("spinBox_3"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 90, 81, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.spinBox_4 = QtGui.QSpinBox(Dialog)
        self.spinBox_4.setGeometry(QtCore.QRect(140, 120, 47, 21))
        self.spinBox_4.setObjectName(_fromUtf8("spinBox_4"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 150, 121, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(30, 120, 91, 17))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.spinBox_5 = QtGui.QSpinBox(Dialog)
        self.spinBox_5.setGeometry(QtCore.QRect(140, 180, 47, 21))
        self.spinBox_5.setObjectName(_fromUtf8("spinBox_5"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(30, 180, 81, 17))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.spinBox_6 = QtGui.QSpinBox(Dialog)
        self.spinBox_6.setGeometry(QtCore.QRect(140, 150, 47, 21))
        self.spinBox_6.setObjectName(_fromUtf8("spinBox_6"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), self.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Swipe:", None))
        self.label_2.setText(_translate("Dialog", "Zero", None))
        self.label_3.setText(_translate("Dialog", "Amplitude:", None))
        self.label_4.setText(_translate("Dialog", "Horizontal tick:", None))
        self.label_5.setText(_translate("Dialog", "Vertical tick:", None))
        self.label_6.setText(_translate("Dialog", "Channel:", None))

    def accept(self):
	print "accept"
    def reject(self):
	print "reject"

