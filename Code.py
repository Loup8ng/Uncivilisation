from pygame import *
import csv

class Personnages () : 
    def __init__ (self, hp= 100, attaque =20) : 
        self.heal= hp 
        self.atq= attaque

    def taper (self, autrePerso) : 
            autrePerso.hp -= self.atq

    def set_hp (self, hp= hp) : 
        self.hp = hp 
    def get_attq (self) :
        return self.attq
    def déplacements (self,case) : 
        #mettre tout ce qu'il faut pour faire déplacer le personnage

class carte () :
    def __init__ (self) :
        return 0
