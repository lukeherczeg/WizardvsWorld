#create parent class  entity with basic attributes and functions
#Objects such as tiles are ints until we have all source files#

import pygame
import os

#entity will have various shared data types
class Entity:
    currentTile: int#################needs to be tile instead of int
    health: int
    attack: int #these variables may change based on how we want to do combat
    defense: int
    max_Movement: int
    cur_Movement: int

    def __init__(self):
        self.currentTile = 0

    def getPosition(self):
        return self.currentTile

#each type of entity will have an "image" method that handles retrieving (but not printing assets)
#this method is responsible for taking in bools that will decipher which image of the character to retrieve

#the wizard will have methods and variables specific to the wizard
class Wizard(Entity):
    def __init__(self):
        Entity.__init__(self)

    def image(self, damaged, attacking):

        #create path to the asset based on what kind of wizard we need to print (ie hurt, attacking, normal)
        if not damaged and not attacking:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'wizhat.png')
        elif damaged:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'wizhurt.png')
        elif attacking:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'wizattack.png')
        else:
            image_path = ''

        wizard = pygame.image.load(image_path)
        return wizard

class Soldier(Entity):

    def __init__(self):
        Entity.__init__(self)

    def image(self, damaged, attacking):

        #create path to the asset based on what kind of soldier we need to print (ie hurt, attacking, normal)
        if not damaged and not attacking:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'soldier.png')
        elif damaged:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'soldierhurt.png')
        elif attacking:
            main_directory = os.path.dirname('WizardvsWorld')
            asset_path = os.path.join(main_directory, 'assets')
            image_path = os.path.join(asset_path, 'soldierattack.png')
        else:
            image_path = ''

        soldier = pygame.image.load(image_path)
        return soldier