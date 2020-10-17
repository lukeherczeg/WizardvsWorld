# create parent class  entity with basic attributes and functions
# Objects such as tiles are ints until we have all source files#

import pygame
import os
from classes.tile import Tile

PLAYER_HEALTH = 100
KNIGHT_HEALTH = 50
ARCHER_HEALTH = 30


# entity will have various shared data types
class Entity:
    currentTile: Tile
    health: int
    attack: int  # these variables may change based on how we want to do combat
    defense: int
    max_Movement: int = 5
    cur_Movement: int
    range: int
    critical_chance: int
    level: int

    def __init__(self):
        self.damaged = False
        self.attacking = False
        defense = 0

    def get_position(self):
        return self.currentTile


# each type of entity will have an "image" method that handles retrieving (but not printing assets)
# this method is responsible for taking in bools that will decipher which image of the character to retrieve

# the wizard will have methods and variables specific to the wizard
class Player(Entity):
    def __init__(self):
        super().__init__()
        self.currentTile = None
        self.health = 100
        self.attack = 20
        self.defense = 5
        self.range = 3
        self.selected = False
        self.level = 1
        self.critical_chance = 25

    def level_up(self, new_level):
        self.level = new_level
        self.health += 15
        self.attack += 5
        self.defense += 1


class Enemy(Entity):
    def __init__(self):
        super().__init__()


class Knight(Enemy):
    max_Movement = 3

    def __init__(self, level):
        super().__init__()
        self.currentTile = None
        self.health = 50 + (level * 5)
        self.attack = 60 + (level * 2)
        self.defense = 5 + (level * 1)
        self.range = 1
        self.critical_chance = 10
        self.attackable = False


class Archer(Enemy):
    max_Movement = 4

    def __init__(self, level):
        super().__init__()
        self.currentTile = None
        self.health = 30 + (level * 2)
        self.attack = 30 + (level * 3)
        self.defense = 0 + (level * 1)
        self.critical_chance = 15
        self.range = 2
        self.attackable = False


class Boss(Enemy):
    ranged: bool
    tiles: [Tile]

    def __init__(self, level):
        super().__init__()


class GreatKnight(Boss):
    range = 1
