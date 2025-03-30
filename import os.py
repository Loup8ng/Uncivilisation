import os
import time
import nbtlib
import numpy as np
import pyautogui
import json

# Fonction pour charger un schéma Litematica
def lire_litematic(fichier):
    data = nbtlib.load(fichier)
    regions = list(data["Regions"].keys())
    print("\n📌 Régions disponibles :")
    for i, region in enumerate(regions):
        print(f"  {i+1}. {region}")
    
    choix = int(input("Sélectionne une région (numéro) : ")) - 1
    region_name = regions[choix]
    region = data["Regions"][region_name]
    
    palette = {v["Name"]: k for k, v in region["Palette"].items()}  # Associer noms à ID
    block_states = region["BlockStates"]
    
    size = region["Size"]
    width, height, depth = size["x"], size["y"], size["z"]
    
    print(f"\n📐 Taille de la structure : {width}x{height}x{depth}")
    
    return region, palette, block_states, width, height, depth

# Fonction pour placer les blocs avec Baritone
def placer_blocs_baritone(x, y, z, block):
    cmd = f"#goto {x} {y} {z}"
    pyautogui.write(cmd)
    pyautogui.press("enter")
    time.sleep(2)
    cmd = f"#place {block}"
    pyautogui.write(cmd)
    pyautogui.press("enter")
    time.sleep(1)

# Fonction pour récupérer les blocs dans un coffre (Baritone)
def recuperer_blocs_baritone(block):
    cmd = f"#mine {block}"
    pyautogui.write(cmd)
    pyautogui.press("enter")
    time.sleep(5)  # Attendre que le bot récupère le bloc

# Menu principal
def menu():
    print("🔹 Bot Constructeur Minecraft 🔹\n")
    mode = input("Choisis le mode : (1) Baritone (2) Mineflayer : ")
    
    dossier = input("➡️  Dossier contenant les schémas : ")
    fichiers = [f for f in os.listdir(dossier) if f.endswith(".litematic")]
    
    if not fichiers:
        print("❌ Aucun fichier .litematic trouvé !")
        return
    
    print("\n📂 Fichiers disponibles :")
    for i, fichier in enumerate(fichiers):
        print(f"  {i+1}. {fichier}")
    
    choix = int(input("Sélectionne un fichier (numéro) : ")) - 1
    chemin_fichier = os.path.join(dossier, fichiers[choix])
    
    region, palette, block_states, width, height, depth = lire_litematic(chemin_fichier)
    
    if mode == "1":
        x_base = int(input("Position X de départ : "))
        y_base = int(input("Position Y de départ : "))
        z_base = int(input("Position Z de départ : "))
        
        for y in range(height):
            for x in range(width):
                for z in range(depth):
                    block_index = x + (y * width) + (z * width * height)
                    block_id = block_states[block_index]
                    block_name = palette.get(block_id, "minecraft:air")
                    
                    if block_name != "minecraft:air":
                        recuperer_blocs_baritone(block_name)
                        placer_blocs_baritone(x_base + x, y_base + y, z_base + z, block_name)
        
        print("✅ Structure construite !")
    elif mode == "2":
        print("🔹 Lancement du bot Mineflayer... (à compléter en JavaScript)")
    else:
        print("❌ Mode invalide !")

menu()
