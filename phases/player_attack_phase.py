from phases.player_movement_phase import *
from classes.user_interface import MessageBox
import time
from classes.entity import Enemy
from phases.counter_attack import CounterAttack, remove_enemy_from_tile_list


class PlayerAttackPhase(Phase):
    player: Player
    currentTile: Tile
    grid: Grid
    data_from_movement: PlayerMovementPhase
    counter_attack: CounterAttack

    def __init__(self, player, data_from_movement=None):
        self.player = player
        self.enemyTile = None
        self.grid = GRID
        self.data_from_movement = data_from_movement
        self.is_tutorial = True

    def attack_enemy_procedure(self, enemy, enemy_tiles):
        if enemy.currentTile is self.enemyTile:
            print(f"Enemy has been attacked!\nInitial enemy health: {enemy.health}")
            damage_taken = self.player.attack - enemy.defense
            self.player.attacking = True
            animate_attack(self.player, enemy)
            self.player.attacking = False
            enemy_health_old = enemy.health
            if damage_taken < 0:
                damage_taken = 0
            enemy.health -= damage_taken

            if isinstance(enemy, Archer):
                if enemy.health / ARCHER_HEALTH <= .2:
                    enemy.damaged = True
            elif isinstance(enemy, Knight):
                if enemy.health / KNIGHT_HEALTH <= .2:
                    enemy.damaged = True

            animate_damage(enemy, enemy_health_old)
            print(f"Updated enemy health: {enemy.health}")

            if enemy.health <= 20:
                enemy.damaged = True

            if enemy.health <= 0:
                enemy.health = 0
                remove_enemy_from_tile_list(enemy, enemy_tiles)
                print("Enemy died!")
                ENTITIES.remove(enemy)
                animate_death(enemy)
            elif enemy.health > 0:
                attacker = CounterAttack(enemy, self.player, enemy_tiles)
                attacker.attempt_counter_attack()

    def attack_selection(self):
        enemy_tiles = GRID.get_attack(self.player.currentTile.row, self.player.currentTile.col, self.player.range)

        self.data_from_movement.enemy_tiles = enemy_tiles

        enemies_within_range = 0
        occupied_enemy_tiles = []
        for tile in enemy_tiles:
            if tile.occupied:
                occupied_enemy_tiles.append(tile)
                enemies_within_range += 1

        draw_tinted_tiles(enemy_tiles, self.player, TileTint.ORANGE)

        if enemies_within_range != 0:

            # TUTORIAL
            if self.is_tutorial:
                MessageBox('Uh oh, enemies are close! Select one of the enemies within range by pressing ENTER'
                                     + ' while they are in your cursor.')
                total_refresh_drawing()


            start_index = len(occupied_enemy_tiles) - 1
            self.data_from_movement.occupied_index = start_index
            self.data_from_movement.select_tile(occupied_enemy_tiles[start_index].row,
                                                occupied_enemy_tiles[start_index].col)
            selecting = True
            while selecting:
                if self.data_from_movement.selection():
                    print(
                        f"You picked the attackable tile ({self.data_from_movement.currentTile.row}, "
                        f"{self.data_from_movement.currentTile.col})!"
                        f" Time to attack!")

                    # A less than ideal line, setting our currentTile to the one
                    # found from ENEMY selection, so this is setting the currenTile
                    # as the tile of the chosen ENEMY.

                    self.enemyTile = self.data_from_movement.currentTile
                    self.player.selected = False
                    draw_entities()
                    selecting = False
        else:
            time.sleep(1)

            # TUTORIAL
            if self.is_tutorial:
                MessageBox('No enemies are close enough to attack. Let\'s pass for now.')
                total_refresh_drawing()

            print(f"No enemies within range, back to selection!")

        draw_tinted_tiles(enemy_tiles, self.player, TileTint.NONE)

    def enter(self):
        print('Entering Attack Selection...')
        self.attack_selection()

    def update(self):
        print('Entering Player Attack Computation...')
        for enemy in ENTITIES:
            if enemy.currentTile is self.enemyTile:
                self.attack_enemy_procedure(enemy, self.data_from_movement.enemy_tiles)
                break

    def exit(self):
        self.data_from_movement.occupied_index = 0
        self.is_tutorial = False
        print('Exiting Player Phase...')
