# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from UiMain import UiMain
from WinDisplaySettings import WinDisplaySettings
from WinCaptureSettings import WinCaptureSettings
from WinFuncGenSettings import WinFuncGenSettings
from SerialPort import SerialPort
from Settings import Settings
from WidgetGraph import WidgetGraph
import sys

class WinMain(QtWidgets.QMainWindow):

    def __init__(self):
        # supeclass constructor
        super(WinMain, self).__init__()

        # setup main user interface
        self.ui_main = UiMain()

        self.settings = Settings()
        self.settings.load()

        self.graph = WidgetGraph(self.settings)
        self.ui_main.setupUi(self, self.graph)

        self.ser_port = SerialPort()

        self.setupWidgets()

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
        for port in self.ser_port.listPorts():
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

    def showWinFuncGenSettings(self):
        self.win_funcgen_settings = WinFuncGenSettings(self.settings)
        self.win_funcgen_settings.show()

    def showWinSelectFile(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '', 'All Files (*);;Python Files (*.py)', options=options)
        self.ui_main.action_show_capture.setEnabled(True)
        self.ui_main.button_show_capture.setEnabled(True)

    def startCapture(self):
        # new capture menu configuration
        self.ui_main.action_start_capture.setEnabled(False)
        self.ui_main.action_stop_capture.setEnabled(True)

        # new buttons configuration
        self.ui_main.button_start_capture.setEnabled(False)
        self.ui_main.button_stop_capture.setEnabled(True)

    def stopCapture(self):
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

    def setSquare(self):
        if self.ui_main.action_square.isChecked() == True:
            self.ui_main.action_sine.setChecked(False)
            self.ui_main.action_sawtooth.setChecked(False)
            self.ui_main.button_start_capture.setEnabled(True)

    def setSawtooth(self):
        if self.ui_main.action_sawtooth.isChecked() == True:
            self.ui_main.action_square.setChecked(False)
            self.ui_main.action_sine.setChecked(False)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win_main = WinMain()
    win_main.show()
    sys.exit(app.exec())