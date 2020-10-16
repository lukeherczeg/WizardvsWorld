import wsl
from draw import pygame, os
from classes.grid import Grid

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BRIGHT_RED = (255, 0, 0)
BLUE = (0, 0, 255)
BRIGHT_GREEN = (0,255,0)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1000
BLOCK_SIZE = 40  # Set the size of the grid block
wsl.set_display_to_host()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.init()

GRID = Grid(WINDOW_WIDTH // BLOCK_SIZE, WINDOW_HEIGHT // BLOCK_SIZE)

X_MOVEMENT_SPEED = 1
Y_MOVEMENT_SPEED = 1
move_wiggle = [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, -1, 0, -1, 0, -1, 0, -1]

main_directory = os.path.dirname('WizardvsWorld')
asset_path = os.path.join(main_directory, 'assets')

#load textures
DIRT_PNG = pygame.image.load(os.path.join(asset_path, 'dirt.png')).convert()
DIRT_BLUE_PNG = pygame.image.load(os.path.join(asset_path, 'dirtBLUE.png')).convert()
DIRT_ORANGE_PNG = pygame.image.load(os.path.join(asset_path, 'dirtORANGE.png')).convert()
DIRT_RED_PNG = pygame.image.load(os.path.join(asset_path, 'dirtRED.png')).convert()
FLOOR_PNG = pygame.image.load(os.path.join(asset_path, 'floor.png')).convert()
FLOOR_BLUE_PNG = pygame.image.load(os.path.join(asset_path, 'floorBLUE.png')).convert()
FLOOR_ORANGE_PNG = pygame.image.load(os.path.join(asset_path, 'floorORANGE.png')).convert()
FLOOR_RED_PNG = pygame.image.load(os.path.join(asset_path, 'floorRED.png')).convert()
GRASS_PNG = pygame.image.load(os.path.join(asset_path, 'grass.png')).convert()
GRASS_BLUE_PNG = pygame.image.load(os.path.join(asset_path, 'grassBLUE.png')).convert()
GRASS_ORANGE_PNG = pygame.image.load(os.path.join(asset_path, 'grassORANGE.png')).convert()
GRASS_RED_PNG = pygame.image.load(os.path.join(asset_path, 'grassRED.png')).convert()
STONE_PNG = pygame.image.load(os.path.join(asset_path, 'stone.png')).convert()
STONE_BLUE_PNG = pygame.image.load(os.path.join(asset_path, 'stoneBLUE.png')).convert()
STONE_ORANGE_PNG = pygame.image.load(os.path.join(asset_path, 'stoneORANGE.png')).convert()
STONE_RED_PNG = pygame.image.load(os.path.join(asset_path, 'stoneRED.png')).convert()

#load entities
ARCHER_PNG = pygame.image.load(os.path.join(asset_path, 'archer.png')).convert_alpha()
ARCHER_ATTACK_PNG = pygame.image.load(os.path.join(asset_path, 'archerattack.png')).convert_alpha()
ARCHER_ATTACKABLE_PNG = pygame.image.load(os.path.join(asset_path, 'archerattackable.png')).convert_alpha()
ARCHER_HURT_PNG = pygame.image.load(os.path.join(asset_path, 'archerhurt.png')).convert_alpha()
KNIGHT_PNG = pygame.image.load(os.path.join(asset_path, 'knight.png')).convert_alpha()
KNIGHT_ATTACK_PNG = pygame.image.load(os.path.join(asset_path, 'knightattack.png')).convert_alpha()
KNIGHT_ATTACKABLE_PNG = pygame.image.load(os.path.join(asset_path, 'knightattackable.png')).convert_alpha()
KNIGHT_HURT_PNG = pygame.image.load(os.path.join(asset_path, 'knighthurt.png')).convert_alpha()
WIZ_PNG = pygame.image.load(os.path.join(asset_path, 'wiz.png')).convert_alpha()
WIZ_ATTACK_PNG = pygame.image.load(os.path.join(asset_path, 'wizattack.png')).convert_alpha()
WIZ_HURT_PNG = pygame.image.load(os.path.join(asset_path, 'wizhurt.png')).convert_alpha()
WIZ_SELECTED_PNG = pygame.image.load(os.path.join(asset_path, 'wizselected.png')).convert_alpha()

#Miscelaneous
SELECT_PNG = pygame.image.load(os.path.join(asset_path, 'select.png')).convert_alpha()
ARROW_PNG = pygame.image.load(os.path.join(asset_path, 'arrow.png')).convert_alpha()
FIREBALL_GIF = [
    pygame.image.load(os.path.join(asset_path, 'fireball/fireball_0.png')).convert_alpha(),
    pygame.image.load(os.path.join(asset_path, 'fireball/fireball_1.png')).convert_alpha(),
    pygame.image.load(os.path.join(asset_path, 'fireball/fireball_2.png')).convert_alpha(),
    pygame.image.load(os.path.join(asset_path, 'fireball/fireball_3.png')).convert_alpha(),
    pygame.image.load(os.path.join(asset_path, 'fireball/fireball_4.png')).convert_alpha(),
]
ARROW_PNG = pygame.image.load(os.path.join(asset_path, 'arrow.png')).convert_alpha()