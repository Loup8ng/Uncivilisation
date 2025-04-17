import pygame
import math
from Scripts.Variables_Globales import *

class Hexagone:
    def __init__(self, coordonnees_px:list[float, float], chemin_sprite:str, coord_q:int = 0, coord_r:int = 0):
        self.radius = HEX_RADIUS
        self.coordonnees_px = coordonnees_px
        self.coordonnées_hex = [coord_q, coord_r]
        self.sprite = self.charger_sprite(chemin_sprite)
    
    def charger_sprite(self, chemin_sprite:str) -> None:
        """Charge le sprite d'un hexagone de la bonne taille"""
        return pygame.transform.scale(pygame.image.load(chemin_sprite).convert_alpha(),(int(self.radius * 2), int(self.radius_vertical() * 2)))

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

    def dessin(self, screen, debugging:bool = False) -> None:
        """Affiche le sprite de l'hexagone au bon endroit, si debugging=True affiche des graphismes de déboguage."""
        centre_x, centre_y = self.coord_centre()
        rect_sprite = self.sprite.get_rect()

        screen.blit(self.sprite, (centre_x - rect_sprite.width // 2, centre_y - rect_sprite.height // 2))

        if debugging :
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
    
    def generer_hexagones(self, chemin_sprite:str) -> list[Hexagone]:
        """Génère une grille d'hexagones en coordonnées axiales."""
        self.grid = []
        for q in range(self.grid_height):
            column = []
            q_offset = q
            for r in range(self.grid_width):
                x = OFFSET_X + HEX_RADIUS * 3/2 * q_offset
                y = OFFSET_Y + HEX_RADIUS * math.sqrt(3) * (r + 0.5 * (q_offset % 2))
                coordonnees_px = [x, y]
                coord_r = r - (q_offset - (q_offset % 2)) // 2
                coord_q = q_offset
                hexagone = Hexagone(coordonnees_px, chemin_sprite, coord_q, coord_r)
                column.append(hexagone)
            self.grid.append(column)

    def dessin(self, screen):
        """Dessine la grille d'hexagones sur l'écran. Ainsi que l'image de fond"""
        screen.blit(self.background, (0, 0))
        for lines in self.grid:
            for hexagone in lines:
                hexagone.dessin(screen, True)
