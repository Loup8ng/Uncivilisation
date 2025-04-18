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
        """Charge le sprite d'un hexagone de la bonne taille (+1 pour éviter le gap entre les hexs)"""
        return pygame.transform.scale(pygame.image.load(chemin_sprite).convert_alpha(), (self.radius * 2 + 1, self.radius_vertical() * 2 + 1))

    def radius_vertical(self) -> float:
        """Rayon vertical de l'hexagone"""
        return self.radius * math.sqrt(3) / 2

    def coord_centre(self) -> tuple[float, float]:
        """Renvoie les coordonnées pixels du centre de l'hexagone"""
        q, r = self.coordonnees_axiales
        return self.hex_to_pixel(q, r)

    def hex_to_pixel(self, q:int, r:int) -> tuple[float, float]:
        """Converti les coordonées axiales en pixels"""
        coord_x = DEPART_X + self.radius * (3/2 * q)
        coord_y = DEPART_Y + self.radius * (math.sqrt(3)/2 * q + math.sqrt(3) * r)
        return (coord_x, coord_y)

    def pixel_to_hex(self, pos:tuple[float,float]) -> tuple[int, int]:
        """Converti les coordonées pixels en axiales en utilisant les calcules de sorcier trouvés sur internet"""
        coord_x = pos[0] - DEPART_X
        coord_y = pos[1] - DEPART_Y

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

    def dessin(self, screen, texture_pack, debugging:bool = False) -> None:
        """Affiche le sprite de l'hexagone en fonction de son biome, si debugging eh bah tu imagine bien ce que ça fait"""
        centre_x, centre_y = self.coord_centre()
        chemin_sprite = texture_pack.get(self.biome)
        sprite = self.charger_sprite(chemin_sprite)
        rect_sprite = sprite.get_rect()
        screen.blit(sprite, (centre_x - rect_sprite.width // 2, centre_y - rect_sprite.height // 2))
        if debugging:
            screen.fill(COLOR_RED, (centre_x - 2, centre_y - 2, 4, 4))
            font = pygame.font.Font(None, 24)
            coord_text = font.render(f"{self.coordonnees_axiales[0]}, {self.coordonnees_axiales[1]}", True, (0, 0, 0))
            text_rect = coord_text.get_rect(center=(centre_x, centre_y))
            screen.blit(coord_text, text_rect)

class Carte:
    def __init__(self, grid_width:int, grid_height:int):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.radius = HEX_RADIUS
        self.dictionnaire_hexagones = {}

    def creer_un_hex(self, coordonnees_pixels:tuple[float, float], chemin_sprite:str) -> Hexagone:
        """Créer un hexagone"""
        return Hexagone(coordonnees_pixels, chemin_sprite)

    def get_hex_at_position(self, coord_point: tuple[float, float]) -> tuple[int, int]:
        """Renvoie l'hexagone aux coordonnées x, y de coord_point"""
        if not self.dictionnaire_hexagones:
            return None
        hexagone = list(self.dictionnaire_hexagones.values())[0]
        q, r = hexagone.pixel_to_hex(coord_point)
        return self.dictionnaire_hexagones.get((q, r))

    def dessin(self, screen, texture_pack, debugging=False) -> None:
        """Dessine la grille d'hexagones sur l'écran, et peut être les graphismes débug aussi"""
        for hexagones in self.dictionnaire_hexagones.values():
            hexagones.dessin(screen, texture_pack, debugging)

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

    def generer(self, biomes:list[str]) -> None:
        """Génère une carte en tenant compte des biomes voisins, les pourcentages sont indiqués dans biome weight"""
        self.dictionnaire_hexagones = {}
        
        for q in range(self.grid_width):
            q_offset = q // 2
            for r in range(-q_offset, self.grid_height - q_offset):
                hex_temp = Hexagone([0, 0], "", q, r)
                x, y = hex_temp.hex_to_pixel(q, r)
                if x < -self.radius or y < -self.radius or x > SCREEN_WIDTH + self.radius or y > SCREEN_HEIGHT + self.radius:
                    continue
                voisin_coords = [(q+direction_q, r+direction_r) for direction_q, direction_r in [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]]
                existing_voisins = [self.dictionnaire_hexagones.get((coord_voisin_q, coord_voisin_r)) for coord_voisin_q, coord_voisin_r in voisin_coords if (coord_voisin_q, coord_voisin_r) in self.dictionnaire_hexagones]
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
                self.dictionnaire_hexagones[(q, r)] = Hexagone([x, y], biome_choisi, q, r)