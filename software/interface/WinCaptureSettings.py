# -*- coding: utf-8 -*-

import PyQt5
import UiCaptureSettings
import sys

class WinCaptureSettings(PyQt5.QtWidgets.QMainWindow):

    def __init__(self, settings, graph, board, winMain):
        # calling superclass constructor
        super(WinCaptureSettings, self).__init__()
        # global objects
        self.settings = settings
        self.graph = graph
        self.board = board
        self.winMain = winMain
        # capture settings ui
        self.ui_capture_settings = UiCaptureSettings.UiCaptureSettings(self)
        # connect ui buttons to modules
        self.ui_capture_settings.button_apply.clicked.connect(self.applyChanges)
        self.ui_capture_settings.button_cancel.clicked.connect(self.close)
        # load settings
        self.loadSettings()

    # load settings to text boxes
    def loadSettings(self):
        # load sample rate
        self.ui_capture_settings.text_sample_rate.setText(str(self.settings.getSampleRate()))
        # load sample channels per board
        self.ui_capture_settings.text_ch_board.setText(str(self.settings.getChannelsPerBoard()))
        # load sample number of boards
        self.ui_capture_settings.text_num_boards.setText(str(self.settings.getNBoards()))
        # load bits per sample
        self.ui_capture_settings.text_bits_sample.setText(str(self.settings.getBitsPerSample()))

    # set new values at settings object
    def applyChanges(self):
        
        self.winMain.stopCapture()
        
        if self.board.setSampleRate( int(self.ui_capture_settings.text_sample_rate.text()) ):
            # set sample rate
            self.settings.setSampleRate(int(self.ui_capture_settings.text_sample_rate.text()))
        
        if self.board.setChannelsperBoard( int(self.ui_capture_settings.text_ch_board.text()) ):
            # set sample channels per board
            self.settings.setChannelsPerBoard(int(self.ui_capture_settings.text_ch_board.text()))
            
        if self.board.setNumAcquisBoards( int(self.ui_capture_settings.text_num_boards.text()) ):    
            # set sample number of boards
            self.settings.setNBoards(int(self.ui_capture_settings.text_num_boards.text()))
            
        if self.board.setBitsPerSample( int(self.ui_capture_settings.text_bits_sample.text()) ):    
            # set bits per sample
            self.settings.setBitsPerSample(int(self.ui_capture_settings.text_bits_sample.text()))
       
        # update graph
        self.graph.configureGraph()
        # close window
        self.close()