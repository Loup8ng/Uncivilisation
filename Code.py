import pygame
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
        return 0

class carte () :
    def __init__ (self) :
        return 0
class Interaction_Hexagone ():
    def __init__ (self) : 
        self.test

pygame.init()

Continuer = True
while continuer : 
    for event.type == QUIT:
        continuer = False
    pygame.display.update()
pygame.quit()
