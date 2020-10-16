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
    attacker: Entity
    victim: Entity

    def __init__(self, attacker, victim, enemy_tiles=None):
        self.attacker = attacker
        self.victim = victim
        self.enemy_tiles = enemy_tiles

    def can_attack(self):
        p1 = [self.attacker.currentTile.row, self.attacker.currentTile.col]
        p2 = [self.victim.currentTile.row, self.victim.currentTile.col]
        distance1 = int(math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)))
        if distance1 <= self.attacker.range:
            return True
        else:
            return False

    def counter_attack(self):
        time.sleep(1)
        print("victim health", end=" ")
        print(self.victim.health)
        self.attacker.attacking = True
        animate_attack(self.attacker, self.victim)
        self.attacker.attacking = False
        old_victim_health = self.victim.health
        damage_taken = self.attacker.attack - self.victim.defense
        if damage_taken < 0:
            damage_taken = 0
        self.victim.health -= damage_taken
        animate_damage(self.victim, old_victim_health)

        if isinstance(self.victim, Enemy):
            if self.victim.health <= 0:
                self.victim.health = 0
                remove_enemy_from_tile(self.enemy_tiles)
                ENTITIES.remove(self.victim)

        print("attacker health after", end=" ")
        print(self.victim.health)

    def enter(self):
        self.counter_attack()
