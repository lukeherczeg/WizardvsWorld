from classes.tile import Tile
from random import random


class Grid:
    STANDABLE_TILE_DENSITY_ODDS: float = 0.98

    def __init__(self, width, height):
        self.GRID_WIDTH = width
        self.GRID_HEIGHT = height


        # INDEX WITH [ROW][COL]
        self._game_map = [[self.__generate_tile(x, y) for x in range(self.GRID_WIDTH)] for y in range(self.GRID_HEIGHT)]

    @property
    def game_map(self):
        return self._game_map

    def is_valid_tile(self, row, col):
        if 0 <= row < self.GRID_HEIGHT and 0 <= col < self.GRID_WIDTH and self.game_map[row][col].standable:
            return True
        else:
            return False

    def get_movement(self, row, col, num_moves):

        tile_list = [self._game_map[row][col]]
        if num_moves == 0:
            return tile_list

        # #proceed top if not at border, above tile is standable, and no wall in the way
        # if(row != 0 and self._game_map[row-1][col].standable and not self._game_map[row][col].walls[0] and not self._game_map[row-1][col].walls[2]):
        #   tile_list.extend(self.get_movement(row-1, col, num_moves-1))

        # #proceed left if not at border, left tile is standable, and no wall in the way
        # if(col != 0 and self._game_map[row][col-1].standable and not self._game_map[row][col].walls[1] and not self._game_map[row][col-1].walls[3]):
        #   tile_list.extend(self.get_movement(row, col-1, num_moves-1))

        # #proceed bottom if not at border, lower tile is standable, and no wall in the way
        # if(row != self.GRID_SIZE-1 and self._game_map[row+1][col].standable and not self._game_map[row][col].walls[2] and not self._game_map[row+1][col].walls[0]):
        #   tile_list.extend(self.get_movement(row+1, col, num_moves-1))

        # #proceed right if not at border, right tile is standable, and no wall in the way
        # if(col != self.GRID_SIZE-1 and self._game_map[row][col+1].standable and not self._game_map[row][col].walls[3] and not self._game_map[row][col+1].walls[1]):
        #   tile_list.extend(self.get_movement(row, col+1, num_moves-1))

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

    def print_map_data(self):
        # Standable map
        for row in self._game_map:
            for col in row:
                print('O' if col.standable else 'X', end=' ')
            print()

        # Wall map
        # for row in self._game_map:
        #   for col in row:
        #     print('|' if col.walls[1] else ' ', end = '')
        #     print('=' if col.walls[0] and col.walls[2] else '-' if col.walls[0] else '_' if col.walls[2] else ' ', end = '')
        #     print('|' if col.walls[3] else ' ', end = '')
        #   print()

        # Position map
        for row in self._game_map:
            for col in row:
                print('(' + str(col.row) + ',' + str(col.col) + ')' + ('O' if col.standable else 'X'), end=' ')
            print()

    def __generate_tile(self, col, row):
        # walls = [self.__generate_true(self.WALL_DENSITY) for x in range(4)]
        return Tile(col=col, row=row, standable=self.__generate_true(self.STANDABLE_TILE_DENSITY_ODDS))

    @staticmethod
    def __generate_true(odds):
        return True if random() < odds else False
