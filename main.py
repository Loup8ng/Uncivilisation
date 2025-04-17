import pygame
from Scripts.Monde import *
from Scripts.Variables_Globales import *
from Scripts.TextureManager import * 

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pack = TexturePack("Assets/Realistic_Pack/Realistic_Pack.json")

fond = "Assets/fond.png"
monde = Carte(50, 22, fond)
monde.generer(biomes_disponibles)
hexa = Hexagone((OFFSET_X,OFFSET_Y), 'montagne')
running= True
#swip = False

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            coord_hex = hexa.pixel_to_hex(mouse_pos)
            print(coord_hex)

    screen.fill((255, 255, 255)) 
    monde.dessin(screen, pack)
    pygame.display.flip()
    clock.tick(FRAMERATE)