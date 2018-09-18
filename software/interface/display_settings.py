import sys

from settings import Settings
from win_display_settings import Ui_DisplaySettingsWindow
from pyqtgraph.Qt import QtCore, QtGui

class DisplaySettings(QtGui.QMainWindow): 
    def __init__(self, parent=None):
        super(DisplaySettings, self).__init__(parent)
        self.settings_data = Settings().load()

        self.ui_display = Ui_DisplaySettingsWindow()
        self.ui_display.setupUi(self)

        # set data
        self.ui_display.input_swipe.setText(str(self.settings_data['swipeSamples']))
        self.ui_display.input_vtick.setText(str(self.settings_data['vertTick']))
        self.ui_display.input_htick.setText(str(self.settings_data['horizTick']))
        self.ui_display.input_ch.setText(str(self.settings_data['showChannels']))
        self.ui_display.input_voltMin.setText(str(self.settings_data['vMin']))
        self.ui_display.input_voltMax.setText(str(self.settings_data['vMax']))
        # init actions
        self.ui_display.button_save.clicked.connect(self.storeDisplaySettings)
        self.ui_display.button_cancel.clicked.connect(self.close)

    def storeDisplaySettings(self):
        flag_err = 1
        try:
            self.settings_data['swipeSamples'] = int(self.ui_display.input_swipe.text())
            check = 1 / self.settings_data['swipeSamples']
        except:
            self.showMessage("Error", "swipeSamples!")
            flag_err = 0
        try:
            self.settings_data['vertTick'] = float(self.ui_display.input_vtick.text())
            check = 1 / self.settings_data['vertTick']
        except:
            self.showMessage("Error", "vertTick!")
            flag_err = 0
        try:
            self.settings_data['horizTick'] = int(self.ui_display.input_htick.text())
            check = 1 / self.settings_data['horizTick']
        except:
            self.showMessage("Error", "horizTick!")
            flag_err = 0
        try:
            self.settings_data['showChannels'] = int(self.ui_display.input_ch.text())
            check = 1 / self.settings_data['horizTick']
        except:
            self.showMessage("Error", "showChannels!")
            flag_err = 0
        try:
            self.settings_data['vMin'] = float(self.ui_display.input_voltMin.text())
        except:
            self.showMessage("Error", "vMin!")
            flag_err = 0
        try:
            self.settings_data['vMax'] = float(self.ui_display.input_voltMax.text())
        except:
            self.showMessage("Error", "vMax!")
            flag_err = 0
        if (self.settings_data['vMax'] < self.settings_data['vMin']):
            self.showMessage("Error", "vMin > vMax!")
            flag_err = 0
        if (flag_err):
            if Settings().store(self.settings_data):
                # self.showMainWindow()
                self.close()


