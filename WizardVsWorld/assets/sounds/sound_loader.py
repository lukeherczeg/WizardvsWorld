import os
from WizardVsWorld.classes.draw import pygame

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

asset_path = os.path.dirname(__file__)

menu_music = pygame.mixer.Sound(os.path.join(asset_path, 'menu_music.ogg'))
game_music_grass = pygame.mixer.Sound(os.path.join(asset_path, 'game_music_grass.ogg'))
game_music_castle = pygame.mixer.Sound(os.path.join(asset_path, 'game_music_castle.ogg'))
game_music_sand = pygame.mixer.Sound(os.path.join(asset_path, 'game_music_sand.ogg'))
game_music_ice = pygame.mixer.Sound(os.path.join(asset_path, 'game_music_ice.ogg'))
game_music_castle_2 = pygame.mixer.Sound(os.path.join(asset_path, 'game_music_castle_2.ogg'))
game_music_over = pygame.mixer.Sound(os.path.join(asset_path, 'game_music_over.ogg'))

fireball_attack_sound = pygame.mixer.Sound(os.path.join(asset_path, 'fireball_attack.ogg'))
firenova_attack_sound = pygame.mixer.Sound(os.path.join(asset_path, 'firenova_attack.ogg'))
sword_attack_sound = pygame.mixer.Sound(os.path.join(asset_path, 'sword_attack.ogg'))
arrow_attack_sound = pygame.mixer.Sound(os.path.join(asset_path, 'arrow_attack.ogg'))
player_heal_sound = pygame.mixer.Sound(os.path.join(asset_path, 'player_heal.ogg'))
block_magic_sound = pygame.mixer.Sound(os.path.join(asset_path, 'magic_block.ogg'))

death_sound = pygame.mixer.Sound(os.path.join(asset_path, 'enemy_died.ogg'))

def stop_playback():
    pygame.mixer.stop()
