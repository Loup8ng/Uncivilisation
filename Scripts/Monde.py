import pygame
import json
import random
import math
from Scripts.Variables_Globales import *

class Hexagone:
    def __init__(self, position:list[float, float], chemin_sprite:str, q:int = 0, r:int = 0):
        """Toutes les valeurs float doivent êtres exprimés en px."""
        self.radius = HEX_RADIUS
        self.position = position
        self.coordonnées_hex = [q, r]
        self.vertices = self.calcul_vertices()
        self.texture = self.charger_texture(chemin_sprite)
        self.biome = 0
        self.couleur = (0, 220, 255)
    
    def charger_texture(self, chemin_sprite:str) -> None:
        return pygame.transform.scale(pygame.image.load(chemin_sprite).convert_alpha(),(int(self.radius * 2), int(self.radius_vertical() * 2)))

    def calcul_vertices(self):
        """Renvoie une liste des sommets de l'hexagone depuis le centre"""
        cx, cy = self.coord_centre()
        points = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)
            x = cx + self.radius * math.cos(angle_rad)
            y = cy + self.radius * math.sin(angle_rad)
            points.append((x, y))
        return points


    def axial_round(self, q, r):
        q_round = round(q)
        r_round = round(r)
        s_round = round(-q - r)
        q_diff = abs(q_round - q)
        r_diff = abs(r_round - r)
        s_diff = abs(s_round - (-q - r))

        if q_diff > r_diff and q_diff > s_diff:
            q_round = -r_round - s_round
        elif r_diff > s_diff:
            r_round = -q_round - s_round
        return (q_round, r_round)

    def pixel_to_flat_hex(self, mouse_coord: tuple[float, float]) -> tuple[int, int]:
        """Convertit des coordonnées pixels en coordonnées hex axiales (q, r), 
        compatibles avec le système odd-q (colonnes impaires décalées vers le bas)."""
        mx = mouse_coord[0] - OFFSET_X
        my = mouse_coord[1] - OFFSET_Y

        # Étape 1 : coordonnées en colonne/ligne (offset)
        q = int((2/3 * mx) / self.radius)
        x_offset = q * self.radius * 3/2
        y_offset = my - (self.radius_vertical() * (q % 2))

        r_offset = int(y_offset / (self.radius_vertical() * 2))

        # Étape 2 : conversion offset -> axial
        r = r_offset - (q - (q % 2)) // 2

        return (q, r)


    def collision_point(self, coord_point:tuple[float, float]) -> bool:
        """Return True si l'hexagone touche le point"""
        return math.dist(coord_point, self.coord_centre()) < self.radius_vertical()

    def coord_centre(self) -> tuple[float, float]:
        """Renvoie les coordonnées (x, y) du centre de l'hexagone"""
        x, y = self.position
        return (x + self.radius / 2, y + self.radius_vertical())

    def radius_vertical(self) -> float:
        """Radius vertical de l'hexagone"""
        return self.radius * math.cos(math.radians(30))

    def dessin(self, screen) -> None:
        """Dessine l'image de l'hexagone centrée sur son centre logique + les coordonnées axiales."""
        centre_x, centre_y = self.coord_centre()
        rect = self.texture.get_rect()
        
        # Dessin de la texture centrée
        screen.blit(self.texture, (centre_x - rect.width // 2, centre_y - rect.height // 2))

        # Affichage d'un petit carré rouge pour visualiser l'origine
        screen.fill((255, 0, 0), (centre_x - 2, centre_y - 2, 4, 4))

        # Affichage des coordonnées q, r
        font = pygame.font.Font(None, 24)
        coord_text = font.render(f"{self.coordonnées_hex[0]}, {self.coordonnées_hex[1]}", True, (0, 0, 0))
        text_rect = coord_text.get_rect(center=(centre_x, centre_y))
        screen.blit(coord_text, text_rect)


class Carte:
    def __init__(self, longueur, largeur, background):
        """Initialise les longueur et largeur de la carte ainsi que la matrice pour la stocker."""
        self.longueur = longueur
        self.largeur = largeur
        self.background = self.charger_background(background)
        self.matrice = []
        self.clic_x = 0  
        self.clic_y = 0

    def charger_background(self, chemin_sprite:str) -> None:
        return pygame.transform.scale(pygame.image.load(chemin_sprite), (SCREEN_HEIGHT, SCREEN_WIDTH)).convert_alpha()

    def creer_un_hex(self, position:tuple[float, float], chemin_sprite:str) -> list[Hexagone]:
        """Créer un hexagone avec un radius et une position la texture est indiquée avec chemin_sprite"""
        return Hexagone(position, chemin_sprite)
    
    def generer_hexagones(self, chemin_sprite:str):
        """Génère une grille d'hexagones en coordonnées axiales q, r
        avec correspondance au système "odd-q" offset de RedBlobGames,
        tout en gardant pixel_to_flat_hex() cohérent."""
        self.matrice = []
        for q in range(self.largeur):
            colonne = []
            q_offset = q
            for r in range(self.longueur):
                # Conversion des coord axiales -> pixel
                x = OFFSET_X + HEX_RADIUS * 3/2 * q_offset
                y = OFFSET_Y + HEX_RADIUS * math.sqrt(3) * (r + 0.5 * (q_offset % 2))
                position = [x, y]

                # Conversion coordonnées de la grille (r,c) -> axiales selon odd-q
                axial_r = r - (q_offset - (q_offset % 2)) // 2
                axial_q = q_offset

                hexagone = Hexagone(position, chemin_sprite, axial_q, axial_r)
                colonne.append(hexagone)
            self.matrice.append(colonne)

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
        """Dessine tous les hexagones sur l'écran."""
        screen.blit(self.background, (0, 0))
        for ligne in self.matrice:
            for hexagone in ligne:
                hexagone.dessin(screen)

    def afficher_onglet(self, position, screen, test:Hexagone):
        dialog_surface = pygame.Surface((600, 400))
        dialog_surface.fill((50, 50, 50))
        police = pygame.font.Font(None, 50)
        print (test.position)
            #i, j = coord
            #hexa = self.matrice[i][j]
            #x, y = hexa["x"], hexa["y"]
            #if hexa["biome"] == image:
            #    biome_name = "Plaine"
            #elif hexa["biome"] == hexa_rouge:
            #    biome_name = "Montagne"
            #elif hexa["biome"] == hexa_foret:
            #    biome_name = "Forêt"
            #else:
            #    biome_name = "Lac"
            #texte_biome = police.render(f"Biome: {biome_name}", True, (255, 255, 255))
        texte_coord = police.render(f"Coord: {test.position}", True, (255, 255, 255))
            #dialog_surface.blit(texte_biome, (50, 100))
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
