# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 15:25:18 2021

@author: Asaphe Magno
"""

import pygame as pg

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

## After, add parameter "visible" in the classes.
## Use concat 
##

class Image:
    
    def __init__(self, dimensions, local_pos):
        self.type_of_elem  = IMAGE            
        self.dimensions    = dimensions
        self.local_pos     = local_pos        


class ProgressBar:
    
    def __init__(self, orient, dimension, local_pos, progress_perc, border_color, bar_color):        
        self.type_of_elem    = PROGRESS_BAR
        # Orientation of the bar
        self.orient          = orient
        self.outer_dimension = dimension
        self.outer_local_pos = local_pos        
        self.progress_perc   = progress_perc
        self.border_color    = border_color
        self.bar_color       = bar_color
        
        self.UpdateInnerDim()
        self.UpdateInnerPos()

    def UpdateInnerDim(self):
        if(self.orient == ORIENT_VERTICAL):
            self.inner_dimension = (self.outer_dimension[0]-6, (self.outer_dimension[1]-6) * self.progress_perc )
        # ORIENTAÇÃO HORIZONTAL    
        else:            
            self.inner_dimension = ((self.outer_dimension[0] - 6) * self.progress_perc, self.outer_dimension[1] - 6)
        
    def UpdateInnerPos(self):
        if(self.orient == ORIENT_VERTICAL):            
            self.inner_local_pos = (self.outer_local_pos[0] + 3, self.outer_local_pos[1] + 3 + ( (self.outer_dimension[1] - 6) - (self.outer_dimension[1] - 6) * self.progress_perc) )
        # ORIENTAÇÃO HORIZONTAL
        else:            
            self.inner_local_pos = (self.outer_local_pos[0] + 3, self.outer_local_pos[1] + 3)      
                 
    def SetProgress(self, progress_perc):
        self.progress_perc = progress_perc   
                
    def GetDrawParam(self):
        return ([ self.type_of_elem, self.outer_dimension, self.outer_local_pos,
                                     self.inner_dimension, self.inner_local_pos,
                                     self.border_color   , self.bar_color        ])

        
        
        
        
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
    
    def __init__(self, type_of_panel, dimensions, local_pos):
        self.type_of_elem  = PANEL
        self.is_main_panel = type_of_panel
        self.dimensions    = dimensions
        self.local_pos     = local_pos
        
    #def DrawVisElements(self):
        #if (leaf):
        #    return "draw parameters from the visual element"
        #else:
    #        for element in lement:
    #            append(element)
    #        return ()

    def AddVisElement(self, vis_element):
        self.vis_elements.append(vis_element)
        self.num_vis_elem = self.num_vis_elem + 1
        

        
    
def Draw(win, num_elem, elem_draw_param):
    
    for num_elem in range(num_elem):        
        # Visual element it's a Progress Bar
        if( elem_draw_param[num_elem][0] == PROGRESS_BAR ):
            #print(num_elem)
            #print(elem_draw_param[num_elem])
            pg.draw.rect(win, elem_draw_param[num_elem][5], (*elem_draw_param[num_elem][2], *elem_draw_param[num_elem][1]), 1)
            pg.draw.rect(win, elem_draw_param[num_elem][6], (*elem_draw_param[num_elem][4], *elem_draw_param[num_elem][3]))    
            

