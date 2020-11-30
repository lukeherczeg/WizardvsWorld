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
CLOCK = pygame.time.Clock()
FPS = 110

GRID = Grid(WINDOW_WIDTH // BLOCK_SIZE, WINDOW_HEIGHT // BLOCK_SIZE)


MOVEMENT_SPEED = 3
move_wiggle = [-2, 0, -1, 0, -1, 0, 0, 1, 0, 1, 0, 2]
dodge_wiggle = [0, 0, 1]
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
BUSH_PNG = get_block_sized_texture('bush.png', TextureType.TILE_TEXTURE)
BUSH_FIRE_PNG = get_block_sized_texture('bushFIRE.png', TextureType.TILE_TEXTURE)
BUSH_ORANGE_PNG = get_block_sized_texture('bushORANGE.png', TextureType.TILE_TEXTURE)
BUSH_RED_PNG = get_block_sized_texture('bushRED.png', TextureType.TILE_TEXTURE)
CACTUS_PNG = get_block_sized_texture('cactus.png', TextureType.TILE_TEXTURE)
CACTUS_FIRE_PNG = get_block_sized_texture('cactusFIRE.png', TextureType.TILE_TEXTURE)
CACTUS_ORANGE_PNG = get_block_sized_texture('cactusORANGE.png', TextureType.TILE_TEXTURE)
CACTUS_RED_PNG = get_block_sized_texture('cactusRED.png', TextureType.TILE_TEXTURE)
DARK_BRICK_PNG = get_block_sized_texture('darkbrick.png', TextureType.TILE_TEXTURE)
DARK_BRICK_ORANGE_PNG = get_block_sized_texture('darkbrickORANGE.png', TextureType.TILE_TEXTURE)
DARK_BRICK_RED_PNG = get_block_sized_texture('darkbrickRED.png', TextureType.TILE_TEXTURE)
DIRT_PNG = get_block_sized_texture('dirt.png', TextureType.TILE_TEXTURE)
DIRT_BLUE_PNG = get_block_sized_texture('dirtBLUE.png', TextureType.TILE_TEXTURE)
DIRT_FIRE_PNG = get_block_sized_texture('dirtFIRE.png', TextureType.TILE_TEXTURE)
DIRT_ORANGE_PNG = get_block_sized_texture('dirtORANGE.png', TextureType.TILE_TEXTURE)
DIRT_RED_PNG = get_block_sized_texture('dirtRED.png', TextureType.TILE_TEXTURE)
FLOOR_PNG = get_block_sized_texture('floor.png', TextureType.TILE_TEXTURE)
FLOOR_BLUE_PNG = get_block_sized_texture('floorBLUE.png', TextureType.TILE_TEXTURE)
FLOOR_FIRE_PNG = get_block_sized_texture('floorFIRE.png', TextureType.TILE_TEXTURE)
FLOOR_ORANGE_PNG = get_block_sized_texture('floorORANGE.png', TextureType.TILE_TEXTURE)
FLOOR_RED_PNG = get_block_sized_texture('floorRED.png', TextureType.TILE_TEXTURE)
GRASS_PNG = get_block_sized_texture('grass.png', TextureType.TILE_TEXTURE)
GRASS_BLUE_PNG = get_block_sized_texture('grassBLUE.png', TextureType.TILE_TEXTURE)
GRASS_FIRE_PNG = get_block_sized_texture('grassFIRE.png', TextureType.TILE_TEXTURE)
GRASS_ORANGE_PNG = get_block_sized_texture('grassORANGE.png', TextureType.TILE_TEXTURE)
GRASS_RED_PNG = get_block_sized_texture('grassRED.png', TextureType.TILE_TEXTURE)
MUD_PNG = get_block_sized_texture('mud.png', TextureType.TILE_TEXTURE)
MUD_BLUE_PNG = get_block_sized_texture('mudBLUE.png', TextureType.TILE_TEXTURE)
MUD_FIRE_PNG = get_block_sized_texture('mudFIRE.png', TextureType.TILE_TEXTURE)
MUD_ORANGE_PNG = get_block_sized_texture('mudORANGE.png', TextureType.TILE_TEXTURE)
MUD_RED_PNG = get_block_sized_texture('mudRED.png', TextureType.TILE_TEXTURE)
MUD_BRICK_PNG = get_block_sized_texture('mudbrick.png', TextureType.TILE_TEXTURE)
MUD_BRICK_ORANGE_PNG = get_block_sized_texture('mudbrickORANGE.png', TextureType.TILE_TEXTURE)
MUD_BRICK_RED_PNG = get_block_sized_texture('mudbrickRED.png', TextureType.TILE_TEXTURE)
ROCK_PNG = get_block_sized_texture('rock.png', TextureType.TILE_TEXTURE)
ROCK_FIRE_PNG = get_block_sized_texture('rockFIRE.png', TextureType.TILE_TEXTURE)
ROCK_ORANGE_PNG = get_block_sized_texture('rockORANGE.png', TextureType.TILE_TEXTURE)
ROCK_RED_PNG = get_block_sized_texture('rockRED.png', TextureType.TILE_TEXTURE)
STONE_PNG = get_block_sized_texture('stone.png', TextureType.TILE_TEXTURE)
STONE_BLUE_PNG = get_block_sized_texture('stoneBLUE.png', TextureType.TILE_TEXTURE)
STONE_ORANGE_PNG = get_block_sized_texture('stoneORANGE.png', TextureType.TILE_TEXTURE)
STONE_RED_PNG = get_block_sized_texture('stoneRED.png', TextureType.TILE_TEXTURE)
SAND_PNG = get_block_sized_texture('sand.png', TextureType.TILE_TEXTURE)
SAND_BLUE_PNG = get_block_sized_texture('sandBLUE.png', TextureType.TILE_TEXTURE)
SAND_FIRE_PNG = get_block_sized_texture('sandFIRE.png', TextureType.TILE_TEXTURE)
SAND_ORANGE_PNG = get_block_sized_texture('sandORANGE.png', TextureType.TILE_TEXTURE)
SAND_RED_PNG = get_block_sized_texture('sandRED.png', TextureType.TILE_TEXTURE)
SNOW_PNG = get_block_sized_texture('snow.png', TextureType.TILE_TEXTURE)
SNOW_BLUE_PNG = get_block_sized_texture('snowBLUE.png', TextureType.TILE_TEXTURE)
SNOW_FIRE_PNG = get_block_sized_texture('snowFIRE.png', TextureType.TILE_TEXTURE)
SNOW_ORANGE_PNG = get_block_sized_texture('snowORANGE.png', TextureType.TILE_TEXTURE)
SNOW_RED_PNG = get_block_sized_texture('snowRED.png', TextureType.TILE_TEXTURE)
WOOD_PNG = get_block_sized_texture('wood.png', TextureType.TILE_TEXTURE)
WOOD_BLUE_PNG = get_block_sized_texture('woodBLUE.png', TextureType.TILE_TEXTURE)
WOOD_FIRE_PNG = get_block_sized_texture('woodFIRE.png', TextureType.TILE_TEXTURE)
WOOD_ORANGE_PNG = get_block_sized_texture('woodORANGE.png', TextureType.TILE_TEXTURE)
WOOD_RED_PNG = get_block_sized_texture('woodRED.png', TextureType.TILE_TEXTURE)

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
GREAT_MARKSMAN_PNG = get_block_sized_texture('greatmarksman.png', TextureType.ENTITY)
GREAT_MARKSMAN_ATTACK_PNG = get_block_sized_texture('greatmarksmanattack.png', TextureType.ENTITY)
GREAT_MARKSMAN_HURT_PNG = get_block_sized_texture('greatmarksmanhurt.png', TextureType.ENTITY)
WIZ_PNG = get_block_sized_texture('wiz.png', TextureType.ENTITY)
WIZ_ATTACK_PNG = get_block_sized_texture('wizattack.png', TextureType.ENTITY)
WIZ_HURT_PNG = get_block_sized_texture('wizhurt.png', TextureType.ENTITY)
WIZ_SELECTED_PNG = get_block_sized_texture('wizselected.png', TextureType.ENTITY)
WIZ_HEALING_PNG = get_block_sized_texture('wizhealing.png', TextureType.ENTITY)
WIZARD_KING_PNG = get_block_sized_texture('wizardking.png', TextureType.ENTITY)
WIZARD_KING_ATTACK_PNG = get_block_sized_texture('wizardkingattack.png', TextureType.ENTITY)
WIZARD_KING_HURT_PNG = get_block_sized_texture('wizardkinghurt.png', TextureType.ENTITY)

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
FIREBALL_LARGE_GIF = [
    get_block_sized_texture('fireball/fireball_0.png', TextureType.MISC, 45),
    get_block_sized_texture('fireball/fireball_1.png', TextureType.MISC, 45),
    get_block_sized_texture('fireball/fireball_2.png', TextureType.MISC, 45),
    get_block_sized_texture('fireball/fireball_3.png', TextureType.MISC, 45),
    get_block_sized_texture('fireball/fireball_4.png', TextureType.MISC, 45),
]
LOGO_PNG = get_texture('logo.png', TextureType.MISC)
BACKGROUND_PNG = get_texture('background.png', TextureType.MISC)
BACKGROUND_SMALL_PNG = get_texture('backgroundSMALL.png', TextureType.MISC)
WIZ_LARGE_PNG = get_texture('wizLARGE.png', TextureType.MISC)

