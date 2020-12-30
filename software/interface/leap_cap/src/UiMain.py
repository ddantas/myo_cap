# -*- coding: utf-8 -*-

import PyQt5

WIN_TITLE = 'LeapCap'

class UiMain:

    def __init__(self, win_main):
        # window to design ui
        self.win_main = win_main
        #window size
        self.win_main.showMaximized()
        self.win_main.setMinimumWidth(1368)
        self.win_main.setMinimumHeight(768)
        #window name
        self.win_main.setWindowTitle(WIN_TITLE)
        #main widget
        self.central_widget = PyQt5.QtWidgets.QWidget()
        self.win_main.setCentralWidget(self.central_widget)
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
        # add sessions to menubar
        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_capture.menuAction())
        self.menu_bar.addAction(self.menu_settings.menuAction())
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
        self.action_start_capture = PyQt5.QtWidgets.QAction('Start capture')
        self.action_stop_capture = PyQt5.QtWidgets.QAction('Stop capture')
        self.action_show_capture = PyQt5.QtWidgets.QAction('Show capture')
        # add options to menu capture
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
        # create select file button
        self.button_select_file = PyQt5.QtWidgets.QPushButton()
        self.button_select_file.setText('Select file')
        # create display settings button
        self.button_display_settings = PyQt5.QtWidgets.QPushButton()
        self.button_display_settings.setText('Display settings')
        # create capture settings button
        self.button_capture_settings = PyQt5.QtWidgets.QPushButton()
        self.button_capture_settings.setText('Capture settings')
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

    def posWidgets(self):
        # menu bar position
        self.grid_widget.setMenuBar(self.menu_bar)
        # task bar position
        taskbar_row = 0
        self.grid_widget.addWidget(self.combo_data_source, taskbar_row, 0)
        self.grid_widget.addWidget(self.combo_port, taskbar_row, 1,)
        self.grid_widget.addWidget(self.button_select_file, taskbar_row, 2)
        self.grid_widget.addWidget(self.button_display_settings, taskbar_row, 3)
        self.grid_widget.addWidget(self.button_capture_settings, taskbar_row, 4)
        self.grid_widget.addWidget(self.info_graph, taskbar_row, 5)
        self.grid_widget.addWidget(self.button_start_capture, taskbar_row, 6)
        self.grid_widget.addWidget(self.button_stop_capture, taskbar_row, 7)
        self.grid_widget.addWidget(self.button_save_capture, taskbar_row, 8)
        self.grid_widget.addWidget(self.button_show_capture, taskbar_row, 9)
        
        # create temp label 
        self.fill_later = PyQt5.QtWidgets.QLabel()
        self.fill_later.setText('Fill later')
        self.fill_later.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        fill_later_row = 1
        fill_later_colspan = 10 # number of taskbar widgets
        self.grid_widget.addWidget(self.fill_later, fill_later_row, 0, 1, fill_later_colspan)