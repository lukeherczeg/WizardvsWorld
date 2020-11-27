import os
from WizardVsWorld.classes.draw import pygame

pygame.mixer.init()

asset_path = os.path.dirname(__file__)

menu_music = pygame.mixer.Sound(os.path.join(asset_path, 'menu_song.wav'))