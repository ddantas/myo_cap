# -*- coding: utf-8 -*-

import PyQt5

WIN_TITLE = 'LeapCap'

class UiMain:

    def __init__(self, win_main, graph):
        # window to design ui
        self.win_main = win_main
        #window size
        self.win_main.showMaximized()
        self.win_main.setMinimumWidth(1366)
        self.win_main.setMinimumHeight(768)
        #window name
        self.win_main.setWindowTitle(WIN_TITLE)
        #main widget
        self.central_widget = PyQt5.QtWidgets.QWidget()
        self.win_main.setCentralWidget(self.central_widget)
        #graph
        self.graph = graph
        #layout inicialization
        self.grid_widget = PyQt5.QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.grid_widget)
        #layout construction
        self.createMenuBar()
        self.createTaskBar()
        self.posWidgets()

    def createMenuBar(self):
        # create menubar object
        self.menu_bar = PyQt5.QtWidgets.QMenuBar()
        self.menu_bar.setEnabled(True)
        self.menu_bar.setNativeMenuBar(True)
        # sessions for menubar
        self.createMenuFile()
        self.createMenuCapture()
        self.createMenuSettings()
        self.createMenuFuncGen()
        # add sessions to menubar
        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_capture.menuAction())
        self.menu_bar.addAction(self.menu_settings.menuAction())
        self.menu_bar.addAction(self.menu_funcgen.menuAction())
        # set window menubar
        self.win_main.setMenuBar(self.menu_bar)

    def createMenuFile(self):
        # create menu file
        self.menu_file = PyQt5.QtWidgets.QMenu(self.menu_bar)
        self.menu_file.setTitle('File')
        # create options for menu file
        self.action_load_capture = PyQt5.QtWidgets.QAction('Load capture')
        self.action_save_capture = PyQt5.QtWidgets.QAction('Save capture')
        self.action_load_emg_signal = PyQt5.QtWidgets.QAction('Load EMG signal')
        self.action_exit = PyQt5.QtWidgets.QAction('Exit')
        # add options to menu file
        self.menu_file.addAction(self.action_load_capture)
        self.menu_file.addAction(self.action_save_capture)
        self.menu_file.addAction(self.action_load_emg_signal)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)

    def createMenuCapture(self):
        # create menu capture
        self.menu_capture = PyQt5.QtWidgets.QMenu(self.menu_bar)
        self.menu_capture.setTitle('Capture')
        # create options for menu capture
        self.action_subject_window = PyQt5.QtWidgets.QAction('Subject window')
        self.action_start_capture = PyQt5.QtWidgets.QAction('Start capture')
        self.action_stop_capture = PyQt5.QtWidgets.QAction('Stop capture')
        self.action_show_capture = PyQt5.QtWidgets.QAction('Show capture')
        # add options to menu capture
        self.menu_capture.addAction(self.action_subject_window)
        self.menu_capture.addSeparator()
        self.menu_capture.addAction(self.action_start_capture)
        self.menu_capture.addAction(self.action_stop_capture)
        self.menu_capture.addAction(self.action_show_capture)

    def createMenuSettings(self):
        # create menu settings
        self.menu_settings = PyQt5.QtWidgets.QMenu(self.menu_bar)
        self.menu_settings.setTitle('Settings')
        # create options for menu settings
        self.action_load_settings = PyQt5.QtWidgets.QAction('Load settings')
        self.action_save_settings = PyQt5.QtWidgets.QAction('Save settings')
        self.action_emg_capture_settings = PyQt5.QtWidgets.QAction('EMG capture settings')
        self.action_emg_display_settings = PyQt5.QtWidgets.QAction('EMG display settings')
        self.action_emg_comm_settings = PyQt5.QtWidgets.QAction('EMG communication settings')
        self.action_emg_emulation = PyQt5.QtWidgets.QAction('EMG emulation')
        self.action_gesture_capture_settings = PyQt5.QtWidgets.QAction('Gesture capture settings')
        # add options to menu settings
        self.menu_settings.addAction(self.action_load_settings)
        self.menu_settings.addAction(self.action_save_settings)
        self.menu_settings.addSeparator()
        self.menu_settings.addAction(self.action_emg_capture_settings)
        self.menu_settings.addAction(self.action_emg_display_settings)
        self.menu_settings.addAction(self.action_emg_comm_settings)
        self.menu_settings.addAction(self.action_emg_emulation)
        self.menu_settings.addSeparator()
        self.menu_settings.addAction(self.action_gesture_capture_settings)
        # set EMG emulation as checkable
        self.action_emg_emulation.setCheckable(True)
        
    def createMenuFuncGen(self):
        # create menu function generator
        self.menu_funcgen = PyQt5.QtWidgets.QMenu(self.menu_bar)
        self.menu_funcgen.setTitle('Function generator')
        # create options for menu function generator
        self.action_funcgen_settings = PyQt5.QtWidgets.QAction('Settings')
        self.action_sine = PyQt5.QtWidgets.QAction('Sine')
        self.action_square = PyQt5.QtWidgets.QAction('Square')
        self.action_sawtooth = PyQt5.QtWidgets.QAction('Sawtooth')
        self.action_stresstest = PyQt5.QtWidgets.QAction('Start stress test')
        # add options to menu function generator
        self.menu_funcgen.addAction(self.action_funcgen_settings)
        self.menu_funcgen.addSeparator()
        self.menu_funcgen.addAction(self.action_sine)
        self.menu_funcgen.addAction(self.action_square)
        self.menu_funcgen.addAction(self.action_sawtooth)
        self.menu_funcgen.addSeparator()
        self.menu_funcgen.addAction(self.action_stresstest)
        # set some options as checkable
        self.action_sine.setCheckable(True)
        self.action_square.setCheckable(True)
        self.action_sawtooth.setCheckable(True)    

    def createTaskBar(self):
        # create combo boxes for task bar
        self.createTaskBarComboBoxes()
        # create buttons for task bar
        self.createTaskBarButtons()
        # create label with graphic informations for task bar
        self.createTaskBarInfoGraph()

    def createTaskBarComboBoxes(self):
        # create data source combo box
        self.combo_data_source = PyQt5.QtWidgets.QComboBox()
        self.combo_data_source.setEditable(False)
        self.combo_data_source.addItem('Serial')
        self.combo_data_source.addItem('File')
        self.combo_data_source.setFixedWidth(60)
        # create port combo box
        self.combo_port = PyQt5.QtWidgets.QComboBox()        
        self.combo_port.setEditable(False)
        self.combo_port.setFixedWidth(150)

    def createTaskBarButtons(self):
        # create subject window button
        self.button_subject_window = PyQt5.QtWidgets.QPushButton()
        self.button_subject_window.setText('Subject window')
        # create start capture button
        self.button_start_capture = PyQt5.QtWidgets.QPushButton()
        self.button_start_capture.setText('Start capture')
        # create stop capture button
        self.button_stop_capture = PyQt5.QtWidgets.QPushButton()
        self.button_stop_capture.setText('Stop capture')
        # create show capture button
        self.button_show_capture = PyQt5.QtWidgets.QPushButton()
        self.button_show_capture.setText('Show capture')
        # create save button
        self.button_save_capture = PyQt5.QtWidgets.QPushButton()
        self.button_save_capture.setText('Save Capture')

    def createTaskBarInfoGraph(self):
        # create label to show graphic informations
        self.info_graph = PyQt5.QtWidgets.QLabel()
        self.info_graph.setText('Graphic informations')
        self.info_graph.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.info_graph.setFixedWidth(400)

    def updateInfoGraph(self, settings):
        self.info_graph.setText(            'Swipe: '    + str( settings.getSwipe() ) + ' | Vmin: '          + str( settings.getVMin() ) +
                                            ' | Vmax: '  + str( settings.getVMax() )  + ' | Vtick: '         + str( settings.getVTick() ) +
                                            ' | Htick: ' + str( settings.getHTick() ) + ' | Show channels: ' + str( settings.getTotChannels() ) )

    def posWidgets(self):
        # menu bar position
        self.grid_widget.setMenuBar(self.menu_bar)
        # task bar position
        taskbar_row = 0
        self.grid_widget.addWidget(self.combo_data_source, taskbar_row, 0)
        self.grid_widget.addWidget(self.combo_port, taskbar_row, 1,)
        self.grid_widget.addWidget(self.info_graph, taskbar_row, 2)
        self.grid_widget.addWidget(self.button_subject_window, taskbar_row, 3)
        self.grid_widget.addWidget(self.button_start_capture, taskbar_row, 4)
        self.grid_widget.addWidget(self.button_stop_capture, taskbar_row, 5)
        self.grid_widget.addWidget(self.button_save_capture, taskbar_row, 6)
        self.grid_widget.addWidget(self.button_show_capture, taskbar_row, 7)
        
        # graph position
        graph_row = 1
        graph_colspan = 10 # number of taskbar widgets
        self.grid_widget.addWidget(self.graph, graph_row, 0, 1, graph_colspan)

    def setupWidgets(self):
        # setup menu
        
        # menu file
        self.action_load_capture.triggered.connect(self.win_main.showWinSelectFile)
        self.action_exit.triggered.connect(self.win_main.close)
        self.action_save_capture.triggered.connect(self.win_main.saveCapture)
        self.action_load_emg_signal.triggered.connect(self.win_main.loadEMGSignal)
        
        #menu capture
        self.action_subject_window.triggered.connect(self.win_main.showSubjectWindow)
        
        self.action_start_capture.triggered.connect(self.win_main.startCapture)
        self.action_stop_capture.triggered.connect(self.win_main.stopCapture)
        self.action_show_capture.triggered.connect(self.win_main.showCapture)
        
        # menu settings
        self.action_load_settings.triggered.connect(self.win_main.loadSettings)
        self.action_save_settings.triggered.connect(self.win_main.saveSettings)
        
        self.action_emg_capture_settings.triggered.connect(self.win_main.showEMGWinCaptureSettings)
        self.action_emg_display_settings.triggered.connect(self.win_main.showEMGWinDisplaySettings)
        self.action_emg_comm_settings.triggered.connect(self.win_main.showEMGWinCommSettings)
        self.action_emg_emulation.triggered.connect(self.win_main.showEMGEmulation)
  
        self.action_gesture_capture_settings.triggered.connect(self.win_main.showGestureCaptureSettings)
        
        # menu function generator
        self.action_funcgen_settings.triggered.connect(self.win_main.showWinFuncGenSettings)
        self.action_sine.triggered.connect(self.win_main.setSine)
        self.action_square.triggered.connect(self.win_main.setSquare)
        self.action_sawtooth.triggered.connect(self.win_main.setSawtooth)
        self.action_stresstest.triggered.connect(self.win_main.showWinStresstest)
                        
        # setup buttons
        self.button_subject_window.clicked.connect(self.win_main.showSubjectWindow)
        self.button_start_capture.clicked.connect(self.win_main.startCapture)
        self.button_stop_capture.clicked.connect(self.win_main.stopCapture)
        self.button_show_capture.clicked.connect(self.win_main.showCapture)
        self.button_save_capture.clicked.connect(self.win_main.saveCapture)
                
        # setup graph configurations
        self.updateInfoGraph(self.win_main.leap_cap_settings)
        
        # setup combo box for serial ports
        for port in self.win_main.board.listPorts():        self.combo_port.addItem(port)            
    
        # Sync the Boar With the Interface Settings     
        self.combo_port.setCurrentIndex(-1)
        self.combo_port.currentIndexChanged.connect( self.win_main.syncBoard )            
        
    def startCaptureClicked(self):
        self.button_start_capture.setEnabled(False)
        self.action_start_capture.setEnabled(False)
        self.action_show_capture.setEnabled(False)
        self.button_show_capture.setEnabled(False)
        
    def stopCaptureClicked(self):
        self.button_start_capture.setEnabled(True)
        self.action_start_capture.setEnabled(True)
        self.action_show_capture.setEnabled(True)
        self.button_show_capture.setEnabled(True)
        
    def showCaptureClicked(self):
        self.button_start_capture.setEnabled(False)
        self.action_start_capture.setEnabled(False)
        self.button_stop_capture.setEnabled(False)
        self.action_stop_capture.setEnabled(False)
        self.button_save_capture.setEnabled(False)
        self.action_save_capture.setEnabled(False)
        self.action_show_capture.setEnabled(False)
        self.button_show_capture.setEnabled(False)        
        
    def showCaptureUnClicked(self):
        self.button_start_capture.setEnabled(True)
        self.action_start_capture.setEnabled(True)
        self.button_stop_capture.setEnabled(True)
        self.action_stop_capture.setEnabled(True)
        self.button_save_capture.setEnabled(True)
        self.action_save_capture.setEnabled(True)
        self.action_show_capture.setEnabled(True)
        self.button_show_capture.setEnabled(True)