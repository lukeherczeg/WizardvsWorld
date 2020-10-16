import sys
import os
import pygame
import math
import time
from assets.image_loader import *
from const import TextureType, TileTint
from classes.entity import Player, Archer, Knight, PLAYER_HEALTH, ARCHER_HEALTH, KNIGHT_HEALTH

ENTITIES = []

# NOTES:
# There are DRAW functions and ANIMATE functions.
# DRAW - code runs almost instantly and repaints screen
# ANIMATE - code runs with delay for animation time and maintains screen state outside of animation

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


def draw_tinted_tiles(tile_list, entity, tint):
    for tile in tile_list:
        tile_img = _get_tile_img(tile, tint)
        tile_rect = tile_img.get_rect()
        tile_rect = tile_rect.move([tile.col * BLOCK_SIZE, tile.row * BLOCK_SIZE])
        SCREEN.blit(tile_img, tile_rect)

    entity_img = _get_entity_img(entity)
    entity_rect = entity_img.get_rect()
    entity_rect = entity_rect.move([entity.get_position().col * BLOCK_SIZE, entity.get_position().row * BLOCK_SIZE])
    SCREEN.blit(entity_img, entity_rect)
    draw_entities()
    pygame.display.flip()


def draw_selected_tile(tile):
    tile_img = SELECT_PNG
    tile_rect = tile_img.get_rect()
    tile_rect = tile_rect.move([tile.col * BLOCK_SIZE, tile.row * BLOCK_SIZE])
    SCREEN.blit(tile_img, tile_rect)
    pygame.display.flip()


def draw_entities(ignorables=None, hard=True):
    if ignorables is None:
        entities = ENTITIES
    else:
        entities = filter(lambda entity: entity not in ignorables, ENTITIES)

    for entity in entities:
        entity_img = _get_entity_img(entity)
        entity_rect = entity_img.get_rect()
        entity_rect = entity_rect.move([entity.get_position().col * BLOCK_SIZE, entity.get_position().row * BLOCK_SIZE])
        SCREEN.blit(entity_img, entity_rect)
        if hard: pygame.display.update(entity_rect)


def animate_move(entity, old_pos):
    # Initialize start and end points and covert to pixel values
    target_x, target_y = entity.get_position().col * BLOCK_SIZE, entity.get_position().row * BLOCK_SIZE
    old_x, old_y = old_pos
    old_x = old_x * BLOCK_SIZE
    old_y = old_y * BLOCK_SIZE

    # Create rect of moving entity
    entity_img = _get_entity_img(entity)
    entity_rect = entity_img.get_rect()
    entity_rect = entity_rect.move([old_x, old_y])

    # For animating perpendicular wiggle while walking
    wiggle_index = 0

    # TO BE CHANGED, move horizontally
    while old_x != target_x:
        if old_x < target_x:
            entity_rect = entity_rect.move([X_MOVEMENT_SPEED, move_wiggle[wiggle_index]])
            old_x = old_x + X_MOVEMENT_SPEED
        elif old_x > target_x:
            entity_rect = entity_rect.move([-X_MOVEMENT_SPEED, move_wiggle[wiggle_index]])
            old_x = old_x - X_MOVEMENT_SPEED

        wiggle_index = 0 if wiggle_index == len(move_wiggle) - 1 else wiggle_index + 1

        # redraw the grid and entities besides the one being animated,
        # then draw animation frame of entity
        draw_grid()
        draw_entities(ignorables=[entity])
        SCREEN.blit(entity_img, entity_rect)
        pygame.display.flip()

    # TO BE CHANGED, move vertically
    while old_y != target_y:
        if old_y < target_y:
            entity_rect = entity_rect.move([move_wiggle[wiggle_index], Y_MOVEMENT_SPEED])
            old_y = old_y + Y_MOVEMENT_SPEED
        elif old_y > target_y:
            entity_rect = entity_rect.move([move_wiggle[wiggle_index], -Y_MOVEMENT_SPEED])
            old_y = old_y - Y_MOVEMENT_SPEED

        wiggle_index = 0 if wiggle_index == len(move_wiggle) - 1 else wiggle_index + 1

        # redraw the grid and entities besides the one being animated,
        # then draw animation frame of entity
        draw_grid()
        draw_entities(ignorables=[entity])
        SCREEN.blit(entity_img, entity_rect)
        pygame.display.flip()

    # this is done to re-center the final animation sprite and ensure game state is up to date
    total_refresh_drawing()


def animate_attack(attacker, victim):
    if isinstance(attacker, Knight):
        animate_knight_attack()
    else:
        # Initialize start and end points and covert to pixel values
        start_x = attacker.get_position().col * BLOCK_SIZE
        start_y = attacker.get_position().row * BLOCK_SIZE
        target_x = victim.get_position().col * BLOCK_SIZE
        target_y = victim.get_position().row * BLOCK_SIZE

        # point attack at enemy
        angle = math.atan2(-(start_y - target_y), start_x - target_x)
        angle = math.degrees(angle)

        # get proportion of x movement to y movement needed
        if target_y == start_y:
            x_diff = 1
        else:
            x_diff = math.ceil(abs((target_x - start_x) / (target_y - start_y)))
        if target_x == start_x:
            y_diff = 1
        else:
            y_diff = math.ceil(abs((target_y - start_y) / (target_x - start_x)))

        coords = (start_x,start_y,target_x,target_y,x_diff,y_diff,angle)

        if isinstance(attacker, Player):
            animate_player_attack(coords)
        elif isinstance(attacker, Archer):
            animate_archer_attack(coords)
    
