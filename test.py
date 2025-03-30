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

def draw_parallel_line(position):
    """ Dessine une droite parallèle passant par le point cliqué """
    x0, y0 = position  # Récupère le point cliqué
    b_prime = y0 - a * x0  # Nouvelle ordonnée à l'origine
    print(b_prime)
    
    # On trace la droite parallèle avec le même coefficient directeur
    x1, y1 = 0, a * 0 + b_prime  # Point à x=0
    x2, y2 = 500, a * 500 + b_prime  # Point à x=500
    print (a*500+b_prime)
    

    pygame.draw.line(screen, (255, 0, 0), (x1, y1), (x2, y2), 2)  # Ligne rouge
    pygame.display.flip()

running = True
draw_base()

while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                draw_parallel_line(event.pos)  # Dessine une ligne parallèle au clic

pygame.quit()

   