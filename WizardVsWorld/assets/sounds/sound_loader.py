import os
from WizardVsWorld.classes.draw import pygame

pygame.mixer.init()

asset_path = os.path.dirname(__file__)

menu_music = pygame.mixer.Sound(os.path.join(asset_path, 'menu_music.wav'))
fireball_attack = pygame.mixer.Sound(os.path.join(asset_path, 'fireball_attack.wav'))
sword_attack = pygame.mixer.Sound(os.path.join(asset_path, 'sword_attack.wav'))