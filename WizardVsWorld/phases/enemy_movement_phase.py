from WizardVsWorld.classes.tile import Tile
from WizardVsWorld.classes.entity import Entity, Boss, GreatMarksman, WizardKing
from WizardVsWorld.classes.draw import *
from WizardVsWorld.classes.phase import Phase
import random
import math


class EnemyAIMovement(Phase):
    player_position: Tile
    Enemies: [Entity]
    grid: Grid

    def __init__(self):
        self.Enemies = ENTITIES[1:]
        self.Player = ENTITIES[0]
        self.player_position = self.Player.get_position()
        self.grid = GRID

    def gets_closer(self, enemy, new_position):
        p1 = [self.player_position.row, self.player_position.col]
        p2 = [enemy.currentTile.row, enemy.currentTile.col]
        p3 = [new_position.row, new_position.col]

        curr_distance_to_player = math.sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))
        new_distance_to_player = math.sqrt(((p3[0] - p1[0]) ** 2) + ((p3[1] - p1[1]) ** 2))

        if curr_distance_to_player > new_distance_to_player:
            return True
        else:
            return False

    def can_move(self, enemy):
        p1 = [self.player_position.row, self.player_position.col]
        p2 = [enemy.currentTile.row, enemy.currentTile.col]
        distance = int(math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)))
        if isinstance(enemy, Boss):
            if distance <= self.Player.range:
                enemy.max_movement = self.Player.range
                return True
            else:
                enemy.max_movement = 0
                return False
        else:
            if distance > 5:
                return False
            else:
                return True

    def untrap_multi_tile_boss(self, enemy):
        if len(enemy.tiles) > 1:
            scales = enemy.get_dimensions()
            GRID.game_map[int(enemy.currentTile.row - 1)][
                int(enemy.currentTile.col)].standable = True

    def add_and_check_tiles(self, tile, dimensions, value, direction):
        if direction == "up":
            new_tile = GRID.game_map[int(tile.row - (dimensions[0] - value))][int(tile.col)]
        elif direction == "down":
            new_tile = GRID.game_map[int(tile.row + (dimensions[0] - value))][int(tile.col)]
        elif direction == "left":
            new_tile = GRID.game_map[int(tile.row)][int(tile.col - (dimensions[1] - value))]
        elif direction == "right":
            new_tile = GRID.game_map[int(tile.row)][int(tile.col + (dimensions[1] - value))]
        if new_tile.standable:
            return new_tile, True
        else:
            return new_tile, False

    def remove_tiles_for_bigger_sprites(self, enemy, movable_tiles, enemy_positions, dimensions):
        tiles = movable_tiles.copy()
        if len(enemy.tiles) > 1:
            position_array = []
            width_value = 1
            for tile in tiles:
                for height_value in range(1, dimensions[0]):
                    temp_tile, return_bool = self.add_and_check_tiles(tile, dimensions, height_value, "up")
                    if return_bool:
                        position_array.append(temp_tile)
                    while True:
                        temp_tile, return_bool = self.add_and_check_tiles(tile, dimensions, height_value, "left")
                        if return_bool:
                            position_array.append(temp_tile)
                        temp_tile, return_bool = self.add_and_check_tiles(tile, dimensions, height_value, "right")
                        if return_bool:
                            position_array.append(temp_tile)
                        if width_value == dimensions[1] - 1 or dimensions[1] - 1 == 0:
                            break
                        width_value += 1
                pos_set = set(position_array)
                enemies_set = set(enemy_positions)
                # false if the intersection is empty set
                output = False if (pos_set.intersection(enemies_set) == set()) else True
                if output:
                    movable_tiles.remove(tile)

    def move_enemy(self, enemy):
        if isinstance(enemy, Boss):
            self.untrap_multi_tile_boss(enemy)
        movable_tiles = GRID.get_movement(enemy.currentTile.row, enemy.currentTile.col, enemy.max_movement, self.Player)
        movable_tiles.remove(enemy.currentTile)
        enemy_positions = []
        for entity in ENTITIES:
            enemy_positions.append(entity.currentTile)
        enemy_positions.remove(enemy.currentTile)


        # Here we copy the movable_tiles array so that we can safely remove elements.
        # We remove every tile that is not closer to the player.
        closer_movable_tiles = movable_tiles.copy()
        for tile in movable_tiles:
            if not self.gets_closer(enemy, tile):  # tile is self.player_position or
                closer_movable_tiles.remove(tile)

        movable_tiles = closer_movable_tiles
        if isinstance(enemy, WizardKing):
            dimensions = enemy.get_dimensions()
            self.remove_tiles_for_bigger_sprites(enemy, movable_tiles, enemy_positions, dimensions)
        # If we are right next to the player, there are no tiles closer; so stay there!
        if len(movable_tiles) == 0:
            return

        # Otherwise, we pick one of the closer tiles at random.
        init_tile = enemy.get_position()
        new_tile = movable_tiles[random.randint(0, len(movable_tiles) - 1)]

        # Grab tiles adjacent to player
        tiles_adjacent_to_player = GRID.get_movement(self.player_position.row, self.player_position.col, 1)
        tiles_adjacent_to_player.remove(self.player_position)

        # dive sprite size by blocksize
        # If it's a knight, rush the player!
        if isinstance(enemy, Knight) or isinstance(enemy, GreatKnight):
            if len(enemy.tiles) == 1:
                for tile in tiles_adjacent_to_player:
                    if tile in movable_tiles:
                        new_tile = tile
                        break
            else:
                for tile in tiles_adjacent_to_player:
                    if tile in movable_tiles:
                        new_tile = tile
                        break
        # If it's an archer, move to a space one away from the player to shoot an arrow!
        elif isinstance(enemy, Archer) or isinstance(enemy, GreatMarksman) or isinstance(enemy, WizardKing):
            # Grab tiles exclusively one space away from the player on all sides
            tiles_one_away_from_player = GRID.get_movement(self.player_position.row, self.player_position.col, 2)
            tiles_one_away_from_player.remove(self.player_position)
            tiles_one_away_from_player = [tile for tile in tiles_one_away_from_player
                                          if tile not in tiles_adjacent_to_player]
            for tile in tiles_one_away_from_player:
                if tile in movable_tiles:
                    new_tile = tile
                    break

        # Drawing enemy movement decision
        draw_tinted_tiles(movable_tiles, TileTint.BLUE)
        draw_selected_tile(enemy.currentTile)
        time.sleep(.2)
        draw_tile(enemy.currentTile)
        draw_entity_from_tile(enemy.currentTile)
        draw_selected_tile(new_tile)
        time.sleep(.2)
        clear_tinted_tiles(movable_tiles)

        enemy.currentTile.occupied = False
        enemy.currentTile = new_tile
        animate_entity_movement(enemy, init_tile, self.Player)
        enemy.currentTile.occupied = True
        if isinstance(enemy, WizardKing):
            enemy.tiles.clear()
            enemy.populate_tiles(enemy.height_tiles, enemy.width_tiles)
        time.sleep(0.3)

    def enter(self):
        self.Enemies = ENTITIES[1:]
        background = pygame.transform.scale(BACKGROUND_PNG, (562, 225))
        animate_text_abs('Enemy Phase', 75, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, BRIGHT_RED, 1, background, 15)
        self.player_position = ENTITIES[0].currentTile
        total_refresh_drawing()

    def update(self):
        for enemy in self.Enemies:
            if self.can_move(enemy):
                self.move_enemy(enemy)

    def exit(self):
        return
