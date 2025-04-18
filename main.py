import pygame
from Scripts.Monde import *
from Scripts.Variables_Globales import *
from Scripts.TextureManager import *
from Scripts.SaveManager import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pack = TexturePack("Assets/Realistic_Pack/Realistic_Pack.json")
fond = "Assets/fond.png"

monde = Carte(MAP_SIZE_X,MAP_SIZE_Y)
monde.generer(biomes_disponibles)
sauvegarde_actuelle = "save-1"

hex_calculateur = Hexagone([DEPART_X, DEPART_Y])

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
        if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F5:
                        save_map(monde, sauvegarde_actuelle)
                        print(f"Map sauvegardé en '{sauvegarde_actuelle}.json'")
                    if event.key == pygame.K_F6:
                        sauvegarde = load_map(sauvegarde_actuelle)
                        if sauvegarde:
                            monde = sauvegarde
                            print(f"Sauvegarde '{sauvegarde_actuelle}.json' en chargement...")
                    if event.key == pygame.K_F7:
                        monde = Carte(MAP_SIZE_X, MAP_SIZE_Y)
                        monde.generer(biomes_disponibles)
                        print("Nouvelle map en génération...")

    screen.fill((255, 255, 255))
    monde.dessin(screen, pack, debugging=False)
    pygame.display.flip()
    clock.tick(FRAMERATE)
