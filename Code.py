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

class Persnnages(): 
    def __init__ (self): 
        pass

class Hexagone:
    def __init__(self, x, y, biome=None):
        """
        Initialise un hexagone avec ses coordonnées et son biome.
         coordonnée X Y
        et type de biome.  #du coup a changer 
        """
        self.x = x
        self.y = y
        self.biome = biome
        self.caracteristiques=None


    def definir_biome(self, biome):
        """
         biome de l'hexagone et ses caractéristiques.
        """
        self.biome=biome
        if biome == "forêt":
            self.caracteristique = "bois disponible"
            consommable_foret =20       # faudra voir comment on peut utiliser les consommables
        elif biome == "montagne":
            self.caracteristique = "riche en minerais"
        elif biome == "lac":
            self.caracteristique = "lac infranchissable"
        elif biome == "plaine":
            self.caracteristique = "terrain facile à traverser"


    def recolter_des_ressources(self,biome):   # FAUDRA IMPLEMENTER CETTE FONCTION DANS LA BOUCLE DE JEU par exemple quand une touche est pressée ca récolte des ressources selon son biome aussi 
        """récolter des ressources selon le biome; il y aura aussi """
        if self.biome=="forêt" and consommable_foret>0 :
             #faut aussi mettre apres la selection de l'hexagone a été faite chaque consommbale est different , pas tous les stocker dans la meme variable 
            b=consommable_foret
            consommable_foret=0
    
    def creer_un_batiment(self):        #pareil que implementer , si c'est u plaine il est possible de créer un "chateau" ou un une ferme etc a voir les autres batiments
        """creer un bat"""
        if self.biome=="plaine":
            self.biome="chateau"    #du coup ce que je veux faire c'est carrément que le biome soit juste remplacé par les propriété du chateau/ d'un point de vue graphique il faudra que ce soit le mm biome juste avec une maison dessus 
    


class Carte:
    def __init__(self, longueur=longueur, largeur= largeur):
        self.longueur = longueur
        self.largeur = largeur
        self.matrice = []



    def propager_biome(self, x, y, biome):
        """
        propage un biome vers les hexagones voisins avec une probabilité de 50% normalement 
        """
# j'ai tout supprimé ca marchait pas et ca faisait tout planter 😭😭😭😭😭 ; mais en vrai sans la méthode ça rend pas si mal je trouve 


    def generation_hexagone (self): 
        """
         génères tous les hexagones de la carte toute en les stockan dans une matrice
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
        Dessine les hexagones en fonction de leur biome.
        """
        for i in self.matrice : 
            for j in i :
                screen.blit(j["biome"], (j["x"], j["y"]))  
        pygame.display.flip() 

    def afficher_onglet(self, position):
        """
        Affiche les informations d'un hexagone en fonction de la position cliquée.
        """
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


while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                position = event.pos
                fbir.afficher_onglet(position)
        
    

pygame.quit()
