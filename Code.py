import pygame
import json
import random
import math

pygame.init()

screen = pygame.display.set_mode((1400, 800))
screen.fill((255,255,255))
pygame.display.flip()

longueur= 20
largeur = 12

background = pygame.transform.scale(pygame.image.load("fond.png"), (1400, 800)).convert_alpha()
image = pygame.image.load("plaine.png").convert_alpha()
hexa_rouge = pygame.image.load("hexagone_rouge.png").convert_alpha()
hexa_foret = pygame.image.load("hexagone_foret.png").convert_alpha()
hexa_lac = pygame.image.load("hexagone_lac.png").convert_alpha()


class Unite:
    def __init__(self, pv, attq, deplacement):
        """
        classe de base pour une unité.
        """
        self.pv = pv
        self.attq = attq
        self.deplacement = deplacement
    
    def est_vivant(self):
        return self.pv > 0

    def attaquer(self, autre_unite):
        autre_unite.subir_degats(self.attq)
    
    def subir_degats(self, degats):
        self.pv -= degats


class Epeiste(Unite):
    def __init__(self):
        """
        crée une unité de type epeiste avec des caractéristiques spécifiques.
        """
        super().__init__(pv=200, attq=50, deplacement=1)  # Épéiste a 200 PV, 50 d'attaque et 1 point de déplacement

class Lancier(Unite):
    def __init__(self):
        """
        crée une unité de type lancier avec des caractéristiques spécifiques.
        """
        super().__init__(pv=200, attq=75, deplacement=3)  # Lancier a 200 PV, 75 d'attaque et 3 points de déplacement

class Carte:
    def __init__(self, longueur=longueur, largeur= largeur):
        """
        Initialise les longueur et largeur de la carte ainsi que la matrice pour la stocker.
        """
        self.longueur = longueur
        self.largeur = largeur
        self.matrice = []
        self.clic_x = 0  
        self.clic_y = 0  

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


    def generation_hexagone (self): 
        """
         génère tous les hexagones de la carte en les stockant dans une matrice
        """
        a=1
        x=0
        y=0
        for i in range (self.longueur) :
            liste=[]
            for j in range(self.largeur):
                biome = self.generer_biome_voisins(i,j)
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

    def generer_biome_voisins(self, i, j):
        """
        Génère un biome en fonction des voisins. Si un voisin est une forêt, il y a 50% de chance de devenir une forêt.
        """
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



    def dessin(self):
        """
        Dessine les hexagones en fonction de leurs biomes et leurs coordonnées.
        """
        for i in self.matrice: 
            for j in i :
                screen.blit(j["biome"], (j["x"] + self.clic_x, j["y"] + self.clic_y)) 
        pygame.display.flip()
       



    def deplacement (self,autre_hexa):
        """méthode qui servira à selectionner une unité dans un hexagone"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            hexa_choisi= 0

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
swip = False  
start_x, start_y = 0, 0 

# la boucle servant à faire fonctionner LE TRUC
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                position = event.pos
                fbir.afficher_onglet(position)
            elif event.button == 3:  # Clic droit pour commencer à déplacer la carte
                swip = True
                pos_depart_x, pos_depart_y = event.pos  # garde la position initiale du clic droit
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  
                swip = False
        if event.type == pygame.MOUSEMOTION:
            if swip:  # deplacer la carte si le clic droit est enfonce
                dx, dy = event.pos[0] - pos_depart_x, event.pos[1] - pos_depart_y
                fbir.clic_x += dx
                fbir.clic_y += dy
                pos_depart_x, pos_depart_y = event.pos
        
#Redessiner la carte avec le déplacement
    screen.fill((255, 255, 255))  
    screen.blit(background, (0, 0))  
    fbir.dessin() 
    pygame.display.flip()   

pygame.quit()



#objectif de la rentrée/ ajouter de la generation logique  aleatoire / deplacer les unités sur la carte/ deplacement de la carte 