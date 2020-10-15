from phases.player_movement_phase import *


class PlayerAttackPhase(Phase):
    player: Player
    currentTile: Tile
    grid: Grid
    movement_data: PlayerMovementPhase

    def __init__(self, player, movement_data):
        self.player = player
        self.currentTile = player.currentTile
        self.grid = GRID
        self.movement_data = movement_data

    def enter(self):
        self.currentTile = self.player.currentTile
        print('Entering Attack Selection...')
        #possible_enemy_tiles = GRID.get_movement_border(self.movement_data.immovable_tiles, self.player.range)

        enemy_tiles = GRID.get_attack(self.currentTile.row, self.currentTile.col, self.player.range)

        #possible_enemy_tiles.extend(self.movement_data.immovable_tiles)

        # for tile in possible_enemy_tiles:
        #     if tile.occupied:
        #         enemy_tiles.append(tile)

        draw_tinted_tiles(enemy_tiles, self.player, TileTint.ORANGE)

    def update(self):
        print('Entering Attack Computation / Animation...')

    def exit(self):
        print('Exiting Player Phase...')
