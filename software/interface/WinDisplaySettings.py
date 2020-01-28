# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from UiDisplaySettings import UiDisplaySettings
import sys

class WinDisplaySettings(QtWidgets.QMainWindow):

    def __init__(self, win_main, settings, graph):
        super(WinDisplaySettings, self).__init__()

        self.win_main = win_main
        self.settings = settings
        self.graph = graph

        self.ui_display_settings = UiDisplaySettings()
        self.ui_display_settings.setupUi(self)

        self.ui_display_settings.button_apply.clicked.connect(self.applyChanges)
        self.ui_display_settings.button_cancel.clicked.connect(self.close)

        self.loadTextBoxes()

    def loadTextBoxes(self):
        self.ui_display_settings.text_swipe.setText(str(self.settings.getSwipe()))
        self.ui_display_settings.text_vtick.setText(str(self.settings.getVTick()))
        self.ui_display_settings.text_htick.setText(str(self.settings.getHTick()))
        self.ui_display_settings.text_vmin.setText(str(self.settings.getVMin()))
        self.ui_display_settings.text_vmax.setText(str(self.settings.getVMax()))
        self.ui_display_settings.text_show_ch.setText(str(self.settings.getShowChannels()))

    def applyChanges(self):
        self.settings.setSwipe(int(self.ui_display_settings.text_swipe.text()))
        self.settings.setVTick(float(self.ui_display_settings.text_vtick.text()))
        self.settings.setHTick(int(self.ui_display_settings.text_htick.text()))
        self.settings.setVMin(float(self.ui_display_settings.text_vmin.text()))
        self.settings.setVMax(float(self.ui_display_settings.text_vmax.text()))
        self.settings.setShowChannels(int(self.ui_display_settings.text_show_ch.text()))

        self.graph.configureGraph()
        self.win_main.updateInfoGraph()

        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win_display_settings = WinDisplaySettings()
    win_display_settings.show()
    sys.exit(app.exec())