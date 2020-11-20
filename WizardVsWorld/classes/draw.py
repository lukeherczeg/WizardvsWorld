import pygame
import sys
import math
import time
import os
from WizardVsWorld.assets.image_loader import *
from WizardVsWorld.classes.const import TileTexture, TileTint, ENTITIES
from WizardVsWorld.classes.entity import Player, Archer, Knight, GreatKnight, WizardKing


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


def draw_rectangular_area(top_left, bottom_right):
    start = top_left.row, top_left.col
    end = bottom_right.row, bottom_right.col

    for i in range(start[0], end[0] + 1):
        for j in range(start[1], end[1] + 1):
            draw_tile(GRID.game_map[i][j])
            # print(f"Drew tile [{i}, {j}].")


def clear_tinted_tiles(tile_list, entity):
    draw_tinted_tiles(tile_list, entity, TileTint.NONE)


def draw_tinted_tiles(tile_list, entity, tint):
    for tile in tile_list:
        tile.tint = tint
        draw_tile(tile)
    for tile in tile_list:
        draw_entity_from_tile(tile)

    draw_entity(entity)
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


def draw_entities_in_rectangular_area(top_left, bottom_right):
    start = top_left.row, top_left.col
    end = bottom_right.row, bottom_right.col

    for entity in ENTITIES:
        if start[0] <= entity.currentTile.row <= end[0] and start[1] <= entity.currentTile.col <= end[1]:
            draw_entity(entity)


def check_for_entities_in_area(top_left, bottom_right):
    start = top_left.row, top_left.col
    end = bottom_right.row, bottom_right.col

    for entity in ENTITIES:
        if start[0] <= entity.currentTile.row <= end[0] and start[1] <= entity.currentTile.col <= end[1]:
            return True

    return False


def draw_entity_from_tile(tile):
    entity_to_draw = None
    for entity in ENTITIES:
        if entity.currentTile == tile:
            entity_to_draw = entity
            break

    if entity_to_draw is not None:
        draw_entity(entity_to_draw)


def draw_entity(entity):
    if entity.tiles is not None:
        if len(entity.tiles) > 1:
            for tile in entity.tiles:
                draw_tile(tile)

    entity_img = _get_entity_img(entity)
    entity_rect = entity_img.get_rect()

    entity_coords = (entity.get_position().col, entity.get_position().row)
    entity_rect = entity_rect.move(_calc_player_coords(entity_coords, entity_rect))
    SCREEN.blit(entity_img, entity_rect)
    pygame.display.update(entity_rect)


def draw_entities(ignorables=None, hard=True):
    if ignorables is None:
        entities = ENTITIES
    else:
        entities = filter(lambda entity: entity not in ignorables, ENTITIES)

    entity_rect = None
    for entity in entities:
        entity_img = _get_entity_img(entity)
        entity_rect = entity_img.get_rect()

        entity_coords = (entity.get_position().col, entity.get_position().row)
        entity_rect = entity_rect.move(_calc_player_coords(entity_coords, entity_rect))
        SCREEN.blit(entity_img, entity_rect)

        if hard: pygame.display.update(entity_rect)


def draw_text(message, size, tile=None, offset=None, color=WHITE):
    # GOTO provided tile
    x_pos = tile.col if tile is not None else 0
    y_pos = tile.row if tile is not None else 0

    # ADD offset to coords
    x_offset, y_offset = offset if offset is not None else (0, 0)
    x_pos, y_pos = x_pos + x_offset, y_pos + y_offset

    # Draw text
    message_font = pygame.font.Font('freesansbold.ttf', size)
    message_text = message_font.render(str(message), True, color)
    message_rect = message_text.get_rect()
    message_rect = message_rect.move([x_pos * BLOCK_SIZE, y_pos * BLOCK_SIZE])
    SCREEN.blit(message_text, message_rect)


def draw_text_abs(message, size, x_pos=0, y_pos=0, color=WHITE):
    # Draw text
    message_font = pygame.font.Font('freesansbold.ttf', size)
    message_text = message_font.render(str(message), True, color)
    message_rect = message_text.get_rect()
    message_rect.center = (x_pos, y_pos)
    SCREEN.blit(message_text, message_rect)
    pygame.display.flip()


