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
SPACER            = 2
LAYOUT            = 3
PANEL             = 4

## All "Visual Elements" have the methods: SetSize(size); SetLocalPos(local_pos); GetSize(); GetLocalPos();

## After, add parameter "visible" in the classes.
## Use concat 

## Image Class ##################################################################################################################
class Image:
    
    def __init__(self, size, local_pos):
        self.type_of_elem  = IMAGE            
        self.size          = size
        self.local_pos     = local_pos        

## Progress Bar Class ###########################################################################################################
class ProgressBar:
    
    def __init__(self, orient, dimension, local_pos, progress_perc, border_color, bar_color):        
        self.type_of_elem    = PROGRESS_BAR
        # Orientation of the bar
        self.orient          = orient
        self.outer_size = dimension
        self.outer_local_pos = local_pos        
        self.progress_perc   = progress_perc
        self.border_color    = border_color
        self.bar_color       = bar_color        
        self.UpdateInnerSize()
        self.UpdateInnerPos()

    def UpdateInnerSize(self):
        if(self.orient == ORIENT_VERTICAL):
            self.inner_size = (self.outer_size[0]-6, (self.outer_size[1]-6) * self.progress_perc )
        # ORIENTAÇÃO HORIZONTAL    
        else:            
            self.inner_size = ((self.outer_size[0] - 6) * self.progress_perc, self.outer_size[1] - 6)
        
    def UpdateInnerPos(self):
        if(self.orient == ORIENT_VERTICAL):            
            self.inner_local_pos = (self.outer_local_pos[0] + 3, self.outer_local_pos[1] + 3 + ( (self.outer_size[1] - 6) - (self.outer_size[1] - 6) * self.progress_perc) )
        # ORIENTAÇÃO HORIZONTAL
        else:            
            self.inner_local_pos = (self.outer_local_pos[0] + 3, self.outer_local_pos[1] + 3)      
                 
    def SetProgress(self, progress_perc):
        self.progress_perc = progress_perc   
                
    def SetSize(self, size):       
        self.outer_size = size
        self.UpdateInnerSize()
        
    def SetLocalPos(self, local_pos):        
        self.outer_local_pos = local_pos  
        self.UpdateInnerPos()
        
    def GetSize(self):       
        return self.outer_size
        
    def GetLocalPos(self):        
        return self.outer_local_pos  
        
    def GetDrawParam(self):
        return ([ self.type_of_elem, self.outer_size   , self.outer_local_pos,
                                     self.inner_size   , self.inner_local_pos,
                                     self.border_color , self.bar_color        ])        
        
## Spacer Class #################################################################################################################        
class Spacer:
    
    def __init__(self, size, local_pos):
        self.type_of_elem  = SPACER
        self.size          = ( int(size[0])     , int(size[1])      )
        self.local_pos     = ( int(local_pos[0]), int(local_pos[1]) )        

