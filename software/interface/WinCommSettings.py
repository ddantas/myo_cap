# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from UiCommSettings import UiCommSettings

class WinCommSettings(QtWidgets.QMainWindow):

    def __init__(self, settings):
        super(WinCommSettings, self).__init__()

        self.settings = settings

        self.ui_comm_settings = UiCommSettings()
        self.ui_comm_settings.setupUi(self)

        self.ui_comm_settings.button_apply.clicked.connect(self.applyChanges)
        self.ui_comm_settings.button_cancel.clicked.connect(self.close)

        self.loadTextBoxes()

    def loadTextBoxes(self):
        self.ui_comm_settings.text_pkt_size.setText(str(self.settings.getPktSize()))
        self.ui_comm_settings.text_baudrate.setText(str(self.settings.getBaudrate()))

    def applyChanges(self):
        self.settings.setPktSize(self.ui_comm_settings.text_pkt_size.text())
        self.settings.setBaudrate(self.ui_comm_settings.text_baudrate.text())
        self.close()