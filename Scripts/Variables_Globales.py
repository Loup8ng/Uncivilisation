SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
FRAMERATE = 75

HEX_RADIUS = 100

MIN_ZOOM = 0.2
MAX_ZOOM = 4.5
ZOOM_SPEED = 0.1

MAP_SIZE_X = 50
MAP_SIZE_Y = 50

COLOR_RED = (255, 0, 0)
COLOR_BLACK = (0, 0, 0)

biomes_disponibles = ["montagne", "plaine", "foret", "sable", "lac"]
biome_weights = {
    "plaine":     {"montagne": 0 ,"plaine": 35, "foret": 50, "sable": 15, "lac": 0},
    "foret":      {"montagne": 60,"plaine": 20, "foret": 20, "sable": 0 , "lac": 0},
    "montagne":   {"montagne": 40,"plaine": 30, "foret": 30, "sable": 0 , "lac": 0},
    "sable":      {"montagne": 0 ,"plaine": 20, "foret": 0 , "sable": 30, "lac": 50},
    "lac":        {"montagne": 0 ,"plaine": 10, "foret": 0 , "sable": 40, "lac": 50}}