def animate_text(message, size, tile=None, offset=None, color=WHITE, onscreen_time=0, background=None):
    # GOTO provided tile
    x_pos = tile.col if tile is not None else 0
    y_pos = tile.row if tile is not None else 0

    # ADD offset to coords
    x_offset, y_offset = offset if offset is not None else (0, 0)
    x_pos, y_pos = x_pos + x_offset, y_pos + y_offset

    message_font = pygame.font.Font('freesansbold.ttf', size)
    message_text = message_font.render(str(message), True, color)
    opacity = 0

    while opacity != 250:
        draw_grid()
        draw_entities(hard=False)
        if not background is None:
            _blit_alpha(SCREEN, background, (x_pos, y_pos), opacity)
        _blit_alpha(SCREEN, message_text, (x_pos, y_pos), opacity)
        pygame.display.flip()
        opacity = opacity + 1

    time.sleep(onscreen_time)

    while opacity != 0:
        draw_grid()
        draw_entities(hard=False)
        if not background is None:
            _blit_alpha(SCREEN, background, (x_pos, y_pos), opacity, True)
        _blit_alpha(SCREEN, message_text, (x_pos, y_pos), opacity, True)
        pygame.display.flip()
        opacity = opacity - 1

    total_refresh_drawing()


def animate_text_abs(message, size, x_pos=0, y_pos=0, color=WHITE, onscreen_time=0,
                     background=None, background_opacity_decrease=0):
    message_font = pygame.font.Font('freesansbold.ttf', size)
    message_text = message_font.render(str(message), True, color)
    opacity = 0

    while opacity != 250:
        draw_grid()
        draw_entities(hard=False)
        if not background is None:
            _blit_alpha(SCREEN, background, (x_pos, y_pos), opacity - background_opacity_decrease, True)
        _blit_alpha(SCREEN, message_text, (x_pos, y_pos), opacity, True)
        pygame.display.flip()
        opacity = opacity + 2

    time.sleep(onscreen_time)

    while opacity != 0:
        draw_grid()
        draw_entities(hard=False)
        if not background is None:
            _blit_alpha(SCREEN, background, (x_pos, y_pos), opacity - background_opacity_decrease, True)
        _blit_alpha(SCREEN, message_text, (x_pos, y_pos), opacity, True)
        pygame.display.flip()
        opacity = opacity - 2

    total_refresh_drawing()


def animate_entity_movement(entity, prev_tile, player=None):
    if isinstance(entity, Player):
        tile_list = GRID.path_to(prev_tile, entity.get_position())
    elif player is not None:
        tile_list = GRID.path_to(prev_tile, entity.get_position(), player)

    for i in range(len(tile_list) - 1):
        old_coords = (tile_list[i].col, tile_list[i].row)
        new_coords = (tile_list[i + 1].col, tile_list[i + 1].row)
        old_pos = _calc_player_coords(old_coords, _get_entity_img(entity).get_rect())
        new_pos = _calc_player_coords(new_coords, _get_entity_img(entity).get_rect())
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
    entity_rect = entity_rect.move(old_pos)

    # For animating perpendicular wiggle while walking and movement speed
    wiggle_index = 0

    # move horizontally
    while old_x != target_x:
        if old_x < target_x:
            entity_rect = entity_rect.move([MOVEMENT_SPEED, move_wiggle[wiggle_index]])
            old_x = old_x + MOVEMENT_SPEED
        elif old_x > target_x:
            entity_rect = entity_rect.move([-MOVEMENT_SPEED, move_wiggle[wiggle_index]])
            old_x = old_x - MOVEMENT_SPEED

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
            entity_rect = entity_rect.move([move_wiggle[wiggle_index], MOVEMENT_SPEED])
            old_y = old_y + MOVEMENT_SPEED
        elif old_y > target_y:
            entity_rect = entity_rect.move([move_wiggle[wiggle_index], -MOVEMENT_SPEED])
            old_y = old_y - MOVEMENT_SPEED

        wiggle_index = 0 if wiggle_index == len(move_wiggle) - 1 else wiggle_index + 1

        # redraw the grid and entities besides the one being animated,
        # then draw animation frame of entity
        draw_grid()
        draw_entities(ignorables=[entity])
        SCREEN.blit(entity_img, entity_rect)
        pygame.display.flip()


