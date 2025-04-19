import json
from Scripts.Monde import *

def save_map(carte, nom_sauvegarde:str):
    """Sauvegarde la map sous forme de dictionnaire dans un JSON nommée 'nom_sauvegarde.json'"""
    donnees_sauvegardes = {
        "grid_width": carte.grid_width,
        "grid_height": carte.grid_height,
        "hexagones": []
    }
    for coords_hex, hexagones in carte.dictionnaire_hexagones.items():
        coord_q, coord_r = coords_hex
        donnees_hex = {
            "coord_q": coord_q,
            "coord_r": coord_r,
            "biome": hexagones.biome
        }
        donnees_sauvegardes["hexagones"].append(donnees_hex)
    with open(f"Saves/{nom_sauvegarde}.json", "w") as sauvegarde:
        json.dump(donnees_sauvegardes, sauvegarde, indent=2)

def load_map(nom_sauvegarde:str):
    """Charge la map 'nom_sauvegarde.json', sauf si elle existe pas (logique)"""
    try:
        with open(f"Saves/{nom_sauvegarde}.json", "r") as nom_sauvegarde:
            sauvegarde = json.load(nom_sauvegarde)
        carte = Carte(sauvegarde["grid_width"], sauvegarde["grid_height"])
        for donnees_chargees in sauvegarde["hexagones"]:
            coord_q = donnees_chargees["coord_q"]
            coord_r = donnees_chargees["coord_r"]
            biome = donnees_chargees["biome"]
            hex_calculateur = Hexagone([0, 0], "", coord_q, coord_r)
            coord_x, coord_y = hex_calculateur.hex_to_pixel(coord_q, coord_r)
            carte.dictionnaire_hexagones[(coord_q, coord_r)] = Hexagone([coord_x, coord_y], biome, coord_q, coord_r)
        carte.calculer_bords_map()
        return carte
    except FileNotFoundError:
        print(f"La sauvegarde '{nom_sauvegarde}.json' n'a pas été trouvé (cheh).")
        return None