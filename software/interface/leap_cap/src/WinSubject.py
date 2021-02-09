import sys
import os

# obtain the myograph path
myograph_import_path = os.path.split( os.path.split( os.path.split(os.path.abspath(__file__))[0] )[0] )[0]
# adds the myograph path for future inclusions 
sys.path.append(myograph_import_path)
images_path = os.path.join( os.path.join( os.path.join(myograph_import_path, 'leap_cap') , 'images') , '')    


import pygame as pg
import Constants as const
import UiSubject

DEFAULT_WIN_SIZE = (800, 600)
DEFAULT_IMG_NAMES = ['1th_flex.png', '1th_flex_curlEC.png', '2in_flexEC.png', '2in_flex_curlEC.png']

class WinSubject:
    
    def __init__(self):
        self.ui_subject = UiSubject.UiSubject()    
                
    def show(self):
        pg.init()
        self.ui_subject.win = pg.display.set_mode(size=self.ui_subject.win_size, flags = pg.RESIZABLE)                
        self.ui_subject.win.fill(self.ui_subject.white)  
        pg.display.set_caption(self.ui_subject.win_title)
        self.ui_subject.drawImages()
        self.ui_subject.SetTimeBarsProgress(0.5, 0.75)
        self.ui_subject.drawTimeBars()
        # Uncoment the next line to show the panel perimeters
        self.ui_subject.PrintPanelPerimeters()
        pg.display.flip()
        
    def close(self):
        pg.display.quit()

    def getKey(self):
        
        if not(self.ui_subject.close):
            
            # Redraw the images            
            #self.drawImages()    
            
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.display.quit(); #sys.exit() if sys is imported
                        self.ui_subject.close = True
                        
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
                        #print('Window resized')
                        #print( 'New resolution: (%d, %d)' % pg.display.get_window_size() )
                        self.ui_subject.win_size = pg.display.get_window_size()
                        self.ui_subject.UpdatePanelsSize()                        
                        self.ui_subject.win.fill(self.ui_subject.white)
                        self.ui_subject.drawImages()
                        self.ui_subject.drawTimeBars()
                        # Uncoment the next line to show the panel perimeters
                        self.ui_subject.PrintPanelPerimeters()
                        pg.display.flip()
                        
            else:   
                    return const.NO_KEY_PRESSED
                           
                
        return const.CLOSE_SUBJECT_WIN            
                    
    
