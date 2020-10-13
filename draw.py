import sys
import os
from classes.grid import Grid

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1000
BLOCK_SIZE = 40

def init(pygame):
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.fill(BLACK)
    grid = Grid(WINDOW_WIDTH // BLOCK_SIZE, WINDOW_HEIGHT // BLOCK_SIZE)
    return screen, grid

def draw_grid(pygame, screen, grid):
    for x in range(grid.GRID_WIDTH):
        for y in range(grid.GRID_HEIGHT):
            tile_img = pygame.image.load(_get_tile_img(grid.game_map[x][y]))
            tile_rect = tile_img.get_rect()
            tile_rect = tile_rect.move([x * BLOCK_SIZE, y * BLOCK_SIZE])
            screen.blit(tile_img, tile_rect)
    pygame.display.flip()

def draw_characters():
    return 0

def _get_tile_img(tile):
    main_directory = os.path.dirname('WizardvsWorld')
    asset_path = os.path.join(main_directory, 'assets')
    if(tile.standable):
        return os.path.join(asset_path, 'grass.png')
    else:
        return os.path.join(asset_path, 'stone.png')

def quit_game(pygame):
    pygame.quit()
    sys.exit()