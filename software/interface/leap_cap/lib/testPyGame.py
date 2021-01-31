import pygame as pg

white = (255,255,255)
win_size = (1368, 768)
win_size = (800, 600)
pg.init()
pg_win = pg.display.set_mode(size= win_size)

pg_win.fill(white)  
pg.display.update()

close = False

while not close:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            #pg.quit() #sys.exit() if sys is imported    
            pg.display.quit()
            close = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                print("Mínimo esquerdo")
            if event.key == pg.K_2:
                print("Anular esquerdo")
            if event.key == pg.K_3:
                print("Médio esquerdo")
            if event.key == pg.K_4:
                print("Indicador esquerdo")
                            # Close Window
            if event.key == pg.K_ESCAPE:
                pg.display.quit()
                close = True
       