from WizardVsWorld.phases.player_movement_phase import *
from WizardVsWorld.classes.user_interface import MessageBox
from WizardVsWorld.classes.attack import CounterAttack, perform_attack


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

    def attack(self, enemy, enemy_tiles):
        perform_attack(self.player, enemy)

        if enemy.health <= 0:
            enemy.currentTile.occupied = False
            ENTITIES.remove(enemy)
            animate_death(enemy)
        elif enemy.health > 0:
            enemy.damaged = False
            attacker = CounterAttack(enemy, self.player, enemy_tiles)
            attacker.attempt_counter_attack()
            time.sleep(.5)

    def attack_enemy_procedure(self, enemy, enemy_tiles):
        if enemy.currentTile is self.enemyTile:
            self.attack(enemy, enemy_tiles)

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
                           + ' while they are in your selector.')
                total_refresh_drawing()

            self.is_tutorial = False

            start_index = len(occupied_enemy_tiles) - 1
            self.data_from_movement.occupied_index = start_index
            row = occupied_enemy_tiles[start_index].row
            col = occupied_enemy_tiles[start_index].col

            self.data_from_movement.select_tile(row, col)
            self.data_from_movement.prev_tile = GRID.game_map[row][col]

            selecting = True
            while selecting:
                if self.data_from_movement.selection():
                    # A less than ideal line, setting our currentTile to the one
                    # found from ENEMY selection, so this is setting the currentTile
                    # as the tile of the chosen ENEMY.

                    self.enemyTile = self.data_from_movement.currentTile
                    self.player.selected = False
                    #draw_entities()
                    selecting = False
        else:
            time.sleep(1)

            # TUTORIAL
            if self.is_tutorial:
                MessageBox('No enemies are close enough to attack. Let\'s pass for now.')
                total_refresh_drawing()

        clear_tinted_tiles(enemy_tiles, self.player)

    def enter(self):
        if not self.data_from_movement.level_complete:
            total_refresh_drawing()  # Attack radius can overwrite text
            self.attack_selection()

    def update(self):
        if not self.data_from_movement.level_complete:
            for enemy in ENTITIES[1:]:
                if enemy.currentTile is self.enemyTile:
                    self.attack_enemy_procedure(enemy, self.data_from_movement.enemy_tiles)
                    break
        else:
            self.data_from_movement.level_complete = False

    def exit(self):
        self.data_from_movement.occupied_index = 0
