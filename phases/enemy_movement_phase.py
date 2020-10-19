from classes.tile import Tile
from classes.entity import Enemy, Entity
from draw import *
from classes.phase import Phase
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
        if distance > 5:
            return False
        else:
            return True

    def move_enemy(self, enemy):
        movable_tiles = GRID.get_movement(enemy.currentTile.row, enemy.currentTile.col, enemy.max_movement, self.Player)
        movable_tiles.remove(enemy.currentTile)

        # Here we copy the movable_tiles array so that we can safely remove elements.
        # We remove every tile that is not closer to the player.
        closer_movable_tiles = movable_tiles.copy()
        for tile in movable_tiles:
            if not self.gets_closer(enemy, tile):  # tile is self.player_position or
                closer_movable_tiles.remove(tile)

        movable_tiles = closer_movable_tiles

        # If we are right next to the player, there are no tiles closer; so stay there!
        if len(movable_tiles) == 0:
            return

        # Otherwise, we pick one of the closer tiles at random.
        init_tile = enemy.get_position()
        new_tile = movable_tiles[random.randint(0, len(movable_tiles) - 1)]

        # Grab tiles adjacent to player
        tiles_adjacent_to_player = GRID.get_movement(self.player_position.row, self.player_position.col, 1)
        tiles_adjacent_to_player.remove(self.player_position)

        # If it's a knight, rush the player!
        if isinstance(enemy, Knight):
            for tile in tiles_adjacent_to_player:
                if tile in movable_tiles:
                    new_tile = tile
                    break
        # If it's an archer, move to a space one away from the player to shoot an arrow!
        elif isinstance(enemy, Archer):
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
        draw_tinted_tiles(movable_tiles, enemy, TileTint.BLUE)
        draw_selected_tile(enemy.currentTile)
        time.sleep(.2)
        draw_tile(enemy.currentTile)
        draw_entities()
        draw_selected_tile(new_tile)
        time.sleep(.2)

        # Old determination of tiles to move to:
        # cannot_move = True
        # while cannot_move:
        #     cannot_move = self.gets_closer(enemy, movable_tiles[new_tile])
        #     if cannot_move:
        #         new_tile = random.randint(0, len(movable_tiles) - 1)

        enemy.currentTile.occupied = False
        enemy.currentTile = new_tile
        animate_entity_movement(enemy, init_tile, self.Player)
        enemy.currentTile.occupied = True
        time.sleep(0.3)

    def enter(self):
        self.Enemies = ENTITIES[1:]
        background = pygame.transform.scale(BACKGROUND_PNG, (750, 300))
        animate_text_abs('Enemy Phase', 100, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, RED, 1, background, 15)
        self.player_position = ENTITIES[0].currentTile
        total_refresh_drawing()

    def update(self):
        print('Entering Enemy Movement Computation / Animation...')
        for enemy in self.Enemies:
            if self.can_move(enemy):
                self.move_enemy(enemy)

    def exit(self):
        print('Exiting Enemy Phase...')
