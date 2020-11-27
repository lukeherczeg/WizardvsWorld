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
    FIRE = 4


class TileTexture(Enum):
    NONE = -1
    GRASS = 0
    DIRT = 1
    STONE = 2
    FLOOR = 3
    BUSH = 4


map_0 = "0000000000000000w00000000" \
        "0000rr0000000000000022222" \
        "00000r000000000r000222332" \
        "0000000000000000000233332" \
        "00000rr000000000000233332" \
        "0000000000000000000233332" \
        "0000000000000000002223f32" \
        "1111111111111111133333f3w" \
        "0000000000000000002223f32" \
        "0000r000000rr000000233332" \
        "00000000000r0000000233332" \
        "0000r00000000000000233332" \
        "0000000000000000000222332" \
        "0000000000000000000022222" \
        "00000000w0000000000000000"

map_1 = "0000000000000r00000000000" \
        "0000000000000000000022222" \
        "000000000000000r000222332" \
        "00r0000000rr0000000233332" \
        "00000rr000000000000233332" \
        "0000000000000r00002233332" \
        "000000000000000000K223f32" \
        "111111111111111111KR33f3w" \
        "000000000000000000K223f32" \
        "000000000000r000002233332" \
        "0000000000000000000233332" \
        "000000000000r000000233332" \
        "000000000000000r000222332" \
        "0000000000000000000022222" \
        "000000000000r000000000000"

map_2 = "0000000000000000000000000" \
        "0000000000000000000022222" \
        "0000000000000000000222332" \
        "0000000000000000000233332" \
        "0000000000000000000233332" \
        "0000000000000000002233332" \
        "000000000000KKK0002223f32" \
        "111111111111KRK1113333f3w" \
        "000000000000KKK0002223f32" \
        "0000000000000000002233332" \
        "0000000000000000000233332" \
        "0000000000000000000233332" \
        "0000000000000000000222332" \
        "0000000000000000000022222" \
        "0000000000000000000000000"

map_3 = "0000000000000000000000000" \
        "0000000000000000000022222" \
        "0000000000000000000222332" \
        "0000000000r00000000233332" \
        "00000000000000r0000233332" \
        "00000000r0000000002233f32" \
        "0000000000000K00R03333f32" \
        "111111111111111R1133f3f3w" \
        "0000000000000K00R03333f32" \
        "00000000000000r0002233f32" \
        "0000000000000000000233332" \
        "0000000000r00000000233332" \
        "0000000000000000000222332" \
        "000000000000r000000022222" \
        "0000000000000000000000000"

map_4 = "0000000000000000000000000" \
        "0000000000000000000022222" \
        "0000000000000000r00222332" \
        "0000000000000000000233332" \
        "00000000000000K0000233332" \
        "0000000000000000r02233332" \
        "000000000000000r001333f32" \
        "1111111111111111113333f3w" \
        "000000000000000r001333f32" \
        "00000000r00000r0000233332" \
        "00000000000000r0000233332" \
        "0000000000000000r00233332" \
        "0000000000000000000222332" \
        "0000000000000000000022222" \
        "0000000000000000000000000"

mapU0 = ""

mapD0 = ""
