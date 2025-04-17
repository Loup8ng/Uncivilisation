import pygame
import math
import random
from Scripts.Variables_Globales import *

biome_weights = {
    "plaine":     {"plaine": 40, "foret": 50, "sable": 10},
    "foret":      {"foret": 30, "plaine": 10, "montagne": 60},
    "montagne":   {"montagne": 40, "foret": 30, "plaine": 30},
    "sable":      {"sable": 30, "plaine": 15, "lac": 55},
    "lac":        {"lac": 70, "sable": 25, "plaine": 5}
}

class Hexagone:
    def __init__(self, coordonnees_px:list[float, float], biome:str, coord_q:int = 0, coord_r:int = 0):
        self.radius = HEX_RADIUS
        self.coordonnees_px = coordonnees_px
        self.coordonnées_hex = [coord_q, coord_r]
        self.biome = biome
    
    def charger_sprite(self, chemin_sprite:str) -> None:
        """Charge le sprite d'un hexagone de la bonne taille"""
        return pygame.transform.scale(pygame.image.load(chemin_sprite).convert_alpha(),(int(self.radius * 2 + 1), int(self.radius_vertical() * 2 + 1)))

    def pixel_to_hex(self, mouse_coord:tuple[float, float]) -> tuple[int, int]:
        """Convertie un point de coordonées x,y en coordonées axiales"""
        mouse_x = mouse_coord[0] - OFFSET_X
        mouse_y = mouse_coord[1] - OFFSET_Y
        coord_q = int((2/3 * mouse_x) / self.radius)
        x_offset = coord_q * self.radius * 3/2
        y_offset = mouse_y - (self.radius_vertical() * (coord_q % 2))
        r_offset = int(y_offset / (self.radius_vertical() * 2))
        coord_r = r_offset - (coord_q - (coord_q % 2)) // 2
        return (coord_q, coord_r)

    def coord_centre(self) -> tuple[float, float]:
        """Renvoie les coordonnées (x, y) du centre de l'hexagone"""
        x, y = self.coordonnees_px
        return (x + self.radius / 2, y + self.radius_vertical())

    def radius_vertical(self) -> float:
        """Rayon vertical de l'hexagone"""
        return self.radius * math.cos(math.radians(30))

    def dessin(self, screen, texture_pack, debugging:bool = False) -> None:
        """Affiche le sprite de l'hexagone au bon endroit en fonction de son biome, si debugging=True affiche des graphismes de déboguage."""
        centre_x, centre_y = self.coord_centre()
        chemin_sprite = texture_pack.get(self.biome)
        sprite = self.charger_sprite(chemin_sprite)
        rect_sprite = sprite.get_rect()
        screen.blit(sprite, (centre_x - rect_sprite.width // 2, centre_y - rect_sprite.height // 2))
        if debugging:
            screen.fill(COLOR_RED, (centre_x - 2, centre_y - 2, 4, 4))
            font = pygame.font.Font(None, 24)
            coord_text = font.render(f"{self.coordonnées_hex[0]}, {self.coordonnées_hex[1]}", True, (0, 0, 0))
            text_rect = coord_text.get_rect(center=(centre_x, centre_y))
            screen.blit(coord_text, text_rect)

class Carte:
    def __init__(self, grid_width:int, grid_height:int, chemin_background:str):
        """Initialise les longueur et largeur de la carte ainsi que la matrice pour la stocker."""
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.background = self.charger_background(chemin_background)
        self.grid = []

    def charger_background(self, chemin_sprite:str) -> None:
        return pygame.transform.scale(pygame.image.load(chemin_sprite), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()

    def creer_un_hex(self, coordonnees_px:tuple[float, float], chemin_sprite:str) -> Hexagone:
        """Créer un hexagone avec un radius et une position la texture est indiquée avec chemin_sprite"""
        return Hexagone(coordonnees_px, chemin_sprite)

    def get_voisins(self, coord_q, coord_r) -> list[Hexagone]:
        """Renvois une liste de voisin de l'hexagone de coordonées (q, r)"""
        directions = [(+1,  0), (0, +1), (-1, +1),
                      (-1,  0), (0, -1), (+1, -1)]
        voisins = []
        for direction_q, direction_r in directions:
            nq = coord_q + direction_q
            nr = coord_r + direction_r
            if 0 <= nq < self.grid_width and 0 <= nr < self.grid_height:
                try:
                    voisins.append(self.grid[nq][nr])
                except IndexError:
                    continue
        return voisins

    def generer(self, biomes: list[str]) -> None:
        """Génère une carte en tenant compte des biomes voisins, les pourcentages sont indiqués dans biome_weight"""
        self.grid = []
        for q in range(self.grid_width):
            colonne = []
            for r in range(self.grid_height):
                x = OFFSET_X + HEX_RADIUS * 3/2 * q
                y = OFFSET_Y + HEX_RADIUS * math.sqrt(3) * (r + 0.5 * (q % 2))
                coord_px = [x, y]
                coord_q = q
                coord_r = r - (q - (q % 2)) // 2

                voisins = []
                if q > 0:
                    voisins += self.get_voisins(q - 1, r)
                if r > 0:
                    voisins += self.get_voisins(q, r - 1)

                biome_scores = {}
                if voisins:
                    for voisin in voisins:
                        if voisin:
                            biome = voisin.biome
                            influence = biome_weights.get(biome, {})
                            for b, poids in influence.items():
                                biome_scores[b] = biome_scores.get(b, 0) + poids
                    total = sum(biome_scores.values())
                    biomes_possibles = list(biome_scores.keys())
                    poids_biomes = list(biome_scores.values())
                    choix = random.choices(biomes_possibles, weights=poids_biomes, k=1)[0]
                else:
                    choix = random.choice(biomes)

                colonne.append(Hexagone(coord_px, choix, coord_q, coord_r))
            self.grid.append(colonne)

    def dessin(self, screen, texture_pack):
        """Dessine la grille d'hexagones sur l'écran. Ainsi que l'image de fond"""
        screen.blit(self.background, (0, 0))
        for ligne in self.grid:
            for hexagone in ligne:
                hexagone.dessin(screen, texture_pack)
