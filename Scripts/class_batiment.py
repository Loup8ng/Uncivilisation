from pygame import *
import  csv

class Batiment():
    def __init__(self,nom,cout,temps_construction,capacite_stockage=None,prerequis=None):
        """Permet d'initialiser les batiments, en donnant :le nom du batiment, 
        son coût en ressources, son temps de construction, sa capacité de stockage 
        si il en as une, et des prérequis pour pouvoir le construire si il y en a."""
        self.nom= nom
        self.cout= cout
        self.temps_construction = temps_construction
        self.capacite_stockage = capacite_stockage
        self.prerequis = prerequis

    def afficher_infos(self):
        """Retourne une chaîne contenant toutes les infos du bâtiment."""
        infos = f"Bâtiment : {self.nom}\n"
        infos += f"Coût : {self.cout}\n"
        infos += f"Temps de construction : {self.temps_construction} tours\n"
        if self.capacite_stockage is not None:
            infos += f"Capacité de stockage : {self.capacite_stockage} unités\n"
        if self.prerequis:
            infos += f"Prérequis : {self.prerequis}\n"
        return infos