## Layout Class #################################################################################################################
class Layout:
    
    def __init__(self, size, local_pos, num_lines, num_colums, list_of_elements, spacer):
        self.type_of_elem       = LAYOUT 
        self.size               = size
        self.local_pos          = local_pos
        self.num_tot_elements   = num_lines * num_colums 
        self.num_lines          = num_lines
        self.num_colums         = num_colums
        self.spacer             = spacer
        self.num_vert_spacers   = self.CalcNumVertSpacers(num_lines, num_colums)
        self.num_hor_spacers    = self.CalcNumHorSpacers (num_lines, num_colums)
        # 2-dim list or grid with "visual elements"
        self.elements           = [None] * self.num_lines
        for line in range(self.num_lines):
            self.elements[line] = [None] * self.num_colums
        # Atach the Elements in the grid    
        self.AtachElements( num_lines, num_colums, list_of_elements)            
        # Set the size of the Elements in the grid    
        self.SetSizeElements  ( self.num_lines, self.num_colums, self.elements, self.spacer)
        # Set the local position of the Elements in the grid    
        self.SetLocalPosElements(self.num_lines, self.num_colums, self.elements, self.spacer)
        
    def CalcNumVertSpacers(self, num_lines, num_colums):        
        # Have zero colums
        if not num_colums:
            num_vert_spacers = 0
            
        # Have one or more colums
        else:
            # Vertical spacers are like vertical bars
            num_vert_spacers = 1 + num_colums         
            
        return num_vert_spacers        
    
    def CalcNumHorSpacers (self, num_lines, num_colums):
        # Have zero lines
        if not num_lines:
            num_hor_spacers = 0
            
        # Have one or more lines
        else:  
            # Horizontal spacers are like horizontal bars
            num_hor_spacers = 1 + num_lines
            
        return num_hor_spacers
    
    # Sets a pointer for each element (object)    
    def AtachElements(self, num_lines, num_colums, list_of_elements):
        for line in range(num_lines):
            for colum in range(num_colums):
                self.elements[line][colum] = list_of_elements[ line + colum ]
    
    def SetSizeElements(self, num_lines, num_colums, elements, spacer):
        width  = int( ( self.GetSize()[0] - self.CalcNumVertSpacers(num_lines, num_colums) * spacer.size[0] ) / num_colums )
        height = int( ( self.GetSize()[1] - self.CalcNumHorSpacers (num_lines, num_colums) * spacer.size[1] ) / num_lines  )        
        for line in range(num_lines):
            for colum in range(num_colums):                                
                elements[line][colum].SetSize( (width, height) )
    
    def SetLocalPosElements(self, num_lines, num_colums, elements, spacer):
        local_pos = [None] * 2
        for line in range(num_lines):
            for colum in range(num_colums):                                
                local_pos[0] = (colum + 1) * spacer.size[0] + colum * self.elements[line][colum].GetSize()[0]
                local_pos[1] = (line  + 1) * spacer.size[1] + line  * self.elements[line][colum].GetSize()[1]
                elements[line][colum].SetLocalPos( (local_pos[0], local_pos[1]) )
    
    # Sets the Layout size        
    def SetSize(self, size):       
        self.size = size        
        # Update the elements size
        self.SetSizeElements(self.num_lines, self.num_colums, self.elements, self.spacer)
        
    # Sets the Layout local position
    def SetLocalPos(self, local_pos):        
        self.local_pos = local_pos  
        # Update the elements local position
        self.SetLocalPosElements(self.num_lines, self.num_colums, self.elements, self.spacer)
    
    # Returns the Layout size    
    def GetSize(self):       
        return self.size
    
    # Returns the Layout local position    
    def GetLocalPos(self):        
        return self.local_pos    

    def GetDrawParam(self):
        list_draw_param = []
        for line in range(self.num_lines):
            for colum in range(self.num_colums):
                #print(self.num_lines)
                #print( '(' + str(line) + str(colum) + ')' )
                # It is a Image or a Progress Bar.
                if( (self.elements[line][colum].type_of_elem == IMAGE) or (self.elements[line][colum].type_of_elem == PROGRESS_BAR) ):
                    # Append the draw parameters of the visual element into the lists of visual elements to be draw
                    list_draw_param.append( self.elements[line][colum].GetDrawParam() )
                # It is a Panel or a Layout    
                elif( (self.elements[line][colum].type_of_elem == PANEL) or (self.elements[line][colum].type_of_elem == PANEL) ):
                    # Join the current list with the lists of the element 
                    list_draw_param = list_draw_param + self.elements[line][colum].GetDrawParam()
            # Returns a list with all draw parameters of all elements inside the layout concatenated     
            return list_draw_param

### Panel Class #################################################################################################################
class Panel:
    
    def __init__(self, type_of_panel, size, local_pos):
        self.type_of_elem  = PANEL
        self.is_main_panel = type_of_panel
        self.size          = size
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
        

        
### Global Methods ##############################################################################################################    
def Draw(win, num_elem, elem_draw_param):
    
    for num_elem in range(num_elem):        
        # Visual element it's a Progress Bar
        if( elem_draw_param[num_elem][0] == PROGRESS_BAR ):
            #print(num_elem)
            #print(elem_draw_param[num_elem])
            pg.draw.rect(win, elem_draw_param[num_elem][5], (*elem_draw_param[num_elem][2], *elem_draw_param[num_elem][1]), 1)
            pg.draw.rect(win, elem_draw_param[num_elem][6], (*elem_draw_param[num_elem][4], *elem_draw_param[num_elem][3]))    
            

