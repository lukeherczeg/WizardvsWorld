from draw import *
from classes.phase import Phase
from classes.entity import Player
from classes.tile import Tile


def select(row, col):
    # print(f"Highlighting ({row}, {col}).")
    draw_selected_tile(GRID.game_map[row][col])


class PlayerMovementPhase(Phase):
    player: Player
    currentTile: Tile
    grid: Grid
    immovable_tiles: [Tile]
    movable_tiles: [Tile]
    enemy_tiles: [Tile]
    occupied_index: int

    def __init__(self, player):
        self.player = player
        self.currentTile = player.currentTile
        self.grid = GRID
        self.immovable_tiles = None
        self.movable_tiles = None
        self.enemy_tiles = None
        self.occupied_index = 0

    def cyclic_last(self, tile_list, current_tile):
        self.occupied_index -= 1
        return tile_list[(current_tile - 1) % len(tile_list)]

    def cyclic_next(self, tile_list, current_tile):
        self.occupied_index += 1
        return tile_list[(current_tile + 1) % len(tile_list)]

    def select_tile(self, row, col):
        """Restricts tile selection based on the tile constraints passed to it.
           If there are no movable or enemy tiles, then it must be normal, free selection phase,
           if there are movable tiles, it sets constraints and tints for the movement phase,
           and if there are enemy tiles, it sets constraints for the attack phase."""

        if self.movable_tiles is None and self.enemy_tiles is None:
            if self.grid.is_valid_standable_tile(row, col):
                draw_tile(self.currentTile)
                self.currentTile = self.grid.game_map[row][col]
                # print(f"You moved to the tile at ({self.currentTile.row}, {self.currentTile.col})")
                select(self.currentTile.row, self.currentTile.col)
                draw_entities()
            else:
                print(f"The tile at ({row}, {col}) is invalid.")

        elif self.movable_tiles and self.grid.is_valid_tile_in_list(row, col, self.movable_tiles):
            draw_tinted_tiles(self.movable_tiles, self.player, TileTint.BLUE)
            self.currentTile = self.grid.game_map[row][col]
            # print(f"You are selecting the move to the tile at ({self.currentTile.row}, {self.currentTile.col})")
            select(self.currentTile.row, self.currentTile.col)

        elif self.enemy_tiles and self.grid.is_valid_tile_in_list(row, col, self.enemy_tiles):
            draw_tinted_tiles(self.enemy_tiles, self.player, TileTint.ORANGE)
            self.currentTile = self.grid.game_map[row][col]
            print(f"You are selecting to attack to the tile at ({self.currentTile.row}, {self.currentTile.col})")
            select(self.currentTile.row, self.currentTile.col)

    def select_by_keypress(self, event):
        row = self.currentTile.row
        col = self.currentTile.col
        if self.enemy_tiles is None:
            if event.key == pygame.K_LEFT:
                self.select_tile(row, col - 1)

            elif event.key == pygame.K_RIGHT:
                self.select_tile(row, col + 1)

            elif event.key == pygame.K_UP:
                self.select_tile(row - 1, col)

            elif event.key == pygame.K_DOWN:
                self.select_tile(row + 1, col)
        else:
            occupied_enemy_tiles = []

            for tile in self.enemy_tiles:
                if tile.occupied:
                    occupied_enemy_tiles.append(tile)

            if event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:
                hovered_tile = self.cyclic_next(occupied_enemy_tiles, self.occupied_index)
                self.select_tile(hovered_tile.row, hovered_tile.col)

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                hovered_tile = self.cyclic_last(occupied_enemy_tiles, self.occupied_index)
                self.select_tile(hovered_tile.row, hovered_tile.col)

    def selection(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if self.movable_tiles is None and self.enemy_tiles is None:
                        return True
                    elif self.movable_tiles:
                        if self.currentTile in self.movable_tiles:
                            return True
                    elif self.enemy_tiles:
                        if self.currentTile in self.enemy_tiles and self.currentTile.occupied:
                            return True

                self.select_by_keypress(event)

    def movement(self):
        movable_tiles = GRID.get_movement(self.currentTile.row, self.currentTile.col, self.player.max_Movement)
        self.immovable_tiles = GRID.get_movement_border(movable_tiles, self.player.range)
        self.movable_tiles = list(set(movable_tiles).difference(set(self.immovable_tiles)))
        draw_tinted_tiles(self.movable_tiles, self.player, TileTint.BLUE)
        draw_tinted_tiles(self.immovable_tiles, self.player, TileTint.RED)

        initial_pos = self.currentTile.col, self.currentTile.row

        select(self.currentTile.row, self.currentTile.col)
        selecting = True
        while selecting:
            if self.selection():
                # print(f"You picked the movable tile ({self.player.currentTile.row}, {self.player.currentTile.col})!"
                #       f" Time to move!")
                self.player.selected = False
                draw_entities()
                selecting = False

        self.player.currentTile = self.currentTile

        animate_move(self.player, initial_pos)
        # print("Okay, time to ATTACK!")

    def enter(self):
        self.enemy_tiles = None
        self.currentTile = self.player.currentTile
        # print('Entering Selection Phase...')
        total_refresh_drawing()
        select(self.currentTile.row, self.currentTile.col)
        selecting = True
        while selecting:
            if self.selection():
                if self.currentTile == self.player.currentTile:
                    # print(f"You picked the player's location! Time to pick your move!")
                    self.player.selected = True
                    draw_entities()
                    selecting = False

    def update(self):
        print('Entering Player Movement Selection...')
        self.movement()

    def exit(self):
        self.movable_tiles = None
        print('Exiting Player Movement Phase...')
