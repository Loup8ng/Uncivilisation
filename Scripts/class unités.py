from pygame import *
import csv

class épéiste():
    def __init__ (self, hp= 150, attack=25) : 
        self.heal= hp 
        self.atq= attack

    def taper (self, autrePerso) : 
            autrePerso.hp -= self.atq

    def set_hp (self, hp= hp) :
        self.hp = hp
    def get_attq (self) :
        return self.attq

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
