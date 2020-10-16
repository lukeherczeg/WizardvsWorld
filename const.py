from enum import Enum

ENTITIES = []

class TileTint(Enum):
    NONE = 0
    BLUE = 1
    RED = 2
    ORANGE = 3


class TextureType(Enum):
    NONE = -1
    GRASS = 0
    DIRT = 1
    STONE = 2
    FLOOR = 3
