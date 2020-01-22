

import sys

from settings import Settings
from win_frequency_funcgen import Ui_DisplaySettingsWindow
from pyqtgraph.Qt import QtCore, QtGui

class FrequencySettings(QtGui.QMainWindow): 
    def __init__(self, parent=None):
        super(FrequencySettings, self).__init__(parent)
        self.settings_data = Settings().load()

        self.ui_display = Ui_DisplaySettingsWindow()
        self.ui_display.setupUi(self)

        # set data
        self.ui_display.input_freq.setText(str(self.settings_data['frequency']))
        # init actions
        self.ui_display.button_save.clicked.connect(self.storeDisplaySettings)
        #self.ui_display.button_save.clicked.connect(self.widget.setFrequency)#teste set
        self.ui_display.button_cancel.clicked.connect(self.close)

    def storeDisplaySettings(self): 
        flag_err = 1
        try:
            self.settings_data['frequency'] = float(self.ui_display.input_freq.text())
            check = 1 / self.settings_data['frequency']
        except:
            self.showMessage("Error", "frequency!")
            flag_err = 0
        if (flag_err):
            if Settings().store(self.settings_data):
                # self.showMainWindow()
                self.close()

    
