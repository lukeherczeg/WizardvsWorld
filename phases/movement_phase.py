from game import *
from classes.phase import Phase
from classes.entity import Player
from classes.tile import Tile
from classes.grid import Grid

def highlight_tile(row, col):
    SCREEN.fill(BLACK)
    draw_grid()
    rect = pygame.Rect((col * BLOCK_SIZE), (row * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(SCREEN, WHITE, rect)
    pygame.display.update()


class PlayerMovementPhase(Phase):
    player: Player
    currentTile: Tile
    grid: Grid

    def __init__(self, player, grid):
        self.player = player
        self.currentTile = player.currentTile
        self.grid = grid

    def select_tile(self, row, col):
        if self.grid.is_valid_tile(row, col):
            self.currentTile = self.grid.game_map[row][col]
            print(f"You moved to the tile at ({self.currentTile.row}, {self.currentTile.col})")
            highlight_tile(self.currentTile.row, self.currentTile.col)
        else:
            print(f"The tile at ({row}, {col}) is invalid.")

    def selection(self):
        highlight_tile(self.currentTile.row, self.currentTile.col)
        selecting = True
        while selecting:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    row = self.currentTile.row
                    col = self.currentTile.col

                    if event.key == pygame.K_RETURN:
                        if self.currentTile == self.player.currentTile:
                            print(f"You picked the player's location! Time to move!")
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

    def enter(self):
        print('Entering Selection Phase...')
        self.selection()

    def update(self):
        print('Entering Player Movement Selection...')

    def exit(self):
        print('Exiting Phase 1...')
