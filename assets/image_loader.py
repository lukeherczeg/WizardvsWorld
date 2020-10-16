import wsl
from const import TextureType
from draw import pygame, os
from classes.grid import Grid

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BRIGHT_RED = (255, 0, 0)
BLUE = (0, 0, 255)
BRIGHT_GREEN = (0, 255, 0)
WINDOW_HEIGHT = 600  # 675
WINDOW_WIDTH = 1000  # 1125
# Set the size of the grid block
BLOCK_SIZE = 40  # 45
wsl.set_display_to_host()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.init()

GRID = Grid(WINDOW_WIDTH // BLOCK_SIZE, WINDOW_HEIGHT // BLOCK_SIZE)

X_MOVEMENT_SPEED = [0,0,0,1]
Y_MOVEMENT_SPEED = [0,0,0,1]
move_wiggle = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1]

main_directory = os.path.dirname('WizardvsWorld')
asset_path = os.path.join(main_directory, 'assets')

textures = []


def get_texture(path, texture_type):
    if texture_type == TextureType.TILE_TEXTURE:
        return pygame.transform.scale(pygame.image.load(os.path.join(asset_path, path)).convert(),
                                      (BLOCK_SIZE, BLOCK_SIZE))
    elif texture_type == TextureType.ENTITY or texture_type == TextureType.MISC:
        return pygame.transform.scale(pygame.image.load(os.path.join(asset_path, path)).convert_alpha(),
                                      (BLOCK_SIZE, BLOCK_SIZE))


# load textures
DIRT_PNG = get_texture('dirt.png', TextureType.TILE_TEXTURE)
DIRT_BLUE_PNG = get_texture('dirtBLUE.png', TextureType.TILE_TEXTURE)
DIRT_ORANGE_PNG = get_texture('dirtORANGE.png', TextureType.TILE_TEXTURE)
DIRT_RED_PNG = get_texture('dirtRED.png', TextureType.TILE_TEXTURE)
FLOOR_PNG = get_texture('floor.png', TextureType.TILE_TEXTURE)
FLOOR_BLUE_PNG = get_texture('floorBLUE.png', TextureType.TILE_TEXTURE)
FLOOR_ORANGE_PNG = get_texture('floorORANGE.png', TextureType.TILE_TEXTURE)
FLOOR_RED_PNG = get_texture('floorRED.png', TextureType.TILE_TEXTURE)
GRASS_PNG = get_texture('grass.png', TextureType.TILE_TEXTURE)
GRASS_BLUE_PNG = get_texture('grassBLUE.png', TextureType.TILE_TEXTURE)
GRASS_ORANGE_PNG = get_texture('grassORANGE.png', TextureType.TILE_TEXTURE)
GRASS_RED_PNG = get_texture('grassRED.png', TextureType.TILE_TEXTURE)
STONE_PNG = get_texture('stone.png', TextureType.TILE_TEXTURE)
STONE_BLUE_PNG = get_texture('stoneBLUE.png', TextureType.TILE_TEXTURE)
STONE_ORANGE_PNG = get_texture('stoneORANGE.png', TextureType.TILE_TEXTURE)
STONE_RED_PNG = get_texture('stoneRED.png', TextureType.TILE_TEXTURE)

# Load entities
ARCHER_PNG = get_texture('archer.png', TextureType.ENTITY)
ARCHER_ATTACK_PNG = get_texture('archerattack.png', TextureType.ENTITY)
ARCHER_ATTACKABLE_PNG = get_texture('archerattackable.png', TextureType.ENTITY)
ARCHER_HURT_PNG = get_texture('archerhurt.png', TextureType.ENTITY)
KNIGHT_PNG = get_texture('knight.png', TextureType.ENTITY)
KNIGHT_ATTACK_PNG = get_texture('knightattack.png', TextureType.ENTITY)
KNIGHT_ATTACKABLE_PNG = get_texture('knightattackable.png', TextureType.ENTITY)
KNIGHT_HURT_PNG = get_texture('knighthurt.png', TextureType.ENTITY)
WIZ_PNG = get_texture('wiz.png', TextureType.ENTITY)
WIZ_ATTACK_PNG = get_texture('wizattack.png', TextureType.ENTITY)
WIZ_HURT_PNG = get_texture('wizhurt.png', TextureType.ENTITY)
WIZ_SELECTED_PNG = get_texture('wizselected.png', TextureType.ENTITY)

# Miscellaneous
SELECT_PNG = get_texture('select.png', TextureType.MISC)
ARROW_PNG = get_texture('arrow.png', TextureType.MISC)
FIREBALL_GIF = [
    get_texture('fireball/fireball_0.png', TextureType.MISC),
    get_texture('fireball/fireball_1.png', TextureType.MISC),
    get_texture('fireball/fireball_2.png', TextureType.MISC),
    get_texture('fireball/fireball_3.png', TextureType.MISC),
    get_texture('fireball/fireball_4.png', TextureType.MISC),
]
LOGO_PNG = pygame.image.load(os.path.join(asset_path, 'logo.png')).convert_alpha()
