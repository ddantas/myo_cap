# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 18:42:02 2021

@author: asaphe
"""

import os
import sys
# obtain the myograph path
myograph_import_path = os.path.split( os.path.split( os.path.split(os.path.abspath(__file__))[0] )[0] )[0]
# adds the myograph path for future inclusions 
sys.path.append(myograph_import_path)

import Settings

class LeapCapSettings(Settings.Settings):
    
    def __init__(self):
        # calling superclass constructor
        super(LeapCapSettings, self).__init__()
        # global objects
        