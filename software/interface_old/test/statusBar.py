import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class statusdemo(QMainWindow):
   def __init__(self, parent = None):
      super(statusdemo, self).__init__(parent)
		
      bar = self.menuBar()
      file = bar.addMenu("File")
      file.addAction("show")
      file.addAction("add")
      file.addAction("remove")
      file.triggered[QAction].connect(self.processtrigger)
      self.setCentralWidget(QTextEdit())
		
      self.statusBar = QStatusBar()
      self.b = QPushButton("click here")
      self.setWindowTitle("QStatusBar Example")
      self.setStatusBar(self.statusBar)
      self.statusBar.showMessage("Channels: 4 | Swipe: 500 ~ 0,5 | Zero: 128 | Amplitude: 3,3 V | hTick: 100 ~ 0,1s | vTick 1,0 V")

   def processtrigger(self,q):
	
      if (q.text() == "show"):
         self.statusBar.showMessage("Channels: 4 | Swipe: 500 ~ 0,5 | Zero: 128 | Amplitude: 3,3 V | hTick: 100 ~ 0,1s | vTick 1,0 V")
			
      if q.text() == "add":
         self.statusBar.addWidget(self.b)
			
      if q.text() == "remove":
         self.statusBar.removeWidget(self.b)
         self.statusBar.show()
			
def main():
   app = QApplication(sys.argv)
   ex = statusdemo()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()