def animate_damage(victim, victim_old_hp):
    
    damage_diff = victim_old_hp - victim.health

    #create number rect
    number_font = pygame.font.Font('freesansbold.ttf', 12)
    number_text = number_font.render(str(damage_diff), True, RED)
    number_rect = number_text.get_rect()
    number_y_var = victim.get_position().row * BLOCK_SIZE
    number_x_fixed = (victim.get_position().col * BLOCK_SIZE) + 30
    number_rect = number_rect.move([number_x_fixed, number_y_var])

    #draw and animate number rect
    y_move_amount = [0,0,0,0,0,0,0,0,0,0,-1]
    y_move_index = 0
    for i in range(120):
        number_rect = number_rect.move([0, y_move_amount[y_move_index]])

        y_move_index = 0 if y_move_index == len(y_move_amount) - 1 else y_move_index + 1

        draw_grid()
        draw_entities(hard=False)
        SCREEN.blit(number_text, number_rect)
        pygame.display.flip()
    
    total_refresh_drawing()

    #create initial rectangles

    # HP bar math 4px by 24px
    hp_bar_y = (victim.get_position().row * BLOCK_SIZE) + 4
    hp_bar_x = (victim.get_position().col * BLOCK_SIZE) + 4
    BAR_LENGTH = 24
    BAR_HEIGHT = 4

    old_hp_ratio = 0
    new_hp_ratio = 0
    if isinstance(victim, Player):
        new_hp_ratio = victim.health / PLAYER_HEALTH
        old_hp_ratio = victim_old_hp / PLAYER_HEALTH
    elif isinstance(victim, Knight):
        new_hp_ratio = victim.health / KNIGHT_HEALTH
        old_hp_ratio = victim_old_hp / KNIGHT_HEALTH
    elif isinstance(victim, Archer):
        new_hp_ratio = victim.health / ARCHER_HEALTH
        old_hp_ratio = victim_old_hp / ARCHER_HEALTH

    green_hp_bar_x_pos = math.floor(BAR_LENGTH * old_hp_ratio)
    green_hp_bar_x_final = math.floor(BAR_HEIGHT * new_hp_ratio)

    x_move_amount = [0,0,0,0,0,0,0,-1]
    x_move_index = 0
    while(green_hp_bar_x_pos != green_hp_bar_x_final):
        draw_grid()
        draw_entities(hard=False)
        pygame.draw.rect(SCREEN, BRIGHT_RED, (hp_bar_x, hp_bar_y, BAR_LENGTH, BAR_HEIGHT))
        pygame.draw.rect(SCREEN, BRIGHT_GREEN, (hp_bar_x, hp_bar_y, green_hp_bar_x_pos, BAR_HEIGHT))
        pygame.display.flip()

        green_hp_bar_x_pos = green_hp_bar_x_pos + x_move_amount[x_move_index]
        x_move_index = 0 if x_move_index == len(x_move_amount) - 1 else x_move_index + 1


def animate_player_attack(coords):
    start_x, start_y, target_x, target_y, x_diff, y_diff, angle = coords
    # For animating fireball gif
    animation_index = 0

    trans_fireballs = []
    for fireball in FIREBALL_GIF:
        trans_fireball = pygame.transform.rotate(fireball, angle - 135)
        trans_fireballs.append(pygame.transform.scale(trans_fireball, (50, 50)))

    while abs(start_x - target_x) >= 15 or abs(start_y - target_y) >= 15:
        # update animation position and frame
        fire_rect = trans_fireballs[animation_index].get_rect()
        fire_rect = fire_rect.move([start_x, start_y])

        # animation logic
        if start_x < target_x:
            start_x = start_x + x_diff
        elif start_x > target_x:
            start_x = start_x - x_diff

        if start_y < target_y:
            start_y = start_y + y_diff
        elif start_y > target_y:
            start_y = start_y - y_diff

        animation_index = 0 if animation_index == len(FIREBALL_GIF) - 1 else animation_index + 1

        # redraw the grid and entities besides the one being animated,
        # then draw animation frame of entity
        draw_grid()
        draw_entities(hard=False)
        SCREEN.blit(trans_fireballs[animation_index], fire_rect)
        pygame.display.flip()

    # this is done to re-center the final animation sprite and ensure game state is up to date
    total_refresh_drawing()

def animate_knight_attack():
    draw_grid()
    draw_entities(hard=False)
    pygame.display.flip()
    time.sleep(0.2)

def animate_archer_attack(coords):
    start_x, start_y, target_x, target_y, x_diff, y_diff, angle = coords
    trans_arrow = pygame.transform.rotate(ARROW_PNG, angle + 90)
    trans_arrow = pygame.transform.scale(trans_arrow, (20, 20))

    while abs(start_x - target_x) >= 2 or abs(start_y - target_y) >= 2:
        # update animation position and frame
        arrow_rect = trans_arrow.get_rect()
        arrow_rect = arrow_rect.move([start_x, start_y])

        # animation logic
        if start_x < target_x:
            start_x = start_x + x_diff
        elif start_x > target_x:
            start_x = start_x - x_diff

        if start_y < target_y:
            start_y = start_y + y_diff
        elif start_y > target_y:
            start_y = start_y - y_diff

        # redraw the grid and entities besides the one being animated,
        # then draw animation frame of entity
        draw_grid()
        draw_entities(hard=False)
        SCREEN.blit(trans_arrow, arrow_rect)
        pygame.display.flip()

    # this is done to re-center the final animation sprite and ensure game state is up to date
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
