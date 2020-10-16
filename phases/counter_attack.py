from draw import *
from classes.tile import Tile
from classes.entity import Entity, Enemy


def remove_enemy_from_tile_list(enemy, enemy_tiles):
    if enemy.health == 0:
        enemy.currentTile.occupied = False
        enemy_tiles.remove(enemy.currentTile)


def can_attack(attacker, victim):
    attackable_tiles = GRID.get_movement(attacker.currentTile.row, attacker.currentTile.col, attacker.range)
    if victim.currentTile in attackable_tiles:
        return True
    else:
        return False


class CounterAttack:
    enemy_tiles: [Tile]
    attacker: Entity
    victim: Entity

    def __init__(self, attacker, victim, enemy_tiles=None):
        self.attacker = attacker
        self.victim = victim
        self.enemy_tiles = enemy_tiles

    def counter_attack(self):
        self.attacker.attacking = True
        animate_attack(self.attacker, self.victim)
        self.attacker.attacking = False
        old_victim_health = self.victim.health
        damage_taken = self.attacker.attack - self.victim.defense
        if damage_taken < 0:
            damage_taken = 0
        self.victim.health -= damage_taken
        self.victim.damaged = True
        animate_damage(self.victim, old_victim_health)

        if isinstance(self.victim, Player):
            print(f"Updated player health: {self.victim.health}")
        else:
            print(f"Updated enemy health: {self.victim.health}")

        if isinstance(self.victim, Enemy):
            enemy = self.victim
            print(f"Enemy died in counter attack!: {self.victim.health}")
            if enemy.health <= 0:
                enemy.health = 0
                remove_enemy_from_tile_list(enemy, self.enemy_tiles)
                ENTITIES.remove(enemy)
                animate_death(enemy)
            else:
                self.victim.damaged = False

        if isinstance(self.victim, Player):
            player = self.victim
            if player.health <= 0:
                player.health = 0
                ENTITIES.remove(player)
                animate_death(player)
                time.sleep(2)
                pygame.quit()
            else:
                self.victim.damaged = False

    def attempt_counter_attack(self):
        time.sleep(1)
        if isinstance(self.attacker, Enemy):
            if can_attack(self.attacker, self.victim):
                print("Ye the knight is goin for it")
                self.counter_attack()
        else:
            self.counter_attack()
