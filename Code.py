import pygame
from Scripts.Monde import *
from Scripts.Variables_Globales import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1400, 800))

image = pygame.image.load("Assets/plaine.png").convert_alpha()
hexa_rouge = pygame.image.load("Assets/hexagone_rouge.png").convert_alpha()
hexa_foret = pygame.image.load("Assets/hexagone_foret.png").convert_alpha()
hexa_lac = pygame.image.load("Assets/hexagone_lac.png").convert_alpha()

monde=Carte(1, 1)
monde.generation_hexagone(hexa_rouge, hexa_lac, image)
screen.blit(monde.charger_background(background), (0,0))
running= True
swip = False  
start_x, start_y = 0, 0 

# la boucle servant à faire fonctionner LE TRUC 
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                position = event.pos
                monde.afficher_onglet(position, screen, hexa_rouge, hexa_lac, image)
            elif event.button == 3:  # Clic droit pour commencer à déplacer la carte
                swip = True
                pos_depart_x, pos_depart_y = event.pos  # garde la position initiale du clic droit
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  
                swip = False
        if event.type == pygame.MOUSEMOTION:
            if swip:  # deplacer la carte si le clic droit est enfonce
                dx, dy = event.pos[0] - pos_depart_x, event.pos[1] - pos_depart_y
                monde.clic_x += dx
                monde.clic_y += dy
                pos_depart_x, pos_depart_y = event.pos
        
    #Redessiner la carte avec le déplacement
    screen.fill((255, 255, 255))  
    screen.blit(monde.charger_background(background), (0,0))
    monde.dessin(screen)
    pygame.display.flip()
    clock.tick(FRAMERATE)

pygame.quit()
#objectif de la rentrée/ ajouter de la generation logique  aleatoire / deplacer les unités sur la carte/ deplacement de la carte 