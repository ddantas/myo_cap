# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 23:07:26 2020

@author: Zero_Desktop
"""
from PyQt5 import QtWidgets
from UiMain import UiMain
from Settings import Settings
from WidgetGraph import WidgetGraph
import sys
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
from Tiva import Tiva
from TextFile import Textfile
from WinDisplaySettings import WinDisplaySettings
from WinCaptureSettings import WinCaptureSettings
from WinCommSettings import WinCommSettings
from WinFuncGenSettings import WinFuncGenSettings

class WinMain(QtWidgets.QMainWindow):


    def __init__(self):
    
        # supeclass constructor
        super(WinMain, self).__init__()

        # setup settings
        self.settings = Settings()
        self.settings.load()

        # setup graph widget
        self.graph = WidgetGraph(self.settings)

        # setup main user interface
        self.ui_main = UiMain(self, self.graph)
        
        # setup board
        self.board = Tiva(self.settings)

        # setup text file
        self.textfile = Textfile()

        self.setupWidgets()

        # Period of the Loop Timer
        self.loop_timer_period   = 0.001
            
        # Initialise the Loop Timer
        self.loop_timer = QtCore.QTimer()
        #self.loop_timer.setSingleShot(True)
        self.loop_timer.timeout.connect( self.main_loop )
        
        self.channel_index  = 0
        
        self.sample_index   = 0
        
        self.plots          = []
        
        # Display Buffer Matrix        
        self.display_buffer = np.zeros(shape=( self.settings.getShowChannels() * self.settings.getNBoards() , self.settings.getSwipe() ), dtype=float)
        
        # List of Plots. One for each channel.
        for channel_index in range( self.settings.getShowChannels() * self.settings.getNBoards() ):
            
            self.plots.append( self.graph.plot( self.display_buffer[channel_index] ) )
                         

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
        self.ui_main.action_sine.triggered.connect(self.setSine)
        self.ui_main.action_square.triggered.connect(self.setSquare)
        self.ui_main.action_sawtooth.triggered.connect(self.setSawtooth)

        self.ui_main.action_start_capture.setEnabled(False)
        self.ui_main.action_stop_capture.setEnabled(False)
        self.ui_main.action_show_capture.setEnabled(False)

        # setup buttons
        self.ui_main.button_select_file.clicked.connect(self.showWinSelectFile)
        self.ui_main.button_display_settings.clicked.connect(self.showWinDisplaySettings)
        self.ui_main.button_capture_settings.clicked.connect(self.showWinCaptureSettings)
        self.ui_main.button_start_capture.clicked.connect(self.startCapture)
        self.ui_main.button_stop_capture.clicked.connect(self.stopCapture)
        self.ui_main.button_show_capture.clicked.connect(self.showCapture)
        self.ui_main.button_select_file.setEnabled(False)
        self.ui_main.button_start_capture.setEnabled(False)
        self.ui_main.button_stop_capture.setEnabled(False)
        self.ui_main.button_show_capture.setEnabled(False)

        # setup combo box for serial ports
        self.ui_main.combo_port.setEnabled(False)
        for port in (self.board).listPorts():
            self.ui_main.combo_port.addItem(port)

        # setup combo box for data source
        self.ui_main.combo_data_source.currentIndexChanged.connect(self.changeDataSource)
        self.ui_main.combo_data_source.setCurrentIndex(-1)

        # setup informations about graph
        self.updateInfoGraph()

    def updateInfoGraph(self):
    
        self.ui_main.info_graph.setText(
            'Swipe: ' + str(self.settings.getSwipe()) + ' | Vmin: ' + str(self.settings.getVMin()) +
            ' | Vmax: ' + str(self.settings.getVMax()) + ' | Vtick: ' + str(self.settings.getVTick()) +
            ' | Htick: ' + str(self.settings.getHTick()) + ' | Show channels: ' + str(self.settings.getShowChannels()))

    def changeDataSource(self, index):

        if index != -1:
            # new buttons configuration
            self.ui_main.button_start_capture.setEnabled(True)
            self.ui_main.button_stop_capture.setEnabled(False)
            self.ui_main.button_show_capture.setEnabled(False)

            # new menu capture configuration
            self.ui_main.action_start_capture.setEnabled(True)
            self.ui_main.action_stop_capture.setEnabled(False)
            self.ui_main.action_show_capture.setEnabled(False)

        # for serial selection
        if index == 0:
            self.ui_main.combo_port.setEnabled(True)
            self.ui_main.button_select_file.setEnabled((False))

        # for file selection
        elif index == 1:
            self.ui_main.button_select_file.setEnabled(True)
            self.ui_main.combo_port.setEnabled(False)

    def loadSettings(self):
        self.settings.load()
        QtWidgets.QMessageBox.about(self, 'Settings loaded!', 'Settings loaded from ' + self.settings.getSettingsPath())
        self.graph.configureGraph()

    def saveSettings(self):
        self.settings.save()
        QtWidgets.QMessageBox.about(self, 'Settings stored!', 'Settings stored at ' + self.settings.getSettingsPath())

    def showWinDisplaySettings(self):
        self.win_display_settings = WinDisplaySettings(self, self.settings, self.graph)
        self.win_display_settings.show()

    def showWinCaptureSettings(self):
        self.win_capture_settings = WinCaptureSettings(self.settings)
        self.win_capture_settings.show()

    def showWinCommSettings(self):
        self.win_comm_settings = WinCommSettings(self.settings)
        self.win_comm_settings.show()

    def showWinFuncGenSettings(self):
        self.win_funcgen_settings = WinFuncGenSettings(self.settings)
        self.win_funcgen_settings.show()

    def showWinSelectFile(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '', 'All Files (*);;Python Files (*.py)', options=options)
        self.ui_main.action_show_capture.setEnabled(True)
        self.ui_main.button_show_capture.setEnabled(True)
        
#######################################################################################################################################################################################

    def main_loop(self):
                
         self.acquire_samples()       
         self.plot_disp_buffer()
         
                
    def plot_disp_buffer(self):
               
        if ( (self.sample_index + 1) % self.settings.getSwipe() ) == 0:
            
            self.sample_index = 0
         
            
        if ( (self.sample_index + 1) % 200 == 0):
                         
            for channel_index in range( self.settings.getShowChannels() * self.settings.getNBoards() ):
                
                # Plot the Channels
                #print('channel = ' + str(channel_index) )
                self.plots[channel_index].setData( self.display_buffer[channel_index] , pen=pg.mkPen('r', width=0.8) ) 
                            
         
    def acquire_samples(self):
                            
        num_channels   = self.settings.getShowChannels() * self.settings.getNBoards()
        received_pkt   = self.board.recvStringPkt( num_channels )
            
        if len( received_pkt ) == num_channels :
             
            for channel_index in range(num_channels):
            
                scaling_factor   = self.graph.num_ticks_ch / (2 ** self.settings.getBitsPerSample() - 1)
                amplitude_offset = channel_index * self.graph.num_ticks_ch
                self.display_buffer[channel_index][self.sample_index] = scaling_factor * received_pkt[channel_index] + amplitude_offset
                    
            self.sample_index += 1
            
        else:
        
            print(len( received_pkt ))
            QMessageBox.about(self, 'Error', 'Samples Missing.')
                
                
    def startCapture(self):
                
        # new capture menu configuration
        self.ui_main.action_start_capture.setEnabled(False)
        self.ui_main.action_stop_capture.setEnabled(True)

        # new buttons configuration
        self.ui_main.button_start_capture.setEnabled(False)
        self.ui_main.button_stop_capture.setEnabled(True)
        
        
        if self.board.getCommStatus() == False:
            self.board.openComm(self.ui_main.combo_port.currentText())


        # Sends a Start Command to the Board and Checks if it was accepted.
        if ( self.board.start() == 'ok' ):       
            
            # Start the Main Loop Timer
            self.loop_timer.start( self.loop_timer_period )
            print('inside')
            
            # Clear the List of Plots and the indexes
            self.channel_index  = 0     
            self.sample_index   = 0        
            self.plots          = []
            
            # Clear and Resize the Display Buffer. 
            self.display_buffer = np.zeros(shape=( self.settings.getShowChannels() * self.settings.getNBoards() , self.settings.getSwipe() ), dtype=float )
            
            # Resize and Reload the List of Plots. 
            for channel_index in range( self.settings.getShowChannels() * self.settings.getNBoards() ):
            
                self.plots.append( self.graph.plot( self.display_buffer[channel_index] ) )
            

            
            '''
            # Initialise the Log File
            num_cols = self.settings.getNBoards() * self.settings.getChannelsPerBoard()
            name_cols = self.patternStr('ch', True)
            format = self.patternStr('%d', False)
            self.log_id = self.textfile.initFile(num_cols, format, name_cols)
            '''
        
        else:            
                QMessageBox.about(self, 'Error', 'The Board did not Started.\nPlease try to Start again or Check the Conection with the Board.')
 

    def stopCapture(self):
        
        # Stop the Main Loop Timer
        self.loop_timer.stop()
             
        # Update the Buttons State
        if self.ui_main.combo_data_source.currentIndex() == 0:
            # new buttons configuration
            self.ui_main.button_start_capture.setEnabled(True)
            self.ui_main.button_stop_capture.setEnabled(False)

            # new capture menu configuration
            self.ui_main.action_start_capture.setEnabled(True)
            self.ui_main.action_stop_capture.setEnabled(False)
            
        elif self.ui_main.combo_data_source.currentIndex() == 1:
            # new buttons configuration
            self.ui_main.button_show_capture.setEnabled(True)
            self.ui_main.button_stop_capture.setEnabled(False)

            # new capture menu configuration
            self.ui_main.action_show_capture.setEnabled(True)
            self.ui_main.action_stop_capture.setEnabled(False)
            
        # Save the Log in the File
        # textfile.save()
            
        # Sends a Stop Command to the Board and Checks if it was accepted.
        self.board.stop() 
        #print( self.board.getSampleRate() )
    
        if ( self.board.stop() != 'ok' ):            
                QMessageBox.about(self, 'Error', 'The Board did not Stoped.\nPlease try to Stop again or Check the Conection with the Board.')
            

    def showCapture(self):
        # new buttons configuration
        self.ui_main.button_show_capture.setEnabled(False)
        self.ui_main.button_stop_capture.setEnabled(True)

        # new capture menu configuration
        self.ui_main.action_show_capture.setEnabled(False)
        self.ui_main.action_stop_capture.setEnabled(True)

    def setSine(self):
        if self.ui_main.action_sine.isChecked() == True:
            self.ui_main.action_square.setChecked(False)
            self.ui_main.action_sawtooth.setChecked(False)
            self.ui_main.button_start_capture.setEnabled(True)
            
            ###
            if self.board.getCommStatus() == False:
                self.board.openComm(self.ui_main.combo_port.currentText())
            
            # Sets the Wve Form to Sine
            self.board.setSineWaveMode()

    def setSquare(self):
        if self.ui_main.action_square.isChecked() == True:
            self.ui_main.action_sine.setChecked(False)
            self.ui_main.action_sawtooth.setChecked(False)
            self.ui_main.button_start_capture.setEnabled(True)
            
            ###
            if self.board.getCommStatus() == False:
                self.board.openComm(self.ui_main.combo_port.currentText())
            
            # Sets the Wve Form to Sine
            self.board.setSquareWaveMode()

    def setSawtooth(self):
        if self.ui_main.action_sawtooth.isChecked() == True:
            self.ui_main.action_square.setChecked(False)
            self.ui_main.action_sine.setChecked(False)
            
            ###
            if self.board.getCommStatus() == False:
                self.board.openComm(self.ui_main.combo_port.currentText())
                
            # Sets the Wve Form to Sine
            self.board.setSawtoothWaveMode()

    def patternStr(self, pattern, num_it, add_it):
        str_out = ''
        for i in range(num_it):
            str_out = str_out + pattern

            if add_it:
                str_out = str_out + str(i)

            if i < num_it - 1:
                str_out = str_out + ';'

        return str_out
    


    
        
if __name__ == "__main__":
    
    app = QtWidgets.QApplication([])    
    app.aboutToQuit.connect(app.deleteLater)
    win_main = WinMain()  
    win_main.show()
    app.exec()
    win_main.board.close()
    app.quit()
    #sys.exit(app.exec())
