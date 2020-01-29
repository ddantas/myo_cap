# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from UiFuncGenSettings import UiFuncGenSettings

class WinFuncGenSettings(QtWidgets.QMainWindow):

    def __init__(self, settings):
        super(WinFuncGenSettings, self).__init__()

        self.settings = settings

        self.ui_funcgen_settings = UiFuncGenSettings()
        self.ui_funcgen_settings.setupUi(self)

        self.ui_funcgen_settings.button_apply.clicked.connect(self.applyChanges)
        self.ui_funcgen_settings.button_cancel.clicked.connect(self.close)

        self.loadTextBoxes()

    def loadTextBoxes(self):
        self.ui_funcgen_settings.text_freq.setText(str(self.settings.getFuncGenFreq()))
        self.ui_funcgen_settings.text_time.setText(str(self.settings.getStressTime()))

    def applyChanges(self):
        self.settings.setFuncGenFreq(self.ui_funcgen_settings.text_freq.text())
        self.settings.setStressTime(self.ui_funcgen_settings.text_time.text())
        self.close()