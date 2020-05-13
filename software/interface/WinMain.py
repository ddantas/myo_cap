# -*- coding: utf-8 -*-

import sys
import time
import datetime as dt
import numpy as np
import PyQt5
import UiMain
import Tiva
import Settings
import WidgetGraph
import TextFile
import WinCaptureSettings
import WinDisplaySettings
import WinCommSettings
import WinFuncGenSettings
import WinStresstest #99

class WinMain(PyQt5.QtWidgets.QMainWindow):

    def __init__(self):
        # supeclass constructor
        super(WinMain, self).__init__()
        # setup settings
        self.settings = Settings.Settings()
        self.settings.load()
        # setup graph widget
        self.graph = WidgetGraph.WidgetGraph(self.settings)
        # setup main user interface
        self.ui_main = UiMain.UiMain(self, self.graph)
        # setup board
        self.board = Tiva.Tiva(self.settings)
        # setup text file
        self.textfile = TextFile.TextFile()
        # setup widgets
        self.setupWidgets()
        # setup timer
        self.timer_capture = PyQt5.QtCore.QTimer()
        self.timer_capture.timeout.connect(self.mainLoop)

    def setupWidgets(self):
        # setup menu
        self.ui_main.action_exit.triggered.connect(self.close)
        self.ui_main.action_start_capture.triggered.connect(self.startCapture)
        self.ui_main.action_stop_capture.triggered.connect(self.stopCapture)
        self.ui_main.action_show_capture.triggered.connect(self.showCapture)
        self.ui_main.action_load_settings.triggered.connect(self.loadSettings)
        self.ui_main.action_save_settings.triggered.connect(self.saveSettings)
        self.ui_main.action_display_settings.triggered.connect(self.showWinDisplaySettings)
        self.ui_main.action_capture_settings.triggered.connect(self.showWinCaptureSettings)
        self.ui_main.action_comm_settings.triggered.connect(self.showWinCommSettings)
        self.ui_main.action_funcgen_settings.triggered.connect(self.showWinFuncGenSettings)
        self.ui_main.action_stresstest.triggered.connect(self.showWinStresstest) #99
        self.ui_main.action_sine.triggered.connect(self.setSine)
        self.ui_main.action_square.triggered.connect(self.setSquare)
        self.ui_main.action_sawtooth.triggered.connect(self.setSawtooth)
        # setup buttons
        self.ui_main.button_select_file.clicked.connect(self.showWinSelectFile)
        self.ui_main.button_display_settings.clicked.connect(self.showWinDisplaySettings)
        self.ui_main.button_capture_settings.clicked.connect(self.showWinCaptureSettings)
        self.ui_main.button_start_capture.clicked.connect(self.startCapture)
        self.ui_main.button_stop_capture.clicked.connect(self.stopCapture)
        self.ui_main.button_show_capture.clicked.connect(self.showCapture)
                
        # setup combo box for serial ports
        for port in self.board.listPorts():
            self.ui_main.combo_port.addItem(port)
        
        # Sync the Boar With the Interface Settings            
        self.ui_main.combo_port.setCurrentIndex(-1)
        self.ui_main.combo_port.currentIndexChanged.connect( self.sync_board_settings )       
        
        # setup graph configurations
        self.updateInfoGraph()

    def updateInfoGraph(self):
        self.ui_main.info_graph.setText(
            'Swipe: ' + str(self.settings.getSwipe()) + ' | Vmin: ' + str(self.settings.getVMin()) +
            ' | Vmax: ' + str(self.settings.getVMax()) + ' | Vtick: ' + str(self.settings.getVTick()) +
            ' | Htick: ' + str(self.settings.getHTick()) + ' | Show channels: ' + str(self.settings.getTotChannels()))

    def loadSettings(self):
        if self.settings.load():
            self.showMessage('Settings loaded!', 'Settings loaded from ' + self.settings.getSettingsPath())
            self.graph.configureGraph()
        else:
            self.showMessage('Error!', 'Insert an settings file at ' + Settings.SETTINGS_PATH)

    def saveSettings(self):
        if self.settings.save():
            self.showMessage('Settings stored!', 'Settings stored at ' + self.settings.getSettingsPath())
        else:
            self.showMessage('Error!', 'Check the path ' + Settings.SETTINGS_PATH)

    def showWinDisplaySettings(self):
        self.win_display_settings = WinDisplaySettings.WinDisplaySettings(self, self.settings, self.graph)
        self.win_display_settings.show()

    def showWinCaptureSettings(self):
        self.win_capture_settings = WinCaptureSettings.WinCaptureSettings(self.settings, self.graph, self.board, self)
        self.win_capture_settings.show()

    def showWinCommSettings(self):
        self.win_comm_settings = WinCommSettings.WinCommSettings(self.settings, self.board, self)
        self.win_comm_settings.show()

    def showWinFuncGenSettings(self):
        self.win_funcgen_settings = WinFuncGenSettings.WinFuncGenSettings(self.settings, self.board, self)
        self.win_funcgen_settings.show()

    def showWinStresstest(self):
        self.win_stress_test = WinStresstest.WinStresstest(self.settings, self.board, self)
        self.win_stress_test.show() #99

    def showWinSelectFile(self):
        self.source = self.ui_main.combo_data_source.currentText()
        if self.source == 'File':
            options = PyQt5.QtWidgets.QFileDialog.Options()
            options |= PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
            self.file_name, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Select capture file', '', 'CSV files (*.csv)', options=options)
            self.openCSV(self.file_name)
        else:
            self.showMessage('Error!', 'Select FILE option at the first combo box.')                

    def showCapture(self):
        self.source = 'Log'
        self.log_pos = 0
        self.graph.createPlots()
        self.timer_capture.start(1000.0/self.settings.getSampleRate())

    def startCapture(self):
        
        self.ui_main.button_start_capture.setEnabled(False)
        self.ui_main.action_start_capture.setEnabled(False)
        self.ui_main.action_show_capture.setEnabled(False)
        self.ui_main.button_show_capture.setEnabled(False)
        
        self.source = self.ui_main.combo_data_source.currentText()
        self.graph.createPlots()
        if self.source == 'Serial':
            self.board.openComm(self.ui_main.combo_port.currentText())
            if self.board.test():
                self.file_name = self.configFile()
                if self.board.start() == 'ok':
                    self.timer_capture.start(0)
                else:
                    self.showMessage('Error!', 'Could not start capture!\nTry to start again or check the conection to the board.')                
            else:
                self.showMessage('Error!', 'Could not connect to the board!\nCheck the conection.')
        elif self.source == 'File':
            self.log_pos = 0
            self.timer_capture.start(1000.0/self.settings.getSampleRate())

    def stopCapture(self):
        self.timer_capture.stop()
        if self.board.getCommStatus():
            self.board.stop()
            if self.board.stop() == 'ok':                            
                self.textfile.saveFile(self.file_name)
                self.showMessage('Capture saved!', self.file_name)
                
                self.ui_main.button_start_capture.setEnabled(True)
                self.ui_main.action_start_capture.setEnabled(True)
                self.ui_main.action_show_capture.setEnabled(True)
                self.ui_main.button_show_capture.setEnabled(True)                                            
            else:
                self.showMessage('Error!', 'Could not stop capture!\nTry to stop again or check the conection to the board.')

    def mainLoop(self):
        if self.source == 'Serial':
            # receive samples from board and save to log
            pkt_samples = self.board.receiveStrPkt()
            self.textfile.saveLog(self.log_id, pkt_samples)
        elif self.source == 'Log':
            # receive samples from log
            if self.log_pos < self.textfile.getLogLength():
                pkt_samples = self.textfile.getLog(self.log_pos)
                self.log_pos += 1
            else:
                self.timer_capture.stop()
                self.showMessage('Finish!', 'All data was plotted.')
                pkt_samples = []
        else:
            # receive samples csv file
            if self.log_pos < len(self.log):
                pkt_samples = self.log[self.log_pos]
                self.log_pos += 1
            else:
                self.timer_capture.stop()
                self.showMessage('Finish!', 'All data was plotted.')
                pkt_samples = []
        # send samples from packet to graph
        if len(pkt_samples):
            self.graph.plotSamples(np.array(pkt_samples))

    """def setSine(self):
        if self.ui_main.action_sine.isChecked():
            self.ui_main.action_square.setChecked(False)
            self.ui_main.action_sawtooth.setChecked(False)
            if self.board.getCommStatus():
                self.board.openComm(self.ui_main.combo_port.currentText())
            # Sets the Wave Form to Sine
            self.board.setSineWaveMode()"""

    def sync_board_settings(self):
            
         if self.board.getCommStatus() == False:
            self.board.openComm(self.ui_main.combo_port.currentText())
            
            self.board.stop()
            
            if   self.ui_main.action_sine.isChecked():      self.board.setSineWaveMode()
            elif self.ui_main.action_square.isChecked():    self.board.setSquareWaveMode()
            elif self.ui_main.action_sawtooth.isChecked():  self.board.setSawtoothWaveMode()
            else:                                           self.board.setAdcMode()
            
            self.board.setFucGenFreq( self.settings.getFuncGenFreq() )
            self.board.setBitsPerSample( self.settings.getBitsPerSample() )
            self.board.setChannelsperBoard( self.settings.getChannelsPerBoard() )
            self.board.setNumAcquisBoards( self.settings.getNBoards() )
            self.board.setPacketSize( self.settings.getPktSize() )
            self.board.setSampleRate( self.settings.getSampleRate() )
            
            self.showMessage('Warnig!', 'The Board on the ' + self.ui_main.combo_port.currentText()  + ' port was synchronized' )
            
        
    def setSine(self):
        self.stopCapture()
        if self.board.getCommStatus() == False:
            self.board.openComm(self.ui_main.combo_port.currentText())
            
        if self.ui_main.action_sine.isChecked() == True:
            self.ui_main.action_square.setChecked(False)
            self.ui_main.action_sawtooth.setChecked(False)
            self.ui_main.button_start_capture.setEnabled(True)         
            # sets the wave form to sine
            if self.board.getFucGenFreq() != self.settings.getFuncGenFreq():
               self.board.setFucGenFreq(self.settings.getFuncGenFreq()) 
            self.board.setSineWaveMode()
        else:   
                self.board.setAdcMode()
                self.ui_main.button_start_capture.setEnabled(True)
        

    """def setSquare(self):
        if self.ui_main.action_square.isChecked():
            self.ui_main.action_sine.setChecked(False)
            self.ui_main.action_sawtooth.setChecked(False)
            if not self.board.getCommStatus():
                self.board.openComm(self.ui_main.combo_port.currentText())
            # Sets the Wve Form to Sine
            self.board.setSquareWaveMode()"""

    def setSquare(self):
        self.stopCapture()
        if self.board.getCommStatus() == False:
                self.board.openComm(self.ui_main.combo_port.currentText())
        if  self.ui_main.action_square.isChecked() == True:
            self.ui_main.action_sine.setChecked(False)
            self.ui_main.action_sawtooth.setChecked(False)
            # sets the wave form to square
            if self.board.getFucGenFreq() != self.settings.getFuncGenFreq():
               self.board.setFucGenFreq(self.settings.getFuncGenFreq())
            self.board.setSquareWaveMode()
        else: 
            self.board.setAdcMode()
            self.ui_main.button_start_capture.setEnabled(True)

    """def setSawtooth(self):
        if self.ui_main.action_sawtooth.isChecked():
            self.ui_main.action_square.setChecked(False)
            self.ui_main.action_sine.setChecked(False)
            if not self.board.getCommStatus():
                self.board.openComm(self.ui_main.combo_port.currentText())
            # Sets the Wve Form to Sine
            self.board.setSawtoothWaveMode()"""
        
    def setSawtooth(self):
        self.stopCapture()
        if self.board.getCommStatus() == False:
            self.board.openComm(self.ui_main.combo_port.currentText())
        if self.ui_main.action_sawtooth.isChecked() == True:
            self.ui_main.action_square.setChecked(False)
            self.ui_main.action_sine.setChecked(False) 
            # sets the wave form to sawtooth
            if self.board.getFucGenFreq() != self.settings.getFuncGenFreq():
               self.board.setFucGenFreq(self.settings.getFuncGenFreq())
            self.board.setSawtoothWaveMode()
        else: 
            self.board.setAdcMode()
            self.ui_main.button_start_capture.setEnabled(True)

    def configFile(self):
        name_cols = self.patternStr('ch', self.settings.getTotChannels(), True)
        format = self.patternStr('%d', self.settings.getTotChannels(), False)
        self.log_id = self.textfile.initFile(format, name_cols)
        date_time = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.textfile.writeHeaderLine('File generated by myo_cap software')
        self.textfile.writeHeaderLine('Available from github.com/ddantas/myo_cap')
        self.textfile.writeHeaderLine('Timestamp: ' + date_time)
        self.textfile.writeHeaderLine('')
        self.textfile.writeHeaderLine('EMG capture settings')
        self.textfile.writeHeaderLine('')
        self.textfile.writeMetadataLine('sampleRate', self.settings.getSampleRate())
        self.textfile.writeMetadataLine('channelsPerBoard', self.settings.getChannelsPerBoard())
        self.textfile.writeMetadataLine('nBoards', self.settings.getNBoards())
        self.textfile.writeMetadataLine('bitsPerSample', self.settings.getBitsPerSample())
        file_name = date_time + '.csv'
        return file_name

    def patternStr(self, pattern, num_it, add_it):
        str_out = ''
        for i in range(num_it):
            str_out = str_out + pattern
            if add_it:
                str_out = str_out + str(i)

            if i < num_it - 1:
                str_out = str_out + ';'
        return str_out

    def showMessage(self, title, body):
        PyQt5.QtWidgets.QMessageBox.about(self, title, body)

    def openCSV(self, file_name):
        self.log = []
        try:
            with open(file_name, 'r') as f:
                for line in f:
                    if line[0] == '#' and line[1] == ' ':
                        line = line.replace(':', '').split(' ')
                        if line[1] == 'sampleRate':
                            self.settings.setSampleRate(int(line[2]))
                        elif line[1] == 'channelsPerBoard':
                            self.settings.setChannelsPerBoard(int(line[2]))
                        elif line[1] == 'nBoards':
                            self.settings.setNBoards(int(line[2]))
                        elif line[1] == 'bitsPerSample':
                            self.settings.setBitsPerSample(int(line[2]))
                    elif (line[0] != '#') and (line != ''):
                        self.log.append(np.fromstring(line, dtype=np.uint16, sep=';'))
            self.graph.configureGraph()
        except:
            self.showMessage('Error!', 'Insert an CSV capture file.')

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication([])    
    app.aboutToQuit.connect(app.deleteLater)
    win_main = WinMain()  
    win_main.show()
    app.exec()
    win_main.board.closeComm()
    app.quit()
