import os
import pygame
import sys
import math
import time
from assets.image_loader import *
from const import TileTexture, TileTint, ENTITIES
from classes.entity import Player, Archer, Knight, PLAYER_HEALTH, ARCHER_HEALTH, KNIGHT_HEALTH


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


def draw_selected_tile(tile, enemy=None):
    if enemy is None:
        tile_img = SELECT_PNG
    elif isinstance(enemy, Knight):
        tile_img = KNIGHT_ATTACKABLE_PNG
    elif isinstance(enemy, Archer):
        tile_img = ARCHER_ATTACKABLE_PNG
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


def draw_text(message, size, tile=None, offset=None, color=WHITE):
    # GOTO provided tile
    x_pos = tile.get_position().col if tile is not None else 0
    y_pos = tile.get_position().row if tile is not None else 0

    # ADD offset to coords
    x_offset, y_offset = offset if offset is not None else (0, 0)
    x_pos, y_pos = x_pos + x_offset, y_pos + y_offset

    # Draw text
    message_font = pygame.font.Font('freesansbold.ttf', size)
    message_text = message_font.render(str(message), True, color)
    message_rect = message_text.get_rect()
    message_rect = message_rect.move([x_pos, y_pos])
    SCREEN.blit(message_text, message_rect)
    pygame.display.flip()

#TODO
def animate_text(message, size, tile=None, offset=None, color=WHITE, time=0):
    return 0


def animate_entity_movement(entity, prev_tile):

    tile_list = GRID.path_to(prev_tile, entity.get_position())

    for i in range(len(tile_list)-1):
        old_pos = (tile_list[i].col*BLOCK_SIZE, tile_list[i].row*BLOCK_SIZE)
        new_pos = (tile_list[i+1].col*BLOCK_SIZE, tile_list[i+1].row*BLOCK_SIZE)
        animate_move(entity, old_pos, new_pos)

    # this is done to re-center the final animation sprite and ensure game state is up to date
    total_refresh_drawing()


def animate_move(entity, old_pos, new_pos):
    # Initialize start and end points and covert to pixel values
    target_x, target_y = new_pos
    old_x, old_y = old_pos

    # Create rect of moving entity
    entity_img = _get_entity_img(entity)
    entity_rect = entity_img.get_rect()
    entity_rect = entity_rect.move([old_x, old_y])

    # For animating perpendicular wiggle while walking and movement speed
    wiggle_index = 0
    move_speed_index = 0

    #move horizontally
    while old_x != target_x:
        if old_x < target_x:
            entity_rect = entity_rect.move([X_MOVEMENT_SPEED[move_speed_index], move_wiggle[wiggle_index]])
            old_x = old_x + X_MOVEMENT_SPEED[move_speed_index]
        elif old_x > target_x:
            entity_rect = entity_rect.move([-X_MOVEMENT_SPEED[move_speed_index], move_wiggle[wiggle_index]])
            old_x = old_x - X_MOVEMENT_SPEED[move_speed_index]

        wiggle_index = 0 if wiggle_index == len(move_wiggle) - 1 else wiggle_index + 1
        move_speed_index = 0 if move_speed_index == len(X_MOVEMENT_SPEED) - 1 else move_speed_index + 1

        # redraw the grid and entities besides the one being animated,
        # then draw animation frame of entity
        draw_grid()
        draw_entities(ignorables=[entity])
        SCREEN.blit(entity_img, entity_rect)
        pygame.display.flip()

    # TO BE CHANGED, move vertically
    while old_y != target_y:
        if old_y < target_y:
            entity_rect = entity_rect.move([move_wiggle[wiggle_index], Y_MOVEMENT_SPEED[move_speed_index]])
            old_y = old_y + Y_MOVEMENT_SPEED[move_speed_index]
        elif old_y > target_y:
            entity_rect = entity_rect.move([move_wiggle[wiggle_index], -Y_MOVEMENT_SPEED[move_speed_index]])
            old_y = old_y - Y_MOVEMENT_SPEED[move_speed_index]

        wiggle_index = 0 if wiggle_index == len(move_wiggle) - 1 else wiggle_index + 1
        move_speed_index = 0 if move_speed_index == len(X_MOVEMENT_SPEED) - 1 else move_speed_index + 1

        # redraw the grid and entities besides the one being animated,
        # then draw animation frame of entity
        draw_grid()
        draw_entities(ignorables=[entity])
        SCREEN.blit(entity_img, entity_rect)
        pygame.display.flip()


