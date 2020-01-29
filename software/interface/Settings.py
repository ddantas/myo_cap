# -*- coding: utf-8 -*-

import datetime
import os

SETTINGS_PATH = "config/settings"

class Settings:

    def __init__(self):
        self.data = {}

    def load(self):
        try:
            settings_file = open(SETTINGS_PATH, "r")
            settings_out = settings_file.readlines()

            for line in settings_out:
                if (line[1] == " "):
                    line = line.replace(":", "").split(" ")
                    if(str(line[1]) == "vMin" or str(line[1]) == "vMax" or str(line[1]) == "vTick"):
                        self.data[str(line[1])] = float(line[2])
                    else:
                        self.data[str(line[1])] = int(line[2])

            settings_file.close()
        except IOError:
            print("Please insert the settings file!")
            print(SETTINGS_PATH)
            print(os.getcwd())

        self.data['pktSize'] = 2
        self.data['baudrate'] = 9600

        self.data['funcGenFreq'] = 100
        self.data['stressTime'] = 10

    def save(self):
        try:
            settings_file = open(SETTINGS_PATH, "w")

            settings_file.write("## File generated by myo_cap software \n" +
                        "## Available from github.com/ddantas/myo_cap \n" +
                        "## Timestamp: " + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + " \n" +
                        "##\n"+
                        "## EMG capture settings \n"+
                        "##\n"+
                        "# sampleRate: "+ str(self.data['sampleRate']) + "\n" +
                        "# channelsPerBoard: " + str(self.data['channelsPerBoard']) + "\n" +
                        "# nBoards: " + str(self.data['nBoards']) + "\n" +
                        "# bitsPerSample: " + str(self.data['bitsPerSample']) + "\n" +
                        "# swipe: "+ str(self.data['swipe']) + "\n" +
                        "# vTick: " + str(self.data['vTick']) + "\n" +
                        "# hTick: " + str(self.data['hTick']) + "\n" +
                        "# vMin: " + str(self.data['vMin']) + "\n" +
                        "# vMax: " + str(self.data['vMax']) + "\n" +
                        "# showChannels: " + str(self.data['showChannels']))

            settings_file.close()

            return True
        except IOError as err:
            print("ERROR!", err)

            return False

    def getSettingsPath(self):
        return SETTINGS_PATH

    def getPktSize(self):
        return self.data['pktSize']

    def getBaudrate(self):
        return self.data['baudrate']

    def getFuncGenFreq(self):
        return self.data['funcGenFreq']

    def getStressTime(self):
        return self.data['stressTime']

    def getSampleRate(self):
        return self.data['sampleRate']

    def getChannelsPerBoard(self):
        return self.data['channelsPerBoard']

    def getNBoards(self):
        return self.data['nBoards']

    def getBitsPerSample(self):
        return self.data['bitsPerSample']

    def getBaudrate(self):
        return self.data['baudrate']

    def getSwipe(self):
        return self.data['swipe']

    def getVTick(self):
        return self.data['vTick']

    def getHTick(self):
        return self.data['hTick']

    def getVMin(self):
        return self.data['vMin']

    def getVMax(self):
        return self.data['vMax']

    def getShowChannels(self):
        return self.data['showChannels']

    def setPktSize(self, value):
        self.data['pktSize'] = value

    def setBaudrate(self, value):
        self.data['baudrate'] = value

    def setFuncGenFreq(self, value):
        self.data['funcGenFreq'] = value

    def setStressTime(self, value):
        self.data['stressTime'] = value

    def setSampleRate(self, value):
        self.data['sampleRate'] = value

    def setChannelsPerBoard(self, value):
        self.data['channelsPerBoard'] = value

    def setNBoards(self, value):
        self.data['nBoards'] = value

    def setBitsPerSample(self, value):
        self.data['bitsPerSample'] = value

    def setBaudrate(self, value):
        self.data['baudrate'] = value

    def setSwipe(self, value):
        self.data['swipe'] = value

    def setVTick(self, value):
        self.data['vTick'] = value

    def setHTick(self, value):
        self.data['hTick'] = value

    def setVMin(self, value):
        self.data['vMin'] = value

    def setVMax(self, value):
        self.data['vMax'] = value

    def setShowChannels(self, value):
        self.data['showChannels'] = value
