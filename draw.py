import sys
import os
import pygame
import math
from assets.image_loader import *
from classes.grid import Grid

GRID = Grid(WINDOW_WIDTH // BLOCK_SIZE, WINDOW_HEIGHT // BLOCK_SIZE)
ENTITIES = []

# NOTES:
# There are DRAW functions and ANIMATE functions.
# DRAW - code runs almost instantly and repaints screen
# ANIMATE - code runs with delay for animation time and maintains screen state outside of animation

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
    tile_img = _get_tile_img(tile)
    tile_rect = tile_img.get_rect()
    tile_rect = tile_rect.move([tile.col * BLOCK_SIZE, tile.row * BLOCK_SIZE])
    SCREEN.blit(tile_img, tile_rect)
    pygame.display.flip()

def draw_highlighted_tiles(tile_list, entity):
    for tile in tile_list:
        draw_highlight_tile(tile)

    entity_img = _get_entity_img(entity)
    entity_rect = entity_img.get_rect()
    entity_rect = entity_rect.move([entity.get_position().col * BLOCK_SIZE, entity.get_position().row * BLOCK_SIZE])
    SCREEN.blit(entity_img, entity_rect)
    pygame.display.flip()

def draw_highlight_tile(tile):
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
        entity_img = _get_entity_img(entity)
        entity_rect = entity_img.get_rect()
        entity_rect = entity_rect.move([entity.get_position().col * BLOCK_SIZE, entity.get_position().row * BLOCK_SIZE])
        SCREEN.blit(entity_img, entity_rect)
        pygame.display.update(entity_rect)

def animate_move(entity, oldPos):
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

        wiggle_index = 0 if wiggle_index == len(move_wiggle)-1 else wiggle_index + 1
        draw_grid()
        draw_characters(ignorables=[entity])
        SCREEN.blit(entity_img, entity_rect)
        pygame.display.flip()

    total_refresh_drawing()

def animate_attack(attacker, victim):
    start_x = attacker.get_position().col*BLOCK_SIZE
    start_y = attacker.get_position().row*BLOCK_SIZE
    target_x = victim.get_position().col*BLOCK_SIZE
    target_y = victim.get_position().row*BLOCK_SIZE
    
    animation_index = 0

    angle = math.atan2(-(start_y-target_y), start_x - target_x)
    angle = math.degrees(angle)

    x_diff = abs(math.ceil((target_x-start_x) / (target_y-start_y)))
    y_diff = abs(math.ceil((target_y-start_y) / (target_x-start_x)))

    trans_fireballs = []
    for fireball in FIREBALL_GIF:
        trans_fireball = pygame.transform.rotate(fireball, angle-135)
        trans_fireballs.append(pygame.transform.scale(trans_fireball, (45,45)))

    while abs(start_x - target_x) >= 3 or abs(start_y - target_y) >= 3:
        fire_rect = trans_fireballs[animation_index].get_rect()
        fire_rect = fire_rect.move([start_x, start_y])
        #animation logic
        if start_x < target_x:
            start_x = start_x + x_diff
        elif start_x > target_x:
            start_x = start_x - x_diff

        if start_y < target_y:
            start_y = start_y + y_diff
        elif start_y > target_y:
            start_y = start_y - y_diff

        animation_index = 0 if animation_index == len(FIREBALL_GIF)-1 else animation_index + 1
        draw_grid()
        draw_characters()
        SCREEN.blit(trans_fireballs[animation_index], fire_rect)
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
    if type(entity).__name__ == "Player":
        return WIZ_PNG
    elif type(entity).__name__ == "Enemy":
        return KNIGHT_PNG


def quit_game():
    pygame.quit()
    sys.exit()
