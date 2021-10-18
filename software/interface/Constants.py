# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 13:09:27 2020

@author: Asaphe Magno
"""

import os

# Activate ou Deactivate the DEBUG
DEBUG = 0

# Used to Resolve the Transmission Mode
UNPACKED = 0
PACKED   = 1

# String Transmission Constants
MAX_CODE = 64
SHIFT    = 60

# Fingers in left hand
THUMB = 1
INDICATOR = 2
MIDDLE = 3
RING = 4
PINKY = 5

# No key pressed
NO_KEY_PRESSED = 0

# Close subject window
CLOSE_SUBJECT_WIN = 255

# Files names and directories
SETTINGS_PATH      = os.path.join( 'config', '' )
SETTINGS_FILE_NAME = 'settings'

LOG_PATH           = os.path.join('data', '')

