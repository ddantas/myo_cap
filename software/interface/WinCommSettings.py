# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from UiCommSettings import UiCommSettings

class WinCommSettings(QtWidgets.QMainWindow):

    def __init__(self, settings):
        super(WinCommSettings, self).__init__()

        self.settings = settings

        self.ui_comm_settings = UiCommSettings(self)

        self.ui_comm_settings.button_apply.clicked.connect(self.applyChanges)
        self.ui_comm_settings.button_cancel.clicked.connect(self.close)

        self.loadSettings()

    def loadSettings(self):
        self.ui_comm_settings.text_pkt_size.setText(str(self.settings.getPktSize()))

    def applyChanges(self):
        self.settings.setPktSize(self.ui_comm_settings.text_pkt_size.text())
        self.close()