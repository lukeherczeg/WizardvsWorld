from draw import *
from classes.phase import Phase
from classes.entity import Player
from classes.tile import Tile


def select(row, col):
    print(f"Highlighting ({row}, {col}).")
    draw_selected_tile(GRID.game_map[row][col])


class PlayerMovementPhase(Phase):
    player: Player
    currentTile: Tile
    grid: Grid

    def __init__(self, player):
        self.player = player
        self.currentTile = player.currentTile
        self.grid = GRID

    def select_tile(self, row, col, movable_tiles=None):
        if movable_tiles is None:
            if self.grid.is_valid_standable_tile(row, col):
                draw_tile(self.currentTile)
                self.currentTile = self.grid.game_map[row][col]
                print(f"You moved to the tile at ({self.currentTile.row}, {self.currentTile.col})")
                select(self.currentTile.row, self.currentTile.col)
                draw_entities()
            else:
                print(f"The tile at ({row}, {col}) is invalid.")
        else:
            if self.grid.is_valid_standable_tile(row, col) and self.grid.game_map[row][col] in movable_tiles:
                draw_tinted_tiles(movable_tiles, self.player, TileTint.BLUE)
                self.currentTile = self.grid.game_map[row][col]
                print(f"You are selecting the move to the tile at ({self.currentTile.row}, {self.currentTile.col})")
                select(self.currentTile.row, self.currentTile.col)

    def selection(self, movable_tiles=None):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                row = self.currentTile.row
                col = self.currentTile.col

                if event.key == pygame.K_RETURN:
                    if movable_tiles is None:
                        return True
                    else:
                        if self.currentTile in movable_tiles:
                            return True

                # If we didn't call with movable tiles, then we can move the selector anywhere
                if movable_tiles is None:
                    if event.key == pygame.K_LEFT:
                        self.select_tile(row, col - 1)

                    elif event.key == pygame.K_RIGHT:
                        self.select_tile(row, col + 1)

                    elif event.key == pygame.K_UP:
                        self.select_tile(row - 1, col)

                    elif event.key == pygame.K_DOWN:
                        self.select_tile(row + 1, col)

                # If movable_tiles exist, then we are selecting only in the bounds of valid movement
                else:
                    if event.key == pygame.K_LEFT:
                        self.select_tile(row, col - 1, movable_tiles)

                    elif event.key == pygame.K_RIGHT:
                        self.select_tile(row, col + 1, movable_tiles)

                    elif event.key == pygame.K_UP:
                        self.select_tile(row - 1, col, movable_tiles)

                    elif event.key == pygame.K_DOWN:
                        self.select_tile(row + 1, col, movable_tiles)

    def movement(self):
        movable_tiles = GRID.get_movement(self.currentTile.row, self.currentTile.col, self.player.max_Movement)
        movable_tiles_border = GRID.get_movement_border(movable_tiles, self.player.range)
        updated_movable_tiles = list(set(movable_tiles).difference(set(movable_tiles_border)))
        draw_tinted_tiles(updated_movable_tiles, self.player, TileTint.BLUE)
        draw_tinted_tiles(movable_tiles_border, self.player, TileTint.RED)

        initial_pos = self.currentTile.col, self.currentTile.row

        select(self.currentTile.row, self.currentTile.col)
        selecting = True
        while selecting:
            if self.selection(updated_movable_tiles):
                print(f"You picked the movable tile ({self.player.currentTile.row}, {self.player.currentTile.col})!"
                      f" Time to move!")
                self.player.selected = False
                draw_entities()
                selecting = False

        self.player.currentTile = self.currentTile

        animate_move(self.player, initial_pos)
        print("Okay, time to ATTACK!")

    def enter(self):
        print('Entering Selection Phase...')
        draw_entities()
        select(self.currentTile.row, self.currentTile.col)
        selecting = True
        while selecting:
            if self.selection():
                if self.currentTile == self.player.currentTile:
                    print(f"You picked the player's location! Time to pick your move!")
                    self.player.selected = True
                    draw_entities()
                    selecting = False

    def update(self):
        print('Entering Player Movement Selection...')
        self.movement()

    def exit(self):
        print('Exiting Phase 1...')
