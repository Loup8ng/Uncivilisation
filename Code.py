import pygame
from Scripts.Monde import *
from Scripts.Variables_Globales import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

image = "Assets/plaine.png"
hexa_rouge = "Assets/hexagone_rouge.png"
hexa_foret = "Assets/hexagone_foret.png"
hexa_lac = "Assets/hexagone_lac.png"

monde=Carte(20, 10, "Assets/fond.png")
monde.generer_hexagones(hexa_lac)
hexa = Hexagone((OFFSET_X,OFFSET_Y), image)
running= True
#swip = False   
#start_x, start_y = 0, 0 

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            coord_hex = hexa.pixel_to_flat_hex(mouse_pos)
            print(coord_hex)

    screen.fill((255, 255, 255)) 
    monde.dessin(screen)
    pygame.display.flip()
    clock.tick(FRAMERATE)