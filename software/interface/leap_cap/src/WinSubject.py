import sys
import os

# obtain the myograph path
myograph_import_path = os.path.split( os.path.split( os.path.split(os.path.abspath(__file__))[0] )[0] )[0]
# adds the myograph path for future inclusions 
sys.path.append(myograph_import_path)
images_path = os.path.join( os.path.join( os.path.join(myograph_import_path, 'leap_cap') , 'images') , '')    


import pygame as pg
import Constants as const

DEFAULT_WIN_SIZE = (800, 600)
DEFAULT_IMG_NAMES = ['1th_flex.png', '1th_flex_curlEC.png', '2in_flexEC.png', '2in_flex_curlEC.png']

class WinSubject:
    
    def __init__(self):
        # Number of images on screen
        self.num_images = 4
        # Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        # Margin in parts of width and high of the screen
        self.x_margin = 0.02
        self.y_margin = 0.02
        # Elements resolution        
        self.win_size = DEFAULT_WIN_SIZE
        self.img_panel_size = ( self.win_size[0], int( 0.5 * self.win_size[1]) )
        self.orig_images_res = (310, 370)          
        # Current images resolution. It will be updated in every redraw.            
        self.current_img_res = self.orig_images_res
        # Elements position. It will be updated in every redraw.
        self.images_position = [(0, 0), (0, 0), (0, 0), (0, 0)]
        # List with four images
        self.images = [0, 0, 0, 0]
        # Load the four imagens. A list with 4 image names it's passed.
        self.loadImages(DEFAULT_IMG_NAMES) 
        # Win title
        self.win_title = 'Subject'
        self.win = None
        # State Variables
        self.close = False      


    def updateImgMargPx(self):
        self.image_margin_px = ( (self.x_margin) * self.img_panel_size[0] , (self.y_margin) * self.img_panel_size[1] )
        print('x margin in px: %d' % self.image_margin_px[0])
        print('y margin in px: %d' % self.image_margin_px[1])
        
    def updateImgRes(self):
        self.updateImgMargPx()
        image_hor_res    = ( self.img_panel_size[0] - (2 + (self.num_images - 1) ) * self.image_margin_px[0] ) / self.num_images 
        image_vert_res   =   self.img_panel_size[1] - ( 2 * self.image_margin_px[1] )
        self.current_img_res = int(image_hor_res) , int(image_vert_res)        
        print( 'Image Resolution: %d,%d' % (image_hor_res, image_vert_res) )        
    
    def updateImgPos(self):
        self.updateImgRes()
        self.images_position = [ (self.image_margin_px[0], self.image_margin_px[1]),
                                 ( (2 * self.image_margin_px[0] +     self.current_img_res[0]), self.image_margin_px[1]),
                                 ( (3 * self.image_margin_px[0] + 2 * self.current_img_res[0]), self.image_margin_px[1]),
                                 ( (4 * self.image_margin_px[0] + 3 * self.current_img_res[0]), self.image_margin_px[1])  ]
        
        for img_pos in range(4):            
            print( 'Image %d Position : %d,%d' % ( img_pos, self.images_position[img_pos][0], self.images_position[img_pos][1] ) ) 

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
        pg.display.flip()    
                
    def show(self):
        pg.init()
        self.win = pg.display.set_mode(size=self.win_size, flags = pg.RESIZABLE)                
        self.win.fill(self.white)  
        pg.display.set_caption(self.win_title)
        self.drawImages()
        
    def close(self):
        pg.display.quit()

    def getKey(self):
        
        if not(self.close):
            
            # Redraw the images            
            #self.drawImages()    
            
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.display.quit(); #sys.exit() if sys is imported
                        self.close = True
                        
                    if event.type == pg.KEYDOWN:                                      
                        # left hand
                        if event.key == pg.K_1:
                            #return const.PINKY
                            return 'PINKY'
                        if event.key == pg.K_2:
                            #return const.RING
                            return 'RING'
                        if event.key == pg.K_3:
                            #return const.MIDDLE
                            return 'MIDDLE'
                        if event.key == pg.K_4:
                            #return const.INDICATOR
                            return 'INDICATOR'
                        if event.key == pg.K_SPACE:
                            #return const.THUMB
                            return 'THUMB'
                        
                        # right hand
                        if event.key == pg.K_SPACE:
                            #return const.THUMB 
                            return 'THUMB'
                        if event.key == pg.K_7:
                            #return const.INDICATOR
                            return 'INDICATOR'
                        if event.key == pg.K_8:
                            #return const.MIDDLE
                            return 'MIDDLE'
                        if event.key == pg.K_9:
                            #return const.RING
                            return 'RING'
                        if event.key == pg.K_0:
                            #return const.PINKY        
                            return 'PINKY'
                        
                    if(event.type == pg.VIDEORESIZE):
                        print('Window resized')
                        print( 'New resolution: (%d, %d)' % pg.display.get_window_size() )
                        self.win_size = pg.display.get_window_size()
                        self.img_panel_size = ( self.win_size[0], int( 0.5 * self.win_size[1]) )
                        self.win.fill(self.white)
                        self.drawImages()
                        
                        
            else:   
                    return const.NO_KEY_PRESSED
                           
                
        return const.CLOSE_SUBJECT_WIN            
                    
    
