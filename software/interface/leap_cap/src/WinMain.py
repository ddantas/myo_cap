# -*- coding: utf-8 -*-

import os
import sys
# obtain the myograph path
myograph_import_path = os.path.split( os.path.split( os.path.split(os.path.abspath(__file__))[0] )[0] )[0]
print(myograph_import_path)
# adds the myograph path for future inclusions 
sys.path.append(myograph_import_path)


import PyQt5
import UiMain
import Settings
import Tiva
import WinCaptureSettings
import WinDisplaySettings
import WinCommSettings
import AuxFunctions as AuxFunc



class WinMain(PyQt5.QtWidgets.QMainWindow):

    def __init__(self):
        
        # supeclass constructor
        super(WinMain, self).__init__()
        # setup settings 
        self.settings = Settings.Settings()
        self.settings.load()
        # setup main user interface
        self.ui_main = UiMain.UiMain(self)
        # setup board
        self.board = Tiva.Tiva(self.settings)
        # setup widgets
        self.setupWidgets()
        # setup timer
        self.timer_capture = PyQt5.QtCore.QTimer()
        self.timer_capture.timeout.connect(self.mainLoop)
        

    def setupWidgets(self):
        # setup menu
        
        # menu file
        self.ui_main.action_load_capture.triggered.connect(self.showWinSelectFile)
        self.ui_main.action_exit.triggered.connect(self.close)
        self.ui_main.action_save_capture.triggered.connect(self.saveCapture)
        self.ui_main.action_load_emg_signal.triggered.connect(self.loadEMGSignal)
        
        #menu capture
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
                
        # setup buttons
        self.ui_main.button_select_file.clicked.connect(self.showWinSelectFile)
        self.ui_main.button_capture_settings.clicked.connect(self.showEMGWinCaptureSettings)
        self.ui_main.button_display_settings.clicked.connect(self.showEMGWinDisplaySettings)

        self.ui_main.button_start_capture.clicked.connect(self.startCapture)
        self.ui_main.button_stop_capture.clicked.connect(self.stopCapture)
        self.ui_main.button_show_capture.clicked.connect(self.showCapture)
        self.ui_main.button_save_capture.clicked.connect(self.saveCapture)
        
        # setup combo box for serial ports
        for port in self.board.listPorts():
            self.ui_main.combo_port.addItem(port)
    
        # Sync the Boar With the Interface Settings     
        self.ui_main.combo_port.setCurrentIndex(-1)
        self.ui_main.combo_port.currentIndexChanged.connect( self.syncBoard )            


    # To implement    
    def mainLoop(self):
        pass

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
        AuxFunc.showMessage('warning!', 'Will be implemented!')

    # to check  
    def startCapture(self):
           
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
        
        self.ui_main.button_start_capture.setEnabled(False)
        self.ui_main.action_start_capture.setEnabled(False)
        self.ui_main.action_show_capture.setEnabled(False)
        self.ui_main.button_show_capture.setEnabled(False)
        
    # to check    
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

    # to check
    def showCapture(self):
        self.source = 'Log'
        self.log_pos = 0
        #self.graph.createPlots()
        self.timer_capture.start(1000.0/self.settings.getSampleRate())
           
    # to implement    
    def loadSettings(self):
        AuxFunc.showMessage('warning!', 'Will be implemented!')
    
    # to implement
    def saveSettings(self):
        AuxFunc.showMessage('warning!', 'Will be implemented!')

    # to check if it is possible do not pass graph as a parammeter to WinCaptureSettings
    def showEMGWinCaptureSettings(self):
        self.stopCapture()
        self.win_capture_settings = WinCaptureSettings.WinCaptureSettings(self.settings, self.graph, self.board)
        self.win_capture_settings.show()  

    # to check if it is possible do not pass graph as a parammeter to WinDisplaySettings
    def showEMGWinDisplaySettings(self):
        self.win_display_settings = WinDisplaySettings.WinDisplaySettings(self, self.settings, self.graph)
        self.win_display_settings.show()

    def showEMGWinCommSettings(self):
        self.stopCapture()
        self.win_comm_settings = WinCommSettings.WinCommSettings(self.settings, self.board)
        self.win_comm_settings.show()        
        
    # to implement        
    def showEMGEmulation(self):
        AuxFunc.showMessage('warning!', 'Please load EMG signal by acessing menu File > Load EMG signal')
        AuxFunc.showMessage('warning!', 'Will be implemented!')
        
    # to implement
    def showGestureCaptureSettings(self):
        AuxFunc.showMessage('warning!', 'Will be implemented!')
 
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
