import wsl
import sys
import os
import pygame
from classes.grid import Grid

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1000
wsl.set_display_to_host()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

X_MOVEMENT_SPEED = 4
Y_MOVEMENT_SPEED = 4
BLOCK_SIZE = 40  # Set the size of the grid block
GRID = Grid(WINDOW_WIDTH // BLOCK_SIZE, WINDOW_HEIGHT // BLOCK_SIZE)

print("Grid initialized.")


def draw_grid():
    for _, col in enumerate(GRID.game_map):
        for _, tile in enumerate(col):
            tile_img = pygame.image.load(_get_tile_img(tile)).convert()
            tile_rect = tile_img.get_rect()
            tile_rect = tile_rect.move([tile.col * BLOCK_SIZE, tile.row * BLOCK_SIZE])
            SCREEN.blit(tile_img, tile_rect)
    pygame.display.flip()


def draw_tile(tile):
    tile_img = pygame.image.load(_get_tile_img(tile)).convert()
    tile_rect = tile_img.get_rect()
    tile_rect = tile_rect.move([tile.col * BLOCK_SIZE, tile.row * BLOCK_SIZE])
    SCREEN.blit(tile_img, tile_rect)
    pygame.display.flip()


def highlight_tile(tile):
    tile_img = pygame.image.load(_get_tile_img(tile)).convert()
    tile_rect = tile_img.get_rect()
    tile_rect = tile_rect.move([tile.col * BLOCK_SIZE, tile.row * BLOCK_SIZE])
    SCREEN.blit(tile_img, tile_rect)
    pygame.display.flip()
    rect = pygame.Rect((tile.col * BLOCK_SIZE), (tile.row * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(SCREEN, WHITE, rect)
    pygame.display.update()


def draw_characters(entities):
    for entity in entities:
        entity_img = pygame.image.load(_get_entity_img(None)).convert_alpha()
        entity_rect = entity_img.get_rect()
        entity_rect = entity_rect.move([entity.get_position().col * BLOCK_SIZE, entity.get_position().row * BLOCK_SIZE])
        SCREEN.blit(entity_img, entity_rect)

    pygame.display.flip()

def move_player(entity, oldPos):
    target_x, target_y = entity.get_position().col*BLOCK_SIZE, entity.get_position().row*BLOCK_SIZE
    old_x, old_y = oldPos
    old_x = old_x*100
    old_y = old_y*100
    entity_img = pygame.image.load(_get_entity_img(entity)).convert_alpha()
    entity_rect = entity_img.get_rect()
    while(old_x != target_x):
        if old_x < target_x:
            entity_rect = entity_rect.move([X_MOVEMENT_SPEED, 0])
            old_x = old_x + 1
        elif old_x > target_x:
            entity_rect = entity_rect.move([-X_MOVEMENT_SPEED, 0])
            old_x = old_x - 1
        if old_y < target_y:
            entity_rect = entity_rect.move([0, Y_MOVEMENT_SPEED])
            old_y = old_y + 1
        elif old_y > target_y:
            entity_rect = entity_rect.move([0, -Y_MOVEMENT_SPEED])
            old_y = old_y - 1
        print(old_x, old_y)
        entity_rect = entity_rect.move([old_x, old_y])
        draw_grid()
        SCREEN.blit(entity_img, entity_rect)
        pygame.display.flip()


def _get_tile_img(tile):
    main_directory = os.path.dirname('WizardvsWorld')
    asset_path = os.path.join(main_directory, 'assets')
    if tile.standable:
        return os.path.join(asset_path, 'grass.png')
    else:
       return os.path.join(asset_path, 'stone.png')


def _get_entity_img(entity):
    main_directory = os.path.dirname('WizardvsWorld')
    asset_path = os.path.join(main_directory, 'assets')
    return os.path.join(asset_path, 'archer.png')


def quit_game():
    pygame.quit()
    sys.exit()
