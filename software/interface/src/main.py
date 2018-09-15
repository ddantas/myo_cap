from PyQt5 import QtGui, QtCore  # Import the PyQt4 module we'll need
import sys  # We need sys so that we can pass argv to QApplication
import threading
import time
# it also keeps events etc that we defined in Qt Designer
import os  # For listing directory methods

sys.path.append('./modules')
import design_Ui  # This file holds our MainWindow and all design related things


class ExampleApp(QtGui.QMainWindow, design_Ui.Ui_MainWindow):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
        #self.pushButton.clicked.connect(self.startLeap)        
        self.pushButton.clicked.connect(self.startKey)
	#self.settings_data = Settings().load()

    def keyPressEvent(self, event):
        super(ExampleApp, self).keyPressEvent(event)
        self.keyPressed.emit(event)

class main():
   
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()  # We set the form to be our ExampleApp (design)
    form.show()  # Show the form
    app.exec_()  # and execute the app

if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
