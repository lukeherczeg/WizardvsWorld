from phases.player_movement_phase import *
import time


class PlayerAttackPhase(Phase):
    player: Player
    currentTile: Tile
    grid: Grid
    data_from_movement: PlayerMovementPhase

    def __init__(self, player, data_from_movement):
        self.player = player
        self.currentTile = player.currentTile
        self.grid = GRID
        self.data_from_movement = data_from_movement

    def attack_selection(self):
        # possible_enemy_tiles = GRID.get_movement_border(self.movement_data.immovable_tiles, self.player.range)

        enemy_tiles = GRID.get_attack(self.currentTile.row, self.currentTile.col, self.player.range)
        self.data_from_movement.enemy_tiles = enemy_tiles

        # possible_enemy_tiles.extend(self.movement_data.immovable_tiles)
        enemies_within_range = 0
        occupied_enemy_tiles = []
        for tile in enemy_tiles:
            if tile.occupied:
                occupied_enemy_tiles.append(tile)
                enemies_within_range += 1

        draw_tinted_tiles(enemy_tiles, self.player, TileTint.ORANGE)

        if enemies_within_range != 0:
            start_index = len(occupied_enemy_tiles) - 1
            self.data_from_movement.occupied_index = start_index
            self.data_from_movement.select_tile(occupied_enemy_tiles[start_index].row, occupied_enemy_tiles[start_index].col)
            selecting = True
            while selecting:
                if self.data_from_movement.selection():
                    print(
                        f"You picked the attackable tile ({self.player.currentTile.row}, {self.player.currentTile.col})!"
                        f" Time to attack!")
                    self.player.selected = False
                    draw_entities()
                    selecting = False
        else:
            time.sleep(1)
            print(f"No enemies within range, back to selection!")

        draw_tinted_tiles(enemy_tiles, self.player, TileTint.NONE)

    def enter(self):
        self.currentTile = self.player.currentTile
        print('Entering Attack Selection...')
        self.attack_selection()

    def update(self):
        print('Entering Attack Computation / Animation...')

    def exit(self):
        self.data_from_movement.occupied_index = 0
        print('Exiting Player Phase...')
