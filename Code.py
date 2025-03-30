import pygame
import random

pygame.init()

screen = pygame.display.set_mode((1400, 800))
screen.fill((255,255,255))
pygame.display.flip()

longueur = 9
largeur = 4

background = pygame.transform.scale(pygame.image.load("fond.png"), (1400, 800)).convert_alpha()
image = pygame.image.load("plaine.png").convert_alpha()
hexa_rouge = pygame.image.load("hexagone_rouge.png").convert_alpha()
hexa_foret = pygame.image.load("hexagone_foret.png").convert_alpha()
hexa_lac = pygame.image.load("hexagone_lac.png").convert_alpha()

class Unite:
    def __init__(self, hp, attq):
        self.hp = hp
        self.attq = attq

    def se_deplacer(self):
        pass  # À implémenter

class Carte:
    def __init__(self, longueur=longueur, largeur=largeur):
        self.longueur = longueur
        self.largeur = largeur
        self.matrice = []

    def calcul_coordonnées(self, position): 
        a = 1.7
        v = 173
        x0, y0 = position
        b = 88
        b_prime = y0 - a * x0
        
        liste = []
        for i in range(self.longueur): 
            k = 0
            for j in range(3): 
                l = a * 500 + b + k * v
                k += 1
                liste.append(l)
        
        hexa = 200 
        num_hexa = round (x0 / hexa)  # Assure un entier
        y1 = a * 500 + b_prime

        liste_d = [0, 1]
        a = 1
        while a < self.longueur:
            a += 2
            liste_d.append(a)
        
        liste_y = [0]
        for i in range(self.largeur):  
            liste_y.append(i)

        if 0 <= num_hexa < len(liste):  
            if liste[num_hexa] - y1 < 86.5: 
                d = int(liste[num_hexa - 1] // v) if num_hexa > 0 else 0
            else: 
                d = int(liste[num_hexa] // v)

            for i in range(len(liste_d) - 1): 
                if liste_d[i] <= d <= liste_d[i+1] and liste_y[i] <= y1: 
                    d = min(max(0, d), self.longueur - 1)  # Empêcher les indices hors limites
                    i = min(max(0, i), self.largeur - 1)  
                    print(f"Hexagone trouvé: ({d}, {i})")  # Debug
                    return d, i  # Indices valides

        print("Aucun hexagone trouvé.")  # Debug
        return None



    def generation_hexagone(self):
        a = 1
        x = 0
        y = 0
        for i in range(self.longueur):
            ligne = []
            for j in range(self.largeur):
                biome = random.choice([hexa_foret, hexa_rouge, hexa_lac, image])
                ligne.append({"biome": biome, "x": x, "y": y})
                y += 174
            self.matrice.append(ligne)
            if a == 1:
                y = 88
                a = 0
            else:
                y = 0
                a = 1
            x += 151
    

    def dessin(self):
        for ligne in self.matrice:
            for hexa in ligne:
                screen.blit(hexa["biome"], (hexa["x"], hexa["y"]))
        pygame.display.flip()

    def afficher_onglet(self, position):
        dialog_surface = pygame.Surface((600, 400))
        dialog_surface.fill((50, 50, 50))
        police = pygame.font.Font(None, 50)

        coord = self.calcul_coordonnées(position)
        print (position, coord)
        if coord:
            i, j = coord
            hexa = self.matrice[i][j]
            x, y = hexa["x"], hexa["y"]

            if hexa["biome"] == image:
                biome_name = "Plaine"
            elif hexa["biome"] == hexa_rouge:
                biome_name = "Montagne"
            elif hexa["biome"] == hexa_foret:
                biome_name = "Forêt"
            else:
                biome_name = "Lac"

            texte_biome = police.render(f"Biome: {biome_name}", True, (255, 255, 255))
            texte_coord = police.render(f"Coord: ({x}, {y})", True, (255, 255, 255))

            dialog_surface.blit(texte_biome, (50, 100))
            dialog_surface.blit(texte_coord, (50, 200))

        screen.blit(dialog_surface, (625, 300))  
        pygame.display.flip()

        dialog_running = True
        while dialog_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    dialog_running = False
                    self.dessin()

fbir = Carte()
fbir.generation_hexagone()
screen.blit(background, (0,0))
fbir.dessin()
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                position = event.pos
                fbir.afficher_onglet(position)

pygame.quit()
