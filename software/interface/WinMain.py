# -*- coding: utf-8 -*-

import datetime as dt
import numpy as np
import PyQt5
import AuxFunctions as AuxFunc
import UiMain
import Tiva
import Settings
import WidgetGraph
import TextFile
import WinCaptureSettings
import WinDisplaySettings
import WinCommSettings
import WinFuncGenSettings
import WinStresstest 
import Constants as const


class WinMain(PyQt5.QtWidgets.QMainWindow):

    def __init__(self):        
        # supeclass constructor
        super(WinMain, self).__init__()
        # setup settings
        self.settings = Settings.Settings()
        self.settings.load(const.SETTINGS_PATH, const.SETTINGS_FILE_NAME)
        # setup graph widget
        self.graph = WidgetGraph.WidgetGraph(self.settings)
        # setup main user interface
        self.ui_main = UiMain.UiMain(self, self.graph)
        # setup board
        self.board = Tiva.Tiva(self.settings)
        # setup text file
        self.textfile = TextFile.TextFile()
        # setup widgets
        self.ui_main.setupWidgets()
        # setup timer
        self.timer_capture = PyQt5.QtCore.QTimer()
        self.timer_capture.timeout.connect(self.mainLoop)
       
## File menu methods ###################################################################################################################################################
        
    def loadCapture(self):
        self.source = self.ui_main.combo_data_source.currentText()
        if self.source == 'File':
            options = PyQt5.QtWidgets.QFileDialog.Options()
            options |= PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
            self.file_name, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Select capture file', '', 'CSV files (*.csv)', options=options)
            self.openCSV(self.file_name)
        else:   AuxFunc.showMessage('Error!', 'Select FILE option first at the combo box.')                

    def saveCapture(self):        
        # Checks if a Start Capture was alredy executed
        if( hasattr(self, 'log_id') ):
            self.stopCapture()            
            date_time = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')        
            self.file_name = date_time + '.csv'
            self.settings.save( const.LOG_PATH, self.file_name)
            self.textfile.saveFile_Old(self.file_name)
            AuxFunc.showMessage('Capture saved!', self.file_name)
        
        else:   AuxFunc.showMessage('Error!', 'Before Save a Capture into a File you should Start one Capture using the Serial Port.')

## Capture menu methods ################################################################################################################################################

    def startCapture(self):           
        self.source = self.ui_main.combo_data_source.currentText()
        self.graph.createPlots()
        #-----------------------------------------------------------------------------------------------------------------------------         
        if self.source == 'Serial':
            self.board.openComm(self.ui_main.combo_port.currentText())
            if self.board.test():               
                if self.board.start() == 'ok':
                    self.logIdGenerator()
                    self.timer_capture.start(0)
                else:      AuxFunc.showMessage('Error!', 'Could not start capture!\nTry to start again or check the conection to the board.');      return -1
            else:          AuxFunc.showMessage('Error!', 'Could not connect to the board!\nCheck the conection.')
        #-----------------------------------------------------------------------------------------------------------------------------
        elif self.source == 'File':
            self.log_pos = 0
            self.timer_capture.start(1000.0/self.settings.getSampleRate())        
        #-----------------------------------------------------------------------------------------------------------------------------
        self.ui_main.startCaptureClicked()        
        
    def stopCapture(self):        
        # Stop the Timer
        self.timer_capture.stop()        
        # Check if the Serial Port is open
        if self.board.getCommStatus():
            self.board.stop()
            if self.board.stop() == 'ok':   self.ui_main.stopCaptureClicked()                                         
            else                        :   AuxFunc.showMessage('Error!', 'Could not stop capture!\nTry to stop again or check the conection to the board.')

    def showCapture(self):
        self.source = 'Log'
        self.log_pos = 0
        self.graph.createPlots()
        self.timer_capture.start(1000.0/self.settings.getSampleRate())
        self.ui_main.showCaptureClicked()
        