def animate_attack(attacker, victim):
    if isinstance(attacker, Knight):
        _animate_knight_attack()
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

        coords = (start_x, start_y, target_x, target_y, x_diff, y_diff, angle)
        if isinstance(attacker, Player):
            _animate_player_attack(coords)
        elif isinstance(attacker, Archer):
            _animate_archer_attack(coords)


def animate_damage(victim, victim_old_hp):
    _animate_damage_number(victim, victim_old_hp)

    time.sleep(0.2)

    _animate_damage_bar(victim, victim_old_hp)


def animate_death(entity):
    entity_img = _get_entity_img(entity)
    wiggle_index = 0
    opacity = 250

    while opacity != 0:
        draw_grid()
        draw_entities()
        _blit_alpha(SCREEN, entity_img, (entity.get_position().col * BLOCK_SIZE + move_wiggle[wiggle_index],
                                         entity.get_position().row * BLOCK_SIZE), opacity)
        pygame.display.flip()

        wiggle_index = 0 if wiggle_index == len(move_wiggle) - 1 else wiggle_index + 1
        opacity = opacity - 2

    total_refresh_drawing()


def update_coordinates(coords, diffs):
    start_x, start_y, target_x, target_y = coords
    x_diff, y_diff = diffs

    # animation logic
    if start_x < target_x:
        start_x = start_x + x_diff
    elif start_x > target_x:
        start_x = start_x - x_diff

    if start_y < target_y:
        start_y = start_y + y_diff
    elif start_y > target_y:
        start_y = start_y - y_diff

    return start_x, start_y


def _animate_player_attack(coords):
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

        start_x, start_y = update_coordinates((start_x, start_y, target_x, target_y), (x_diff, y_diff))

        animation_index = 0 if animation_index == len(FIREBALL_GIF) - 1 else animation_index + 1

        # redraw the grid and entities besides the one being animated,
        # then draw animation frame of entity
        draw_grid()
        draw_entities(hard=False)
        SCREEN.blit(trans_fireballs[animation_index], fire_rect)
        pygame.display.flip()

    # this is done to re-center the final animation sprite and ensure game state is up to date
    total_refresh_drawing()


def _animate_knight_attack():
    draw_grid()
    draw_entities(hard=False)
    time.sleep(0.2)
    pygame.display.flip()
    time.sleep(0.2)


def _animate_archer_attack(coords):
    start_x, start_y, target_x, target_y, x_diff, y_diff, angle = coords
    trans_arrow = pygame.transform.rotate(ARROW_PNG, angle)
    trans_arrow = pygame.transform.scale(trans_arrow, (30, 30))

    while abs(start_x - target_x) >= 2 or abs(start_y - target_y) >= 2:
        # update animation position and frame
        arrow_rect = trans_arrow.get_rect()
        arrow_rect = arrow_rect.move([start_x, start_y])

        start_x, start_y = update_coordinates((start_x, start_y, target_x, target_y), (x_diff, y_diff))

        # redraw the grid and entities besides the one being animated,
        # then draw animation frame of entity
        draw_grid()
        draw_entities(hard=False)
        SCREEN.blit(trans_arrow, arrow_rect)
        pygame.display.flip()

    # this is done to re-center the final animation sprite and ensure game state is up to date
    total_refresh_drawing()


