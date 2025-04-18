import pygame
from Scripts.Monde import *
from Scripts.Variables_Globales import *
from Scripts.TextureManager import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pack = TexturePack("Assets/Realistic_Pack/Realistic_Pack.json")
fond = "Assets/fond.png"

monde = Carte(17,12)
monde.generer(biomes_disponibles)

hex_calculateur = Hexagone([DEPART_X, DEPART_Y], 'montagne')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            hexagone_cible = monde.get_hex_at_position(mouse_pos)
            if hexagone_cible:
                coord_q, coord_r = hexagone_cible.coordonnees_axiales
                print(f"Coordonnées: {coord_q}, {coord_r}, Biome: {hexagone_cible.biome}")

    screen.fill((255, 255, 255))
    monde.dessin(screen, pack, debugging=False)
    pygame.display.flip()
    clock.tick(FRAMERATE)
