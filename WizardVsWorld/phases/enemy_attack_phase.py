from WizardVsWorld.classes.phase import Phase
from WizardVsWorld.classes.attack import *
from WizardVsWorld.classes.user_interface import MessageBox


class EnemyAICombatPhase(Phase):
    player_position: Tile
    Player: Player
    Enemies: [Entity]
    grid: Grid

    def __init__(self):
        self.Enemies = ENTITIES[1:]
        self.Player = ENTITIES[0]
        self.player_position = self.Player.get_position()
        self.grid = GRID
        self.is_tutorial = True
        self.attack_tutorial = True
        self.counter_tutorial = True

    def attack_player_procedure(self, enemy):
        self.Player.healing = False
        attacked = False
        enemy_tiles = GRID.get_attack(self.player_position.row, self.player_position.col, self.Player.range)
        if can_attack(enemy, self.Player) and isinstance(enemy, GreatKnight):
            attacked = True
            randomizer = randint(1, 50)
            if self.Player.health < self.Player.max_health / 4 and randomizer > 25:
                old_attack = enemy.attack
                enemy.attack += 10
                perform_attack(enemy, self.Player)
                enemy.attack = old_attack
            else:
                perform_attack(enemy, self.Player)

        elif can_attack(enemy, self.Player) and isinstance(enemy, WizardKing):
            attacked = True
            randomizer = randint(1, 50)
            if randomizer > 40:
                enemy.prepared_spell = enemy.spellbook[3]
                cast_spell(enemy, enemy)
            elif randomizer > 30:
                enemy.prepared_spell = enemy.spellbook[2]
                cast_spell(enemy, self.Player)
            else:
                enemy.prepared_spell = enemy.spellbook[0]
                cast_spell(enemy, self.Player)

        elif can_attack(enemy, self.Player) and isinstance(enemy, GreatMarksman):
            attacked = True
            randomizer = randint(1, 50)
            # Piercing shot
            if self.Player.health < self.Player.max_health // 2 and randomizer > 10:
                old_defense = self.Player.defense
                self.Player.defense = 0
                perform_attack(enemy, self.Player)
                self.Player.defense = old_defense
            # Fire arrow
            elif randomizer > 40:
                old_attack = self.Player.attack
                self.Player.attack += 20
                perform_attack(enemy, self.Player)
                self.Player.attack = old_attack
            else:
                perform_attack(enemy, self.Player)

        elif can_attack(enemy, self.Player):
            attacked = True
            # TUTORIAL
            if self.attack_tutorial:
                MessageBox('Now your enemies will have a chance to attack you!')
                self.attack_tutorial = False
                total_refresh_drawing()

            perform_attack(enemy, self.Player)

        if attacked:
            if self.Player.health <= 0:
                MessageBox('You died. But that\'s okay! It looks like the Grand Magus still has plans for you...')
                pygame.quit()
                sys.exit()
            elif self.Player.health > 0:
                self.Player.damaged = False
                attacker = CounterAttack(self.Player, enemy, enemy_tiles)
                if self.counter_tutorial:
                    MessageBox('After being attacked, any unit within range will perform a counterattack!')
                    total_refresh_drawing()
                    self.counter_tutorial = False
                attacker.attempt_counter_attack()
            return True

        return False

    def enter(self):
        self.Enemies = ENTITIES[1:]
        self.player_position = self.Player.currentTile

    def update(self):
        valid_attackers = 0
        for enemy in self.Enemies:
            #This is checking if some enemies were deleted form the entities array but not from enemies
            if isinstance(enemy, Enemy) and not enemy.health <= 0:
                if self.attack_player_procedure(enemy):
                    valid_attackers += 1
        # TUTORIAL
        if valid_attackers == 0 and self.attack_tutorial:
            MessageBox('Now your enemies get the chance to attack you! Fortunately for you, none are in range!')
            total_refresh_drawing()

    def exit(self):
        self.is_tutorial = False
