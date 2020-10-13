from classes.tile import Tile
from classes.entity import Entity


class EnemyAI:
    playerPosition: Tile
    currentPosition: Tile
    Player: Entity
    Enemy: Entity

    def __init__(self, wizard, soldier):
        self.playerPosition = wizard.getPosition()
        self.currentPosition = soldier.getPosition()
        self.Player = wizard
        self.Enemy = soldier

    def enemy_ai(self):
        if self.can_enemy_attack(self.Enemy.range):
            print("The Player had " + str(self.Player.health) + " before the enemy attacked")
            damage_taken = self.Enemy.attack - self.Player.defense
            if damage_taken < 0:
                damage_taken = 0
            self.Player.health -= damage_taken
            print("The Player had " + str(self.Player.health) + " after the enemy attacked")

    def can_enemy_attack(self, fight_range):
        print("The player position is currently col: " + str(self.playerPosition.col)
              + " row: " + str(self.playerPosition.row))
        print("The Enemy position is currently col: " + str(self.currentPosition.col)
              + " row " + str(self.currentPosition.row))

        if abs(self.playerPosition.row - self.currentPosition.row) <= fight_range or abs(
                self.playerPosition.col - self.currentPosition.col) <= fight_range:
            print("Enemy can attack!")
            return True
        else:
            return False
