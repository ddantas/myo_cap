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
VERTICAL   = 0
HORIZONTAL = 1

# Type of elements
IMAGE             = 0
PROGRESS_BAR      = 1
SPACER            = 2
LAYOUT            = 3
PANEL             = 4

## All elements but Spacers have the methods: Risize(new_size); SetLocalPos(local_pos); GetSize(); GetLocalPos();


## Image Class ##################################################################################################################
class Image:
    
    def __init__(self, size, local_pos):
        self.type_of_elem  = IMAGE            
        self.size          = size
        self.local_pos     = local_pos        

## Progress Bar Class ###########################################################################################################
## A Progress Bar it's a visual element used to express progress or level of variables.
## It can have horizontal or vertical orientation. Also have a color used in it's border and other used in the bar. 
## It's progress can be setted calling the SetProgress method. And it's size can be choosed during the construction.
class ProgressBar:
    
    # Method: Constructor for the class.
    #
    # Input : orientation      -> [VERTICAL|HORIZONTAL]. Orientation for the progress bar.
    #         outter_size      -> Tuple(outter size in horizontal, outter size in vertical). Size for the progress bar in pixels. 
    #         outter_local_pos -> Tuple(outter local position in horizontal, outter local position in vertical). Outter local position for this 
    #                             progress bar inside a [Panel|Layout].                             
    #         progress_perc    -> Float value [0.0 - 1.0]. The initial percentage of progress for the bar.  
    #                             Can be changed after by calling the SetProgress method. 
    #         border_color     -> Color used in the borders of the progress bar.
    #         bar_color        -> Color used in the internal bar that indicates progress or level.
    #
    # Output: Object of the type ProgressBar constructed.
    def __init__(self, orientation, outter_size, outter_local_pos, progress_perc, border_color, bar_color):        
        self.type_of_elem     = PROGRESS_BAR
        # Orientation of the progress bar
        self.orientation      = orientation
        self.outter_size      = outter_size
        self.outter_local_pos = outter_local_pos        
        self.progress_perc    = progress_perc
        self.border_color     = border_color
        self.bar_color        = bar_color
        self.inner_size       = self.CalcInnerSize(self.orientation, self.outter_size, self.progress_perc)
        self.inner_local_pos  = self.CalcInnerLocalPos(self.orientation, self.outter_size, self.outter_local_pos, self.progress_perc)        
    
    # Method: Resizes this progress bar.
    #         A call to this method probably will be folowed by a call of the SetLocalPos method to update the
    #         local position of this progress bar. 
    #         In that case it's just a method that standardize a resize method since other elements need a more complex action
    #         in a resize situation than just call SetSize.  
    #
    # Input : new_size         -> The new size for the progress bar.
    #
    # Output: None    
    def Resize(self, new_outter_size):
        self.SetSize(new_outter_size)

    # Method: Calculate the inner size of the progress bar. The inner size it's the size of the bar that indicates progress 
    #         or level of a variable.
    #         That size it's dependent of the progress or level. 
    #         If the progress pecentage it's 1.0 (full bar), than this size will be the outter size of the progress bar minus
    #         six pixels in the vertical and in the horizontal.
    #
    # Input : orientation      -> [VERTICAL|HORIZONTAL]. Orientation of the progress bar.
    #         outter_size      -> Tuple(outter size in horizontal, outter size in vertical). Size of the progress bar in pixels.  
    #         progress_perc    -> Float value [0.0 - 1.0]. The current percentage of progress for the bar.  
    #
    # Output: inner_size      -> Tuple(inner size in horizontal, inner size in vertical). Size for bar inside the progress bar in pixels. 
    def CalcInnerSize(self, orientation, outter_size, progress_perc):
        # Orientação vertical
        if(orientation == VERTICAL):
            inner_size = (outter_size[0]-6, (outter_size[1]-6) * progress_perc )
            return inner_size
        # Orientação horizontal
        else:            
            inner_size = ( int( (outter_size[0] - 6) * progress_perc ), int( outter_size[1] - 6 ) )
            return inner_size
        
    # Method: Calculate the inner local position of the progress bar. The inner local position it's the local of the bar that indicates progress 
    #         or level of a variable.
    #         That local position it's dependent of the progress or level.     
    #         For different orientations the calculus it's different.
    #
    # Input : orientation      -> [VERTICAL|HORIZONTAL]. Orientation of the progress bar.
    #         outter_size      -> Tuple(outter size in horizontal, outter size in vertical). Size of the progress bar in pixels.  
    #         outter_local_pos -> Tuple(outter local position in horizontal, outter loca position in vertical). Outter local position for this 
    #                             progress bar inside a [Panel|Layout].                             
    #         progress_perc    -> Float value [0.0 - 1.0]. The current percentage of progress for the bar.  
    #
    # Output: inner_local_pos  -> Tuple(inner local position in horizontal, inner local position in vertical). Inner local position for bar 
    #                             inside the progress bar. Tuple of values in pixels.     
    def CalcInnerLocalPos(self, orientation, outter_size, outter_local_pos, progress_perc):
        # Orientação vertical
        if(orientation == VERTICAL):            
            inner_local_pos = ( int( outter_local_pos[0] + 3 ), int( outter_local_pos[1] + 3 + ( (outter_size[1] - 6) - (outter_size[1] - 6) * progress_perc) ) )
            return inner_local_pos
        # Orientação horizontal
        else:            
            inner_local_pos = ( int( outter_local_pos[0] + 3 ), int( outter_local_pos[1] + 3 ) )      
            return inner_local_pos
                 
    def SetProgress(self, progress_perc):
        self.progress_perc = progress_perc   
                
    def SetSize(self, outter_size):     
        # Sets the new outter size for the progress bar 
        self.outter_size      = outter_size
        # Calculates and sets the new inner size for the progress bar 
        self.inner_size      = self.CalcInnerSize(self.orientation, self.outter_size, self.progress_perc)
        
    def SetLocalPos(self, outter_local_pos):        
        # Sets the new outter local position for the progress bar 
        self.outter_local_pos = outter_local_pos
        # Calculates and sets the new inner local position for the progress bar 
        self.inner_local_pos = self.CalcInnerLocalPos(self.orientation, self.outter_size, self.outter_local_pos, self.progress_perc)
        
    def GetSize(self):       
        return self.outter_size
        
    def GetLocalPos(self):        
        return self.outter_local_pos  
        
    def GetDrawParam(self, pos_offset):
       
        return ([ self.type_of_elem, self.outter_size  , ( pos_offset[0] + self.outter_local_pos[0], pos_offset[1] + self.outter_local_pos[1]  ),
                                     self.inner_size   , ( pos_offset[0] + self.inner_local_pos[0] , pos_offset[1] + self.inner_local_pos[1]   ),
                                     self.border_color , self.bar_color  ])        
        
