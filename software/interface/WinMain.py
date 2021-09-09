# -*- coding: utf-8 -*-

#import time
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
        self.ui_main.action_stresstest.triggered.connect(self.showWinStresstest)
        self.ui_main.action_sine.triggered.connect(self.setSine)
        self.ui_main.action_square.triggered.connect(self.setSquare)
        self.ui_main.action_sawtooth.triggered.connect(self.setSawtooth)
        self.ui_main.action_load_capture.triggered.connect(self.showWinSelectFile)
        self.ui_main.action_save_capture.triggered.connect(self.saveCapture)
        # setup buttons
        self.ui_main.button_select_file.clicked.connect(self.showWinSelectFile)
        self.ui_main.button_display_settings.clicked.connect(self.showWinDisplaySettings)
        self.ui_main.button_capture_settings.clicked.connect(self.showWinCaptureSettings)
        self.ui_main.button_start_capture.clicked.connect(self.startCapture)
        self.ui_main.button_stop_capture.clicked.connect(self.stopCapture)
        self.ui_main.button_show_capture.clicked.connect(self.showCapture)
        self.ui_main.button_save_capture.clicked.connect(self.saveCapture)
                
        # setup combo box for serial ports
        for port in self.board.listPorts():      self.ui_main.combo_port.addItem(port)
        
        # Sync the Boar With the Interface Settings     
        # Uncomment the Next two Lines
        self.ui_main.combo_port.setCurrentIndex(-1)
        self.ui_main.combo_port.currentIndexChanged.connect( self.syncBoard )
        # Comment the Next Line
        #self.board.openComm('COM3')
        #self.sync_board_settings ()

        # setup graph configurations
        self.updateInfoGraph()

    def updateInfoGraph(self):
        self.ui_main.info_graph.setText(
            'Swipe: ' + str(self.settings.getSwipe()) + ' | Vmin: ' + str(self.settings.getVMin()) +
            ' | Vmax: ' + str(self.settings.getVMax()) + ' | Vtick: ' + str(self.settings.getVTick()) +
            ' | Htick: ' + str(self.settings.getHTick()) + ' | Show channels: ' + str(self.settings.getTotChannels()))

    def loadSettings(self):
        if self.settings.load():
            AuxFunc.showMessage('Settings loaded!', 'Settings loaded from ' + self.settings.getSettingsPath())
            self.graph.configureGraph()
        else:
            AuxFunc.showMessage('Error!', 'Insert an valid settings file at: ' + Settings.SETTINGS_PATH)

    def saveSettings(self):
        if self.settings.save():
            AuxFunc.showMessage('Settings stored!', 'Settings stored at: ' + self.settings.getSettingsPath())
        else:
            AuxFunc.showMessage('Error!', 'Check the path ' + Settings.SETTINGS_PATH)

    def showWinDisplaySettings(self):
        self.win_display_settings = WinDisplaySettings.WinDisplaySettings(self, self.settings, self.graph)
        self.win_display_settings.show()

    def showWinCaptureSettings(self):
        self.stopCapture()
        self.win_capture_settings = WinCaptureSettings.WinCaptureSettings(self.settings, self.graph, self.board)
        self.win_capture_settings.show()

    def showWinCommSettings(self):
        self.stopCapture()
        self.win_comm_settings = WinCommSettings.WinCommSettings(self.settings, self.board)
        self.win_comm_settings.show()

    def showWinFuncGenSettings(self):
        self.stopCapture()
        self.win_funcgen_settings = WinFuncGenSettings.WinFuncGenSettings(self.settings, self.board)
        self.win_funcgen_settings.show()

    def showWinStresstest(self):
        self.stopCapture()
        self.win_stress_test = WinStresstest.WinStresstest(self.settings, self.board, self)
        self.win_stress_test.show()

    def showWinSelectFile(self):
        self.source = self.ui_main.combo_data_source.currentText()
        if self.source == 'File':
            options = PyQt5.QtWidgets.QFileDialog.Options()
            options |= PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
            self.file_name, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Select capture file', '', 'CSV files (*.csv)', options=options)
            self.openCSV(self.file_name)
        else:
            AuxFunc.showMessage('Error!', 'Select FILE option first at the combo box.')                

    def showCapture(self):
        self.source = 'Log'
        self.log_pos = 0
        self.graph.createPlots()
        self.timer_capture.start(1000.0/self.settings.getSampleRate())

    def startCapture(self):
           
        self.source = self.ui_main.combo_data_source.currentText()
        self.graph.createPlots()
        if self.source == 'Serial':
            self.board.openComm(self.ui_main.combo_port.currentText())
            if self.board.test():               
                if self.board.start() == 'ok':
                    self.logIdGenerator()
                    self.timer_capture.start(0)
                else:
                    AuxFunc.showMessage('Error!', 'Could not start capture!\nTry to start again or check the conection to the board.')
                    return -1
            else:
                AuxFunc.showMessage('Error!', 'Could not connect to the board!\nCheck the conection.')
        elif self.source == 'File':
            self.log_pos = 0
            self.timer_capture.start(1000.0/self.settings.getSampleRate())
        
        self.ui_main.button_start_capture.setEnabled(False)
        self.ui_main.action_start_capture.setEnabled(False)
        self.ui_main.action_show_capture.setEnabled(False)
        self.ui_main.button_show_capture.setEnabled(False)
        
        
    def stopCapture(self):
        
        # Stop the Timer
        self.timer_capture.stop()
        
        # Check if the Serial Port is open
        if self.board.getCommStatus():
            self.board.stop()
            if self.board.stop() == 'ok':   
                                         
                self.ui_main.button_start_capture.setEnabled(True)
                self.ui_main.action_start_capture.setEnabled(True)
                self.ui_main.action_show_capture.setEnabled(True)
                self.ui_main.button_show_capture.setEnabled(True)   
                                         
            else:
                AuxFunc.showMessage('Error!', 'Could not stop capture!\nTry to stop again or check the conection to the board.')

    def saveCapture(self):
        
        # Checks if a Start Capture was alredy executed
        if( hasattr(self, 'log_id') ):
            self.stopCapture()
            self.file_name = self.writeHeader()
            self.textfile.saveFile_Old(self.file_name)
            AuxFunc.showMessage('Capture saved!', self.file_name)
        
        else:
            AuxFunc.showMessage('Error!', 'Before Save a Capture into a File you should Start one Capture using the Serial Port.')
     
    
    def mainLoop(self):
        
        if self.source == 'Serial':
            
        # receive samples from board          
            # Unpacked Transmission 
            if ( int( self.settings.getPktComp() ) == const.UNPACKED ):                         
                pkt_samples = self.board.receiveStrPkt()
            # Packed Transmission    
            else:                         
                pkt_samples = self.board.receive()         
            
        elif self.source == 'Log':
            # receive samples from log
            if self.log_pos < self.textfile.getLogLength():
                pkt_samples = self.textfile.getLog(self.log_pos)
                self.log_pos += 1
            else:
                self.timer_capture.stop()
                AuxFunc.showMessage('Finish!', 'All data was plotted.')
                pkt_samples = []
        else:
            # receive samples csv file
            if self.log_pos < len(self.log):
                pkt_samples = self.log[self.log_pos]
                self.log_pos += 1
            else:
                self.timer_capture.stop()
                AuxFunc.showMessage('Finish!', 'All data was plotted.')
                pkt_samples = []
                self.ui_main.button_start_capture.setEnabled(True)
                self.ui_main.action_start_capture.setEnabled(True)
                self.ui_main.action_show_capture.setEnabled(True)
                self.ui_main.button_show_capture.setEnabled(True)
                        
        # Check if some Sample was Acquired        
        if len(pkt_samples):
            
            if(const.DEBUG):
                print( "List of Samples: " + str(pkt_samples) )
            
            if (  ( int( self.settings.getPktComp() ) == const.PACKED ) and (self.source == 'Serial')  ):
                
                # send samples from packet to graph
                for instant_index in range(self.board.unpacker.num_instants):
                    
                    # calculate the offset of the instant.
                    instant_offset = self.settings.getTotChannels() * instant_index
                    
                    # save to log
                    self.textfile.saveLog( self.log_id, pkt_samples[ instant_offset : ( instant_offset + self.settings.getTotChannels() ) ] ) 
                    
                    # plot a instant of Samples                    
                    self.graph.plotSamples( np.array(  pkt_samples[ instant_offset : ( instant_offset + self.settings.getTotChannels() ) ] )  )
                    
            # When reading from a File or a Log, the Samples are ploted in a batch with (total number of channels) long.
            else:
                    if self.source == 'Serial':
                        # save to log
                        self.textfile.saveLog(self.log_id, pkt_samples)
                    
                    # Plot a instant of Sample
                    self.graph.plotSamples( np.array( pkt_samples)  )
                

    def syncBoard(self):      
        
        if self.board.getCommStatus() == True:
            self.board.closeComm()

        self.board.openComm(self.ui_main.combo_port.currentText())

        
        if self.board.stop() == 'ok':
            if self.ui_main.action_sine.isChecked():
                self.board.setSineWaveMode()
            elif self.ui_main.action_square.isChecked():
                self.board.setSquareWaveMode()
            elif self.ui_main.action_sawtooth.isChecked():
                self.board.setSawtoothWaveMode()
            else:
                self.board.setAdcMode()

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
            
            
    def logIdGenerator(self):
        
        name_cols = AuxFunc.patternStr('ch', self.settings.getTotChannels(), True)
        format = AuxFunc.patternStr('%d', self.settings.getTotChannels(), False)
        self.log_id = self.textfile.initFile(format, name_cols)
                

    def writeHeader(self):
        
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
