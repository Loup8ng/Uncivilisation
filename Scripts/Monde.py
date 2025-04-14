import pygame
import json
import random
from Scripts.Variables_Globales import *

class Carte:
    def __init__(self, longueur, largeur):
        """Initialise les longueur et largeur de la carte ainsi que la matrice pour la stocker."""
        self.longueur = longueur
        self.largeur = largeur
        self.matrice = []
        self.clic_x = 0  
        self.clic_y = 0

    def charger_background(self, chemin_sprite:str) -> None:
        return pygame.transform.scale(pygame.image.load(chemin_sprite), (SCREEN_HEIGHT, SCREEN_WIDTH)).convert_alpha()

    def charger_hex(self, chemin_sprite:str) -> None:
        return pygame.image.load(chemin_sprite).convert_alpha()

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

    def generation_hexagone (self, hexa_rouge, hexa_lac, image): 
        """Génère tous les hexagones de la carte en les stockant dans une matrice"""
        a=1
        x=0
        y=0
        for i in range (self.longueur) :
            liste=[]
            for j in range(self.largeur):
                biome = self.generer_biome_voisins(i,j, hexa_rouge, hexa_lac, image)
                liste.append({"biome":biome, "x": x, "y":y})
                y += 173
            self.matrice.append(liste)
            if a==1 :
                y = 88
                a = 0
            else:
                y = 0
                a = 1
            x += 150

    def generer_biome_voisins(self, i, j, hexa_rouge, hexa_lac, image):
        """Génère un biome en fonction des voisins. Si un voisin est une forêt, il y a 50% de chance de devenir une forêt."""
        voisins = None
        biome_choisi = random.choice([hexa_rouge, hexa_lac, image])  # Par défaut, un des biomes "naturels" au hasard
        return biome_choisi
        # Si l'un des voisins est une forêt, il y a 50% de chance que le biome de l'hexagone soit une forêt
 #       if hexa_foret in voisins and random.random() < 0.5:
  #          biome_choisi = hexa_foret
   #     if hexa_rouge in voisins and random.random() < 0.5:
    #        biome_choisi = hexa_rouge
     #   if hexa_lac in voisins and random.random() < 0.5:
      #      biome_choisi = hexa_lac

    def dessin(self, screen):
        """Dessine les hexagones en fonction de leurs biomes et leurs coordonnées."""
        for i in self.matrice: 
            for j in i :
                screen.blit(j["biome"], (j["x"] + self.clic_x, j["y"] + self.clic_y)) 
        pygame.display.flip()

    def deplacement (self,autre_hexa):
        """méthode qui servira à selectionner une unité dans un hexagone"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            hexa_choisi= 0

    def afficher_onglet(self, position, screen, hexa_rouge, hexa_lac, image):
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
                    self.dessin(screen  )
        # la boucle servant à faire fonctionner l'affichage de l'onglet
        while dialog_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    self.dessin(screen)
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    dialog_running = False
                    self.dessin(screen)
