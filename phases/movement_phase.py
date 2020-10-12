import pygame

from classes.phase import Phase
from classes.entity import Player
from classes.tile import Tile
from classes.grid import Grid


class PlayerMovementPhase(Phase):

    player: Player
    currentTile: Tile
    grid : Grid

    def __init__(self, player):
        self._player = player
        self._currentTile = player.currentTile
        self._grid = Grid()

    def selection(self):
        selecting = True
        while selecting:

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        selecting = False

                    row = self.currentTile.row
                    col = self.currentTile.col

                    if event.key == pygame.K_LEFT:
                        if self._grid.is_valid_tile(row, col):
                            self.currentTile = self._grid.game_map[row, col - 1]

                    elif event.key == pygame.K_RIGHT:
                        if self._grid.is_valid_tile(row, col + 1):
                            self.currentTile = self._grid.game_map[row, col + 1]

                    elif event.key == pygame.K_UP:
                        if self._grid.is_valid_tile(row + 1, col):
                            self.currentTile = self._grid.game_map[row + 1, col]

                    elif event.key == pygame.K_DOWN:
                        if self._grid.is_valid_tile(row - 1, col):
                            self.currentTile = self._grid.game_map[row - 1, col]

            print(f"You picked the tile at {self.currentTile}")




    def enter(self):
        self.selection()
        print('Entering Player Movement Phase...')

    def update(self):
        print('Main Functions of Phase 1...')

    def exit(self):
        print('Exiting Phase 1...')

