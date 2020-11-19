from WizardVsWorld.phases.player_movement_phase import *
from WizardVsWorld.classes.user_interface import MessageBox, SpellMenu
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
        # If the enemy isn't a boss, or if it is but it only occupies one tile
        is_boss = isinstance(enemy, Boss)
        if not is_boss or (is_boss and isinstance(enemy.tiles, Tile)):
            if enemy.currentTile is self.enemyTile:
                self.attack(enemy, enemy_tiles)
        elif is_boss:
            for tile in enemy.tiles:
                if tile is self.enemyTile:
                    self.attack(enemy, enemy_tiles)

    def attack_selection(self, spell):
        enemy_tiles = GRID.get_attack(self.player.currentTile.row, self.player.currentTile.col, spell.range)

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
            self.data_from_movement.select_tile(occupied_enemy_tiles[start_index].row,
                                                occupied_enemy_tiles[start_index].col)
            selecting = True
            while selecting:
                if self.data_from_movement.selection():
                    # A less than ideal line, setting our currentTile to the one
                    # found from ENEMY selection, so this is setting the currentTile
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

        draw_tinted_tiles(enemy_tiles, self.player, TileTint.NONE)

    # Spells that cast on self don't need to target
    def cast_on_self(self, spell):
        # Cast only on player
        if spell.aoe == 0:
            self.player.decrease_health(spell)
        else:
            pass

    def enter(self):
        if not self.data_from_movement.level_complete:
            # Attack radius can overwrite text
            total_refresh_drawing()

            # Select a spell
            spell_menu = SpellMenu(self.player.spellbook)
            spell_number = spell_menu.await_response()
            chosen_spell = self.player.spellbook[spell_number]

            # These are spells player casts on self (e.g. Heal)
            if chosen_spell.range == 0:
                self.cast_on_self(chosen_spell)
            # These are spells that need to target (e.g. Greater Fireball)
            else:
                self.attack_selection(chosen_spell)

    def update(self):
        if not self.data_from_movement.level_complete:
            for enemy in ENTITIES:
                if enemy.currentTile is self.enemyTile:
                    self.attack_enemy_procedure(enemy, self.data_from_movement.enemy_tiles)
                    break
        else:
            self.data_from_movement.level_complete = False

    def exit(self):
        self.data_from_movement.occupied_index = 0
