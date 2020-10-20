from WizardVsWorld.classes import wsl
from WizardVsWorld.classes.const import TextureType
from WizardVsWorld.classes.draw import pygame
from WizardVsWorld.classes.grid import Grid

import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (100, 0, 0)
BRIGHT_RED = (255, 0, 0)
BLUE = (0, 0, 255)
BRIGHT_GREEN = (0, 255, 0)
GREEN = (34, 139, 34)
WINDOW_HEIGHT = 600  # 675
WINDOW_WIDTH = 1000  # 1125
# Set the size of the grid block
BLOCK_SIZE = 40  # 45
wsl.set_display_to_host()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.init()

GRID = Grid(WINDOW_WIDTH // BLOCK_SIZE, WINDOW_HEIGHT // BLOCK_SIZE)


MOVEMENT_SPEED = 2
move_wiggle = [-1, 0, -1, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0]
# move_wiggle = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1]

asset_path = os.path.dirname(__file__)

textures = []


def get_texture(path, texture_type):
    if texture_type == TextureType.TILE_TEXTURE:
        return pygame.image.load(os.path.join(asset_path, path)).convert()
    elif texture_type == TextureType.ENTITY or texture_type == TextureType.MISC:
        return pygame.image.load(os.path.join(asset_path, path)).convert_alpha()


def get_block_sized_texture(path, texture_type, block_size=BLOCK_SIZE):
    return pygame.transform.scale(get_texture(path, texture_type), (block_size, block_size))


# load textures
DIRT_PNG = get_block_sized_texture('dirt.png', TextureType.TILE_TEXTURE)
DIRT_BLUE_PNG = get_block_sized_texture('dirtBLUE.png', TextureType.TILE_TEXTURE)
DIRT_ORANGE_PNG = get_block_sized_texture('dirtORANGE.png', TextureType.TILE_TEXTURE)
DIRT_RED_PNG = get_block_sized_texture('dirtRED.png', TextureType.TILE_TEXTURE)
FLOOR_PNG = get_block_sized_texture('floor.png', TextureType.TILE_TEXTURE)
FLOOR_BLUE_PNG = get_block_sized_texture('floorBLUE.png', TextureType.TILE_TEXTURE)
FLOOR_ORANGE_PNG = get_block_sized_texture('floorORANGE.png', TextureType.TILE_TEXTURE)
FLOOR_RED_PNG = get_block_sized_texture('floorRED.png', TextureType.TILE_TEXTURE)
GRASS_PNG = get_block_sized_texture('grass.png', TextureType.TILE_TEXTURE)
GRASS_BLUE_PNG = get_block_sized_texture('grassBLUE.png', TextureType.TILE_TEXTURE)
GRASS_ORANGE_PNG = get_block_sized_texture('grassORANGE.png', TextureType.TILE_TEXTURE)
GRASS_RED_PNG = get_block_sized_texture('grassRED.png', TextureType.TILE_TEXTURE)
STONE_PNG = get_block_sized_texture('stone.png', TextureType.TILE_TEXTURE)
STONE_BLUE_PNG = get_block_sized_texture('stoneBLUE.png', TextureType.TILE_TEXTURE)
STONE_ORANGE_PNG = get_block_sized_texture('stoneORANGE.png', TextureType.TILE_TEXTURE)
STONE_RED_PNG = get_block_sized_texture('stoneRED.png', TextureType.TILE_TEXTURE)
BUSH_PNG = pygame.image.load(os.path.join(asset_path, 'bush.png')).convert()
BUSH_ORANGE_PNG = pygame.image.load(os.path.join(asset_path, 'bushORANGE.png')).convert()
BUSH_RED_PNG = pygame.image.load(os.path.join(asset_path, 'bushRED.png')).convert()

# Load entities
ARCHER_PNG = get_block_sized_texture('archer.png', TextureType.ENTITY)
ARCHER_ATTACK_PNG = get_block_sized_texture('archerattack.png', TextureType.ENTITY)
ARCHER_ATTACKABLE_PNG = get_block_sized_texture('archerattackable.png', TextureType.ENTITY)
ARCHER_HURT_PNG = get_block_sized_texture('archerhurt.png', TextureType.ENTITY)
KNIGHT_PNG = get_block_sized_texture('knight.png', TextureType.ENTITY)
KNIGHT_ATTACK_PNG = get_block_sized_texture('knightattack.png', TextureType.ENTITY)
KNIGHT_ATTACKABLE_PNG = get_block_sized_texture('knightattackable.png', TextureType.ENTITY)
KNIGHT_HURT_PNG = get_block_sized_texture('knighthurt.png', TextureType.ENTITY)
GREATKNIGHT_PNG = get_block_sized_texture('greatknight.png', TextureType.ENTITY)
GREATKNIGHT_ATTACK_PNG = get_block_sized_texture('greatknightattack.png', TextureType.ENTITY)
GREATKNIGHT_HURT_PNG = get_block_sized_texture('greatknighthurt.png', TextureType.ENTITY)
WIZ_PNG = get_block_sized_texture('wiz.png', TextureType.ENTITY)
WIZ_ATTACK_PNG = get_block_sized_texture('wizattack.png', TextureType.ENTITY)
WIZ_HURT_PNG = get_block_sized_texture('wizhurt.png', TextureType.ENTITY)
WIZ_SELECTED_PNG = get_block_sized_texture('wizselected.png', TextureType.ENTITY)

# Miscellaneous
SELECT_PNG = get_block_sized_texture('select.png', TextureType.MISC)
ARROW_PNG = get_block_sized_texture('arrow.png', TextureType.MISC)
FIREBALL_GIF = [
    get_block_sized_texture('fireball/fireball_0.png', TextureType.MISC),
    get_block_sized_texture('fireball/fireball_1.png', TextureType.MISC),
    get_block_sized_texture('fireball/fireball_2.png', TextureType.MISC),
    get_block_sized_texture('fireball/fireball_3.png', TextureType.MISC),
    get_block_sized_texture('fireball/fireball_4.png', TextureType.MISC),
]
LOGO_PNG = get_texture('logo.png', TextureType.MISC)
BACKGROUND_PNG = get_texture('background.png', TextureType.MISC)
BACKGROUND_SMALL_PNG = get_texture('backgroundSMALL.png', TextureType.MISC)
WIZ_LARGE_PNG = get_texture('wizLARGE.png', TextureType.MISC)

