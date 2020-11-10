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
        enemy_tiles = GRID.get_attack(self.player_position.row, self.player_position.col, self.Player.range)
        if can_attack(enemy, self.Player):
            # TUTORIAL
            if self.attack_tutorial:
                MessageBox('Now your enemies will have a chance to attack you!')
                self.attack_tutorial = False
                total_refresh_drawing()

            perform_attack(enemy, self.Player)

            if self.Player.health <= 0:
                ENTITIES.remove(self.Player)
                animate_death(self.Player)
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
        else:
            return False

    def enter(self):
        self.Enemies = ENTITIES[1:]
        self.player_position = self.Player.currentTile

    def update(self):
        valid_attackers = 0
        for enemy in self.Enemies:
            if isinstance(enemy, Enemy):
                if self.attack_player_procedure(enemy):
                    valid_attackers += 1
        # TUTORIAL
        if valid_attackers == 0 and self.attack_tutorial:
            MessageBox('Now your enemies get the chance to attack you! Fortunately for you, none are in range!')
            total_refresh_drawing()

    def exit(self):
        self.is_tutorial = False
