import sys

from settings import Settings
from win_capture_settings import Ui_CaptureSettingsWindow
from pyqtgraph.Qt import QtCore, QtGui

class CaptureSettings(QtGui.QMainWindow): 
    def __init__(self, parent=None):
        super(CaptureSettings, self).__init__(parent)

        self.settings_data = Settings().load()

        self.ui_caps = Ui_CaptureSettingsWindow()
        self.ui_caps.setupUi(self)

        # set capture data
        self.ui_caps.input_sampleR.setText(str(self.settings_data['sampleRate']))
        self.ui_caps.input_ch.setText(str(self.settings_data['channelsPerBoard']))
        self.ui_caps.input_numofboards.setText(str(self.settings_data['nBoards']))
        self.ui_caps.input_bits.setText(str(self.settings_data['bitsPerSample']))

        # init actions
        self.ui_caps.button_save.clicked.connect(self.storeCaptureSettings)
        self.ui_caps.button_cancel.clicked.connect(self.close)


    def storeCaptureSettings(self):
        flag_err = 1
        try:
            self.settings_data['sampleRate'] = int(self.ui_caps.input_sampleR.text())
        except:
            self.showMessage("Error", "Sample Rate!")
            flag_err = 0
        try:
            self.settings_data['channelsPerBoard'] = int(self.ui_caps.input_ch.text())
        except:
            self.showMessage("Error", "channelsPerBoard!")
            flag_err = 0
        try:
            self.settings_data['nBoards'] = int(self.ui_caps.input_numofboards.text())
        except:
            self.showMessage("Error", "nBoards!")
            flag_err = 0
        try:
            self.settings_data['bitsPerSample'] = int(self.ui_caps.input_bits.text())
        except:
            self.showMessage("Error", "bitsPerSample!")
            flag_err = 0
        if(flag_err):
            self.settings_data['showChannels'] = int(self.settings_data['channelsPerBoard']) * int(self.settings_data['nBoards'])

            if Settings().store(self.settings_data):
                # self.showMainWindow()
                self.close()