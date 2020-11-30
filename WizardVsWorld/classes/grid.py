from WizardVsWorld.classes.const import ENTITIES
from WizardVsWorld.classes.tile import Tile, TileTexture
from random import random
import os  # importing for reading maps inside of /maps

from WizardVsWorld.classes.entity import Knight, Archer, GreatKnight, GreatMarksman, WizardKing
from WizardVsWorld.classes.const import *


class Grid:
    STANDABLE_TILE_DENSITY_ODDS: float = 0.98

    def __init__(self, width, height, map_number=0):
        self.GRID_WIDTH = width
        self.GRID_HEIGHT = height
        # Variables to keep track of level
        self.map_number = map_number
        self.map_layout = map_0
        self.win_tiles = [None] * 4
        # INDEX WITH [ROW][COL]
        self._game_map = [[self.generate_tile(x, y) for x in range(self.GRID_WIDTH)] for y in range(self.GRID_HEIGHT)]
        self.defeated_maps = [False] * 13

    @property
    def game_map(self):
        return self._game_map

    def set_game_map(self, map1):
        self._game_map = map1

    def is_valid_tile_in_list(self, row, col, tile_list):
        if self.is_valid_tile(row, col) and self.game_map[row][col] in tile_list:
            return True
        else:
            return False

    def is_valid_standable_tile(self, row, col):
        if self.is_valid_tile(row, col) and self.game_map[row][col].standable:
            return True
        else:
            return False

    def is_valid_tile(self, row, col):
        if 0 <= row < self.GRID_HEIGHT and 0 <= col < self.GRID_WIDTH:
            return True
        else:
            return False

    def handle_tile(self, row, col, movable_tiles, adjacent_movable_tiles,
                    non_standable_tiles, valid_edge_tiles, valid_tiles):
        if self.is_valid_tile(row, col):
            new_tile = self._game_map[row][col]
            if new_tile in movable_tiles and not new_tile.occupied:
                adjacent_movable_tiles += 1
            elif not new_tile.standable or new_tile.occupied:
                non_standable_tiles.append(new_tile)
            else:
                valid_edge_tiles.append(new_tile)
        else:
            valid_tiles -= 1

    def get_movement_border(self, movable_tiles, attack_range):
        tile_list = []
        non_standable_tiles = []

        # This is a fairly complicated algorithm for determining the border tiles of
        # valid movement tiles as well as non-standable tiles anywhere in between.

        for tile in movable_tiles:
            valid_edge_tiles = []
            adjacent_movable_tiles = 0
            valid_tiles = 4

            row = tile.row + 1
            col = tile.col

            self.handle_tile(row, col, movable_tiles, adjacent_movable_tiles,
                             non_standable_tiles, valid_edge_tiles, valid_tiles)

            row = tile.row - 1
            col = tile.col

            self.handle_tile(row, col, movable_tiles, adjacent_movable_tiles,
                             non_standable_tiles, valid_edge_tiles, valid_tiles)

            row = tile.row
            col = tile.col + 1

            self.handle_tile(row, col, movable_tiles, adjacent_movable_tiles,
                             non_standable_tiles, valid_edge_tiles, valid_tiles)

            row = tile.row
            col = tile.col - 1

            self.handle_tile(row, col, movable_tiles, adjacent_movable_tiles,
                             non_standable_tiles, valid_edge_tiles, valid_tiles)

            # If the counters are different, we have an edge!
            if adjacent_movable_tiles != valid_tiles:
                tile_list.extend(list(dict.fromkeys(valid_edge_tiles)))

        tile_list.extend(non_standable_tiles)
        return tile_list

    def get_attack(self, row, col, range):

        tile_list = [self._game_map[row][col]]
        if range == 0:
            return tile_list

        # proceed top if not at border
        if row != 0:
            tile_list.extend(self.get_attack(row - 1, col, range - 1))

        # proceed left if not at border
        if col != 0:
            tile_list.extend(self.get_attack(row, col - 1, range - 1))

        # proceed bottom if not at border
        if row != self.GRID_HEIGHT - 1:
            tile_list.extend(self.get_attack(row + 1, col, range - 1))

        # proceed right if not at border
        if col != self.GRID_WIDTH - 1:
            tile_list.extend(self.get_attack(row, col + 1, range - 1))

        # array syntax flattens and dict.fromKeys removes duplicates
        return list(dict.fromkeys(tile_list))

    def get_movement(self, row, col, num_moves, player=None):

        tile_list = [self._game_map[row][col]]
        if num_moves == 0:
            return tile_list

        # proceed top if not at border, above tile is standable
        if row != 0 and self._game_map[row - 1][col].standable and not self._game_map[row - 1][col].occupied:
            tile_not_player_occupied = (player is not None and self._game_map[row - 1][col] is not player.currentTile)

            if player is None:
                tile_list.extend(self.get_movement(row - 1, col, num_moves - 1))
            elif tile_not_player_occupied:
                tile_list.extend(self.get_movement(row - 1, col, num_moves - 1, player))

        # proceed left if not at border, left tile is standable
        if col != 0 and self._game_map[row][col - 1].standable and not self._game_map[row][col - 1].occupied:
            tile_not_player_occupied = (player is not None and self._game_map[row][col - 1] is not player.currentTile)

            if player is None:
                tile_list.extend(self.get_movement(row, col - 1, num_moves - 1))
            elif tile_not_player_occupied:
                tile_list.extend(self.get_movement(row, col - 1, num_moves - 1, player))

        # proceed bottom if not at border, lower tile is standable
        if row != self.GRID_HEIGHT - 1 and self._game_map[row + 1][col].standable and not self._game_map[row + 1][
            col].occupied:
            tile_not_player_occupied = (player is not None and self._game_map[row + 1][col] is not player.currentTile)

            if player is None:
                tile_list.extend(self.get_movement(row + 1, col, num_moves - 1))
            elif tile_not_player_occupied:
                tile_list.extend(self.get_movement(row + 1, col, num_moves - 1, player))

        # proceed right if not at border, right tile is standable
        if col != self.GRID_WIDTH - 1 and self._game_map[row][col + 1].standable and not self._game_map[row][
            col + 1].occupied:
            tile_not_player_occupied = (player is not None and self._game_map[row][col + 1] is not player.currentTile)

            if player is None:
                tile_list.extend(self.get_movement(row, col + 1, num_moves - 1))
            elif tile_not_player_occupied:
                tile_list.extend(self.get_movement(row, col + 1, num_moves - 1, player))

        # array syntax flattens and dict.fromKeys removes duplicates
        return list(dict.fromkeys(tile_list))

    # Greedy search for a path to a tile
    def path_to(self, start_tile, end_tile, player=None):
        to_visit = [start_tile]
        visited = {start_tile: None}  # Tile maps to its parent tile

        while len(to_visit) != 0:
            current = to_visit.pop(0)

            if current is end_tile:
                tile = current
                solution = []
                while visited[tile] is not None:
                    solution.append(tile)
                    tile = visited[tile]
                solution.append(start_tile)
                solution.reverse()
                return solution
            # get_movement will also return the current tile, so we remove it from edges.
            edges = self.get_movement(current.row, current.col, 1)
            edges.remove(current)

            # We seek edges that are standable and non-occupied
            # Then we check if player has been passed to this function,
            # and if it has, that means this is an enemy, which must avoid
            # the player's current tile.
            for edge in edges:
                if edge.standable and not edge.occupied and edge not in visited:
                    if player is None or edge is not player.currentTile:
                        visited[edge] = current
                        to_visit.append(edge)

    def print_map_data(self):
        # Standable map
        for row in self._game_map:
            for col in row:
                print('O' if col.standable else 'X', end=' ')
            print()

        # Position map
        for row in self._game_map:
            for col in row:
                print('(' + str(col.row) + ',' + str(col.col) + ')' + ('O' if col.standable else 'X'), end=' ')
            print()

    def generate_tile(self, col, row):
        standable = self.__generate_true(self.STANDABLE_TILE_DENSITY_ODDS)
        # we need to calculate the index for the tile value once the string is read from file
        index = col + (row * 25)
        layout = self.map_layout
        map_index = 0

        direction = ''

        if index < 25:
            direction = 'north'
        elif index > 349:
            direction = 'south'
        elif index % 25 == 0:
            direction = 'west'
        elif index % 24 == 0:
            direction = 'east'

        if direction == 'north':
            map_index = 1
        if direction == 'east':
            map_index = 0
        if direction == 'west':
            map_index = 3
        if direction == 'south':
            map_index = 2

        # if the value is 0 (most tiles) randomly generate that tile
        # letters signify that an enemy is to be spawned on the texture type initial "f" or "d" or "g" etc.
        # r means it is a random texture type
        if layout[index] == '0' or layout[index] == 'r' or layout[index] == 'K' or layout[index] == 'R':
            # walls = [self.__generate_true(self.WALL_DENSITY) for x in range(4)]
            if self.__generate_true(.15):
                return Tile(col=col, row=row, standable=True, texture_type=TileTexture.DIRT)
            elif not standable and not layout[index] == 'r':  # check that before creating non-standable tile enemy
                # is not spawned there
                return Tile(col=col, row=row, standable=standable, texture_type=TileTexture.BUSH)
            else:
                return Tile(col=col, row=row, standable=True, texture_type=TileTexture.GRASS)
        # load a texture based on layout
        # grass spawnable tiles
        elif layout[index] == '1' or layout[index] == 'd':
            return Tile(col=col, row=row, standable=True, texture_type=TileTexture.DIRT)
        elif layout[index] == '2' or layout[index] == 'g':
            return Tile(col=col, row=row, standable=True, texture_type=TileTexture.GRASS)
        elif layout[index] == '3' or layout[index] == 'f' or layout[index] == 'G' or layout[index] == 'W':
            return Tile(col=col, row=row, standable=True, texture_type=TileTexture.FLOOR)
        # sand spawnable tiles
        elif layout[index] == '4' or layout[index] == 's':
            return Tile(col=col, row=row, standable=True, texture_type=TileTexture.SAND)
        elif layout[index] == '5' or layout[index] == 'm' or layout[index] == 'A':
            return Tile(col=col, row=row, standable=True, texture_type=TileTexture.MUD)
        # snow spawnable tiles
        elif layout[index] == '6' or layout[index] == 'i':
            return Tile(col=col, row=row, standable=True, texture_type=TileTexture.SNOW)
        elif layout[index] == '7' or layout[index] == 'p':
            return Tile(col=col, row=row, standable=True, texture_type=TileTexture.WOOD)
        # unstandable/unspawnable tiles
        elif layout[index] == 'b':
            return Tile(col=col, row=row, standable=False, texture_type=TileTexture.BUSH)
        elif layout[index] == 'C':
            return Tile(col=col, row=row, standable=False, texture_type=TileTexture.CACTUS)
        elif layout[index] == 'c':
            return Tile(col=col, row=row, standable=False, texture_type=TileTexture.ROCK)
        elif layout[index] == '[':
            return Tile(col=col, row=row, standable=False, texture_type=TileTexture.STONE)
        elif layout[index] == '{':
            return Tile(col=col, row=row, standable=False, texture_type=TileTexture.MUD_BRICK)
        elif layout[index] == '<':
            return Tile(col=col, row=row, standable=False, texture_type=TileTexture.DARK_BRICK)
        # win tiles are as follows, w for grass level, v for sand level, and x for snow level
        elif layout[index] == 'w':
            self.win_tiles[map_index] = Tile(col=col, row=row, standable=True,
                                             texture_type=TileTexture.FLOOR, win_tile=True)
            return self.win_tiles[map_index]
        elif layout[index] == 'x':
            self.win_tiles[map_index] = Tile(col=col, row=row, standable=True,
                                             texture_type=TileTexture.WOOD, win_tile=True)
            return self.win_tiles[map_index]
        elif layout[index] == 'v':
            self.win_tiles[map_index] = Tile(col=col, row=row, standable=True,
                                             texture_type=TileTexture.MUD, win_tile=True)
            return self.win_tiles[map_index]
        else:
            return Tile(col=col, row=row, standable=False, texture_type=TileTexture.BUSH)

    @staticmethod
    def __generate_true(odds):
        return True if random() < odds else False

    # spawns enemies, needs to be called somewhere for new a level so that new enemies are spawned
    def generate_enemies(self, level):
        # spawn 30% knight 70% archer

        layout = self.map_layout
        index = 0
        while index < len(layout):
            if layout[index] == 'r' or layout[index] == 'd' or layout[index] == 'f' or layout[index] == 'g' or \
                    layout[index] == 'K' or layout[index] == 'R' or layout[index] == 'G' or layout[index] == 'A' or \
                    layout[index] == 'W' or layout[index] == 's' or layout[index] == 'm' or layout[index] == 'i' or \
                    layout[index] == 'p':
                # need to translate index into a set of coordinates
                x = index % self.GRID_WIDTH
                y = index // self.GRID_WIDTH
                if layout[index] == 'K':
                    knight = Knight(level)
                    knight.currentTile = self.game_map[y][x]
                    knight.currentTile.occupied = True
                    ENTITIES.append(knight)
                elif layout[index] == 'R':
                    archer = Archer(level)
                    archer.currentTile = self.game_map[y][x]
                    archer.currentTile.occupied = True
                    ENTITIES.append(archer)
                elif layout[index] == 'G':
                    boss = GreatKnight(level)
                    boss.currentTile = self.game_map[y][x]
                    boss.currentTile.occupied = True
                    ENTITIES.append(boss)
                elif layout[index] == 'A':
                    boss = GreatMarksman(level)
                    boss.currentTile = self.game_map[y][x]
                    boss.currentTile.occupied = True
                    ENTITIES.append(boss)
                elif layout[index] == 'W':
                    boss = WizardKing(level)
                    boss.currentTile = self.game_map[y][x]
                    boss.currentTile.occupied = True
                    boss.populate_tiles(boss.height_tiles, boss.width_tiles)
                    ENTITIES.append(boss)
                elif self.__generate_true(.7):  # create archer
                    archer = Archer(level)
                    archer.currentTile = self.game_map[y][x]
                    archer.currentTile.occupied = True
                    ENTITIES.append(archer)
                else:  # create knight
                    knight = Knight(level)
                    knight.currentTile = self.game_map[y][x]
                    knight.currentTile.occupied = True
                    ENTITIES.append(knight)
            index += 1

        # Luke testing
        # boss = GreatKnight(level)
        # boss.currentTile = self.game_map[0][15]
        # boss.currentTile.occupied = True
        # ENTITIES.append(boss)

    # Map index system:
    #    1  2  3  4
    #    o  o  o  o
    # 0  5  6  7  8
    # o  o  o  o  o
    #    9 10 11 12
    #    o  o  o  o

    # function used in init to get path to file names for map layouts
    def update_layout(self, direction='east'):
        if self.map_number == 0:
            self.map_number = 5
        else:
            if direction == 'east':
                self.map_number += 1
            elif direction == 'west':
                self.map_number -= 1
            elif direction == 'north':
                self.map_number -= 4
            elif direction == 'south':
                self.map_number += 4

        self.load_map(self.map_number)

    def load_map(self, level):
        if level == 0:
            self.map_layout = map_0
        elif level == 1:
            self.map_layout = map_1
        elif level == 2:
            self.map_layout = map_2
        elif level == 3:
            self.map_layout = map_3
        elif level == 4:
            self.map_layout = map_4
        elif level == 5:
            self.map_layout = map_5
        elif level == 6:
            self.map_layout = map_6
        elif level == 7:
            self.map_layout = map_7
        elif level == 8:
            self.map_layout = map_8
        elif level == 9:
            self.map_layout = map_9
        elif level == 10:
            self.map_layout = map_10
        elif level == 11:
            self.map_layout = map_11
        elif level == 12:
            self.map_layout = map_12