## Settings menu methods ###############################################################################################################################################        

    def loadSettings(self):
        if self.settings.load(const.SETTINGS_PATH, const.SETTINGS_FILE_NAME):    
                                    AuxFunc.showMessage('Settings loaded!', 'Settings loaded from ' + self.settings.getSettingsPath());    self.graph.configureGraph()            
        else                   :    AuxFunc.showMessage('Error!', 'Insert an valid settings file at: ' + Settings.SETTINGS_PATH)

    def saveSettings(self):
        if self.settings.save(const.SETTINGS_PATH, const.SETTINGS_FILE_NAME):    
                                    AuxFunc.showMessage('Settings stored!', 'Settings stored at: ' + self.settings.getSettingsPath());
        else                   :    AuxFunc.showMessage('Error!', 'Check the path ' + Settings.SETTINGS_PATH)
            
    def showWinCaptureSettings(self):
        self.stopCapture()
        self.win_capture_settings = WinCaptureSettings.WinCaptureSettings(self.settings, self.graph, self.board)
        self.win_capture_settings.show()        

    def showWinDisplaySettings(self):
        self.win_display_settings = WinDisplaySettings.WinDisplaySettings(self, self.settings, self.graph)
        self.win_display_settings.show()

    def showWinCommSettings(self):
        self.stopCapture()
        self.win_comm_settings = WinCommSettings.WinCommSettings(self.settings, self.board)
        self.win_comm_settings.show()
        
## Function generator menu methods #####################################################################################################################################        

    def showWinFuncGenSettings(self):
        self.stopCapture()
        self.win_funcgen_settings = WinFuncGenSettings.WinFuncGenSettings(self.settings, self.board)
        self.win_funcgen_settings.show()

    def setSine(self):                
        if self.board.getCommStatus() == False:              self.board.openComm(self.ui_main.combo_port.currentText())
        self.stopCapture()            
        if self.ui_main.action_sine.isChecked() == True:     self.board.setSineWaveMode();     self.ui_main.sineWaveClicked()
        else:                                                self.board.setAdcMode()

    def setSquare(self):
        if self.board.getCommStatus() == False:              self.board.openComm(self.ui_main.combo_port.currentText())
        self.stopCapture()            
        if self.ui_main.action_square.isChecked() == True:   self.board.setSquareWaveMode();   self.ui_main.squareWaveClicked()
        else:                                                self.board.setAdcMode()

    def setSawtooth(self):        
        if self.board.getCommStatus() == False:              self.board.openComm(self.ui_main.combo_port.currentText())
        self.stopCapture()            
        if self.ui_main.action_sawtooth.isChecked() == True: self.board.setSawtoothWaveMode(); self.ui_main.sawtoothWaveClicked()
        else:                                                self.board.setAdcMode()

    def showWinStresstest(self):
        self.stopCapture()
        self.win_stress_test = WinStresstest.WinStresstest(self.settings, self.board, self)
        self.win_stress_test.show()

