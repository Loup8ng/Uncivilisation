import pygame
import math
import random
from Scripts.Variables_Globales import *

class Hexagone:
    def __init__(self, coordonnees_pixels:list[float, float], biome:str ="", coord_q:int = 0, coord_r:int = 0):
        self.radius = HEX_RADIUS
        self.coordonnees_pixels = coordonnees_pixels
        self.coordonnees_axiales = [coord_q, coord_r]
        self.biome = biome

    def charger_sprite(self, chemin_sprite:str) -> None:
        """Charge le sprite d'un hexagone de la bonne taille (+2 pour éviter le gap entre les hexs)"""
        return pygame.transform.scale(pygame.image.load(chemin_sprite).convert_alpha(), (self.radius * 2 + 2, self.radius_vertical() * 2 + 2))

    def radius_vertical(self) -> float:
        """Rayon vertical de l'hexagone"""
        return self.radius * math.sqrt(3) / 2

    def coord_centre(self) -> tuple[float, float]:
        """Renvoie les coordonnées pixels du centre de l'hexagone"""
        coord_q, coord_r = self.coordonnees_axiales
        return self.hex_to_pixel(coord_q, coord_r)

    def hex_to_pixel(self, coord_q:int, coord_r:int) -> tuple[float, float]:
        """Converti les coordonées axiales en pixels"""
        coord_x = self.radius * (3/2 * coord_q)
        coord_y = self.radius * (math.sqrt(3)/2 * coord_q + math.sqrt(3) * coord_r)
        return (coord_x, coord_y)

    def pixel_to_hex(self, pos:tuple[float,float]) -> tuple[int, int]:
        """Converti les coordonées pixels en axiales en utilisant les calcules de sorcier trouvés sur internet"""
        coord_x = pos[0]
        coord_y = pos[1]

        size = self.radius
        coord_q = (coord_x * 2/3) / size
        coord_r = (-coord_x/3 + math.sqrt(3)/3 * coord_y) / size
        
        coord_x_cube = coord_q
        coord_z_cube = coord_r
        coord_y_cube = -coord_x_cube - coord_z_cube

        coord_x_cube_round = round(coord_x_cube)
        coord_y_cube_round = round(coord_y_cube)
        coord_z_cube_round = round(coord_z_cube)

        coord_x_diff = abs(coord_x_cube_round - coord_x_cube)
        coord_y_diff = abs(coord_y_cube_round - coord_y_cube)
        coord_z_diff = abs(coord_z_cube_round - coord_z_cube)

        if coord_x_diff > coord_y_diff and coord_x_diff > coord_z_diff:
            coord_x_cube_round = -coord_y_cube_round - coord_z_cube_round
        elif coord_y_diff > coord_z_diff:
            coord_y_cube_round = -coord_x_cube_round - coord_z_cube_round
        else:
            coord_z_cube_round = -coord_x_cube_round - coord_y_cube_round
        return (coord_x_cube_round, coord_z_cube_round)

