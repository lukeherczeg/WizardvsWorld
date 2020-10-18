from const import CRIT_MULTIPLIER
from draw import *
from classes.tile import Tile
from classes.entity import Entity, Enemy
from random import randint
from math import ceil


def can_attack(attacker, victim):
    attackable_tiles = GRID.get_movement(attacker.currentTile.row, attacker.currentTile.col, attacker.range)
    if victim.currentTile in attackable_tiles:
        return True
    else:
        return False


def perform_attack(attacker, victim):
    attacker.attacking = True
    animate_attack(attacker, victim)
    attacker.attacking = False

    damage_taken = calculate_damage(attacker, victim)
    if damage_taken < 0:
        damage_taken = 0

    health_before_attack = victim.health
    victim.health -= damage_taken
    victim.damaged = True

    if victim.health == 0:
        # Makes the health bar animation better :)
        victim.health = victim.health - 10

    animate_damage(victim, health_before_attack)


def calculate_damage(attacker, victim):
    chance = randint(0, 100)
    if chance <= attacker.critical_chance:
        return ceil((attacker.attack * CRIT_MULTIPLIER)) - victim.defense
    else:
        return attacker.attack - victim.defense


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
        damage_taken = calculate_damage(self.attacker, self.victim)
        if damage_taken < 0:
            damage_taken = 0
        self.victim.health -= damage_taken
        self.victim.damaged = True
        animate_damage(self.victim, old_victim_health)

        time.sleep(.25)
        if isinstance(self.victim, Player):
            print(f"Updated player health: {self.victim.health}")
        else:
            print(f"Updated enemy health: {self.victim.health}")

        if isinstance(self.victim, Enemy):
            enemy = self.victim
            if enemy.health <= 0:
                print(f"Enemy died in counter attack!: {self.victim.health}")
                enemy.health = 0
                enemy.currentTile.occupied = False
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
                self.counter_attack()
        else:
            self.counter_attack()
