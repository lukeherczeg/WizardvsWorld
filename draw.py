import wsl
import sys
import os
import pygame
from assets.image_loader import *
from classes.grid import Grid

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BRIGHT_RED = (255, 0, 0)
BLUE = (0, 0, 255)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1000
wsl.set_display_to_host()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

X_MOVEMENT_SPEED = 1
Y_MOVEMENT_SPEED = 1
move_wiggle = [0,0,0,1,1,1,1,0,0,0,-1,-1,-1]
BLOCK_SIZE = 40  # Set the size of the grid block
GRID = Grid(WINDOW_WIDTH // BLOCK_SIZE, WINDOW_HEIGHT // BLOCK_SIZE)
ENTITIES = []

def total_refresh_drawing():
    draw_grid()
    draw_characters()
    pygame.display.flip()

def draw_grid():
    for _, col in enumerate(GRID.game_map):
        for _, tile in enumerate(col):
            tile_img = _get_tile_img(tile)
            tile_rect = tile_img.get_rect()
            tile_rect = tile_rect.move([tile.col * BLOCK_SIZE, tile.row * BLOCK_SIZE])
            SCREEN.blit(tile_img, tile_rect)

def draw_tile(tile):
    tile_img = pygame.image.load(_get_tile_img(tile)).convert()
    tile_rect = tile_img.get_rect()
    tile_rect = tile_rect.move([tile.col * BLOCK_SIZE, tile.row * BLOCK_SIZE])
    SCREEN.blit(tile_img, tile_rect)
    pygame.display.flip()

def show_movable_tiles(tile_list, entity):
    for tile in tile_list:
        highlight_tile(tile)
    
    entity_img = _get_entity_img(entity)
    entity_rect = entity_img.get_rect()
    entity_rect = entity_rect.move([entity.get_position().col * BLOCK_SIZE, entity.get_position().row * BLOCK_SIZE])
    SCREEN.blit(entity_img, entity_rect)
    pygame.display.flip()

def highlight_tile(tile):
    tile_img = _get_tile_img(tile, 'blue')
    tile_rect = tile_img.get_rect()
    tile_rect = tile_rect.move([tile.col * BLOCK_SIZE, tile.row * BLOCK_SIZE])
    SCREEN.blit(tile_img, tile_rect)

def draw_characters(ignorables=None):
    if ignorables is None:
        entities = ENTITIES
    else:
        entities = filter(lambda entity: not entity in ignorables, ENTITIES)

    for entity in entities:
        entity_img = _get_entity_img(None)
        entity_rect = entity_img.get_rect()
        entity_rect = entity_rect.move([entity.get_position().col * BLOCK_SIZE, entity.get_position().row * BLOCK_SIZE])
        SCREEN.blit(entity_img, entity_rect)
        pygame.display.update(entity_rect)

def move_player(entity, oldPos):
    target_x, target_y = entity.get_position().col*BLOCK_SIZE, entity.get_position().row*BLOCK_SIZE
    old_x, old_y = oldPos
    old_x = old_x*BLOCK_SIZE
    old_y = old_y*BLOCK_SIZE
    entity_img = _get_entity_img(entity)
    entity_rect = entity_img.get_rect()
    entity_rect = entity_rect.move([old_x, old_y])
    wiggle_index = 0

    while(old_x != target_x):
        if old_x < target_x:
            entity_rect = entity_rect.move([X_MOVEMENT_SPEED, move_wiggle[wiggle_index]])
            old_x = old_x + X_MOVEMENT_SPEED
        elif old_x > target_x:
            entity_rect = entity_rect.move([-X_MOVEMENT_SPEED, move_wiggle[wiggle_index]])
            old_x = old_x - X_MOVEMENT_SPEED
        wiggle_index = wiggle_index + 1
        if(wiggle_index == len(move_wiggle)):
            wiggle_index = 0
        draw_grid()
        draw_characters(ignorables=[entity])
        SCREEN.blit(entity_img, entity_rect)
        pygame.display.flip()

    while(old_y != target_y):
        if old_y < target_y:
            entity_rect = entity_rect.move([move_wiggle[wiggle_index], Y_MOVEMENT_SPEED])
            old_y = old_y + Y_MOVEMENT_SPEED
        elif old_y > target_y:
            entity_rect = entity_rect.move([move_wiggle[wiggle_index], -Y_MOVEMENT_SPEED])
            old_y = old_y - Y_MOVEMENT_SPEED

        wiggle_index = wiggle_index + 1
        if(wiggle_index == len(move_wiggle)):
            wiggle_index = 0
        draw_grid()
        draw_characters(ignorables=[entity])
        SCREEN.blit(entity_img, entity_rect)
        pygame.display.flip()
    
    total_refresh_drawing()


def _get_tile_img(tile, highlight=None):
    if(highlight == 'blue'):
        if tile.standable:
            return GRASS_BLUE_PNG
        else:
            return STONE_RED_PNG
    if tile.standable:
        return GRASS_PNG
    else:
        return STONE_PNG


def _get_entity_img(entity):
    return WIZ_PNG


def quit_game():
    pygame.quit()
    sys.exit()
