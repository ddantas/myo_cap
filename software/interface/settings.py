from win_capture_settings import Ui_CaptureSettingsWindow
from win_display_settings import Ui_DisplaySettingsWindow
from pyqtgraph.Qt import QtCore, QtGui

class Settings(QtGui.QMainWindow):
    def __init__(self, window):
        QtGui.QMainWindow.__init__(self)
        
        self.settings_file = open("config/settings", "r")
        self.settings_out = self.settings_file.readlines()
        self.settings_data = self.load()
        self.window = window

    def load(self):
        try:
            data = {}
            for line in self.settings_out:
                if (line[1] == " "):
                    line = line.replace(":", "").split(" ")
                    data[str(line[1])] = float(line[2])
            return data
        except IOError:
            if(type == capture_file): data = [2000, 4, 1, 12]
            else: data = [1000, 0.0, 1.0, 100.0, -2.0, 2.0]
            return data

      # show capture settings
    
    # def capture(self):
    #     self.ui_caps = Ui_CaptureSettingsWindow()
    #     self.ui_caps.setupUi(self)

    #     # set capture data
    #     self.ui_caps.input_sampleR.setText(str(self.settings_data['sampleRate']))
    #     self.ui_caps.input_ch.setText(str(self.settings_data['channelsPerBoard']))
    #     self.ui_caps.input_numofboards.setText(str(self.settings_data['nBoards']))
    #     self.ui_caps.input_bits.setText(str(self.settings_data['bitsPerSample']))
    #     # init actions
    #     self.ui_caps.button_save.clicked.connect(self.storeCaptureSettings)
    #     self.ui_caps.button_cancel.clicked.connect(self.window.close)
    #     # self.stopTimer()
    #     self.window.show()

    # # show display settings
    # def display(self):
    #     self.ui_display = Ui_DisplaySettingsWindow()
    #     self.ui_display.setupUi(self)
    #     # set data
    #     self.ui_display.input_swipe.setText(str(self.settings_data['swipeSamples']))
    #     self.ui_display.input_zero.setText(str(self.settings_data['zero']))
    #     self.ui_display.input_vtick.setText(str(self.settings_data['vertTick']))
    #     self.ui_display.input_htick.setText(str(self.settings_data['horizTick']))
    #     self.ui_display.input_ampS.setText(str(self.settings_data['vMin']))
    #     self.ui_display.input_ampE.setText(str(self.settings_data['vMax']))
    #     # init actions
    #     self.ui_display.button_save.clicked.connect(self.storeDisplaySettings)
    #     self.ui_display.button_cancel.clicked.connect(self.window.close)
    #     # self.stopTimer()
    #     self.window.show()

    # # store display settings
    # def storeDisplaySettings(self):
    #     try:
    #         self.settings_data['swipeSamples'] = int(self.ui_display.input_swipe.text())
    #         check = 1 / self.swipe
    #     except:
    #         self.settings_data['swipeSamples'] = 1000
    #         print("ERROR swipe!")
    #     try:
    #         self.settings_data['zero'] = float(self.ui_display.input_zero.text())
    #     except:
    #         self.settings_data['zero'] = 0.0
    #         print("ERROR zero!")
    #     try:
    #         self.settings_data['vertTick'] = float(self.ui_display.input_vtick.text())
    #         check = 1 / self.vtick
    #     except:
    #         self.settings_data['vertTick'] = 1.0
    #         print("ERROR vtick!")
    #     try:
    #         self.settings_data['horizTick'] = float(self.ui_display.input_htick.text())
    #         check = 1 / self.htick
    #     except:
    #         self.settings_data['horizTick'] = 100.0
    #         print("ERROR htick!")
    #     try:
    #         self.settings_data['vMin'] = float(self.ui_display.input_ampS.text())
    #     except:
    #         self.settings_data['vMin'] = -2.0
    #         print("ERROR ampS!")
    #     try:
    #         self.settings_data['vMax'] = float(self.ui_display.input_ampE.text())
    #     except:
    #         self.settings_data['vMax'] = 2.0
    #         print("ERROR ampE!")

    #     self.settings_file.write("## File generated by leap_cap software \n"+
    #                             "## Available from github.com/ddantas/leap_cap \n"+
    #                             "## Timestamp: "+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+" \n"+
    #                             "##\n"+
    #                             "## EMG capture settings \n"+
    #                             "##\n")
    #     self.settings_file.writelines([
    #                             "# sampleRate: "+ str(self.settings_data['sampleRate']) + "\n", 
    #                             "# channelsPerBoard: " + str(self.settings_data['channelsPerBoard']) + "\n", 
    #                             "# nBoards: " + str(self.settings_data['nBoards']) + "\n", 
    #                             "# bitsPerSample: " + str(self.settings_data['bitsPerSample']) + "\n"
    #                         ])
    #     self.settings_file.write("##\n## EMG display settings\n##\n")
    #     self.settings_file.writelines([
    #                             "# swipeSamples: "+ str(self.settings_data['swipeSamples']) + "\n", 
    #                             "# zero: " + str(self.settings_data['zero']) + "\n", 
    #                             "# vertTick: " + str(self.settings_data['vertTick']) + "\n", 
    #                             "# horizTick: " + str(self.settings_data['horizTick']) + "\n", 
    #                             "# vMin: " + str(self.settings_data['vMin']) + "\n", 
    #                             "# vMax: " + str(self.settings_data['vMax'])
    #                         ])
    #     # self.clearGraph()
    #     # window.close()

    # # store capture settings
    # def storeCaptureSettings(self):
    #     try:
    #         self.settings_data['sampleRate'] = int(self.ui_caps.input_sampleR.text())
    #     except:
    #         print("ERROR sample rate!")

    #     self.settings_file.write("## File generated by leap_cap software \n"+
    #                             "## Available from github.com/ddantas/leap_cap \n"+
    #                             "## Timestamp: "+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+" \n"+
    #                             "##\n"+
    #                             "## EMG capture settings \n"+
    #                             "##\n")
    #     self.settings_file.writelines([
    #                             "# sampleRate: "+ str(self.settings_data['sampleRate']) + "\n", 
    #                             "# channelsPerBoard: " + str(self.settings_data['channelsPerBoard']) + "\n", 
    #                             "# nBoards: " + str(self.settings_data['nBoards']) + "\n", 
    #                             "# bitsPerSample: " + str(self.settings_data['bitsPerSample']) + "\n"
    #                         ])
    #     self.settings_file.write("##\n## EMG display settings\n##\n")
    #     self.settings_file.writelines([
    #                             "# swipeSamples: "+ str(self.settings_data['swipeSamples']) + "\n", 
    #                             "# zero: " + str(self.settings_data['zero']) + "\n", 
    #                             "# vertTick: " + str(self.settings_data['vertTick']) + "\n", 
    #                             "# horizTick: " + str(self.settings_data['horizTick']) + "\n", 
    #                             "# vMin: " + str(self.settings_data['vMin']) + "\n", 
    #                             "# vMax: " + str(self.settings_data['vMax'])
    #                         ])
    #     # self.clearGraph()
    #     window.close()

    def __exit__(self):
        self.settings_file.close()
