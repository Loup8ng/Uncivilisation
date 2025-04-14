import pygame

pygame.init()

# Création de l'écran
screen = pygame.display.set_mode((500, 500))
screen.fill((255, 255, 255))

# Chargement de l'hexagone rouge
hexa_rouge = pygame.image.load("hexagone_rouge.png").convert_alpha()
screen.blit(hexa_rouge, (0, 0))
pygame.display.flip()

# Coefficient directeur
a = 1.70  # La pente des droites

def draw_base():
    """ Redessine l'hexagone et la ligne de base """
    screen.fill((255, 255, 255))  # Nettoie l'écran
    screen.blit(hexa_rouge, (0, 0))  # Replace l'image de l'hexagone
    pygame.display.flip()

def calcul_coordonnées (position,)

running = True
draw_base()

while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
               position = event.pos
pygame.quit()
