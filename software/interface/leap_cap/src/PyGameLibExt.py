# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 15:25:18 2021

@author: Asaphe Magno
"""

# Colors Definition
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Constants for orientation
ORIENT_VERTICAL   = 0
ORIENT_HORIZONTAL = 1

# Type of elements
IMAGE             = 0
PROGRESS_BAR      = 1
SPACCER           = 2
LAYOUT            = 3
PANEL             = 4

class Image:
    
    def __init__(self, dimensions, local_pos):
        self.type_of_elem  = IMAGE            
        self.dimensions    = dimensions
        self.local_pos     = local_pos        


class ProgressBar:
    
    def __init__(self, orient, dimensions, local_pos, progress_perc, border_color, bar_color):        
        self.type_of_elem  = PROGRESS_BAR
        # Orientation of the bar
        self.orient        = orient
        self.dimensions    = dimensions
        self.local_pos     = local_pos
        self.progress_perc = progress_perc
        self.border_color  = border_color
        self.bar_color     = bar_color
        
    def SetProgress(self, progress_perc):
        self.progress_perc = progress_perc   
        
class Spaccer:
    
    def __init__(self, dimensions, local_pos):
        self.type_of_elem  = SPACCER
        self.dimensions    = dimensions
        self.local_pos     = local_pos        

class Layout:
    
    def __init__(self):
        self.type_of_elem  = LAYOUT
        # visual elements 
        self.num_tot_elements  = 0
        self.num_lines         = 0
        self.num_elem_per_line = []
        self.elements          = []        

class Panel:
    
    def __init__(self, local_pos, dimensions, type_of_panel):
        self.type_of_elem  = PANEL
        self.is_main_panel = type_of_panel
        self.dimensions    = dimensions
        self.local_pos     = local_pos

    def AddVisElement(self, vis_element):
        self.vis_elements.append(vis_element)
        self.num_vis_elem = self.num_vis_elem + 1
        

        
    
    
    

