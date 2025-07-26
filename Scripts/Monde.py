import pygame
import math
import random
from Scripts.Variables_Globales import *

class Hexagone:
    def __init__(self, coordonnees_pixels:list[float, float], biome:str = "", coord_q:int = 0, coord_r:int = 0,ressources=0):
        self.radius = HEX_RADIUS
        self.coordonnees_pixels = coordonnees_pixels
        self.coordonnees_axiales = [coord_q, coord_r]
        self.biome = biome
        self.ressources_biomes = ressources

    def charger_sprite(self, chemin_sprite:str) -> None:
        """Charge le sprite d'un hexagone de la bonne taille (+2 pixels pour éviter le gap entre les hexs)"""
        return pygame.transform.scale(pygame.image.load(chemin_sprite).convert_alpha(), (self.radius * 2 + 2, self.radius_vertical() * 2 + 2))

    def radius_vertical(self) -> float:
        """Rayon vertical de l'hexagone"""
        return self.radius * math.sqrt(3) / 2

    def coord_centre(self) -> tuple[float, float]:
        """Renvoi les coordonnées pixels du centre de l'hexagone"""
        coord_q, coord_r = self.coordonnees_axiales
        return self.hex_to_pixel(coord_q, coord_r)

    def hex_to_pixel(self, coord_q:int, coord_r:int) -> tuple[float, float]:
        """Converti les coordonées axiales en pixels"""
        coord_x = self.radius * (3/2 * coord_q)
        coord_y = self.radius * (math.sqrt(3)/2 * coord_q + math.sqrt(3) * coord_r)
        return (coord_x, coord_y)

    def pixel_to_hex(self, pos:tuple[float,float]) -> tuple[int, int]:
        """Converti les coordonées pixels en axiales en utilisant les calculs de sorcier trouvés sur internet"""
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
        self.valeur_zoom = 1.0
        self.font = pygame.font.Font(None, 24)

    def creer_un_hex(self, coordonnees_pixels:tuple[float, float], chemin_sprite:str) -> Hexagone:
        """Créer un hexagone, note: parfois pour faire des calculs il est nécessaire d'avoir un hexagone temporaire pour. (c'est l'hex_calculateur)"""
        return Hexagone(coordonnees_pixels, chemin_sprite)

    def get_hex_at_position(self, coord_point:tuple[float, float]) -> Hexagone:
        """Renvoie l'hexagone aux coordonnées x, y en tenant compte du zoom et de la position de caméra"""
        if  self.dictionnaire_hexagones:
            coord_ajuste_x = (coord_point[0] - self.coord_camera_x) / self.valeur_zoom
            coord_ajuste_y = (coord_point[1] - self.coord_camera_y) / self.valeur_zoom
            hex_calculateur = Hexagone([0, 0])
            coord_q, coord_r = hex_calculateur.pixel_to_hex((coord_ajuste_x, coord_ajuste_y))
            return self.dictionnaire_hexagones.get((coord_q, coord_r))
        else:
            return None

    def calculer_bords_map(self) -> None:
        """Calcule les coordonnées des bords de la map"""
        self.camera_min_x = float('inf')
        self.camera_min_y = float('inf')
        self.camera_max_x = float('-inf')
        self.camera_max_y = float('-inf')
        for hexagone in self.dictionnaire_hexagones.values():
            coord_centre_x, coord_centre_y = hexagone.coord_centre()
            nouveau_radius = hexagone.radius * self.valeur_zoom
            nouveau_radius_vertical = hexagone.radius_vertical() * self.valeur_zoom
            self.camera_min_x = min(self.camera_min_x, coord_centre_x * self.valeur_zoom)
            self.camera_min_y = min(self.camera_min_y, coord_centre_y * self.valeur_zoom)
            self.camera_max_x = max(self.camera_max_x, coord_centre_x * self.valeur_zoom)
            self.camera_max_y = max(self.camera_max_y, coord_centre_y * self.valeur_zoom)

    def corriger_pos_camera(self) -> None:
        """Corrige la position de la caméra pour être sur de ne pas dépasser dans le vide"""
        largeur_map = self.camera_max_x - self.camera_min_x
        hauteur_map = self.camera_max_y - self.camera_min_y
        if largeur_map <= SCREEN_WIDTH:
            self.coord_camera_x = (SCREEN_WIDTH - largeur_map) / 2 - self.camera_min_x
        else:
            self.coord_camera_x = max(min(self.coord_camera_x, -self.camera_min_x), SCREEN_WIDTH - self.camera_max_x)
        if hauteur_map <= SCREEN_HEIGHT:
            self.coord_camera_y = (SCREEN_HEIGHT - hauteur_map) / 2 - self.camera_min_y
        else:
            self.coord_camera_y = max(min(self.coord_camera_y, -self.camera_min_y), SCREEN_HEIGHT - self.camera_max_y)

    def zoomer_vers(self, facteur_zoom:float, coord_point_x:float, coord_point_y:float) -> None:
        """Zoom la caméra vers un point de coordonnées coord_point_x et coord_point_y"""
        if facteur_zoom < 1.0:
            if self.camera_min_x == float('inf') or self.camera_max_x == float('-inf'):
                self.calculer_bords_map()
            largeur_map = self.camera_max_x - self.camera_min_x
            hauteur_map = self.camera_max_y - self.camera_min_y
            nouvelle_valeur_zoom = self.valeur_zoom * facteur_zoom
            nouvelle_largeur_map = largeur_map / self.valeur_zoom * nouvelle_valeur_zoom
            nouvelle_hauteur_map = hauteur_map / self.valeur_zoom * nouvelle_valeur_zoom
            if nouvelle_largeur_map < SCREEN_WIDTH or nouvelle_hauteur_map < SCREEN_HEIGHT:
                return None
        nouvelle_valeur_zoom_corrige = max(MIN_ZOOM, min(self.valeur_zoom * facteur_zoom, MAX_ZOOM))
        zoom_ratio = nouvelle_valeur_zoom_corrige / self.valeur_zoom
        self.coord_camera_x = coord_point_x - (coord_point_x - self.coord_camera_x) * zoom_ratio
        self.coord_camera_y = coord_point_y - (coord_point_y - self.coord_camera_y) * zoom_ratio
        self.valeur_zoom = nouvelle_valeur_zoom_corrige
        self.calculer_bords_map()
        self.corriger_pos_camera()

    def swip(self, direction_x:float, direction_y:float) -> None:
        """Bouge la caméra en prenant en compte les limites de la map"""
        self.coord_camera_x += direction_x
        self.coord_camera_y += direction_y
        if self.camera_min_x == float('inf') or self.camera_max_x == float('-inf'):
            self.calculer_bords_map()
        self.corriger_pos_camera()

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

    def dessin(self, screen, texture_pack, is_coordonnees_visibles=False) -> None:
        """Dessine seulement les hexagones visibles à l'écran avec une marge"""
        marge = HEX_RADIUS * self.valeur_zoom
        for coords, hexagone in self.dictionnaire_hexagones.items():
            coord_centre_x, coord_centre_y = hexagone.coord_centre()
            coord_screen_x = coord_centre_x * self.valeur_zoom + self.coord_camera_x
            coord_screen_y = coord_centre_y * self.valeur_zoom + self.coord_camera_y
            if (-marge <= coord_screen_x <= SCREEN_WIDTH + marge and -marge <= coord_screen_y <= SCREEN_HEIGHT + marge):
                chemin_sprite = texture_pack.get(hexagone.biome)
                hex_calculateur = Hexagone([0, 0], "")
                hex_calculateur.radius = hexagone.radius * self.valeur_zoom
                sprite = hex_calculateur.charger_sprite(chemin_sprite)
                rect_sprite = sprite.get_rect()
                screen.blit(sprite, (coord_screen_x - rect_sprite.width // 2, coord_screen_y - rect_sprite.height // 2))
                if is_coordonnees_visibles:
                    screen.fill(COLOR_RED, (coord_screen_x - 2, coord_screen_y - 2, 4, 4))
                    coord_text = self.font.render(f"{hexagone.coordonnees_axiales[0]}, {hexagone.coordonnees_axiales[1]}", True, (0, 0, 0))
                    text_rect = coord_text.get_rect(center=(coord_screen_x, coord_screen_y))
                    screen.blit(coord_text, text_rect)

    def attribution_ressources(self):
        return random.randint(1,100000)
        

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
                self.dictionnaire_hexagones[(coord_q, coord_r)] = Hexagone([coord_x, coord_y], biome_choisi, coord_q, coord_r,self.attribution_ressources())
        self.calculer_bords_map()