def animate_attack(attacker, victim):
    if isinstance(attacker, Knight) or isinstance(attacker, GreatKnight):
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


def animate_miss(victim):
    _animate_miss_text(victim)


def animate_damage(victim, victim_old_hp, crit=False):
    _animate_damage_number(victim, victim_old_hp, crit)

    time.sleep(0.2)

    _animate_damage_bar(victim, victim_old_hp)


def animate_death(entity):
    entity_img = _get_entity_img(entity)
    wiggle_index = 0
    opacity = 250

    while opacity != 0:
        draw_grid()
        draw_entities()
        entity_pos = (entity.get_position().col, entity.get_position().row)
        entity_pos = _calc_player_coords(entity_pos, entity_img.get_rect(), (move_wiggle[wiggle_index], 0))
        _blit_alpha(SCREEN, entity_img, tuple(entity_pos), opacity)
        pygame.display.flip()

        wiggle_index = 0 if wiggle_index == len(move_wiggle) - 1 else wiggle_index + 1
        opacity = opacity - 2

    total_refresh_drawing()


def animate_map_transition(old_grid, old_enemies, player):
    new_grid_offset = WINDOW_WIDTH
    old_grid_offset = 0

    player_x = player.get_position().col * BLOCK_SIZE
    player_y = player.get_position().row * BLOCK_SIZE
    player_target_x = player_x + BLOCK_SIZE

    # For animating perpendicular wiggle while walking and movement speed
    wiggle_index = 0
    x_index = 0

    move_x = [0, 0, 0, 0, 0, 0, 0, 0, 1]

    while new_grid_offset >= 0:
        for _, col in enumerate(old_grid.game_map):
            for _, tile in enumerate(col):
                tile_img = _get_tile_img(tile)
                tile_rect = tile_img.get_rect()
                tile_rect = tile_rect.move([(tile.col * BLOCK_SIZE) + old_grid_offset, tile.row * BLOCK_SIZE])
                SCREEN.blit(tile_img, tile_rect)

        for _, col in enumerate(GRID.game_map):
            for _, tile in enumerate(col):
                tile_img = _get_tile_img(tile)
                tile_rect = tile_img.get_rect()
                tile_rect = tile_rect.move([(tile.col * BLOCK_SIZE) + new_grid_offset, tile.row * BLOCK_SIZE])
                SCREEN.blit(tile_img, tile_rect)

        if (player_x < player_target_x):
            player_x = player_x + move_x[x_index]
            player_y = player_y + move_wiggle[wiggle_index]

            x_index = 0 if x_index == len(move_x) - 1 else x_index + 1
            wiggle_index = 0 if wiggle_index == len(move_wiggle) - 1 else wiggle_index + 1

        player_img = _get_entity_img(player)
        player_rect = player_img.get_rect()
        player_rect = player_rect.move([player_x + old_grid_offset, player_y])

        SCREEN.blit(player_img, player_rect)

        for entity in old_enemies:
            entity_img = _get_entity_img(entity)
            entity_rect = entity_img.get_rect()
            entity_pos = (entity.get_position().col, entity.get_position().row)
            entity_pos = _calc_player_coords(entity_pos, entity_rect, (old_grid_offset, 0))
            entity_rect = entity_rect.move(entity_pos)
            SCREEN.blit(entity_img, entity_rect)

        entities = ENTITIES[1:]

        for entity in entities:
            entity_img = _get_entity_img(entity)
            entity_rect = entity_img.get_rect()
            entity_pos = (entity.get_position().col, entity.get_position().row)
            entity_pos = _calc_player_coords(entity_pos, entity_rect, (new_grid_offset, 0))
            entity_rect = entity_rect.move(entity_pos)
            SCREEN.blit(entity_img, entity_rect)

        new_grid_offset = new_grid_offset - 1
        old_grid_offset = old_grid_offset - 1

        pygame.display.flip()

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


