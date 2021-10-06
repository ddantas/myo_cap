# -*- coding: utf-8 -*-

import PyQt5
import UiDisplaySettings
import sys

class WinDisplaySettings(PyQt5.QtWidgets.QMainWindow):

    def __init__(self, win_main, settings, graph):
        # calling superclass constructor
        super(WinDisplaySettings, self).__init__()
        # global objects
        self.win_main = win_main
        self.settings = settings
        self.graph = graph
        # display settings ui
        self.ui_display_settings = UiDisplaySettings.UiDisplaySettings(self)
        # connect ui buttons to modules
        self.ui_display_settings.button_apply.clicked.connect(self.applyChanges)
        self.ui_display_settings.button_cancel.clicked.connect(self.close)
        #load settings
        self.loadSettings()

    # load settings to text boxes
    def loadSettings(self):
        # load swipe
        self.ui_display_settings.text_swipe.setText(str(self.settings.getSwipe()))
        # load vtick
        self.ui_display_settings.text_vtick.setText(str(self.settings.getVTick()))
        # load htick
        self.ui_display_settings.text_htick.setText(str(self.settings.getHTick()))
        # load vmin
        self.ui_display_settings.text_vmin.setText(str(self.settings.getVMin()))
        # load vmax
        self.ui_display_settings.text_vmax.setText(str(self.settings.getVMax()))

    # set new values at settings object
    def applyChanges(self):
        # set swipe
        self.settings.setSwipe(int(self.ui_display_settings.text_swipe.text()))
        # set vtick
        self.settings.setVTick(float(self.ui_display_settings.text_vtick.text()))
        # set htick
        self.settings.setHTick(int(self.ui_display_settings.text_htick.text()))
        # set vmin
        self.settings.setVMin(float(self.ui_display_settings.text_vmin.text()))
        # set vmax
        self.settings.setVMax(float(self.ui_display_settings.text_vmax.text()))
        # update graph
        self.graph.configureGraph()
        # update graph informations at main window
        self.win_main.ui_main.updateInfoGraph(self.settings)
        # close window
        self.close()