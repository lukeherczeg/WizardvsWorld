from classes.tile import Tile, TextureType
from random import random
import os #importing for reading maps inside of /maps

LEVEL = 0

class Grid:
    STANDABLE_TILE_DENSITY_ODDS: float = 0.98

    def __init__(self, width, height, map_layout=None):
        self.GRID_WIDTH = width
        self.GRID_HEIGHT = height
        if map_layout is None:
            self.map_layout = self.update_layout(LEVEL)
        else:
            self.map_layout = map_layout
        # INDEX WITH [ROW][COL]
        self._game_map = [[self.__generate_tile(x, y) for x in range(self.GRID_WIDTH)] for y in range(self.GRID_HEIGHT)]

    @property
    def game_map(self):
        return self._game_map

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

            row = tile.row - 1
            col = tile.col

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

            row = tile.row
            col = tile.col + 1

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

            row = tile.row
            col = tile.col - 1

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

            # If the counters are different, we have an edge!
            if adjacent_movable_tiles != valid_tiles:
                tile_list.extend(list(dict.fromkeys(valid_edge_tiles)))

        tile_list.extend(non_standable_tiles)
        return tile_list

    def get_attack(self, row, col, num_moves):

        tile_list = [self._game_map[row][col]]
        if num_moves == 0:
            return tile_list

        # proceed top if not at border
        if row != 0:
            tile_list.extend(self.get_attack(row - 1, col, num_moves - 1))

        # proceed left if not at border
        if col != 0:
            tile_list.extend(self.get_attack(row, col - 1, num_moves - 1))

        # proceed bottom if not at border
        if row != self.GRID_HEIGHT - 1:
            tile_list.extend(self.get_attack(row + 1, col, num_moves - 1))

        # proceed right if not at border
        if col != self.GRID_WIDTH - 1:
            tile_list.extend(self.get_attack(row, col + 1, num_moves - 1))

        # array syntax flattens and dict.fromKeys removes duplicates
        return list(dict.fromkeys(tile_list))

    def get_movement(self, row, col, num_moves):

        tile_list = [self._game_map[row][col]]
        if num_moves == 0:
            return tile_list

        # proceed top if not at border, above tile is standable
        if row != 0 and self._game_map[row - 1][col].standable:
            tile_list.extend(self.get_movement(row - 1, col, num_moves - 1))

        # proceed left if not at border, left tile is standable
        if col != 0 and self._game_map[row][col - 1].standable:
            tile_list.extend(self.get_movement(row, col - 1, num_moves - 1))

        # proceed bottom if not at border, lower tile is standable
        if row != self.GRID_HEIGHT - 1 and self._game_map[row + 1][col].standable:
            tile_list.extend(self.get_movement(row + 1, col, num_moves - 1))

        # proceed right if not at border, right tile is standable
        if col != self.GRID_WIDTH - 1 and self._game_map[row][col + 1].standable:
            tile_list.extend(self.get_movement(row, col + 1, num_moves - 1))

        # array syntax flattens and dict.fromKeys removes duplicates
        return list(dict.fromkeys(tile_list))

    # Greedy search for a path to a tile
    def path_to(self, start_tile, end_tile):
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

            edges = self.get_movement(current.row, current.col, 1)
            for edge in edges:
                if edge not in visited:
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

    def __generate_tile(self, col, row):
        standable = self.__generate_true(self.STANDABLE_TILE_DENSITY_ODDS)
        #we need to calculate the index for the tile value once the string is read from file
        index = col + (row * 25)
        layout = self.map_layout
        #if the value is 0 (most tiles) randomly generate that tile
        if layout[index] == '0':
            # walls = [self.__generate_true(self.WALL_DENSITY) for x in range(4)]
            if standable:
                if self.__generate_true(.7):
                    return Tile(col=col, row=row, standable=standable, texture_type=TextureType.GRASS)
                else:
                    return Tile(col=col, row=row, standable=standable, texture_type=TextureType.DIRT)
            else:
                return Tile(col=col, row=row, standable=standable, texture_type=TextureType.STONE)
        elif layout[index] == '1':
            return Tile(col=col, row=row, standable=True, texture_type=TextureType.DIRT)
        elif layout[index] == '2':
            return Tile(col=col, row=row, standable=False, texture_type=TextureType.STONE)
        elif layout[index] == '3':
            return Tile(col=col, row=row, standable=True, texture_type=TextureType.FLOOR)
        else:
            return Tile(col=col, row=row, standable=True, texture_type=TextureType.GRASS)

    @staticmethod
    def __generate_true(odds):
        return True if random() < odds else False

    #function used in init to get path to file names for map layouts
    def update_layout(self, level):
        lev = str(level)
        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'maps')
        map = os.path.join(asset_path, 'map')
        map += lev
        map += '.txt'
        with open(map, 'r') as file:
            string = file.read().replace('\n', '')
            self.map_layout = string
        return string

