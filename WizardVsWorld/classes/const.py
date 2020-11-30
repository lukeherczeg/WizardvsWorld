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
    WOOD = 5
    DARK_BRICK = 6
    SNOW = 7
    ROCK = 8
    MUD = 9
    MUD_BRICK = 10
    SAND = 11
    CACTUS = 12

#start map
map_0 = "0000000000000000000000000" \
        "0000rr00000000000000[[[[[" \
        "00000r000000000r000[[[33[" \
        "0000000000000000000[3333[" \
        "00000rr000000000000[3333[" \
        "0000000000000000000[3333[" \
        "000000000000000000[[[3f3[" \
        "11111111111111111f3333fGw" \
        "000000000000000000[[[3f3[" \
        "0000r000000rr000000[3333[" \
        "00000000000r0000000[3333[" \
        "0000r00000000000000[3333[" \
        "0000000000000000000[[[33[" \
        "00000000000000000000[[[[[" \
        "0000000000000000000000000"

#Middle row maps
map_5 = "0000000c6c000r0cxc0000000" \
        "00000000000000066600[[[[[" \
        "0000000000000000000[[[33[" \
        "000000R000000000000[3333[" \
        "00000RR000000000000[3333[" \
        "000000000000000000[[3333[" \
        "000000000KRK0000000[[3333" \
        "1111111111K1111111333333[" \
        "000000000KRK0000000[[333w" \
        "000000000000000000[[3333[" \
        "00000RR000000000000[3333[" \
        "000000R000000000000[3333[" \
        "0000000000000000000[[[33[" \
        "00000004440000000000[[[[[" \
        "0000000CvC00r00C4C0000000"

map_6 = "0000000c6c00000cxc0000000" \
        "00000003330000066600[[[[[" \
        "0000000000000000000[[[33[" \
        "0000000000K00000000[3333[" \
        "000000000KRK0000000[33G3[" \
        "[0000R0000K0000R00[[3333[" \
        "w30000000000000000[[[3333" \
        "[311111111111111113333G3[" \
        "330000000000000000[[[333w" \
        "[0000R0000K0000R00[[3333[" \
        "000000000KRK0000000[33G3[" \
        "0000000000K00000000[3333[" \
        "0000000000000000000[[[33[" \
        "00000004440000033300[[[[[" \
        "0000000CvC00000C4C0000000"

map_7 = "0000000000000000000000000" \
        "0000000000000000000000000" \
        "0000000000000000000000000" \
        "0000000000000000000000000" \
        "0000000000000000000000000" \
        "[[000000000000000000000[[" \
        "w000000000000000000000003" \
        "[[000000000000000000000[[" \
        "300000000000000000000000w" \
        "[[000000000000000000000[[" \
        "0000000000000000000000000" \
        "0000000000000000000000000" \
        "0000000000000000000000000" \
        "0000000000000000000000000" \
        "0000000000000000000000000"

map_8 = "0000000030000000w00000000" \
        "0000000000000000000000000" \
        "0000000000000000000000000" \
        "0000000000000000000000000" \
        "0000000000000000000000000" \
        "[[00000000000000000000000" \
        "w000000000000000000000000" \
        "[[00000000000000000000000" \
        "3000000000000000000000000" \
        "[[00000000000000000000000" \
        "0000000000000000000000000" \
        "0000000000000000000000000" \
        "0000000000000000000000000" \
        "0000000000000000000000000" \
        "00000000w0000000300000000"

#top row maps
map_1 = "6666666666666666c66666666" \
        "6666666666666666666666666" \
        "6c666<<<<<<<<<<<<<<<<<<<<" \
        "66666<777777777777777777<" \
        "66666<7777777777777777<<<" \
        "66666<7777777777777<77<6c" \
        "66c66<7777777777777<77667" \
        "66666<7777777777777<77<6c" \
        "66666<7777777777777<7766x" \
        "c6666<777777777<<<<<77<6c" \
        "66666<7777777777777777<66" \
        "6666c<7<7<77777<7<7777<<<" \
        "66666<<<7<<<<<<<7<<<<<<<<" \
        "666c666222666666666666666" \
        "6666666bwb66666b2b6666666"

map_2 = "66666666666666666c6666666" \
        "6666c66666666666666666666" \
        "66666666666<7<66666666666" \
        "6666666<<<<<7<<<<<6666666" \
        "6666666<777777777<6666666" \
        "c666666<777777777<666666c" \
        "x666666<777777777<6666667" \
        "c666666<777777777<666666c" \
        "7666666<<<<<<<<<<<666666x" \
        "c666666666666c6666666666c" \
        "6666666666666666666666666" \
        "666c666666666666c66666666" \
        "666c666666666666666666666" \
        "6666666222666666666c66666" \
        "6666666bwb66666b2b666c[[["