class Carte:
    def __init__(self, grid_width:int, grid_height:int):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.radius = HEX_RADIUS
        self.dictionnaire_hexagones = {}
        self.coord_camera_x = 0
        self.coord_camera_y = 0
        self.camera_min_x = 0
        self.camera_min_y = 0
        self.camera_max_x = 0
        self.camera_max_y = 0

    def creer_un_hex(self, coordonnees_pixels:tuple[float, float], chemin_sprite:str) -> Hexagone:
        """Créer un hexagone"""
        return Hexagone(coordonnees_pixels, chemin_sprite)

    def get_hex_at_position(self, coord_point: tuple[float, float]) -> Hexagone:
        """Renvoie l'hexagone aux coordonnées x, y de coord_point en tenant compte du déplacement de la caméra"""
        if self.dictionnaire_hexagones:
            coord_ajuste_x = coord_point[0] - self.coord_camera_x
            coord_ajuste_y = coord_point[1] - self.coord_camera_y
            hex_calculateur = Hexagone([0, 0])
            coord_q, coord_r = hex_calculateur.pixel_to_hex((coord_ajuste_x, coord_ajuste_y))
            return self.dictionnaire_hexagones.get((coord_q, coord_r))
        else :
            return None

    def calculer_bords_map(self):
        """Calcule les coordonnées des bords de la map"""
        self.camera_min_x = float('inf')
        self.camera_min_y = float('inf')
        self.camera_max_x = float('-inf')
        self.camera_max_y = float('-inf')
        for hexagone in self.dictionnaire_hexagones.values():
            coord_centre_x, coord_centre_y = hexagone.coord_centre()
            self.camera_min_x = min(self.camera_min_x, coord_centre_x - hexagone.radius/2.5)
            self.camera_min_y = min(self.camera_min_y, coord_centre_y )
            self.camera_max_x = max(self.camera_max_x, coord_centre_x + hexagone.radius/2.5)
            self.camera_max_y = max(self.camera_max_y, coord_centre_y )

    def dessin(self, screen, texture_pack, debugging=False) -> None:
        """Dessine uniquement les hexagones visibles à l'écran avec une marge quand même (buffer)"""
        buffer = HEX_RADIUS
        for coords, hexagone in self.dictionnaire_hexagones.items():
            coord_centre_x, coord_centre_y = hexagone.coord_centre()
            coord_screen_x = coord_centre_x + self.coord_camera_x
            coord_screen_y = coord_centre_y + self.coord_camera_y
            if (-buffer <= coord_screen_x <= SCREEN_WIDTH + buffer and 
                -buffer <= coord_screen_y <= SCREEN_HEIGHT + buffer):
                chemin_sprite = texture_pack.get(hexagone.biome)
                sprite = hexagone.charger_sprite(chemin_sprite)
                rect_sprite = sprite.get_rect()
                screen.blit(sprite, (coord_screen_x - rect_sprite.width // 2, coord_screen_y - rect_sprite.height // 2))
                if debugging:
                    screen.fill(COLOR_RED, (coord_screen_x - 2, coord_screen_y - 2, 4, 4))
                    font = pygame.font.Font(None, 24)
                    coord_text = font.render(f"{hexagone.coordonnees_axiales[0]}, {hexagone.coordonnees_axiales[1]}", True, COLOR_BLACK)
                    text_rect = coord_text.get_rect(center=(coord_screen_x, coord_screen_y))
                    screen.blit(coord_text, text_rect)

    def get_voisins(self, coord_q:int, coord_r:int) -> list[Hexagone]:
        """Renvois une liste de voisin de l'hexagone de coordonées (q, r)"""
        directions_voisins = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
        liste_voisins = []
        for direction_q, direction_r in directions_voisins:
            voisin_q = coord_q + direction_q
            voisin_r = coord_r + direction_r
            voisin_coord = (voisin_q, voisin_r)
            if voisin_coord in self.dictionnaire_hexagones:
                liste_voisins.append(self.dictionnaire_hexagones[voisin_coord])
        return liste_voisins

    def swip(self, direction_x:float, direction_y:float) -> None:
        """Bouge la caméra avec direction_x et direction_y, bloque si on touche les limites de la map"""
        deplacement_camera_x = self.coord_camera_x + direction_x
        deplacement_camera_y = self.coord_camera_y + direction_y
        if self.camera_min_x == float('inf') or self.camera_max_x == float('-inf'):
            self.calculer_bords_map()
        left_limit = -self.camera_min_x
        right_limit = SCREEN_WIDTH - self.camera_max_x
        top_limit = -self.camera_min_y
        bottom_limit = SCREEN_HEIGHT - self.camera_max_y
        self.coord_camera_x = max(min(deplacement_camera_x, left_limit), right_limit)
        self.coord_camera_y = max(min(deplacement_camera_y, top_limit), bottom_limit)

    def generer(self, biomes:list[str]) -> None:
        """Génère une carte en tenant compte des biomes voisins, les pourcentages sont indiqués dans biome weight"""
        self.dictionnaire_hexagones = {}
        for coord_q in range(self.grid_width):
            q_offset = coord_q // 2
            for coord_r in range(-q_offset, self.grid_height - q_offset):
                hex_calculateur = Hexagone([0, 0], "", coord_q, coord_r)
                coord_x, coord_y = hex_calculateur.hex_to_pixel(coord_q, coord_r)
                existing_voisins = self.get_voisins(coord_q, coord_r)
                biome_scores = {}
                if existing_voisins:
                    for voisin in existing_voisins:
                        if voisin:
                            biome = voisin.biome
                            influence = biome_weights.get(biome, {})
                            for biome, poids in influence.items():
                                biome_scores[biome] = biome_scores.get(biome, 0) + poids
                    biomes_possibles = list(biome_scores.keys())
                    poids_biomes = list(biome_scores.values())
                    biome_choisi = random.choices(biomes_possibles, weights=poids_biomes, k=1)[0] if biomes_possibles else random.choice(biomes)
                else:
                    biome_choisi = random.choice(biomes)
                self.dictionnaire_hexagones[(coord_q, coord_r)] = Hexagone([coord_x, coord_y], biome_choisi, coord_q, coord_r)
        self.calculer_bords_map()