def _animate_damage_number(victim, victim_old_hp):
    damage_diff = victim_old_hp - victim.health

    # create number rect
    number_font = pygame.font.Font('freesansbold.ttf', 14)
    number_font.set_bold(True)
    number_font.set_italic(True)
    number_text = number_font.render(str(damage_diff), True, RED)
    number_rect = number_text.get_rect()
    number_y_var = victim.get_position().row * BLOCK_SIZE
    number_x_fixed = (victim.get_position().col * BLOCK_SIZE) + 30
    number_rect = number_rect.move([number_x_fixed, number_y_var])

    # create victime rect
    victim_rect = _get_entity_img(victim).get_rect()
    victim_rect = victim_rect.move([victim.get_position().col * BLOCK_SIZE, victim.get_position().row * BLOCK_SIZE])

    # animation arrays and indexes
    y_move_amount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1]
    y_move_index = 0
    wiggle_index = 0
    for i in range(120):
        # animate
        number_rect = number_rect.move([0, y_move_amount[y_move_index]])
        victim_rect = victim_rect.move([move_wiggle[wiggle_index], 0])

        # prepare next frame
        y_move_index = 0 if y_move_index == len(y_move_amount) - 1 else y_move_index + 1
        wiggle_index = 0 if wiggle_index == len(move_wiggle) - 1 else wiggle_index + 1

        # draw
        draw_grid()
        draw_entities(hard=False, ignorables=[victim])
        SCREEN.blit(number_text, number_rect)
        SCREEN.blit(_get_entity_img(victim), victim_rect)
        pygame.display.flip()

    total_refresh_drawing()


def _animate_damage_bar(victim, victim_old_hp):
    # HP bar math 4px by 24px
    hp_bar_y = (victim.get_position().row * BLOCK_SIZE) + 4
    hp_bar_x = (victim.get_position().col * BLOCK_SIZE) + 4
    bar_length = 24
    bar_height = 4

    # get ratios for scaling health reduction graphically
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

    # prevent negative health
    if new_hp_ratio < 0:
        new_hp_ratio = 0

    # track start and stop of green movement
    green_hp_bar_x_pos = math.floor(bar_length * old_hp_ratio)
    green_hp_bar_x_final = math.floor(bar_length * new_hp_ratio)

    # animate
    x_move_amount = [0, 0, 0, 0, 0, 0, 0, -1]
    x_move_index = 0
    while green_hp_bar_x_pos != green_hp_bar_x_final:
        # draw
        draw_grid()
        draw_entities(hard=False)
        pygame.draw.rect(SCREEN, BRIGHT_RED, (hp_bar_x, hp_bar_y, bar_length, bar_height))
        pygame.draw.rect(SCREEN, BRIGHT_GREEN, (hp_bar_x, hp_bar_y, green_hp_bar_x_pos, bar_height))
        pygame.display.flip()

        # load next animation frame
        green_hp_bar_x_pos = green_hp_bar_x_pos + x_move_amount[x_move_index]
        x_move_index = 0 if x_move_index == len(x_move_amount) - 1 else x_move_index + 1


def _blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


def _get_tile_img(tile, tint=None):
    if tile.texture_type == TileTexture.GRASS:
        if tint == TileTint.BLUE:
            return GRASS_BLUE_PNG
        elif tint == TileTint.RED:
            return GRASS_RED_PNG
        elif tint == TileTint.ORANGE:
            return GRASS_ORANGE_PNG
        else:
            return GRASS_PNG
    if tile.texture_type == TileTexture.DIRT:
        if tint == TileTint.BLUE:
            return DIRT_BLUE_PNG
        elif tint == TileTint.RED:
            return DIRT_RED_PNG
        elif tint == TileTint.ORANGE:
            return DIRT_ORANGE_PNG
        else:
            return DIRT_PNG
    elif tile.texture_type == TileTexture.STONE:
        if tint == TileTint.BLUE:
            return STONE_BLUE_PNG
        elif tint == TileTint.RED:
            return STONE_RED_PNG
        elif tint == TileTint.ORANGE:
            return STONE_ORANGE_PNG
        else:
            return STONE_PNG
    elif tile.texture_type == TileTexture.FLOOR:
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
