from classes.tile import Tile
from classes.entity import Player, Enemy, Entity
from draw import *
from classes.phase import Phase


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
        print("The player position is currently col: " + str(self.player_position.col)
              + " row: " + str(self.player_position.row))
        print("The Enemy position is currently col: " + str(enemy.currentTile.col)
              + " row " + str(enemy.currentTile.row))

        if abs(self.player_position.row - enemy.currentTile.row) <= fight_range or abs(
                self.player_position.col - enemy.currentTile.col) <= fight_range:
            print("Enemy can attack!")
            return True
        else:
            return False

    def update(self):
        print('Entering Attack Computation / Animation...')

    def exit(self):
        print('Exiting Player Phase...')
