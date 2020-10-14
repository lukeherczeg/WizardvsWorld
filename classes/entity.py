# create parent class  entity with basic attributes and functions
# Objects such as tiles are ints until we have all source files#

import pygame
import os
from assets.image_loader import GRID
from classes.tile import Tile


# entity will have various shared data types
class Entity:
    currentTile: Tile
    health: int
    attack: int  # these variables may change based on how we want to do combat
    defense: int
    max_Movement: int = 5
    cur_Movement: int
    range: int

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
        self.currentTile = GRID.game_map[1][1]
        self.health = 100
        self.attack = 20
        self.defense = 5
        self.range = 2
        self.selected = False


class Enemy(Entity):
    def __init__(self):
        super().__init__()


class Knight(Enemy):
    def __init__(self):
        super().__init__()
        self.currentTile = GRID.game_map[0][1]
        self.health = 50
        self.attack = 10
        self.defense = 5
        self.range = 1
        self.attackable = False


class Archer(Enemy):
    def __init__(self):
        super().__init__()
        self.currentTile = GRID.game_map[0][2]
        self.health = 30
        self.attack = 15
        self.defense = 0
        self.range = 2
        self.attackable = False
