# create parent class  entity with basic attributes and functions
# Objects such as tiles are ints until we have all source files#

import pygame
import os
from draw import GRID
from classes.tile import Tile


# entity will have various shared data types
class Entity:
    currentTile: Tile
    health: int
    attack: int  # these variables may change based on how we want to do combat
    defense: int
    max_Movement: int
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
        self.isSelected = False

    # @staticmethod
    def image(self):

        # create path to the asset based on what kind of wizard we need to print (ie hurt, attacking, normal)
        if self.damaged:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'wizhurt.png')
        elif self.attacking:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'wizattack.png')
        elif self.isSelected:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'wizselected.png')
        else:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'wiz.png')

        wizard = pygame.image.load(image_path)
        return wizard


class Enemy(Entity):
    def __init__(self):
        super().__init__()
        self.currentTile = GRID.game_map[0][1]
        self.health = 50
        self.attack = 10
        self.defense = 5
        self.range = 1
        self.isAttackable = False

    # @staticmethod
    def image(self):

        # create path to the asset based on what kind of soldier we need to print (ie hurt, attacking, normal)
        if self.damaged:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'knighthurt.png')
        elif self.attacking:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'knightattack.png')
        elif self.isAttackable:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'knightattackable.png')
        else:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'knight.png')

        knight = pygame.image.load(image_path)
        return knight


class Archer(Enemy):
    def __init__(self):
        super().__init__()
        self.currentTile = GRID.game_map[0][2]
        self.health = 30
        self.attack = 15
        self.defense = 0
        self.range = 2
        self.isAttackable = False

    def image(self):

        # create path to the asset based on what kind of soldier we need to print (ie hurt, attacking, normal)
        if self.damaged:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'archerhurt.png')
        elif self.attacking:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'archerattack.png')
        elif self.isAttackable:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'archerattackable.png')
        else:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'archer.png')

        archer = pygame.image.load(image_path)
        return archer
