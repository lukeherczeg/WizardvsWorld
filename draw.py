import sys
import os
import pygame
from assets.image_loader import *
from const import TextureType, TileTint
from classes.entity import Player, Archer, Knight

ENTITIES = []


def total_refresh_drawing():
    draw_grid()
    draw_entities()
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


def draw_highlighted_tiles(tile_list, entity, tint):
    for tile in tile_list:
        tile_img = _get_tile_img(tile, tint)
        tile_rect = tile_img.get_rect()
        tile_rect = tile_rect.move([tile.col * BLOCK_SIZE, tile.row * BLOCK_SIZE])
        SCREEN.blit(tile_img, tile_rect)

    entity_img = _get_entity_img(entity)
    entity_rect = entity_img.get_rect()
    entity_rect = entity_rect.move([entity.get_position().col * BLOCK_SIZE, entity.get_position().row * BLOCK_SIZE])
    SCREEN.blit(entity_img, entity_rect)
    pygame.display.flip()


def draw_highlighted_tile(tile):
    tile_img = _get_tile_img(tile, TileTint.BLUE)
    tile_rect = tile_img.get_rect()
    tile_rect = tile_rect.move([tile.col * BLOCK_SIZE, tile.row * BLOCK_SIZE])
    SCREEN.blit(tile_img, tile_rect)
    pygame.display.flip()


def draw_entities(ignorables=None):
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


def move_player(entity, old_pos):
    target_x, target_y = entity.get_position().col * BLOCK_SIZE, entity.get_position().row * BLOCK_SIZE
    old_x, old_y = old_pos
    old_x = old_x * BLOCK_SIZE
    old_y = old_y * BLOCK_SIZE
    entity_img = _get_entity_img(entity)
    entity_rect = entity_img.get_rect()
    entity_rect = entity_rect.move([old_x, old_y])
    wiggle_index = 0

    while old_x != target_x:
        if old_x < target_x:
            entity_rect = entity_rect.move([X_MOVEMENT_SPEED, move_wiggle[wiggle_index]])
            old_x = old_x + X_MOVEMENT_SPEED
        elif old_x > target_x:
            entity_rect = entity_rect.move([-X_MOVEMENT_SPEED, move_wiggle[wiggle_index]])
            old_x = old_x - X_MOVEMENT_SPEED
        wiggle_index = wiggle_index + 1
        if wiggle_index == len(move_wiggle):
            wiggle_index = 0
        draw_grid()
        draw_entities(ignorables=[entity])
        SCREEN.blit(entity_img, entity_rect)
        pygame.display.flip()

    while old_y != target_y:
        if old_y < target_y:
            entity_rect = entity_rect.move([move_wiggle[wiggle_index], Y_MOVEMENT_SPEED])
            old_y = old_y + Y_MOVEMENT_SPEED
        elif old_y > target_y:
            entity_rect = entity_rect.move([move_wiggle[wiggle_index], -Y_MOVEMENT_SPEED])
            old_y = old_y - Y_MOVEMENT_SPEED

        wiggle_index = wiggle_index + 1
        if wiggle_index == len(move_wiggle):
            wiggle_index = 0
        draw_grid()
        draw_entities(ignorables=[entity])
        SCREEN.blit(entity_img, entity_rect)
        pygame.display.flip()

    total_refresh_drawing()


def _get_tile_img(tile, tint=None):
    if tile.texture_type == TextureType.GRASS:
        if tint == TileTint.BLUE:
            return GRASS_BLUE_PNG
        elif tint == TileTint.RED:
            return GRASS_RED_PNG
        elif tint == TileTint.ORANGE:
            return GRASS_ORANGE_PNG
        else:
            return GRASS_PNG
    if tile.texture_type == TextureType.DIRT:
        if tint == TileTint.BLUE:
            return DIRT_BLUE_PNG
        elif tint == TileTint.RED:
            return DIRT_RED_PNG
        elif tint == TileTint.ORANGE:
            return DIRT_ORANGE_PNG
        else:
            return DIRT_PNG
    elif tile.texture_type == TextureType.STONE:
        if tint == TileTint.BLUE:
            return STONE_BLUE_PNG
        elif tint == TileTint.RED:
            return STONE_RED_PNG
        elif tint == TileTint.ORANGE:
            return STONE_ORANGE_PNG
        else:
            return STONE_PNG
    elif tile.texture_type == TextureType.FLOOR:
        if tint == TileTint.BLUE:
            return FLOOR_BLUE_PNG
        elif tint == TileTint.RED:
            return FLOOR_RED_PNG
        elif tint == TileTint.ORANGE:
            return FLOOR_ORANGE_PNG
        else:
            return FLOOR_PNG


def _get_entity_img(entity):
    if isinstance(entity, Player):
        if entity.attacking:
            return WIZ_ATTACK_PNG
        elif entity.damaged:
            return WIZ_HURT_PNG
        elif entity.selected:
            return WIZ_SELECTED_PNG
        else:
            return WIZ_PNG

    if isinstance(entity, Knight):
        if entity.attacking:
            return KNIGHT_ATTACK_PNG
        elif entity.damaged:
            return KNIGHT_HURT_PNG
        elif entity.attackable:
            return KNIGHT_ATTACKABLE_PNG
        else:
            return KNIGHT_PNG

    if isinstance(entity, Archer):
        if entity.attacking:
            return ARCHER_ATTACK_PNG
        elif entity.damaged:
            return ARCHER_HURT_PNG
        elif entity.attackable:
            return ARCHER_ATTACKABLE_PNG
        else:
            return ARCHER_PNG


def quit_game():
    pygame.quit()
    sys.exit()
