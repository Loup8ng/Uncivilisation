import pygame
import json
import random
import math

pygame.init()

screen = pygame.display.set_mode((1400, 800))
screen.fill((255,255,255))
pygame.display.flip()

longueur= 9
largeur = 4

background = pygame.transform.scale(pygame.image.load("fond.png"), (1400, 800)).convert_alpha()
image = pygame.image.load("plaine.png").convert_alpha()
hexa_rouge = pygame.image.load("hexagone_rouge.png").convert_alpha()
hexa_foret = pygame.image.load("hexagone_foret.png").convert_alpha()
hexa_lac = pygame.image.load("hexagone_lac.png").convert_alpha()

class Unite(): 
    #classe qui nous servira à faire toutes les méthodes en rapport de nos unités 
    
    
    def __init__ (self): 

        #pas encore au stad de travailler avec d'autres joueurs
        self.hp=hp
        self.attq=attq


    def se_deplacer():
        """méthode qui servira à déplacer une unité déplacer d'un hexagone à un autre voisin"""
        pass
    # a faire

class Carte:
    def __init__(self, longueur=longueur, largeur= largeur):
        """
        Initialise les longueur et largeur de la carte ainsi que la matrice pour la stocker.
        """
        self.longueur = longueur
        self.largeur = largeur
        self.matrice = []



    def propager_biome(self, x, y, biome):
        """
        Propage un biome vers les hexagones voisins avec une probabilité de 50% normalement 
        """
    # a refaire entierement avec le "nouveau" code les hexagones sont pour l'instant générés aléatoirement


    def generation_hexagone (self): 
        """
         génères tous les hexagones de la carte en les stockant dans une matrice
        """
        a=1
        x=0
        y=0
        for i in range (self.longueur) :
            liste=[]
            for j in range(self.largeur):
                biome = random.choice([hexa_foret, hexa_rouge, hexa_lac, image])
                liste.append({"biome":biome, "x": x, "y":y})
                self.matrice.append(liste)
                y += 173
            if a==1 :
                y = 87.5
                a = 0
            else:
                y = 0
                a = 1
            x += 150
        

    def dessin(self):
        """
        Dessine les hexagones en fonction de leurs biomes et leurs coordonnées.
        """
        for i in self.matrice : 
            for j in i :
                screen.blit(j["biome"], (j["x"], j["y"]))  
        pygame.display.flip() 

    def afficher_onglet(self, position):
        """
        Affiche les informations d'un hexagone en fonction de la position de la souris quand un clique est détecté.
        """
        #probleme : - le click ne marche que en haut à gauche d'un hexagone (affiche un onglet noir si l'hexagone est selectionné en bas )
        #           - l'onglet ne se déplace pas (si on clique sur un hexagone, l'onglet s'affiche à un seul endroit donc les hexagones en dessous sont inaccessible le fait de clicker une deuxieme fois supprime l'onglet mais ça serait mieux depouvoir le déplacer)

        dialog_surface = pygame.Surface((600, 400))
        dialog_surface.fill((50, 50, 50)) 

        police = pygame.font.Font(None, 50)

        for i in self.matrice: 
            for j in i:
                x, y = j["x"], j["y"]
                if x <= position[0] <= x + 100 and y <= position[1] <= y + 87:

                    if j["biome"] == image:
                        couleur = "plaine"
                    elif j["biome"] == hexa_rouge:
                        couleur = "montagne"
                    elif j["biome"] == hexa_foret:
                        couleur = "forêt"
                    elif j["biome"] == hexa_lac:
                        couleur = "lac"

                    texte_couleur = police.render(f"Biome: {couleur}", True, (255, 255, 255))
                    texte_coord = police.render(f"Coordonnées: ({x}, {y})", True, (255, 255, 255))

                    dialog_surface.blit(texte_couleur, (50, 100))
                    dialog_surface.blit(texte_coord, (50, 200))

        screen.blit(dialog_surface, (625, 300))  
        pygame.display.flip()

        dialog_running = True

        # la boucle servant à faire fonctionner l'affichage de l'onglet
        while dialog_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    self.dessin()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    dialog_running = False
                    self.dessin()




fbir=Carte()
fbir.generation_hexagone()
screen.blit(background, (0,0))
fbir.dessin()
pygame.display.flip()
running= True

# la boucle servant à faire fonctionner LE TRUC
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                position = event.pos
                fbir.afficher_onglet(position)
        
    

pygame.quit()
