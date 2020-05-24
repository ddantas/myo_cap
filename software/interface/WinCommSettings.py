# -*- coding: utf-8 -*-

import PyQt5
import UiCommSettings

class WinCommSettings(PyQt5.QtWidgets.QMainWindow):

    def __init__(self, settings, board, win_main):
        # calling superclass constructor
        super(WinCommSettings, self).__init__()
        # global objects
        self.settings = settings
        self.board = board
        self.win_main = win_main
        # ui display settings
        self.ui_comm_settings = UiCommSettings.UiCommSettings(self)
        # connect ui buttons to modules
        self.ui_comm_settings.button_apply.clicked.connect(self.applyChanges)
        self.ui_comm_settings.button_cancel.clicked.connect(self.close)
        #load settings
        self.loadSettings()

    # load settings to text boxes
    def loadSettings(self):
        # load packet size
        self.ui_comm_settings.text_pkt_size.setText(str(self.settings.getPktSize()))
        # load packet compression
        if self.settings.getPktComp():
            self.ui_comm_settings.check_pkt_compression.setChecked(True)

    # set new values at settings object
    def applyChanges(self):
        try:
            # set packet size
            if self.board.setPacketSize(int(self.ui_comm_settings.text_pkt_size.text())):
                self.settings.setPktSize(self.ui_comm_settings.text_pkt_size.text())
            # set packet compression
            self.settings.setPktComp(int(self.ui_comm_settings.check_pkt_compression.isChecked()))
        except:
            self.win_main.showMessage('Error','Communication settings did not apply!\nPlease, connect the board.')
        # close window
        self.close()