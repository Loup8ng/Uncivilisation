import json

background = "Assets/fond.png"

class TexturePack:
    def __init__(self, chemin_pack_json:str):
        self.textures = self.charger_pack(chemin_pack_json)

    def charger_pack(self, chemin_pack_json:str) -> dict:
        with open(chemin_pack_json, 'r', encoding='utf-8') as texture_pack_json:
            texture_pack_dict = json.load(texture_pack_json)
        return texture_pack_dict

    def get(self, nom_texture:str) -> str:
        """Retourne le chemin d'une texture à partir de son nom"""
        return self.textures.get(nom_texture, None)
