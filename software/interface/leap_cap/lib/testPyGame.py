import pygame

pygame.init()
pygame.display.set_mode(size=(800,600))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print("Mínimo esquerdo")
            if event.key == pygame.K_2:
                print("Anular esquerdo")
            if event.key == pygame.K_3:
                print("Médio esquerdo")
            if event.key == pygame.K_4:
                print("Indicador esquerdo")
