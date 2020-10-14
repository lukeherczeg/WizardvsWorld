from draw import pygame, os

main_directory = os.path.dirname('WizardvsWorld')
asset_path = os.path.join(main_directory, 'assets')

GRASS_PNG = pygame.image.load(os.path.join(asset_path, 'grass.png'))

GRASS_BLUE_PNG = pygame.image.load(os.path.join(asset_path, 'grassBLUE.png'))

STONE_RED_PNG = pygame.image.load(os.path.join(asset_path, 'stoneRED.png'))

STONE_PNG = pygame.image.load(os.path.join(asset_path, 'stone.png'))

WIZ_PNG = pygame.image.load(os.path.join(asset_path, 'wiz.png'))
