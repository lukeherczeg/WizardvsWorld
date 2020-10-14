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

    def select_tile(self, row, col):
        if self.grid.is_valid_standable_tile(row, col):
            draw_tile(self.currentTile)
            self.currentTile = self.grid.game_map[row][col]
            print(f"You moved to the tile at ({self.currentTile.row}, {self.currentTile.col})")
            select(self.currentTile.row, self.currentTile.col)
            draw_entities()
        else:
            print(f"The tile at ({row}, {col}) is invalid.")

    def selection(self):
        select(self.currentTile.row, self.currentTile.col)
        selecting = True
        while selecting:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    row = self.currentTile.row
                    col = self.currentTile.col

                    if event.key == pygame.K_RETURN:
                        if self.currentTile == self.player.currentTile:
                            print(f"You picked the player's location! Time to move!")
                            self.player.selected = True
                            draw_entities()
                            selecting = False
                        else:
                            print(f"You tried to pick the tile at ({row}, {col})"
                                  f", that's not the player silly!")

                    if event.key == pygame.K_LEFT:
                        self.select_tile(row, col - 1)

                    elif event.key == pygame.K_RIGHT:
                        self.select_tile(row, col + 1)

                    elif event.key == pygame.K_UP:
                        self.select_tile(row - 1, col)

                    elif event.key == pygame.K_DOWN:
                        self.select_tile(row + 1, col)

    def movement(self):
        movable_tiles = GRID.get_movement(self.currentTile.row, self.currentTile.col, self.player.max_Movement)
        movable_tiles_border = GRID.get_movement_border(movable_tiles, self.player.range)
        draw_tinted_tiles(movable_tiles, self.player, TileTint.BLUE)
        draw_tinted_tiles(movable_tiles_border, self.player, TileTint.RED)

    def enter(self):
        print('Entering Selection Phase...')
        self.selection()

    def update(self):
        print('Entering Player Movement Selection...')
        self.movement()

    def exit(self):
        print('Exiting Phase 1...')
