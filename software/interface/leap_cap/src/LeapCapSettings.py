# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 18:42:02 2021

@author: Asaphe Magno
"""
import datetime
import os
import sys
# obtain the myograph path
MYOGRAPH_PATH = os.path.dirname( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
# adds the myograph path for future inclusions 
sys.path.append(MYOGRAPH_PATH)

import TextFile
import Settings

LEAPCAP_SETTINGS_PATH  = os.path.join( MYOGRAPH_PATH, 'leap_cap', 'src', 'config', '')
FILE_NAME      = 'settings'

# Type of parameters definition
LIST_INT32_PARAM  = ['sampleRate', 'channelsPerBoard', 'nBoards', 'bitsPerSample', 'swipe', 'hTick', 'baudrate', 'pktSize', 'pktComp', 'funcGenFreq', 'stressTime']
LIST_FLOAT_PARAM  = ['vMin', 'vMax', 'vTick']
LIST_STRING_PARAM = ['emulationData', 'emulationFlag', 'device', 'routine', 'hand']


class LeapCapSettings(Settings.Settings):
    
    def __init__(self):
        # calling superclass constructor
        super(LeapCapSettings, self).__init__()
        # global objects
        self.settings = {}
           
    # Method: Save the program settings. That method shold be called only when the method load() was already called or when all settings parameters were previously 
    #         defined in the settings dictionary variable. The output file name and path are defined as constants in the begining of the file.
    # Input : None
    # Output: None
    def save(self, path, file_name):        
        # Instatiates a TextFile object to manipulate a text file.
        txt_file = TextFile.TextFile()     
        
        # Writes the header of the text file
        txt_file.writeHeaderLine('File generated by myo_cap software')
        txt_file.writeHeaderLine('Available from github.com/ddantas/leap_cap')
        txt_file.writeHeaderLine( 'Timestamp: ' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') )
        txt_file.writeHeaderLine('')
        
        # Writes EMG capture settings header
        txt_file.writeHeaderLine('EMG capture settings')
        txt_file.writeHeaderLine('')
        # Writes EMG capture settings metadata
        txt_file.writeMetadataLine('sampleRate', self.settings['sampleRate'] )
        txt_file.writeMetadataLine('channelsPerBoard', self.settings['channelsPerBoard'] )
        txt_file.writeMetadataLine('nBoards', self.settings['nBoards'] )
        txt_file.writeMetadataLine('bitsPerSample', self.settings['bitsPerSample'] )
        txt_file.writeMetadataLine('swipe', self.settings['swipe'] )
        txt_file.writeMetadataLine('vTick', self.settings['vTick'] )
        txt_file.writeMetadataLine('hTick', self.settings['hTick'] )
        txt_file.writeMetadataLine('vMin', self.settings['vMin'] )
        txt_file.writeMetadataLine('vMax', self.settings['vMax'] )
        txt_file.writeHeaderLine('')        
        
        # Writes EMG emulation settings header
        txt_file.writeHeaderLine('EMG emulation settings')
        txt_file.writeHeaderLine('')
        # Writes EMG emulation settings metadata
        txt_file.writeMetadataLine('emulationFlag', self.settings['emulationFlag'] )
        txt_file.writeMetadataLine('emulationData', self.settings['emulationData'] )
        txt_file.writeHeaderLine('')        
                
        # Writes EMG communication settings header
        txt_file.writeHeaderLine('EMG communication settings')
        txt_file.writeHeaderLine('')
        # Writes EMG communication settings metadata
        txt_file.writeMetadataLine('baudrate', self.settings['baudrate'] )
        txt_file.writeMetadataLine('pktSize', self.settings['pktSize'] )
        txt_file.writeMetadataLine('pktComp', self.settings['pktComp'] )
        txt_file.writeHeaderLine('')        

        # Writes EMG function generator settings header
        txt_file.writeHeaderLine('EMG function generator settings')
        txt_file.writeHeaderLine('')
        # Writes EMG function generator settings metadata
        txt_file.writeMetadataLine('funcGenFreq', self.settings['funcGenFreq'] )
        txt_file.writeMetadataLine('stressTime', self.settings['stressTime'] )        
        txt_file.writeHeaderLine('')

        # Writes esture capture settings header
        txt_file.writeHeaderLine('Gesture capture settings')
        txt_file.writeHeaderLine('')
        # Writes gesture capture settings metadata
        txt_file.writeMetadataLine('device', self.settings['device'] )
        txt_file.writeMetadataLine('routine', self.settings['routine'] )
        txt_file.writeMetadataLine('hand', self.settings['hand'] )
        txt_file.writeHeaderLine('')

        # Writes Data header
        txt_file.writeHeaderLine('Data') 
        
        # Saves the text lines stored in the text_file object into the settings file. 
        txt_file.saveFile( path, file_name )
        
        # Success flag
        return True
        
## LeapCap Exclusive get and set methods ############################################

    def getSettingsPath(self):
        return LEAPCAP_SETTINGS_PATH        

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
