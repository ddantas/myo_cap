# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

WIN_TITLE = 'Myograph'

class UiMain:

    def setupUi(self, win_main, graph):
        self.win_main = win_main

        #window size
        self.win_main.showMaximized()
        self.win_main.setMinimumWidth(1280)
        self.win_main.setMinimumHeight(600)

        #window name
        self.win_main.setWindowTitle(WIN_TITLE)

        #main widget
        self.central_widget = QtWidgets.QWidget()
        self.win_main.setCentralWidget(self.central_widget)

        #graph
        self.graph = graph

        #layout inicialization
        self.grid_widget = QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.grid_widget)

        #layout construction
        self.createMenuBar()
        self.createTaskBar()
        self.posWidgets()

    def createMenuBar(self):
        self.menu_bar = QtWidgets.QMenuBar()

        self.menu_bar.setEnabled(True)
        self.menu_bar.setNativeMenuBar(True)

        self.createMenuFile()
        self.createMenuCapture()
        self.createMenuSettings()

        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_capture.menuAction())
        self.menu_bar.addAction(self.menu_settings.menuAction())

        self.win_main.setMenuBar(self.menu_bar)

    def createMenuFile(self):
        self.menu_file = QtWidgets.QMenu(self.menu_bar)
        self.menu_file.setTitle("File")

        self.action_load_capture = QtWidgets.QAction('Load capture')
        self.action_save_capture = QtWidgets.QAction('Save capture')
        self.action_exit = QtWidgets.QAction('Exit')

        self.menu_file.addAction(self.action_load_capture)
        self.menu_file.addAction(self.action_save_capture)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)

    def createMenuCapture(self):
        self.menu_capture = QtWidgets.QMenu(self.menu_bar)
        self.menu_capture.setTitle("Capture")

        self.action_start_capture = QtWidgets.QAction('Start capture')
        self.action_stop_capture = QtWidgets.QAction('Stop capture')
        self.action_show_capture = QtWidgets.QAction('Show capture')

        self.menu_capture.addAction(self.action_start_capture)
        self.menu_capture.addAction(self.action_stop_capture)
        self.menu_capture.addAction(self.action_show_capture)

    def createMenuSettings(self):
        self.menu_settings = QtWidgets.QMenu(self.menu_bar)
        self.menu_settings.setTitle("Settings")

        self.action_load_settings = QtWidgets.QAction('Load settings')
        self.action_save_settings = QtWidgets.QAction('Save settings')
        self.action_capture_settings = QtWidgets.QAction('Capture settings')
        self.action_display_settings = QtWidgets.QAction('Display settings')

        self.menu_settings.addAction(self.action_load_settings)
        self.menu_settings.addAction(self.action_save_settings)
        self.menu_settings.addSeparator()
        self.menu_settings.addAction(self.action_capture_settings)
        self.menu_settings.addAction(self.action_display_settings)

    def createTaskBar(self):
        self.createTaskBarComboBoxes()
        self.createTaskBarButtons()
        self.createTaskBarInfoGraph()

    def createTaskBarComboBoxes(self):
        self.combo_data_source = QtWidgets.QComboBox()
        self.combo_port = QtWidgets.QComboBox()

        self.combo_data_source.setEditable(False)
        self.combo_port.setEditable(False)

        self.combo_data_source.addItem('Serial')
        self.combo_data_source.addItem('File')

        self.combo_data_source.setFixedWidth(75)
        self.combo_port.setFixedWidth(150)

    def createTaskBarButtons(self):
        self.button_select_file = QtWidgets.QPushButton()
        self.button_display_settings = QtWidgets.QPushButton()
        self.button_capture_settings = QtWidgets.QPushButton()
        self.button_start_capture = QtWidgets.QPushButton()
        self.button_stop_capture = QtWidgets.QPushButton()
        self.button_show_capture = QtWidgets.QPushButton()

        self.button_select_file.setText("Select file")
        self.button_display_settings.setText("Display settings")
        self.button_capture_settings.setText("Capture settings")
        self.button_start_capture.setText("Start capture")
        self.button_stop_capture.setText("Stop capture")
        self.button_show_capture.setText("Show capture")

    def createTaskBarInfoGraph(self):
        self.info_graph = QtWidgets.QLabel()

        self.info_graph.setText('Graphic informations')

        self.info_graph.setAlignment(QtCore.Qt.AlignCenter)
        self.info_graph.setFixedWidth(500)

    def posWidgets(self):
        #menu bar position
        self.grid_widget.setMenuBar(self.menu_bar)

        #task bar position
        taskbar_row = 0
        self.grid_widget.addWidget(self.combo_data_source, taskbar_row, 0)
        self.grid_widget.addWidget(self.combo_port, taskbar_row, 1,)
        self.grid_widget.addWidget(self.button_select_file, taskbar_row, 2)
        self.grid_widget.addWidget(self.button_display_settings, taskbar_row, 3)
        self.grid_widget.addWidget(self.button_capture_settings, taskbar_row, 4)
        self.grid_widget.addWidget(self.info_graph, taskbar_row, 5)
        self.grid_widget.addWidget(self.button_start_capture, taskbar_row, 6)
        self.grid_widget.addWidget(self.button_stop_capture, taskbar_row, 7)
        self.grid_widget.addWidget(self.button_show_capture, taskbar_row, 8)

        #graph position
        graph_row = 1
        graph_colspan = 9 #number of taskbar widgets
        self.grid_widget.addWidget(self.graph, graph_row, 0, 1, graph_colspan)