## Application methods #############################################################################################################################
         
    def mainLoop(self):
        #--------------------------------------------------------------------------------------------------------------------------------------------
        # Samples acquisition -----------------------------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------------------------------------------
        if self.source == 'Serial':            
        # receive samples from board          
            # Unpacked Transmission 
            if ( self.settings.getPktComp() == const.UNPACKED ):     pkt_samples = self.board.receiveStrPkt()
            # Packed Transmission    
            else:   pkt_samples = self.board.receive()         
        #--------------------------------------------------------------------------------------------------------------------------------------------    
        elif self.source == 'Log':
            # receive samples from log
            if self.log_pos < self.textfile.getLogLength():
                pkt_samples = self.textfile.getLog(self.log_pos)
                self.log_pos += 1
            else:
                self.timer_capture.stop()
                self.ui_main.showCaptureUnClicked()
                AuxFunc.showMessage('Finish!', 'All data was plotted.')
                pkt_samples = []
        #--------------------------------------------------------------------------------------------------------------------------------------------                
        elif self.source == 'File':
            # receive samples csv file
            if self.log_pos < len(self.log):
                pkt_samples = self.log[self.log_pos]
                self.log_pos += 1
            else:
                self.timer_capture.stop()
                AuxFunc.showMessage('Finish!', 'All data was plotted.')
                pkt_samples = []
                self.ui_main.stopCaptureClicked()                
                
        #--------------------------------------------------------------------------------------------------------------------------------------------
        # Log of samples ----------------------------------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------------------------------------------
        
        # Checks if some sample was acquired and if this is a capture through the serial port.        
        if len(pkt_samples) and (self.source == 'Serial'):
            
            num_instants = 1
            # More than one instant for each request.
            if( self.settings.getPktComp() == const.PACKED ):    num_instants = self.board.unpacker.num_instants            
            
            # Sliding window of samples
            for instant_index in range(num_instants):
                # calculate the offset of the instant.
                instant_offset = self.settings.getTotChannels() * instant_index
                # save to log
                self.textfile.saveLog( self.log_id, pkt_samples[ instant_offset : ( instant_offset + self.settings.getTotChannels() ) ] ) 
                
        #--------------------------------------------------------------------------------------------------------------------------------------------
        # Display of samples ------------------------------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------------------------------------------

        # Checks if some sample was acquired.        
        if len(pkt_samples):
            
            # Debug: Displays the acquired samples on terminal.
            if(const.DEBUG):     print( "List of Samples: " + str(pkt_samples) )

            num_instants = 1
            # More than one instant for each request.
            if( self.settings.getPktComp() == const.PACKED and self.source == 'Serial' ):    num_instants = self.board.unpacker.num_instants
            
            # Sliding window of samples
            for instant_index in range(num_instants):
                    # calculate the offset of the instant.
                    instant_offset = self.settings.getTotChannels() * instant_index
                    # plot a instant of Samples                    
                    self.graph.plotSamples( np.array(  pkt_samples[ instant_offset : ( instant_offset + self.settings.getTotChannels() ) ] )  )
        #--------------------------------------------------------------------------------------------------------------------------------------------

    def syncBoard(self):              
        if self.board.getCommStatus() == True:            self.board.closeComm()
        self.board.openComm(self.ui_main.combo_port.currentText())
        # Communication test
        if self.board.stop() == 'ok':
            # Sets the waveform transmitted from the board
            if self.ui_main.action_sine.isChecked()      :   self.board.setSineWaveMode()
            elif self.ui_main.action_square.isChecked()  :   self.board.setSquareWaveMode()                
            elif self.ui_main.action_sawtooth.isChecked():   self.board.setSawtoothWaveMode()             
            else                                         :   self.board.setAdcMode()            
            self.board.setFucGenFreq(self.settings.getFuncGenFreq())
            self.board.setBitsPerSample(self.settings.getBitsPerSample())
            self.board.setChannelsperBoard(self.settings.getChannelsPerBoard())
            self.board.setNumAcquisBoards(self.settings.getNBoards())
            self.board.setPacketSize(self.settings.getPktSize())
            self.board.setSampleRate(self.settings.getSampleRate())
            self.board.setTransmissionMode( int( self.settings.getPktComp() ) )
            
            AuxFunc.showMessage('Warnig!', 'The Board on the ' + self.ui_main.combo_port.currentText()  + ' port was synchronized.' )
        else:
            AuxFunc.showMessage('Error!', 'The Board on the ' + self.ui_main.combo_port.currentText()  + ' did not be synchronized.' )        
                    
    def logIdGenerator(self):        
        name_cols = AuxFunc.patternStr('ch', self.settings.getTotChannels(), True)
        format = AuxFunc.patternStr('%d', self.settings.getTotChannels(), False)
        self.log_id = self.textfile.initFile(format, name_cols)                

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
            AuxFunc.showMessage('Error!', 'Insert an CSV capture file.')


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication([])    
    app.aboutToQuit.connect(app.deleteLater)
    win_main = WinMain()  
    win_main.show()
    app.exec()
    win_main.board.closeComm()
    app.quit()
