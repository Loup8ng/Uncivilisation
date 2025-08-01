import pygame
from Scripts.Monde import *
from Scripts.Variables_Globales import *
from Scripts.TextureManager import *
from Scripts.SaveManager import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
texture_pack = TexturePack("Assets/Realistic_Pack/Realistic_Pack.json")

monde = Carte(MAP_SIZE_X,MAP_SIZE_Y)
monde.generer(biomes_disponibles)
sauvegarde_actuelle = "save-50x50"

swipping = False
last_mouse_pos = None

hex_calculateur = Hexagone([0, 0])
is_coordonnees_visibles = False

running = True
fenetre_ouverte=False
while running:
    pygame.display.set_caption(str(clock.get_fps()))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not fenetre_ouverte:
                mouse_pos = pygame.mouse.get_pos()
                hexagone_cible = monde.get_hex_at_position(mouse_pos)
                if hexagone_cible:
                    coord_q, coord_r = hexagone_cible.coordonnees_axiales
                    print(f"Coordonnées: {coord_q}, {coord_r}, Biome: {hexagone_cible.biome}, ressources: {hexagone_cible.ressources_biomes}")
            if event.button == 3:
                swipping = True
                last_mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                swipping = False
        if event.type == pygame.MOUSEMOTION:
            if swipping:
                current_mouse_pos = pygame.mouse.get_pos()
                direction_x = current_mouse_pos[0] - last_mouse_pos[0]
                direction_y = current_mouse_pos[1] - last_mouse_pos[1]
                monde.swip(direction_x, direction_y)
                last_mouse_pos = current_mouse_pos
        if event.type == pygame.MOUSEWHEEL:
            coord_mouse_x, coord_mouse_y = pygame.mouse.get_pos()
            if event.y > 0:
                facteur_zoom = 1.0 + ZOOM_SPEED
            else:
                facteur_zoom = 1.0 - ZOOM_SPEED
            monde.zoomer_vers(facteur_zoom, coord_mouse_x, coord_mouse_y)
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
            if event.key == pygame.K_F8:
                if is_coordonnees_visibles :
                    is_coordonnees_visibles = False
                else:
                    is_coordonnees_visibles = True
            if event.key == pygame.K_c:
                # Toggle affichage de la "fenêtre"
                fenetre_ouverte = not fenetre_ouverte
        if event.type == pygame.MOUSEBUTTONDOWN:
            if fenetre_ouverte and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                 # Dans le traitement des clics
                bouton_rect = pygame.Rect(210, 160, 200, 40)
                if bouton_rect.collidepoint(mouse_x, mouse_y):
                    fenetre_ouverte = False
                # Rectangle de la "fenêtre"
                fenetre_rect = pygame.Rect(200, 150, 500, 400)
                if fenetre_rect.collidepoint(mouse_x, mouse_y):
                   pass
                else:
                    fenetre_ouverte = not fenetre_ouverte


                

    screen.fill((255, 255, 255))
    monde.dessin(screen, texture_pack, is_coordonnees_visibles)

    if fenetre_ouverte:
        overlay = pygame.Surface((500, 400), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # fond semi-transparent
        screen.blit(overlay, (200, 150))
        pygame.draw.rect(screen, (255, 255, 255), (200, 150, 500, 400), 3)

        font = pygame.font.SysFont("arial", 24)
        texte = font.render("Menu de contruction (appuie sur C pour fermer)", True, (255, 255, 255))
        screen.blit(texte, (220, 160))

        # Dans le dessin de la fenêtre
        rect1=pygame.draw.rect(screen, (100, 200, 100), (210, 160, 150, 100))  # bouton vert
        image_boutton1 = pygame.transform.scale(pygame.image.load("Assets/mine_lvl_1.png"),(150, 100)).convert_alpha()
        screen.blit(image_boutton1, (210, 160))

    pygame.display.flip()
    clock.tick(FRAMERATE)
