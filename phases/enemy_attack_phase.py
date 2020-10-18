from classes.phase import Phase
from classes.attack import *
from classes.user_interface import MessageBox


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

    def attack_player_procedure(self, enemy):
        enemy_tiles = GRID.get_attack(self.player_position.row, self.player_position.col, self.Player.range)
        if can_attack(enemy, self.Player):
            time.sleep(0.25)

            perform_attack(enemy, self.Player)

            if self.Player.health <= 0:
                ENTITIES.remove(self.Player)
                animate_death(self.Player)
                time.sleep(2)
                pygame.quit()
                sys.exit()
            elif self.Player.health > 0:
                self.Player.damaged = False
                attacker = CounterAttack(self.Player, enemy, enemy_tiles)
                attacker.attempt_counter_attack()

    def enter(self):
        self.Enemies = ENTITIES[1:]
        #draw_text_abs('Enemy Attack', 72, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        #pygame.time.delay(2000)
        self.player_position = self.Player.currentTile

        # TUTORIAL
        if self.is_tutorial:
            MessageBox('Now your enemies will have a chance to attack you!')
            total_refresh_drawing()

    def update(self):
        print('Entering Enemy Attack Computation')
        for enemy in self.Enemies:
            if isinstance(enemy, Enemy):
                self.attack_player_procedure(enemy)

    def exit(self):
        print('Exiting Enemy Phase...')
        self.is_tutorial = False
