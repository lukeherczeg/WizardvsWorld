from enum import Enum

ENTITIES = []

CRIT_MULTIPLIER = 2


class TextureType(Enum):
    TILE_TEXTURE = 1
    ENTITY = 2
    MISC = 3


class TileTint(Enum):
    NONE = 0
    BLUE = 1
    RED = 2
    ORANGE = 3


class TileTexture(Enum):
    NONE = -1
    GRASS = 0
    DIRT = 1
    STONE = 2
    FLOOR = 3
    BUSH = 4
