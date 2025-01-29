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