## Spacer Class #################################################################################################################        
## That class it's used to inform vertical and horizontal spancing between visual elements.
## It's not used as a visual element. So it won't be included in panels or layouts. Just will be used as a reference. 
class Spacer:
    
    # Method: Constructor for the class.      
    #
    # Input : size             -> Tuple(width of vertical spacers, height of horizontal spacers). Size in Pixels.
    #                             Note: A vertical spacer have vertical orientation and so spaces horizontally elements.
    #                                   A horizontal spacer have horizontal orientation and so spaces vertically elements.
    # Output: Object of the type Spacer constructed.
    def __init__(self, size):
        self.type_of_elem  = SPACER
        self.size          = ( int(size[0]) ,int(size[1]) )        

## Layout Class #################################################################################################################
## That Class represents a layout inside a Window, Panel or even another Layout. 
## A Layout it's a structure that mananges automatically the size and position of elements attached to it.
## Elements that can be attached are of the type: Image, Progress Bar, Panel, and Layout.  
## A Layout have (number of lines * number of colums) elements organized in (number of lines) lines and (number of colums) colums.
## The elements attached are spaced vertically and horizontally according with the spacer object provided to the class constructor.
## A list of lists arranged as a matrix(grid) contain pointers to the elements(objects) attached to the layout. 
## The vertical and horizontal spacers are not attached to the grid. But they serve as a reference to the attached 
## elements size and position.  
class Layout:
    
    # Method: Constructor for the class.      
    #
    # Input : size             -> Tuple(size in horizontal, size in vertical). Size of this Layout. Size in Pixels.
    #         local_pos        -> Tuple(position in horizontal, position in vertical). Local position of this layout inside
    #                             a Window, Panel or another Layout.    
    #         num_lines        -> Number of lines for the the Layout.      
    #         num_colums       -> Number of colums for the the Layout.  
    #         list_of_elements -> List of [Images | Progress Bars | Panels | Layouts] containing 
    #                             at least (number of lines * number of colums) elements. 
    #         spacer           -> Object of type "Spacer". The spacer won't attached to the Layout,
    #                             but your dimensions will serve to the elements size and position calculation.
    #
    # Output: Object of the type Layout constructed.
    def __init__(self, size, local_pos, num_lines, num_colums, list_of_elements, spacer):
        self.type_of_elem       = LAYOUT 
        self.size               = size
        self.local_pos          = local_pos
        self.num_tot_elements   = num_lines * num_colums 
        self.num_lines          = num_lines
        self.num_colums         = num_colums
        self.spacer             = spacer
        # Calculate the number of vertical spacers inside the Layout
        # Note: A vertical spacer have vertical orientation and so spaces horizontally elements.
        self.num_vert_spacers   = self.CalcNumVertSpacers(num_lines, num_colums)
        # Calculate the number of horizontal spacers inside the Layout
        # Note: A horizontal spacer have horizontal orientation and so spaces vertically elements.
        self.num_hor_spacers    = self.CalcNumHorSpacers (num_lines, num_colums)
        # List of lists arranged as a matrix(grid) contain pointers to the elements(objects) attached to the layout.
        self.elements           = [None] * self.num_lines
        for line in range(self.num_lines):
            self.elements[line] = [None] * self.num_colums
        # Atach the Elements in the grid    
        self.AttachElements( num_lines, num_colums, list_of_elements)            
        # Set the size of the Elements in the grid    
        self.SetSizeElements  ( self.num_lines, self.num_colums, self.elements, self.spacer)
        # Set the local position of the Elements in the grid    
        self.SetLocalPosElements(self.num_lines, self.num_colums, self.elements, self.spacer)
        
    # Method: Calculate the number of vertical spacers inside the Layout.
    #         Note: A vertical spacer have vertical orientation and so spaces horizontally elements.
    #
    # Input : None
    #
    # Output: Integer. Number of vertical spacers inside the Layout.  
    def CalcNumVertSpacers(self, num_lines, num_colums):        
        # Have zero colums
        if not num_colums:
            num_vert_spacers = 0
            
        # Have one or more colums
        else:
            # Vertical spacers are like vertical bars
            num_vert_spacers = 1 + num_colums         
            
        return num_vert_spacers            
    
    # Method: Calculate the number of horizontal spacers inside the Layout.
    #         Note: A horizontal spacer have horizontal orientation and so spaces vertically elements.
    #
    # Input : None
    #
    # Output: Integer. Number of horizontal spacers inside the Layout      
    def CalcNumHorSpacers (self, num_lines, num_colums):
        # Have zero lines
        if not num_lines:
            num_hor_spacers = 0
            
        # Have one or more lines
        else:  
            # Horizontal spacers are like horizontal bars
            num_hor_spacers = 1 + num_lines
            
        return num_hor_spacers
        
    # Method: Attach elements in the spaces inside the layout.    
    #         Images, Progress bars, Panels or even Layouts can be attached in positions inside a Layout.
    #         There are (number of lines * number of colums) spaces inside the layout.
    #         Just the (number of lines * number of colums) first elements in the list given are attached.  
    #         Each position have just a pointer to the real object. So no new space it is used.  
    #         Don't attach the same objet to more than one position. Because of the reason above.       
    #
    # Input : num_lines        -> Number of lines inside the Layout.
    #         num_colums       -> Number of colums inside the Layout.        
    #         list_of_elements -> List of [Images | Progress Bars | Panels | Layouts] containing 
    #                             at least (number of lines * number of colums) elements.       
    #
    # Output: None    
    def AttachElements(self, num_lines, num_colums, list_of_elements):
        for line in range(num_lines):
            for colum in range(num_colums):
                self.elements[line][colum] = list_of_elements[ line * num_colums + colum ]

    # Method: Sets the calculated value of width and hight for each element inside the Layout.
    #         This values are written inside each object attached to the Layout.
    #         This method accounts for the own Layout size.  
    #
    # Input : num_lines        -> Number of lines inside the Layout.
    #         num_colums       -> Number of colums inside the Layout.        
    #         elements         -> List of all elements attached to this Layout.
    #         spacer           -> Object of type "Spacer". The spacer won't attached to the Layout,
    #                             but your dimensions will serve to the elements size and position calculation.           
    #
    # Output: None
    def SetSizeElements(self, num_lines, num_colums, elements, spacer):
        width  = int( ( self.GetSize()[0] - self.CalcNumVertSpacers(num_lines, num_colums) * spacer.size[0] ) / num_colums )
        height = int( ( self.GetSize()[1] - self.CalcNumHorSpacers (num_lines, num_colums) * spacer.size[1] ) / num_lines  )        
        for line in range(num_lines):
            for colum in range(num_colums):                                
                elements[line][colum].SetSize( (width, height) )
                
    # Method: Sets the local position(position inside the layout) for each element inside the Layout.
    #         This values are written inside each object attached to the Layout.
    #         This method accounts for the own Layout size.  
    #
    # Input : num_lines        -> Number of lines inside the Layout.
    #         num_colums       -> Number of colums inside the Layout.        
    #         elements         -> List of all elements attached to this Layout.
    #         spacer           -> Object of type "Spacer". The spacer won't attached to the Layout,
    #                             but your dimensions will serve to the elements position calculation.           
    #
    # Output: None    
    def SetLocalPosElements(self, num_lines, num_colums, elements, spacer):
        local_pos = [None] * 2
        for line in range(num_lines):
            for colum in range(num_colums):                                
                local_pos[0] = (colum + 1) * spacer.size[0] + colum * self.elements[line][colum].GetSize()[0]
                local_pos[1] = (line  + 1) * spacer.size[1] + line  * self.elements[line][colum].GetSize()[1]
                elements[line][colum].SetLocalPos( (local_pos[0], local_pos[1]) )
    
    # Method: Sets the size of this Layout.
    #
    # Input : size             -> Tuple(size in horizontal, size in vertical). New values to the layout size. Size in Pixels.
    #
    # Output: None
    def SetSize(self, size):       
        self.size = size        
        # Update the elements size
        self.SetSizeElements(self.num_lines, self.num_colums, self.elements, self.spacer)
    
    # Method: Sets the local position of this Layout inside a [Panel|Layout].
    #
    # Input : local_pos        -> Tuple(position in horizontal, position in vertical). New values to the layout local position. 
    #
    # Output: None    
    def SetLocalPos(self, local_pos):        
        self.local_pos = local_pos  
        # Update the elements local position
        self.SetLocalPosElements(self.num_lines, self.num_colums, self.elements, self.spacer)
    
    # Method: Returns the current size of this Layout. 
    #
    # Input : None
    #
    # Output: size             -> Tuple(size in horizontal, size in vertical)
    def GetSize(self):       
        return self.size
    
    # Method: Returns the current local position of this Layout inside a [Panel|Layout]. 
    #
    # Input : None
    #
    # Output: size             -> Tuple(size in horizontal, size in vertical). Size in Pixels.
    def GetLocalPos(self):        
        return self.local_pos    

    # Method: Returns a list of elements draw parameters.
    #         The size of the list returned is (number of lines * number of colums). 
    #         Each position in the returned list it's a list of draw parameters for the element attached in this layout.
    #         Example: list_returned[0] -> It's a list containing the draw parameters for the element attached in the 
    #                  higher and left position of the layout.
    #         Note 1: If a element attached to this layout is a [Panel|Layout] than the list returned will be the result of
    #                 the concatenation between the list of elements draw parameters of all other elements inside the this layout
    #                 with the list of elements draw parameters of the element of the type [Panel|Layout] also attached to
    #                 this Layout.       
    #         Note 2: The global position of one element it's the result of the sum of the local position of 
    #                 this element with the position of the element that contais it(pos_offset). 
    #                 global position = pos_offset + local_pos.
    #         The list returned can be passed to the "Draw" method inside this Lib. 
    # Input : pos_offset       -> Position Offset in pixels. It's used to calculate the global(in the window) position of the 
    #                             elements. It accumulates the offsets up to this Layout.
    #                             Note: The global position of one element it's the result of the sum of the local position of 
    #                                   this element with the position of the element that contais it(pos_offset). 
    #                                   global position = pos_offset + local_pos.       
    # Output: list             -> List of elements draw parameters. Example: list_returned[0] -> It's a list containing the     
    #                             draw parameters for the element attached in the higher and left position of the layout.
    def GetDrawParam(self, pos_offset):
        # Update the position offset with the local position of this Layout.
        pos_offset      = ( pos_offset[0] + self.local_pos[0], pos_offset[1] + self.local_pos[1]  )
        list_draw_param = []
        for line in range(self.num_lines):
            for colum in range(self.num_colums):
                # It is a Image or a Progress Bar.
                if( (self.elements[line][colum].type_of_elem == IMAGE) or (self.elements[line][colum].type_of_elem == PROGRESS_BAR) ):
                    # Append the draw parameters of the visual element into the lists of visual elements to be draw
                    list_draw_param.append( self.elements[line][colum].GetDrawParam(pos_offset) )
                # It is a Panel or a Layout    
                elif( (self.elements[line][colum].type_of_elem == PANEL) or (self.elements[line][colum].type_of_elem == LAYOUT) ):
                    # Join the current list with the lists of the element 
                    list_draw_param = list_draw_param + self.elements[line][colum].GetDrawParam(pos_offset)
        # Returns a list with all draw parameters of all elements inside the layout concatenated     
        return list_draw_param

