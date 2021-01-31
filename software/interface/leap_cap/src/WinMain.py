# -*- coding: utf-8 -*-

import os
import sys
# obtain the myograph path
myograph_import_path = os.path.split( os.path.split( os.path.split(os.path.abspath(__file__))[0] )[0] )[0]
# adds the myograph path for future inclusions 
sys.path.append(myograph_import_path)

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



class WinMain(PyQt5.QtWidgets.QMainWindow):

    def __init__(self):        
        # supeclass constructor
        super(WinMain, self).__init__()
        # setup LeapCap settings 
        self.leap_cap_settings = LeapCapSettings.LeapCapSettings()
        self.leap_cap_settings.load() 
        # setup graph widget
        self.graph = WidgetGraph.WidgetGraph(self.leap_cap_settings)
        # setup main user interface
        self.ui_main = UiMain.UiMain(self, self.graph)
        # setup board
        self.board = Tiva.Tiva(self.leap_cap_settings)
        # setup widgets
        self.setupWidgets()
        # setup main loop timer
        self.timer_main_loop = PyQt5.QtCore.QTimer()
        self.timer_main_loop.timeout.connect(self.mainLoop)
        self.timer_main_loop.start()  
        # subject windows is open
        self.subj_win_is_open = 0
                
        
    def setupWidgets(self):
        # setup menu
        
        # menu file
        self.ui_main.action_load_capture.triggered.connect(self.showWinSelectFile)
        self.ui_main.action_exit.triggered.connect(self.close)
        self.ui_main.action_save_capture.triggered.connect(self.saveCapture)
        self.ui_main.action_load_emg_signal.triggered.connect(self.loadEMGSignal)
        
        #menu capture
        self.ui_main.action_subject_window.triggered.connect(self.showSubjectWindow)
        
        self.ui_main.action_start_capture.triggered.connect(self.startCapture)
        self.ui_main.action_stop_capture.triggered.connect(self.stopCapture)
        self.ui_main.action_show_capture.triggered.connect(self.showCapture)
        
        # menu settings
        self.ui_main.action_load_settings.triggered.connect(self.loadSettings)
        self.ui_main.action_save_settings.triggered.connect(self.saveSettings)
        
        self.ui_main.action_emg_capture_settings.triggered.connect(self.showEMGWinCaptureSettings)
        self.ui_main.action_emg_display_settings.triggered.connect(self.showEMGWinDisplaySettings)
        self.ui_main.action_emg_comm_settings.triggered.connect(self.showEMGWinCommSettings)
        self.ui_main.action_emg_emulation.triggered.connect(self.showEMGEmulation)
  
        self.ui_main.action_gesture_capture_settings.triggered.connect(self.showGestureCaptureSettings)
        
        # menu function generator
        self.ui_main.action_funcgen_settings.triggered.connect(self.showWinFuncGenSettings)
        self.ui_main.action_sine.triggered.connect(self.setSine)
        self.ui_main.action_square.triggered.connect(self.setSquare)
        self.ui_main.action_sawtooth.triggered.connect(self.setSawtooth)
        self.ui_main.action_stresstest.triggered.connect(self.showWinStresstest)
        
                
        # setup buttons
        self.ui_main.button_subject_window.clicked.connect(self.showSubjectWindow)
        self.ui_main.button_start_capture.clicked.connect(self.startCapture)
        self.ui_main.button_stop_capture.clicked.connect(self.stopCapture)
        self.ui_main.button_show_capture.clicked.connect(self.showCapture)
        self.ui_main.button_save_capture.clicked.connect(self.saveCapture)
        
        
        # setup graph configurations
        self.updateInfoGraph()
        
        
        # setup combo box for serial ports
        for port in self.board.listPorts():
            self.ui_main.combo_port.addItem(port)
    
        # Sync the Boar With the Interface Settings     
        self.ui_main.combo_port.setCurrentIndex(-1)
        self.ui_main.combo_port.currentIndexChanged.connect( self.syncBoard )            

    def updateInfoGraph(self):
        self.ui_main.info_graph.setText(
            'Swipe: ' + str(self.leap_cap_settings.getSwipe()) + ' | Vmin: ' + str(self.leap_cap_settings.getVMin()) +
            ' | Vmax: ' + str(self.leap_cap_settings.getVMax()) + ' | Vtick: ' + str(self.leap_cap_settings.getVTick()) +
            ' | Htick: ' + str(self.leap_cap_settings.getHTick()) + ' | Show channels: ' + str(self.leap_cap_settings.getTotChannels()))
        
    # In development    
    def mainLoop(self):        
        # Get the key pressed and handle actions on the subject window
        if(self.subj_win_is_open):
            key_pressed = self.win_subject.getKey() 
            if((key_pressed == const.CLOSE_SUBJECT_WIN)):
                self.subj_win_is_open = 0
                del self.win_subject
            if( (key_pressed != const.NO_KEY_PRESSED) and (key_pressed != const.CLOSE_SUBJECT_WIN) ):
                 print('The key pressed was %s' % key_pressed)       

    def showWinSelectFile(self):
        self.source = self.ui_main.combo_data_source.currentText()
        if self.source == 'File':
            options = PyQt5.QtWidgets.QFileDialog.Options()
            options |= PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
            self.file_name, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Select capture file', '', 'CSV files (*.csv)', options=options)
            self.openCSV(self.file_name)
        else:
            AuxFunc.showMessage('Error!', 'Select FILE option first at the combo box.')  
    
    # to implement
    def openCSV(self, file_name):
        AuxFunc.showMessage('warning!', 'Will be implemented!')
    
    # to implement
    def saveCapture(self):
        AuxFunc.showMessage('warning!', 'Will be implemented!')

    # to implement                
    def loadEMGSignal(self):
        options = PyQt5.QtWidgets.QFileDialog.Options()
        options |= PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
        self.file_name, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Select EMG capture file', '', 'CSV files (*.csv)', options=options)
        self.openCSVEMG(self.file_name)        
        
    def openCSVEMG(file_name):
        AuxFunc.showMessage('warning!', 'Function in development!')
    
    def showSubjectWindow(self):        
        self.win_subject = WinSubject.WinSubject()
        self.win_subject.show()
        self.subj_win_is_open = 1

    # to check  
    def startCapture(self):      

        #AuxFunc.showMessage('warning!', 'Function in development!')
        '''   
        self.source = self.ui_main.combo_data_source.currentText()
        #self.graph.createPlots()
        if self.source == 'Serial':
            self.board.openComm(self.ui_main.combo_port.currentText())
            if self.board.test():               
                if self.board.start() == 'ok':
                    #self.logIdGenerator()
                    self.timer_capture.start(0)
                else:
                    AuxFunc.showMessage('Error!', 'Could not start capture!\nTry to start again or check the conection to the board.')
                    return -1
            else:
                AuxFunc.showMessage('Error!', 'Could not connect to the board!\nCheck the conection.')
        elif self.source == 'File':
            self.log_pos = 0
            self.timer_capture.start(1000.0/self.settings.getSampleRate())
        '''
        self.ui_main.button_start_capture.setEnabled(False)
        self.ui_main.action_start_capture.setEnabled(False)
        self.ui_main.action_show_capture.setEnabled(False)
        self.ui_main.button_show_capture.setEnabled(False)
        
    # to check    
    def stopCapture(self):        

        #AuxFunc.showMessage('warning!', 'Function in development!')
        '''
        # Stop the Timer
        self.timer_capture.stop()
        
        # Check if the Serial Port is open
        if self.board.getCommStatus():
            self.board.stop()
            if self.board.stop() == 'ok':   
        '''                                         
        self.ui_main.button_start_capture.setEnabled(True)
        self.ui_main.action_start_capture.setEnabled(True)
        self.ui_main.action_show_capture.setEnabled(True)
        self.ui_main.button_show_capture.setEnabled(True)   
        '''                                 
            else:
                AuxFunc.showMessage('Error!', 'Could not stop capture!\nTry to stop again or check the conection to the board.')
        '''
    # to check
    def showCapture(self):        
        AuxFunc.showMessage('warning!', 'Function in development!')
        
        '''
        self.source = 'Log'
        self.log_pos = 0
        self.graph.createPlots()
        self.timer_capture.start(1000.0/self.settings.getSampleRate())
        '''
           
    def loadSettings(self):
        if(self.leap_cap_settings.load()):
            AuxFunc.showMessage('Menssage of confirmation.', 'Settings were loaded!')
        else:
            AuxFunc.showMessage('warning!', 'Problem in load settings!')
    
    def saveSettings(self):
        if(self.leap_cap_settings.save()):
            AuxFunc.showMessage('Menssage of confirmation.', 'Settings were saved!')
        else:
            AuxFunc.showMessage('warning!', 'Problem in save settings!')

    # to check if it is possible do not pass graph as a parammeter to WinCaptureSettings
    def showEMGWinCaptureSettings(self):
        #self.stopCapture()
        self.win_emg_capture_settings = WinCaptureSettings.WinCaptureSettings(self.leap_cap_settings, self.graph, self.board)
        self.win_emg_capture_settings.show()  
        
    def showEMGWinDisplaySettings(self):
        self.win_emg_display_settings = WinDisplaySettings.WinDisplaySettings(self, self.leap_cap_settings, self.graph)
        self.win_emg_display_settings.show()

    def showEMGWinCommSettings(self):
        #self.stopCapture()
        self.win_emg_comm_settings = WinCommSettings.WinCommSettings(self.leap_cap_settings, self.board)
        self.win_emg_comm_settings.show()        
        
    def showEMGEmulation(self):
        AuxFunc.showMessage('warning!', 'Please load EMG signal by acessing menu File > Load EMG signal')
        AuxFunc.showMessage('warning!', 'Function in development!')
        
    def showGestureCaptureSettings(self):
        #self.stopCapture()
        self.win_gesture_cap_settings = WinGestureCapSettings.WinGestureCapSettings()
        self.win_gesture_cap_settings.show()
        
    def showWinFuncGenSettings(self):
        #self.stopCapture()
        self.win_funcgen_settings = WinFuncGenSettings.WinFuncGenSettings(self.leap_cap_settings, self.board)
        self.win_funcgen_settings.show()
        
    def setSine(self):
        #self.stopCapture()
        #uxFunc.showMessage('warning!', 'Function in development!')        
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
        #self.stopCapture()
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

 
    def showWinStresstest(self):
        #self.stopCapture()
        self.win_stress_test = WinStresstest.WinStresstest(self.leap_cap_settings, self.board, self)
        self.win_stress_test.show()

        
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
            
            
            
if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication([])    
    app.aboutToQuit.connect(app.deleteLater)
    win_main = WinMain()  
    win_main.show()
    app.exec()
    win_main.board.closeComm()
    app.quit()
