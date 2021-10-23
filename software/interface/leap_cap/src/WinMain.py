# -*- coding: utf-8 -*-

import os
import sys
# obtain the myograph path
MYOGRAPH_PATH = os.path.dirname( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
# adds the myograph path for future inclusions 
sys.path.append(MYOGRAPH_PATH)

import numpy as np
import datetime as dt
import PyQt5
import UiMain
import LeapCapSettings
import Tiva
import WinSubject
import WidgetGraph
import WinCaptureSettings
import WinDisplaySettings
import WinCommSettings
import WinGestureCapSettings
import WinFuncGenSettings
import WinStresstest
import AuxFunctions as AuxFunc
import Constants    as const
import Settings
import TextFile

LEAPCAP_SETTINGS_PATH  = os.path.join( MYOGRAPH_PATH, 'leap_cap', 'src', 'config', '')

class WinMain(PyQt5.QtWidgets.QMainWindow):

    def __init__(self):        
        # supeclass constructor
        super(WinMain, self).__init__()
        # setup LeapCap settings 
        self.leap_cap_settings = LeapCapSettings.LeapCapSettings()
        self.leap_cap_settings.load(LEAPCAP_SETTINGS_PATH, const.SETTINGS_FILE_NAME)
        # setup graph widget
        self.graph = WidgetGraph.WidgetGraph(self.leap_cap_settings)
        # setup main user interface
        self.ui_main = UiMain.UiMain(self, self.graph)
        # setup board
        self.board = Tiva.Tiva(self.leap_cap_settings)
        # setup text file
        self.textfile = TextFile.TextFile()
        # setup settings
        self.settings = Settings.Settings()
        self.settings.load(const.SETTINGS_PATH, const.SETTINGS_FILE_NAME)
        # setup widgets
        self.ui_main.setupWidgets()
        # setup subject window polling timer
        self.timer_win_subj_polling = PyQt5.QtCore.QTimer()
        self.timer_win_subj_polling.timeout.connect(self.winSubjGetKey)
        self.timer_win_subj_polling.start(100)  
        self.subj_win_is_open = 0
        # setup main loop timer
        self.timer_main_loop = PyQt5.QtCore.QTimer()
        self.timer_main_loop.timeout.connect(self.mainLoop)        
        # subject windows is open        


## File menu methods #############################################################################################################################

    # Probably it won't be implemented
    def openCSV(self, file_name):
        AuxFunc.showMessage('warning!', 'Will be implemented!')
    
    # Probably it won't be implemented
    def openCSVEMG(file_name):
        AuxFunc.showMessage('warning!', 'Function in development!')             

    def showWinSelectFile(self):
        self.source = self.ui_main.combo_data_source.currentText()
        if self.source == 'File':
            options = PyQt5.QtWidgets.QFileDialog.Options()
            options |= PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
            self.file_name, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Select capture file', '', 'CSV files (*.csv)', options=options)
            # Will change
            self.openCSV(self.file_name)
        else:
            AuxFunc.showMessage('Error!', 'Select FILE option first at the combo box.')  
            
    # to modify to accommodate the gesture devices needs.
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
        
    # To modify to be compliant with LeapCap log.
    def loadEMGSignal(self):
        self.source = self.ui_main.combo_data_source.currentText()
        if self.source == 'File':
            options = PyQt5.QtWidgets.QFileDialog.Options()
            options |= PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
            self.file_name, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Select capture file', '', 'CSV files (*.csv)', options=options)
            self.openCSV(self.file_name)
        else:   AuxFunc.showMessage('Error!', 'Select FILE option first at the combo box.')                

## Capture menu methods #############################################################################################################################

    def showSubjectWindow(self):                
        if(self.leap_cap_settings.getHand() == 'Left' ):    hand_chosen = WinSubject.LEFT_HAND      
        elif(self.leap_cap_settings.getHand() == 'Right'):  hand_chosen = WinSubject.RIGHT_HAND
        else:      AuxFunc.showMessage('warning!', 'Hand side not recognized!')
        # Will get the time step from the Settings
        time_step         = 50        
        routine_file_name = self.leap_cap_settings.getCaptureRoutine()
        self.win_subject  = WinSubject.WinSubject(routine_file_name, time_step, hand_chosen)
        self.win_subject.show()
        self.subj_win_is_open = 1

    # to check  
    def startCapture(self):           
        if(self.subj_win_is_open):     self.win_subject.startTimer() 
        self.source = self.ui_main.combo_data_source.currentText()
        self.graph.createPlots()
        #-----------------------------------------------------------------------------------------------------------------------------         
        if self.source == 'Serial':
            self.board.openComm(self.ui_main.combo_port.currentText())
            if self.board.test():               
                if self.board.start() == 'ok':
                    self.logIdGenerator()
                    self.timer_main_loop.start(0)
                else:      AuxFunc.showMessage('Error!', 'Could not start capture!\nTry to start again or check the conection to the board.');      return -1
            else:          AuxFunc.showMessage('Error!', 'Could not connect to the board!\nCheck the conection.')
        #-----------------------------------------------------------------------------------------------------------------------------
        elif self.source == 'File':
            self.log_pos = 0
            self.timer_main_loop.start(1000.0/self.settings.getSampleRate())        
        #-----------------------------------------------------------------------------------------------------------------------------
        self.ui_main.startCaptureClicked()
        
    # to check    
    def stopCapture(self):        
        # Stops the winsubject timer
        if(self.subj_win_is_open):     self.win_subject.stopTimer()
        # Stops the Timer
        self.timer_main_loop.stop()        
        # Check if the Serial Port is open
        if self.board.getCommStatus():
            self.board.stop()
            if self.board.stop() == 'ok':   self.ui_main.stopCaptureClicked()                                         
            else                        :   AuxFunc.showMessage('Error!', 'Could not stop capture!\nTry to stop again or check the conection to the board.')
            
    # to check
    def showCapture(self):
        self.source = 'Log'
        self.log_pos = 0
        self.graph.createPlots()
        self.timer_main_loop.start(1000.0/self.settings.getSampleRate())
        self.ui_main.showCaptureClicked()        
        
## Settings menu methods #############################################################################################################################

    def loadSettings(self):        
        if(self.leap_cap_settings.load(LEAPCAP_SETTINGS_PATH, const.SETTINGS_FILE_NAME)):   
                                             AuxFunc.showMessage('Menssage of confirmation.', 'Settings were loaded!');  self.graph.configureGraph()            
        else:                                AuxFunc.showMessage('warning!', 'Problem in loading settings!')
    
    def saveSettings(self):
        if(self.leap_cap_settings.save(LEAPCAP_SETTINGS_PATH, const.SETTINGS_FILE_NAME)):   
                                             AuxFunc.showMessage('Menssage of confirmation.', 'Settings were saved!')
        else:                                AuxFunc.showMessage('warning!', 'Problem in saving settings!')

    # to check if it is possible do not pass graph as a parammeter to WinCaptureSettings
    def showEMGWinCaptureSettings(self):
        self.stopCapture()
        self.win_emg_capture_settings = WinCaptureSettings.WinCaptureSettings(self.leap_cap_settings, self.graph, self.board)
        self.win_emg_capture_settings.show()  
        
    def showEMGWinDisplaySettings(self):
        self.win_emg_display_settings = WinDisplaySettings.WinDisplaySettings(self, self.leap_cap_settings, self.graph)
        self.win_emg_display_settings.show()

    def showEMGWinCommSettings(self):
        self.stopCapture()
        self.win_emg_comm_settings = WinCommSettings.WinCommSettings(self.leap_cap_settings, self.board)
        self.win_emg_comm_settings.show()        
        
    def showEMGEmulation(self):
        AuxFunc.showMessage('warning!', 'Please load EMG signal by acessing menu File > Load EMG signal')
        AuxFunc.showMessage('warning!', 'Function in development!')
        
    def showGestureCaptureSettings(self):
        self.stopCapture()
        self.win_gesture_cap_settings = WinGestureCapSettings.WinGestureCapSettings(self.leap_cap_settings)
        self.win_gesture_cap_settings.show()

## Function generator menu methods ##################################################################################################################

    def showWinFuncGenSettings(self):
        self.stopCapture()
        self.win_funcgen_settings = WinFuncGenSettings.WinFuncGenSettings(self.leap_cap_settings, self.board)
        self.win_funcgen_settings.show()
        
    def setSine(self):                
        if self.board.getCommStatus() == False:             self.board.openComm(self.ui_main.combo_port.currentText())
        self.stopCapture()            
        if self.ui_main.action_sine.isChecked() == True:    self.board.setSineWaveMode();   self.ui_main.sineWaveClicked()
        else:                                               self.board.setAdcMode();                        

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
        #self.stopCapture()
        self.win_stress_test = WinStresstest.WinStresstest(self.leap_cap_settings, self.board, self)
        self.win_stress_test.show()
        
## Application methods #############################################################################################################################

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
            self.board.setFucGenFreq(self.leap_cap_settings.getFuncGenFreq())
            self.board.setBitsPerSample(self.leap_cap_settings.getBitsPerSample())
            self.board.setChannelsperBoard(self.leap_cap_settings.getChannelsPerBoard())
            self.board.setNumAcquisBoards(self.leap_cap_settings.getNBoards())
            self.board.setPacketSize(self.leap_cap_settings.getPktSize())
            self.board.setSampleRate(self.leap_cap_settings.getSampleRate())
            self.board.setTransmissionMode( int( self.leap_cap_settings.getPktComp() ) )
            
            AuxFunc.showMessage('Warnig!', 'The Board on the ' + self.ui_main.combo_port.currentText()  + ' port was synchronized.' )
        else:
            AuxFunc.showMessage('Error!', 'The Board on the ' + self.ui_main.combo_port.currentText()  + ' did not be synchronized.' )    

    # Get the key pressed and handle actions on the subject window.
    # This Method need to be constantly called to keep the subject window alive.
    def winSubjGetKey(self):
        if(self.subj_win_is_open):
            key_pressed = self.win_subject.getKey() 
            if((key_pressed == const.CLOSE_SUBJECT_WIN)):
                self.subj_win_is_open = 0
                del self.win_subject
            if( (key_pressed != const.NO_KEY_PRESSED) and (key_pressed != const.CLOSE_SUBJECT_WIN) ):
                 print('The key pressed was %s' % key_pressed)

    def logIdGenerator(self):        
        name_cols = AuxFunc.patternStr('ch', self.settings.getTotChannels(), True)
        format = AuxFunc.patternStr('%d', self.settings.getTotChannels(), False)
        self.log_id = self.textfile.initFile(format, name_cols)   
        
    # In development    
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
                self.timer_main_loop.stop()
                self.ui_main.showCaptureUnClicked()
                AuxFunc.showMessage('Finish!', 'All data was plotted.')
                pkt_samples = []
        #--------------------------------------------------------------------------------------------------------------------------------------------                
        elif self.source == 'File':
            # receive samples csv file
            if self.log_pos < self.textfile.getLogLength():
                pkt_samples = self.textfile.getLog(self.log_pos)
                self.log_pos += 1
            else:
                self.timer_capture.stop()
                self.ui_main.stopCaptureClicked()
                AuxFunc.showMessage('Finish!', 'All data was plotted.')
                pkt_samples = []                
                
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
               
        

## Main file code #############################################################################################################################

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication([])    
    app.aboutToQuit.connect(app.deleteLater)
    win_main = WinMain()  
    win_main.show()
    app.exec()
    win_main.board.closeComm()
    app.quit()
