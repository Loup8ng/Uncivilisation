SCREEN_WIDTH = 1170
SCREEN_HEIGHT = 940
FRAMERATE = 75

HEX_RADIUS = 50

DEPART_X = 0
DEPART_Y = 0
MAP_SIZE_X = 17
MAP_SIZE_Y = 12

COLOR_RED = (255, 0, 0)

biomes_disponibles = ["montagne", "plaine", "foret", "sable", "lac"]
biome_weights = {
    "plaine":     {"plaine": 35, "foret": 50, "sable": 15},
    "foret":      {"plaine": 20,"foret": 20, "montagne": 60},
    "montagne":   {"plaine": 30, "foret": 30, "montagne": 40 },
    "sable":      {"plaine": 20, "sable": 30, "lac": 50},
    "lac":        {"plaine": 10, "sable": 40, "lac": 50}}