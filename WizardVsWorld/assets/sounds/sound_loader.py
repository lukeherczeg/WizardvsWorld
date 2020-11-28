import os
from WizardVsWorld.classes.draw import pygame

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

asset_path = os.path.dirname(__file__)

menu_music = pygame.mixer.Sound(os.path.join(asset_path, 'menu_music.ogg'))
game_music = pygame.mixer.Sound(os.path.join(asset_path, 'game_music.ogg'))
game_music.set_volume(0.3)

fireball_attack_sound = pygame.mixer.Sound(os.path.join(asset_path, 'fireball_attack.ogg'))
sword_attack_sound = pygame.mixer.Sound(os.path.join(asset_path, 'sword_attack.ogg'))
arrow_attack_sound = pygame.mixer.Sound(os.path.join(asset_path, 'arrow_attack.ogg'))

death_sound = pygame.mixer.Sound(os.path.join(asset_path, 'enemy_died.ogg'))
