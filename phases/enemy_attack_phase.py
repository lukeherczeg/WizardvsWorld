from classes.tile import Tile
from classes.entity import Enemy, Entity
from draw import *
from classes.phase import Phase
from phases.counter_attack import *
from phases.counter_attack import CounterAttack


class EnemyAICombatPhase(Phase):
    player_position: Tile
    Player: Player
    Enemies: [Entity]
    grid: Grid

    def __init__(self):
        self.Enemies = ENTITIES
        self.player_position = ENTITIES[0].get_position()
        self.Player = ENTITIES[0]
        self.grid = GRID

    def enter(self):
        self.player_position = ENTITIES[0].currentTile
        for enemy in self.Enemies:
            if isinstance(enemy, Enemy):
                if enemy.health > 0:
                    self.attack_player_procedure(enemy)

    def attack_player_procedure(self, enemy):
        enemy_tiles = GRID.get_attack(self.player_position.row, self.player_position.col, self.Player.range)
        time.sleep(0.25)
        if self.can_enemy_attack(enemy, enemy.range):
            enemy.attacking = True
            print("Player Health A ", end="")
            print(self.Player.health)
            animate_attack(enemy, self.Player)
            enemy.attacking = False
            player_health_old = self.Player.health
            damage_taken = enemy.attack - self.Player.defense
            if damage_taken < 0:
                damage_taken = 0
            self.Player.health -= damage_taken
            animate_damage(self.Player, player_health_old)

            print("Player Health B ", end="")
            counter_attack = CounterAttack(self.Player, enemy, enemy_tiles)
            counter_attack.enter()
            print(self.Player.health)

    def can_enemy_attack(self, enemy, fight_range):
        p1 = [self.player_position.row, self.player_position.col]
        p2 = [enemy.currentTile.row, enemy.currentTile.col]
        distance1 = int(math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)))
        if distance1 <= fight_range:
            return True
        else:
            return False

    def update(self):
        print('Entering Enemy Attack Computation / Animation...')

    def exit(self):
        print('Exiting Player Phase...')