### Panel Class #################################################################################################################
## That Class represents a panel inside a Window, Panel or even another Panel. 
## A panel it's a structure that mananges the size and position of elements attached to it.
## Elements that can be included are of the type: Image, Progress Bar, Panel, and Layout.  
## A list of elements contain pointers to each element(objects) included in the panel. 
## To resize this panel call the method Resize and after the SetLocalPos method to update the local position of this panel inside
## another element.
## The positioning of the elements inside this panel after the creation of the panel it's handled by the own panel. 
## This class it's not intended to remove or add elements after the object creation.
class Panel:
    
    # Method: Constructor for the class.
    #
    # Input : type_of_panel    -> Type of the panel. The options are: MAIN_PANEL (panel included in a window) or
    #                             SUB_PANEL (panel inside a [Panel|Layout]).  
    #         size             -> Tuple(size in horizontal, size in vertical). Size for the Panel. 
    #                             Note: If this panel it's a MAIN_PANEL, than size probably will be the same of the window
    #                                   that contain this Panel.
    #         local_pos        -> Tuple(position in horizontal, position in vertical). Local position for this 
    #                             Panel inside a [Panel|Layout].
    #                             Note: If this panel it's a MAIN_PANEL, than local_pos probably will be (0, 0).
    #         num_elem         -> Number of elements inside the Panel.
    #         list_of_elements -> List of elements to be inserted in this Panel.    
    #         list_sizes       -> List of the Tuples for each element in Panel. Tuple(size in horizontal, size in vertical).
    #                             Ex: list_sizes[0] have a size tuple for the first element in the list of 
    #                             elements(list_of_elements[0]). Size in Pixels.
    #         list_local_pos   -> List of the Tuples for each element in Panel. Tuple(local position in horizontal, 
    #                             local position in vertical).
    #                             Ex: list_local_pos[0] have a local position tuple for the first element in the list of 
    #                             elements(list_of_elements[0]).  
    #
    # Output: Object of the type Layout constructed.
    def __init__(self, type_of_panel, size, local_pos, num_elem, list_of_elements, list_sizes, list_local_pos):
        # Type of this element -> PANEL
        self.type_of_elem       = PANEL
        # Variable to check if this panel is the Main Panel         
        self.is_main_panel      = type_of_panel
        # Original size of this panel
        self.original_size      = size
        # Current size of this panel
        self.size               = size
        # Local position of this panel
        self.local_pos          = local_pos
        # Number of elements of this panel
        self.num_elem           = num_elem
        # List of pointers to the visual elements(objects) conteined in this panel.
        self.elements           = list_of_elements[:num_elem]            
        # Stores the original list of sizes of the elements
        self.lst_orig_sizes     = list_sizes
        # Set the size of the Elements contained in the panel
        self.SetSizeElements  (self.num_elem, self.elements, self.lst_orig_sizes)
        # Stores the original list of local positions of the elements
        self.lst_orig_local_pos = list_local_pos
        # Set the local position of the Elements contained in the panel
        self.SetLocalPosElements(self.num_elem, self.elements, self.lst_orig_local_pos)

    # Method: Resizes this panel and all elements contained it.
    #         If this panel has elements that contain other elements than the resizing will propagate until all 
    #         elements inside this panel were resized. 
    #         The changes in the panel size will be reflected in the scale factor.
    #         A call to this method probably will be folowed by a call of the SetLocalPos method to update the
    #         local position of this panel. 
    #
    # Input : new_size         -> The new size for the panel.
    #
    # Output: None        
    def Resize(self, new_size):      
        # Scale of fator it's used to deduce the new sizes e positions for the elements included in panel.
        # scale_factor = (scale_factor_horizontal, scale_factor_vertical)
        self.scale_factor = (new_size[0]/self.original_size[0] , new_size[1]/self.original_size[1])
        # Calculate the new sizes for the elements inside this panel
        lst_sizes         = self.CalcSizeElements(self.scale_factor)
        # Calculate the new local positions for the elements inside this panel
        lst_local_pos     = self.CalcLocalPosElements(self.scale_factor)
        # Update the panel size
        self.SetSize(new_size)
        # Update the elements size        
        self.SetSizeElements(self.num_elem, self.elements, lst_sizes)
        # Update the elements local position                
        self.SetLocalPosElements(self.num_elem, self.elements, lst_local_pos)    

    # Method: Calculates new values for the list of sizes for the elements contained in the Panel.
    #         The new sizes for the elements will be based in the ration of the current size of the panel by the original 
    #         size of the panel.
    #         The changes in the panel size will be reflected in the scale factor.
    #  
    # Input : scale_factor     -> Scale factor that will be aplied to the size of the elements contained in this panel.
    #                              The scale factor it's the ratio of the current panel size by the original panel size. 
    #
    # Output: lst_sizes        -> List with new sizes for the elements inside the panel.
    def CalcSizeElements(self, scale_factor):        
        lst_sizes = []
        for elem_order in range(self.num_elem):            
            lst_sizes.append( ( int( scale_factor[0] * self.lst_orig_sizes[elem_order][0]), 
                                int( scale_factor[1] * self.lst_orig_sizes[elem_order][1]) ) )       
        return lst_sizes    
        
    # Method: Calculates new values for the list of positions for the elements contained in the Panel.
    #         The new positions will be based in the ration of the current size of the panel by the original size of the
    #         panel.
    #         The changes in the panel size will be reflected in the scale factor.
    #
    # Input : scale_factor     -> Scale factor that will be aplied to the position of the elements contained in this panel.
    #                              The scale factor it's the ratio of the current panel size by the original panel size. 
    #
    # Output: lst_local_pos    -> List with new local positions for the elements inside the panel.
    def CalcLocalPosElements(self, scale_factor):        
        lst_local_pos = []
        for elem_order in range(self.num_elem):
            lst_local_pos.append( ( int( scale_factor[0] * self.lst_orig_local_pos[elem_order][0] ),
                                    int( scale_factor[1] * self.lst_orig_local_pos[elem_order][1] ) ) )
        return lst_local_pos
               
    # Method: Sets the width and hight for each element inside the Panel.
    #         This values are written inside each object contained in the Panel.
    #         This method accounts for the own panel size.  
    #         Important: After call this method, the method SetLocalPosElements must be called to update the position
    #                    of the elements inside this Panel.    
    # Input : num_elem         -> Number of elements inside the Panel.
    #         list_of_elements -> List of elements contained in this Panel.    
    #         list_sizes       -> List of the Tuples for each element in Panel. Tuple(size in horizontal, size in vertical).
    #                             Ex: list_sizes[0] have a size tuple for the first element in the list of 
    #                             elements(list_of_elements[0]). Size in Pixels. 
    #
    # Output: None
    def SetSizeElements(self, num_elem, list_of_elements, list_sizes):
        for elem_order in range(num_elem):
            list_of_elements[elem_order].SetSize( list_sizes[elem_order] )
                
    # Method: Sets the local position(position inside the Panel) for each element contained in the Panel.
    #         This values are written inside each object contained in the Panel.
    #
    # Input : num_elem         -> Number of elements inside the Panel.
    #         list_of_elements -> List of elements contained in this Panel.    
    #         list_local_pos   -> List of the Tuples for each element in Panel. Tuple(local position in horizontal, 
    #                             local position in vertical).
    #                             Ex: list_local_pos[0] have a local position tuple for the first element in the list of 
    #                             elements(list_of_elements[0]).  
    #
    # Output: None    
    def SetLocalPosElements(self, num_elem, list_of_elements, list_local_pos):        
        for elem_order in range(num_elem):
            list_of_elements[elem_order].SetLocalPos( list_local_pos[elem_order] )
    
    # Method: Sets the size of this Panel. This method also calls SetSizeElements to update the size of the elements contained
    #         in this panel. After call SetSize it's necessary call the function SetLocalPos to update the position of this panel. 
    #
    # Input : size             -> Tuple(size in horizontal, size in vertical). Values for the panel size. Size in Pixels.
    #
    # Output: None
    def SetSize(self, size):       
        self.size = size        
    
    # Method: Sets the local position of this panel inside a [Panel|Layout].
    #
    # Input : local_pos        -> Tuple(position in horizontal, position in vertical). New values for the panel local position. 
    #
    # Output: None    
    def SetLocalPos(self, local_pos):        
        self.local_pos = local_pos  
    
    # Method: Returns the current size of this Panel. 
    #
    # Input : None
    #
    # Output: size             -> Tuple(size in horizontal, size in vertical)
    def GetSize(self):       
        return self.size
    
    # Method: Returns the current local position of this Panel inside a [Panel|Layout|Window]. 
    #
    # Input : None
    #
    # Output: size             -> Tuple(size in horizontal, size in vertical)
    def GetLocalPos(self):        
        return self.local_pos    

    # Method: Returns a list of elements draw parameters.
    #         The size of the list returned is (num_elem). 
    #         Each position in the returned list it's a list of draw parameters for the element contained in this panel.
    #         Example: list_returned[0] -> It's a list containing the draw parameters for the first included element in this panel.
    #         Note 1: If a element contained in this panel is a [Panel|Layout] than the list returned will be the result of
    #                 the concatenation between the list of elements draw parameters of all other elements inside the this panel
    #                 with the list of elements draw parameters of the element of the type [Panel|Layout] also contained in
    #                 this Layout.       
    #         Note 2: The global position of one element it's the result of the sum of the local position of 
    #                 this element with the position of the element that contais it(pos_offset). 
    #                 global position = pos_offset + local_pos.
    #         The list returned can be passed to the "Draw" method inside this Lib. 
    # Input : pos_offset       -> Position Offset in pixels. It's used to calculate the global(in the window) position of the 
    #                             elements. It accumulates the offsets up to this Panel.
    #                             Note: The global position of one element it's the result of the sum of the local position of 
    #                                   this element with the position of the element that contais it(pos_offset). 
    #                                   global position = pos_offset + local_pos.       
    # Output: list             -> List of elements draw parameters. Example: list_returned[0] -> It's a list containing the     
    #                             draw parameters for the first included element in this Panel.
    def GetDrawParam(self, pos_offset):
        # Update the position offset with the local position of this Panel.
        pos_offset      = ( pos_offset[0] + self.local_pos[0], pos_offset[1] + self.local_pos[1]  )
        list_draw_param = []
        for elem_order in range(self.num_elem):
            # It is a Image or a Progress Bar.
            if( (self.elements[elem_order].type_of_elem == IMAGE) or (self.elements[elem_order].type_of_elem == PROGRESS_BAR) ):
                # Append the draw parameters of the visual element into the lists of visual elements to be draw
                list_draw_param.append( self.elements[elem_order].GetDrawParam(pos_offset) )
            # It is a Panel or a Layout    
            elif( (self.elements[elem_order].type_of_elem == PANEL) or (self.elements[elem_order].type_of_elem == LAYOUT) ):
                # Join the current list with the lists of the element 
                list_draw_param = list_draw_param + self.elements[elem_order].GetDrawParam(pos_offset)
        # Returns a list with all draw parameters of all elements inside the panel concatenated     
        return list_draw_param    

        
### Global Methods ##############################################################################################################    
def Draw(win, elem_draw_param):
    num_elem = len(elem_draw_param)
    for num_elem in range(num_elem):        
        # Visual element it's a Progress Bar
        if( elem_draw_param[num_elem][0] == PROGRESS_BAR ):
            pg.draw.rect(win, elem_draw_param[num_elem][5], (*elem_draw_param[num_elem][2], *elem_draw_param[num_elem][1]), 1)
            pg.draw.rect(win, elem_draw_param[num_elem][6], (*elem_draw_param[num_elem][4], *elem_draw_param[num_elem][3])   )    
            