def _animate_miss_text(victim):
    # create number rect
    number_font = pygame.font.Font('freesansbold.ttf', 16)
    number_font.set_bold(False)
    number_font.set_italic(False)
    number_text = number_font.render("Miss!", True, BLACK)
    number_rect = number_text.get_rect()
    number_y_var = (victim.get_position().row * BLOCK_SIZE + 8)
    number_x_fixed = (victim.get_position().col * BLOCK_SIZE) + 30
    number_rect = number_rect.move([number_x_fixed, number_y_var])

    victim_rect = _get_entity_img(victim).get_rect()
    victim_rect = victim_rect.move([victim.get_position().col * BLOCK_SIZE, victim.get_position().row * BLOCK_SIZE])

    # animation arrays and indexes
    y_move_amount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1]
    y_move_index = 0
    wiggle_index = 0
    wiggle_length = 160
    for i in range(wiggle_length):
        number_rect = number_rect.move([0, y_move_amount[y_move_index]])

        victim_rect = victim_rect.move([dodge_wiggle[wiggle_index], 0])

        # prepare next frame
        y_move_index = 0 if y_move_index == len(y_move_amount) - 1 else y_move_index + 1
        wiggle_index = 0 if wiggle_index == len(dodge_wiggle) - 1 else wiggle_index + 1

        # # draw
        draw_grid()
        draw_entities(hard=False, ignorables=[victim])
        SCREEN.blit(_get_entity_img(victim), victim_rect)
        SCREEN.blit(number_text, number_rect)
        pygame.display.flip()

    total_refresh_drawing()


def _animate_damage_number(victim, victim_old_hp, crit):
    damage_diff = victim_old_hp - victim.health

    if crit:
        crit_font = pygame.font.Font('freesansbold.ttf', 10)
        crit_font.set_bold(True)
        crit_font.set_italic(True)
        crit_text = crit_font.render('CRIT!', True, BRIGHT_RED)
        crit_rect = crit_text.get_rect()
        crit_y_var = victim.get_position().row * BLOCK_SIZE + 4
        crit_x_fixed = victim.get_position().col * BLOCK_SIZE + 30
        crit_rect = crit_rect.move([crit_x_fixed, crit_y_var])

    # create number rect
    number_font = pygame.font.Font('freesansbold.ttf', 17 if crit else 16)
    number_font.set_bold(True)
    number_font.set_italic(True) if crit else number_font.set_italic(False)
    number_text = number_font.render(str(damage_diff), True, BRIGHT_RED)
    number_rect = number_text.get_rect()
    number_y_var = (victim.get_position().row * BLOCK_SIZE + 12) if crit else \
        (victim.get_position().row * BLOCK_SIZE + 8)
    number_x_fixed = (victim.get_position().col * BLOCK_SIZE) + 30
    number_rect = number_rect.move([number_x_fixed, number_y_var])

    # create victim rect
    victim_rect = _get_entity_img(victim).get_rect()
    victim_coords = _calc_player_coords((victim.get_position().col, victim.get_position().row), victim_rect)
    victim_rect = victim_rect.move(victim_coords)

    # animation arrays and indexes
    y_move_amount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1]
    y_move_index = 0
    wiggle_index = 0
    # They wiggle for more time if they get crit
    wiggle_length = (300 if crit else 160)
    for i in range(wiggle_length):
        # animate
        number_rect = number_rect.move([0, y_move_amount[y_move_index]])

        if crit:
            crit_rect = crit_rect.move([0, y_move_amount[y_move_index]])
            victim_rect = victim_rect.move([move_wiggle[wiggle_index] * 1.9, 0])
        else:
            victim_rect = victim_rect.move([move_wiggle[wiggle_index], 0])

        # prepare next frame
        y_move_index = 0 if y_move_index == len(y_move_amount) - 1 else y_move_index + 1
        wiggle_index = 0 if wiggle_index == len(move_wiggle) - 1 else wiggle_index + 1

        # draw
        draw_grid()
        draw_entities(hard=False, ignorables=[victim])
        SCREEN.blit(_get_entity_img(victim), victim_rect)
        if crit:
            SCREEN.blit(crit_text, crit_rect)
        SCREEN.blit(number_text, number_rect)
        pygame.display.flip()

    total_refresh_drawing()


