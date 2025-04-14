from pygame import *
import cvs

class batiment():
    def __init__(self,nom,cout,temps_construction,capacite_stockage=None,prerequis=None):
        """Permet d'initialiser les batiments, en donnant :le nom du batiment, 
        son coût en ressources, son temps de construction, sa capacité de stockage 
        si il en as une, et des prérequis pour pouvoir le construire si il y en a."""
        self.nom= nom
        self.cout= cout
        self.temps_construction = temps_construction
        #self.capacite_stockage = capacite_stockage if capacite_stockage != 0
        #self.prerequis = prerequis if prerequis != []

        def afficher_infos(self):
            """Afficher l'ensemble des informations du batiments"""
             infos = "Bâtiment: " + (self.nom)\n
             "Coût: " + (self.cout)\n
             "Temps de construction: " + (self.temps_construction) + " tours"\n
        if self.capacite_stockage:
            infos += "Capacité de stockage: " + (self.capacite_stockage)\n
        if self.prerequis:
            infos += "Prérequis: " + (self.prerequis)\n
        return infos