map_3 = "6666666666666666666666666" \
        "6666666666666666666666666" \
        "66666cc66666666666cc66666" \
        "66666c7777777777777c6666" \
        "66666<77<<<777<<<77<66666" \
        "c6666<7777777777777<6666c" \
        "x6666<7777777777777<66667" \
        "c6666<7777777777777<6666c" \
        "76666<7777777777777<6666x" \
        "c6666<7777777777777<6666c" \
        "66666<77<<<777<<<77<66666" \
        "6666677777777777777766666" \
        "6666666666666666666666666" \
        "6[6[6[6[6[6[6[6[6[6[6[6[6" \
        "[[[[[[[[[[[[[[[[[[[[[[[[["

map_4 = "66c6666666<<<<<<<<<<<<<<<" \
        "6666666c66<7777777777777<" \
        "6666666666<<777777777777<" \
        "66666c66666<777777777777<" \
        "66666666666<<77777777777<" \
        "c666666c6666<77777777777<" \
        "x66666666666<<7777777777<" \
        "c6666666c6666<7777777777<" \
        "7666666666c66<<77<77<777<" \
        "c6666666666666<7<6776<77<" \
        "66666666666c66<<<67766<<<" \
        "66c66666666666666c77c6666" \
        "6666666666666666666666666" \
        "6c6c6c63336c6c6c6c6c6c6c6" \
        "[[[[[[[[w[[[[[[[3[[[[[[[["

#bottom row maps
map_9 = "444C444b2b44444bwb4444444" \
        "4444444444444442224444444" \
        "4C4444444m444444444444444" \
        "44444444444444444{{{44444" \
        "4s44{{{44s44C4444{m{44444" \
        "4C44{m{4444444444C444444C" \
        "44444444C44s444{{{4444445" \
        "444444444444444{m{444444C" \
        "444C4444444444444444C444v" \
        "4{4{4{4{4{44444{4{4{4{4{C" \
        "{5{5{5{5{5m555m5{5{5{5{5{" \
        "{5555m55555mmm55555m5555{" \
        "{55A555m555555555m555555{" \
        "{5555m555555555555555555{" \
        "{{{{{{{{{{{{{{{{{{{{{{{{{"

map_10 ="4444444b2b44444bwb4444[[[" \
        "4C4444444444444222444C444" \
        "55C5m555555mm5555555C5555" \
        "5555555555555555mm5555555" \
        "{{{{5{{{{5{{{{5{{{{5{{{{{" \
        "C55{5{mm{5{mm{5{mm{5{555C" \
        "v4444444444444444444444s5" \
        "C4444444444444444444444sC" \
        "54444444444444444444444sv" \
        "C55{5{mm{5{mm{5{mm{5{555C" \
        "{{{{5{{{{5{{{{5{{{{5{{{{{" \
        "5555555555m55555555555555" \
        "55C55m55555555m555C555555" \
        "444444444444C44444444s444" \
        "44444C4s44444444C44444444"

map_11 ="[[[[[[[[[[[[[[[[[[[[[[[[[" \
        "4[4[4[4[4[4[4[4[4[4[4[4[4" \
        "4444444s4s4C4444444444444" \
        "44s4{5544s4ss4444455{4444" \
        "4444{555444444s44555{4444" \
        "C444445554s4s4445s55{444C" \
        "v44s444444s44445555444445" \
        "C444{{4{{{4C444{4{{{4444C" \
        "54444444s4444444444s4444v" \
        "C4444444s44444444s444444C" \
        "44s4C{{54{{44s{s{{{{{s444" \
        "4444{545554444{44s55{4444" \
        "44s4444555{444{555444s444" \
        "44444s4444C4s4C4444444444" \
        "4444C44444444444444444444"

map_12 ="[[[[[[[[3[[[[[[[w[[[[[[[[" \
        "4C4C4C4C4C4C4C43334C4C4C4" \
        "4444444444444444444444444" \
        "4C444s44s44s4444444444444" \
        "4444444C4444444C4C4C4C4C4" \
        "C44s444444s444C{{{{{{{{{{" \
        "v44444s444444C{{44455555{" \
        "C4444444s444C{444455555m{" \
        "544s4444444C{44{44555m5m{" \
        "C4444s4444C{444{455m5555{" \
        "444444444C{44s4{55m55m55{" \
        "44444444C{44444{5555m555{" \
        "4444444C{4s4s44{55m55m55{" \
        "444444C{4444444{5G5555G5{" \
        "444444444444444{{{{{{{{{{"