from draw import pygame, os
import wsl

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1000
BLOCK_SIZE = 40
wsl.set_display_to_host()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.init()

X_MOVEMENT_SPEED = 1
Y_MOVEMENT_SPEED = 1
move_wiggle = [0,0,0,1,0,1,0,1,0,1,0,0,0,-1,0,-1,0,-1,0,-1]

main_directory = os.path.dirname('WizardvsWorld')
asset_path = os.path.join(main_directory, 'assets')

GRASS_PNG = pygame.image.load(os.path.join(asset_path, 'grass.png')).convert()
GRASS_BLUE_PNG = pygame.image.load(os.path.join(asset_path, 'grassBLUE.png')).convert()
STONE_RED_PNG = pygame.image.load(os.path.join(asset_path, 'stoneRED.png')).convert()
STONE_PNG = pygame.image.load(os.path.join(asset_path, 'stone.png')).convert()
WIZ_PNG = pygame.image.load(os.path.join(asset_path, 'wiz.png')).convert_alpha()
KNIGHT_PNG = pygame.image.load(os.path.join(asset_path, 'knight.png')).convert_alpha()
FIREBALL_GIF = [pygame.image.load(os.path.join(asset_path, 'fireball/fireball_0.png')).convert_alpha(),
pygame.image.load(os.path.join(asset_path, 'fireball/fireball_1.png')).convert_alpha(),
pygame.image.load(os.path.join(asset_path, 'fireball/fireball_2.png')).convert_alpha(),
pygame.image.load(os.path.join(asset_path, 'fireball/fireball_3.png')).convert_alpha(),
pygame.image.load(os.path.join(asset_path, 'fireball/fireball_4.png')).convert_alpha()]
