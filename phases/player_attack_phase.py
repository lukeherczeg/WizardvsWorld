from draw import *
from classes.phase import Phase
from classes.entity import Player
from classes.tile import Tile


def select(row, col):
    print(f"Highlighting ({row}, {col}).")
    draw_selected_tile(GRID.game_map[row][col])


class PlayerAttackPhase(Phase):
    player: Player
    currentTile: Tile
    grid: Grid

    def __init__(self, player):
        self.player = player
        self.currentTile = player.currentTile
        self.grid = GRID

    def enter(self):
        print('Entering Attack Selection...')

    def update(self):
        print('Entering Attack Computation / Animation...')

    def exit(self):
        print('Exiting Player Phase...')
