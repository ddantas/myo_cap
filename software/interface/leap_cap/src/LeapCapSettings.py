# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 18:42:02 2021

@author: asaphe
"""
import datetime
import os
import sys
# obtain the myograph path
myograph_import_path = os.path.split( os.path.split( os.path.split(os.path.abspath(__file__))[0] )[0] )[0]
# adds the myograph path for future inclusions 
sys.path.append(myograph_import_path)

import Settings
import TextFile2

SETTINGS_PATH  = myograph_import_path + '\\leap_cap\\src\\config\\'
FILE_NAME      = 'settings'


class LeapCapSettings(Settings.Settings):
    
    def __init__(self):
        # calling superclass constructor
        super(LeapCapSettings, self).__init__()
        # global objects
        self.txt_file = TextFile2.TextFile()     
        #self.settings = {}
        
    def load(self):
        try:
            
            self.txt_file.openFile( SETTINGS_PATH + FILE_NAME )   
            self.settings = self.txt_file.metadata_dict.copy() 
            
            print( self.txt_file.header_lines )
            #print( self.txt_file.metadata_lines )
            print( self.txt_file.metadata_dict )
            print( self.txt_file.data_lines )     
            
            
            # settings_file = open(SETTINGS_PATH, 'r')
            # settings_out = settings_file.readlines()
                        
            # for line in settings_out:
            #    if (line[1] == ' '):
            #        line = line.replace(':', '').replace('\n', '').split(' ')                    
            #        if(str(line[1]) == 'vMin' or str(line[1]) == 'vMax' or str(line[1]) == 'vTick'):
            #            self.settings[str(line[1])] = float(line[2])
            #        elif(str(line[1]) == 'emulationFlag' or str(line[1]) == 'emulationData' or 
            #             str(line[1]) == 'device' or str(line[1]) == 'routine' or str(line[1]) == 'hand') :
            #            self.settings[line[1]] = line[2]
            #        else:
            #            self.settings[str(line[1])] = int(line[2])
            #settings_file.close()
            #return True
        except:
            return False

    def save(self):
        try:
            settings_file = open(SETTINGS_PATH, 'w')
            settings_file.write('## File generated by myo_cap software \n' +
                        '## Available from github.com/ddantas/leap_cap \n' +
                        '## Timestamp: ' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ' \n' +
                        '##\n'+
                        '## EMG capture settings\n' +
                        '##\n'+
                        '# sampleRate: ' + str(self.getSampleRate()) + '\n' +
                        '# channelsPerBoard: ' + str(self.getChannelsPerBoard()) + '\n' +
                        '# nBoards: ' + str(self.getNBoards()) + '\n' +
                        '# bitsPerSample: ' + str(self.getBitsPerSample()) + '\n' +
                        '# swipe: '+ str(self.getSwipe()) + '\n' +
                        '# vTick: ' + str(self.getVTick()) + '\n' +
                        '# hTick: ' + str(self.getHTick()) + '\n' +
                        '# vMin: ' + str(self.getVMin()) + '\n' +
                        '# vMax: ' + str(self.getVMax()) + '\n' +
                        '##\n' +
                        '## EMG emulation settings\n' +
                        '##\n' +
                        '# emulationFlag: ' + self.getEmulationFlag() + '\n' +
                        '# emulationData: ' + self.getEmulationData() + '\n' +
                        '##\n'+
                        '## EMG communication settings\n' +
                        '##\n'+
                        '# baudrate: ' + str(self.getBaudrate()) + '\n' +
                        '# pktSize: ' + str(self.getPktSize()) + '\n' +
                        '# pktComp: ' + str(self.getPktComp()) + '\n' +
                        '##\n'+
                        '## EMG function generator settings\n' +
                        '##\n'+
                        '# funcGenFreq: ' + str(self.getFuncGenFreq()) + '\n' +
                        '# stressTime: ' + str(self.getStressTime()) + '\n' +
                        '##\n' +
                        '## Gesture capture settings\n' 
                        '##\n' +
                        '# device: ' + self.getDeviceType() + '\n' +
                        '# routine: ' + self.getCaptureRoutine() + '\n' +
                        '# hand: ' + self.getHand()  
                        )
            settings_file.close()
            return True
        except:
            return False

    def getSettingsPath(self):
        return SETTINGS_PATH        

    def getEmulationFlag(self):
        return self.settings['emulationFlag'] 
        
    def getEmulationData(self):
        return self.settings['emulationData'] 
        
    def getDeviceType(self):
        return self.settings['device'] 
        
    def getCaptureRoutine(self):
        return self.settings['routine'] 
        
    def getHand(self):
        return self.settings['hand'] 
    
    def setEmulationFlag(self,value):
        self.settings['emulationFlag'] = value
        
    def setEmulationData(self,value):
        self.settings['emulationData'] = value
        
    def setDeviceType(self,value):
        self.settings['device'] = value 
        
    def setCaptureRoutine(self,value):
        self.settings['routine'] = value 
        
    def setHand(self,value):
        self.settings['hand'] = value  
