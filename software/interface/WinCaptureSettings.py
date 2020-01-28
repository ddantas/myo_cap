# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from UiCaptureSettings import UiCaptureSettings
import sys

class WinCaptureSettings(QtWidgets.QMainWindow):

    def __init__(self, settings):
        super(WinCaptureSettings, self).__init__()

        self.settings = settings

        self.ui_capture_settings = UiCaptureSettings()
        self.ui_capture_settings.setupUi(self)

        self.ui_capture_settings.button_apply.clicked.connect(self.applyChanges)
        self.ui_capture_settings.button_cancel.clicked.connect(self.close)

        self.loadTextBoxes()

    def loadTextBoxes(self):
        self.ui_capture_settings.text_sample_rate.setText(str(self.settings.getSampleRate()))
        self.ui_capture_settings.text_ch_board.setText(str(self.settings.getChannelsPerBoard()))
        self.ui_capture_settings.text_num_boards.setText(str(self.settings.getNBoards()))
        self.ui_capture_settings.text_bits_sample.setText(str(self.settings.getBitsPerSample()))

    def applyChanges(self):
        self.settings.setSampleRate(int(self.ui_capture_settings.text_sample_rate.text()))
        self.settings.setChannelsPerBoard(int(self.ui_capture_settings.text_ch_board.text()))
        self.settings.setNBoards(int(self.ui_capture_settings.text_num_boards.text()))
        self.settings.setBitsPerSample(int(self.ui_capture_settings.text_bits_sample.text()))
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win_display_settings = WinCaptureSettings()
    win_display_settings.show()
    sys.exit(app.exec())