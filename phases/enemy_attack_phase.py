from classes.phase import Phase
from phases.counter_attack import *
from phases.counter_attack import CounterAttack
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
        attacker = CounterAttack(self.Player, enemy, enemy_tiles)
        time.sleep(0.25)
        if can_attack(enemy, self.Player):
            enemy.attacking = True
            print(f"Player has been attacked!\nInitial player health: {self.Player.health}")
            animate_attack(enemy, self.Player)
            enemy.attacking = False
            player_health_old = self.Player.health
            damage_taken = enemy.attack - self.Player.defense
            if damage_taken < 0:
                damage_taken = 0
            self.Player.health -= damage_taken

            if self.Player.health / PLAYER_HEALTH <= .8:
                self.Player.damaged = True

            animate_damage(self.Player, player_health_old)
            print(f"Updated player health: {self.Player.health}")

            if self.Player.health <= 0:
                self.Player.health = 0
                ENTITIES.remove(self.Player.health)
                animate_death(self.Player.health)
                time.sleep(2)
                pygame.quit()
            elif self.Player.health > 0:
                attacker.attempt_counter_attack()

    def enter(self):
        self.Enemies = ENTITIES[1:]
        print('Entering Enemy Attack Selection')
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
