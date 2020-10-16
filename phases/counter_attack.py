from draw import *
from classes.tile import Tile
from classes.entity import Entity, Enemy


def remove_enemy_from_tile(enemy_tiles):
    for enemy in ENTITIES:
        for tile in enemy_tiles:
            if enemy.currentTile is tile:
                if enemy.health == 0:
                    tile.occupied = False
                    enemy_tiles.remove(tile)


class CounterAttack:
    enemy_tiles: [Tile]
    entity1: Entity
    entity2: Entity

    def __init__(self, entity1, entity2, enemy_tiles=None):
        self.entity1 = entity1
        self.entity2 = entity2
        self.enemy_tiles = enemy_tiles

    def can_attack(self):
        p1 = [self.entity1.currentTile.row, self.entity1.currentTile.col]
        p2 = [self.entity2.currentTile.row, self.entity2.currentTile.col]
        distance1 = int(math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)))
        if distance1 <= self.entity1.range:
            return True
        else:
            return False

    def counter_attack(self):
        print("Entity2 health", end=" ")
        print(self.entity2.health)
        damage_taken = self.entity1.attack - self.entity2.defense
        if damage_taken < 0:
            damage_taken = 0
        self.entity2.health -= damage_taken
        if isinstance(self.entity2, Enemy):
            self.entity2.health = 0
            remove_enemy_from_tile(self.enemy_tiles)
            ENTITIES.remove(self.entity2)

        print("Entity1 health after", end=" ")
        print(self.entity2.health)

    def enter(self):
        self.counter_attack()
