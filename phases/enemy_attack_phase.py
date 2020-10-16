from classes.tile import Tile
from classes.entity import Player, Enemy, Entity
from draw import *
from classes.phase import Phase
from classes.user_interface import MessageBox


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
        self.is_tutorial = True

    def enter(self):
        self.player_position = ENTITIES[0].currentTile

        # TUTORIAL
        if self.is_tutorial:
            MessageBox('Now your enemies will have a chance to attack you!')
            total_refresh_drawing()

        for enemy in self.Enemies:
            if isinstance(enemy, Enemy):
                if enemy.health > 0:
                    self.attack_player_procedure(enemy)

    def attack_player_procedure(self, enemy):
        if self.can_enemy_attack(enemy, enemy.range):
            print("The Player had " + str(self.Player.health) + " before the enemy attacked")
            damage_taken = enemy.attack - self.Player.defense
            if damage_taken < 0:
                damage_taken = 0
            self.Player.health -= damage_taken
            print("The Player had " + str(self.Player.health) + " after the enemy attacked")

    def can_enemy_attack(self, enemy, fight_range):

        p1 = [self.player_position.row, self.player_position.col]
        p2 = [enemy.currentTile.row, enemy.currentTile.col]
        distance1 = int(math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)))
        if distance1 <= fight_range:
            return True
        else:
            return False

    def update(self):
        print('Entering Attack Computation / Animation...')

    def exit(self):
        self.is_tutorial = False
