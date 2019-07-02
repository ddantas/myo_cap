from PyQt5 import QtGui, QtCore  # Import the PyQt4 module we'll need
import sys  # We need sys so that we can pass argv to QApplication
from win_main import Ui_MainWindow

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically

        self.actionStart_Capture.triggered.connect(self.widget.startCapture)
        self.actionStop_Capture.triggered.connect(self.widget.stopCapture)
        self.actionShow_Capture.triggered.connect(self.widget.showCapture)

        self.actionLoad_Capture.triggered.connect(self.widget.showInputFile)
        self.actionSave_Capture.triggered.connect(self.widget.storeLogData)
        # self.actionLoad_Settings.triggered.connect(self.widget.showInputFile)       
        # self.actionSave_Settings.triggered.connect(self.widget.showInputFile)

        self.actionDisplay_Settings.triggered.connect(self.widget.showDisplaySettings)
        self.actionCapture_Settings.triggered.connect(self.widget.showCaptureSettings)

if __name__ == '__main__':  # if we're running file directly and not importing it
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    window = MainWindow()  # We set the window to be our ExampleApp (design
    window.show()  # Show the window
    app.exec_()  # and execute the app
