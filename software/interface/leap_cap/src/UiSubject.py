# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 19:17:30 2021

@author: Asaphe Magno
"""

import sys
import os

# obtain the myograph path
myograph_import_path = os.path.split( os.path.split( os.path.split(os.path.abspath(__file__))[0] )[0] )[0]
# adds the myograph path for future inclusions 
sys.path.append(myograph_import_path)
images_path = os.path.join( os.path.join( os.path.join(myograph_import_path, 'leap_cap') , 'images') , '')    


import pygame as pg

DEFAULT_WIN_SIZE = (800, 600)
DEFAULT_IMG_NAMES = ['1th_flex.png', '1th_flex_curlEC.png', '2in_flexEC.png', '2in_flex_curlEC.png']


class UiSubject:
    
    def __init__(self):
        # Colors        
        self.black = (0, 0, 0)
        self.red  = (255, 0, 0)
        self.green  = (0, 255, 0)
        self.blue  = (0, 0, 255)
        self.white = (255, 255, 255)
        
        # Win title
        self.win_title = 'Subject'
        self.win = None
        # Elements resolution        
        self.win_size = DEFAULT_WIN_SIZE
        # State Variables
        self.close = False      
        
        # Margin in parts of width and high of the screen
        self.x_margin = 0.02
        self.y_margin = 0.03
        
        # Images panel
        ## Images panel screen percentage
        self.images_pn_screen_perc = 0.5
        self.img_panel_size = ( self.win_size[0], int( self.images_pn_screen_perc * self.win_size[1]) )
        self.img_panel_pos  = (0, 0)
        # Number of images on screen
        self.num_images = 4
        self.orig_images_res = (310, 370)          
        # Current images resolution. It will be updated in every redraw.            
        self.current_img_res = self.orig_images_res
        self.image_margin_px = (0, 0)
        # Elements position. It will be updated in every redraw.
        self.images_position = [(0, 0), (0, 0), (0, 0), (0, 0)]
        # List with four images
        self.images = [0, 0, 0, 0]
        # Load the four imagens. A list with 4 image names it's passed.
        self.loadImages(DEFAULT_IMG_NAMES) 
                
        # Time bar painel
        ## Time panel vertical screen percentage        
        self.time_bars_pn_scree_perc  = 0.09        
        self.time_bars_pn_size = ( self.win_size[0], int( self.time_bars_pn_scree_perc * self.win_size[1]) )
        self.time_bars_pn_pos  = ( 0, self.img_panel_size[1])
        
        # Picture time bar. That bar that stay under the first image. 
        self.time_pic_bar_pos      = (self.image_margin_px[0], self.time_bars_pn_pos[1] + self.image_margin_px[1])
        ## 14 px for bars have a good look in a window with vertical resolutions around 600 px
        self.time_pic_bar_size     = (self.current_img_res[0], (14 * self.win_size[1]) / 600 )
        self.time_pic_bar_border_color = self.black
        self.time_pic_bar_color    = self.blue
        self.time_pic_bar_perc     = 0.2
        
        # Experiment time bar.
        self.exper_time_bar_pos      = (self.image_margin_px[0], self.time_bars_pn_pos[1] + self.time_pic_bar_size[1] + 2 * self.image_margin_px[1])
        ## 14 px for bars have a good look in a window with vertical resolutions around 600 px
        self.exper_time_bar_size     = (self.win_size[0] - 2 * self.image_margin_px[0], (14 * self.win_size[1]) / 600)
        self.exper_time_bar_border_color = self.black
        self.exper_time_bar_color    = self.blue
        self.exper_time_bar_perc     = 0.3
        
        # Joint angles painel
        ## Joint panel vertical screen percentage        
        self.joint_angles_pn_scree_perc  = 0.2        
        self.joint_angles_pn_size = ( self.current_img_res[0], int( self.joint_angles_pn_scree_perc * self.win_size[1]) )
        self.joint_angles_pn_pos  = ( self.image_margin_px[0], self.img_panel_size[1] + self.time_bars_pn_size[1] )
        
        # Fingers with joint angles
        #self.fingers =  [[,], [,], [,], [,] ]
        
        # Joint Bars
        
        
    def UpdatePanelsSize(self):
        self.UpdateImagesPanel()
        self.UpdateTimeBarsPanel()
        self.UpdateJointAnglesPanel()
        
    def UpdateJointAnglesPanel(self):
        self.joint_angles_pn_size = ( self.current_img_res[0], int( self.joint_angles_pn_scree_perc * self.win_size[1]) )
        self.joint_angles_pn_pos  = ( self.image_margin_px[0], self.img_panel_size[1] + self.time_bars_pn_size[1] )
        
    def UpdateImagesPanel(self):
        self.img_panel_size = ( self.win_size[0], int( self.images_pn_screen_perc * self.win_size[1]) )
    
    def UpdateTimeBarsPanel(self):
        self.time_bars_pn_size = ( self.win_size[0], int( self.time_bars_pn_scree_perc * self.win_size[1]) )
        self.time_bars_pn_pos  = ( 0, self.img_panel_size[1])        
        
    def updateTimeBarsPos(self):
        self.updateImgPos()
        # update the picture time bar 
        self.time_pic_bar_pos      = (self.image_margin_px[0] , self.time_bars_pn_pos[1] + self.image_margin_px[1])
        ## 14 px for bars have a good look in a window with vertical resolutions around 600 px
        self.time_pic_bar_size     = (self.current_img_res[0], (14 * self.win_size[1]) / 600 )
        # update the experiment time bar
        self.exper_time_bar_pos      = (self.image_margin_px[0], self.time_bars_pn_pos[1] + self.time_pic_bar_size[1] + 2 * self.image_margin_px[1])
        ## 14 px for bars have a good look in a window with vertical resolutions around 600 px
        self.exper_time_bar_size     = (self.win_size[0] - 2 * self.image_margin_px[0], (14 * self.win_size[1]) / 600)
    
    def drawTimeBars(self):
        self.updateTimeBarsPos()
        # Draw time picture bar
        self.DrawHorBar(self.time_pic_bar_pos, self.time_pic_bar_size, self.time_pic_bar_border_color, self.time_pic_bar_color, self.time_pic_bar_perc)
        # Draw experiment time bar
        self.DrawHorBar(self.exper_time_bar_pos, self.exper_time_bar_size, self.exper_time_bar_border_color, self.exper_time_bar_color, self.exper_time_bar_perc)        
                
        #self.DrawVertBar( (200,500), self.time_pic_bar_size, self.time_pic_bar_border_color, self.time_pic_bar_color, 0.7)
        
    def SetTimeBarsProgress(self, time_pic_bar_perc, exper_time_bar_perc):
        self.time_pic_bar_perc   = time_pic_bar_perc 
        self.exper_time_bar_perc = exper_time_bar_perc
        
    def DrawHorBar(self, pos, size, border_color, bar_color, progress):
        pg.draw.rect(self.win, border_color, (*pos, *size), 1)
        innerPos  = (pos[0]+3, pos[1]+3)
        innerSize = ((size[0]-6) * progress, size[1]-6)
        pg.draw.rect(self.win, bar_color, (*innerPos, *innerSize))    
        
    def DrawVertBar(self, pos, size, border_color, bar_color, progress):
        pg.draw.rect(self.win, border_color, (*pos, *size), 1)
        innerPos  = (pos[0]+3, pos[1]+ 3 + ( (size[1]-6) -(size[1]-6) * progress ) )
        innerSize = (size[0]-6, (size[1]-6) * progress )
        pg.draw.rect(self.win, bar_color, (*innerPos, *innerSize))    

    def updateImgMargPx(self):
        self.image_margin_px = ( (self.x_margin) * self.img_panel_size[0] , (self.y_margin) * self.img_panel_size[1] )
        #print('x margin in px: %d' % self.image_margin_px[0])
        #print('y margin in px: %d' % self.image_margin_px[1])
        
    def updateImgRes(self):
        self.updateImgMargPx()
        image_hor_res    = ( self.img_panel_size[0] - (2 + (self.num_images - 1) ) * self.image_margin_px[0] ) / self.num_images 
        image_vert_res   =   self.img_panel_size[1] - ( 2 * self.image_margin_px[1] )
        self.current_img_res = int(image_hor_res) , int(image_vert_res)        
        #print( 'Image Resolution: %d,%d' % (image_hor_res, image_vert_res) )        
    
    def updateImgPos(self):
        self.updateImgRes()
        self.images_position = [ (self.image_margin_px[0], self.image_margin_px[1]),
                                 ( (2 * self.image_margin_px[0] +     self.current_img_res[0]), self.image_margin_px[1]),
                                 ( (3 * self.image_margin_px[0] + 2 * self.current_img_res[0]), self.image_margin_px[1]),
                                 ( (4 * self.image_margin_px[0] + 3 * self.current_img_res[0]), self.image_margin_px[1])  ]
        
        #for img_pos in range(4):            
        #    print( 'Image %d Position : %d,%d' % ( img_pos, self.images_position[img_pos][0], self.images_position[img_pos][1] ) ) 

    # image_names it's a list of 4 strings with the image names. 
    def loadImages(self, image_names):     
        for num_img in range(4):
            self.images[num_img] = pg.image.load(images_path + image_names[num_img])
        
    def rescaleImages(self):
        # reload the images
        self.loadImages(DEFAULT_IMG_NAMES)        
        # rescale the image
        for num_img in range(4):
            self.images[num_img] = pg.transform.scale(self.images[num_img], self.current_img_res)

    def drawImages(self):
        self.updateImgPos()
        self.rescaleImages()
        # draw the images
        for num_img in range(4):
            self.win.blit(self.images[num_img], self.images_position[num_img])       
    
    # Method used to check the panels position
    def PrintPanelPerimeters(self):          
        self.UpdatePanelsSize()
        pg.draw.rect(self.win, self.green,( *self.img_panel_pos, *self.img_panel_size), 1)
        pg.draw.rect(self.win, self.red,( *self.time_bars_pn_pos, *self.time_bars_pn_size), 1)
        pg.draw.rect(self.win, self.green,( *self.joint_angles_pn_pos, *self.joint_angles_pn_size), 1)