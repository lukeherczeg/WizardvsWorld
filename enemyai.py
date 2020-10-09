
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

    def enemyAI(self):
        if self.canEnemyAttack(self.Enemy.range):
            print("The Player had " + str(self.Player.health) + " before the enemy attacked")
            damageTaken = self.Enemy.attack - self.Player.defense
            if damageTaken < 0:
                damageTaken = 0
            self.Player.health -= damageTaken
            print("The Player had " + str(self.Player.health) + " after the enemy attacked")

    def canEnemyAttack(self, fightRange):
        print("The player position is currently col: " + str(self.playerPosition.row) + " row: " + str(self.playerPosition.row))
        print("The Enemy position is currently col: " + str(self.currentPosition.col) + " row " + str(self.currentPosition.row))

        if abs(self.playerPosition.row - self.currentPosition.row) <= fightRange or abs(
                self.playerPosition.col - self.currentPosition.col) <= fightRange:
            print("Enemy can attack!")
            return True
        else:
            return False