def _animate_damage_bar(victim, victim_old_hp):
    # HP bar math 4px by 42px (old : 24)
    hp_bar_y = ((victim.get_position().row + 1) * BLOCK_SIZE) - _get_entity_img(victim).get_rect().size[1]
    hp_bar_x = (victim.get_position().col * BLOCK_SIZE) - 1  # (old: + 4)
    bar_length = 42
    bar_height = 4

    # get ratios for scaling health reduction graphically
    new_hp_ratio = victim.health / victim.max_health
    old_hp_ratio = victim_old_hp / victim.max_health

    # prevent negative health
    if new_hp_ratio < 0:
        new_hp_ratio = 0

    # track start and stop of green movement
    green_hp_bar_x_pos = math.floor(bar_length * old_hp_ratio)
    green_hp_bar_x_final = math.floor(bar_length * new_hp_ratio)

    # animate
    x_move_amount = [0, 0, 0, 0, 0, 0, 0, -1]
    x_move_index = 0
    while green_hp_bar_x_pos >= green_hp_bar_x_final:
        # draw
        draw_grid()
        draw_entities(hard=False)
        pygame.draw.rect(SCREEN, BRIGHT_RED, (hp_bar_x, hp_bar_y, bar_length, bar_height))
        if ((green_hp_bar_x_final != green_hp_bar_x_pos) or new_hp_ratio != 0):
            pygame.draw.rect(SCREEN, BRIGHT_GREEN, (hp_bar_x, hp_bar_y, green_hp_bar_x_pos, bar_height))
        pygame.display.flip()

        # load next animation frame
        green_hp_bar_x_pos = green_hp_bar_x_pos + x_move_amount[x_move_index]
        x_move_index = 0 if x_move_index == len(x_move_amount) - 1 else x_move_index + 1


def _blit_alpha(target, source, location, opacity, centered=False):
    x = location[0] if not centered else location[0] - (source.get_width() // 2)
    y = location[1] if not centered else location[1] - (source.get_height() // 2)
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, (x, y))


def _get_tile_img(tile):
    if tile.texture_type == TileTexture.GRASS:
        if tile.tint == TileTint.BLUE:
            return GRASS_BLUE_PNG
        elif tile.tint == TileTint.RED:
            return GRASS_RED_PNG
        elif tile.tint == TileTint.ORANGE:
            return GRASS_ORANGE_PNG
        else:
            return GRASS_PNG
    if tile.texture_type == TileTexture.DIRT:
        if tile.tint == TileTint.BLUE:
            return DIRT_BLUE_PNG
        elif tile.tint == TileTint.RED:
            return DIRT_RED_PNG
        elif tile.tint == TileTint.ORANGE:
            return DIRT_ORANGE_PNG
        else:
            return DIRT_PNG
    elif tile.texture_type == TileTexture.STONE:
        if tile.tint == TileTint.BLUE:
            return STONE_BLUE_PNG
        elif tile.tint == TileTint.RED:
            return STONE_RED_PNG
        elif tile.tint == TileTint.ORANGE:
            return STONE_ORANGE_PNG
        else:
            return STONE_PNG
    elif tile.texture_type == TileTexture.FLOOR:
        if tile.tint == TileTint.BLUE:
            return FLOOR_BLUE_PNG
        elif tile.tint == TileTint.RED:
            return FLOOR_RED_PNG
        elif tile.tint == TileTint.ORANGE:
            return FLOOR_ORANGE_PNG
        else:
            return FLOOR_PNG
    elif tile.texture_type == TileTexture.BUSH:
        if tile.tint == TileTint.ORANGE:
            return BUSH_ORANGE_PNG
        elif tile.tint == TileTint.RED:
            return BUSH_RED_PNG
        else:
            return BUSH_PNG


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

    if isinstance(entity, GreatKnight):
        if entity.attacking:
            return GREATKNIGHT_ATTACK_PNG
        elif entity.damaged:
            return GREATKNIGHT_HURT_PNG
        else:
            return GREATKNIGHT_PNG

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

    if isinstance(entity, WizardKing):
        return WIZARDKING_PNG


def _calc_player_coords(entity_pos, entity_rect, offset=None):
    x_point = (entity_pos[0] * BLOCK_SIZE) - ((entity_rect.size[0] - BLOCK_SIZE) / 2)
    y_point = (entity_pos[1] * BLOCK_SIZE) - (entity_rect.size[1] - BLOCK_SIZE) - 3

    if offset:
        x_point = x_point + offset[0]
        y_point = y_point + offset[1]

    return [x_point, y_point]


def quit_game():
    pygame.quit()
    sys.exit()
