from phases.player_movement_phase import *
import time
from classes.entity import Enemy
from phases.counter_attack import CounterAttack, remove_enemy_from_tile


class PlayerAttackPhase(Phase):
    player: Player
    currentTile: Tile
    grid: Grid
    data_from_movement: PlayerMovementPhase
    counter_attack: CounterAttack

    def __init__(self, player, data_from_movement=None):
        self.player = player
        self.currentTile = player.currentTile
        self.grid = GRID
        self.data_from_movement = data_from_movement

    def attack_enemy_procedure(self, enemy, enemy_tiles):
        if enemy.currentTile is self.data_from_movement.currentTile:
            print("Enemy Before attack", end=" ")
            print(enemy.health)
            damage_taken = self.player.attack - enemy.defense
            if damage_taken < 0:
                damage_taken = 0
            enemy.health -= damage_taken
            animate_attack(self.player, enemy)
            if enemy.health < 0:
                enemy.health = 0
                remove_enemy_from_tile(enemy_tiles)
                ENTITIES.remove(enemy)
            elif enemy.health > 0:
                print("Enemy Health after attack", end=" ")
                print(enemy.health)
                counter_attack = CounterAttack(enemy, self.player)
                counter_attack.enter()

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
            self.data_from_movement.select_tile(occupied_enemy_tiles[start_index].row,
                                                occupied_enemy_tiles[start_index].col)
            selecting = True
            while selecting:
                if self.data_from_movement.selection():
                    # print(
                    #     f"You picked the attackable tile ({self.data_from_movement.currentTile.row}, "
                    #     f"{self.data_from_movement.currentTile.col})!"
                    #     f" Time to attack!")
                    for enemy in ENTITIES:
                        if isinstance(enemy, Enemy):
                            self.attack_enemy_procedure(enemy, enemy_tiles)

                    self.player.selected = False
                    draw_entities()
                    selecting = False
        else:
            time.sleep(1)
            # print(f"No enemies within range, back to selection!")

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
