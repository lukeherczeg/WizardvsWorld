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
    for x, col in enumerate(grid.game_map):
        for y, tile in enumerate(col):
            draw_tile(pygame, screen, tile)
    pygame.display.flip()

def draw_tile(pygame, screen, tile):
    tile_img = pygame.image.load(_get_tile_img(tile))
    tile_rect = tile_img.get_rect()
    tile_rect = tile_rect.move([tile.col * BLOCK_SIZE, tile.row * BLOCK_SIZE])
    screen.blit(tile_img, tile_rect)

def draw_characters(pygame, screen, entities):
    for entity in entities:
        entity_img = pygame.image.load(_get_entity_img(None))
        entity_rect = entity_img.get_rect()
        entity_rect = entity_rect.move([entity.get_position().col * BLOCK_SIZE, entity.get_position().row * BLOCK_SIZE])
        screen.blit(entity_img, entity_rect)

    pygame.display.flip()

def _get_tile_img(tile):
    main_directory = os.path.dirname('WizardvsWorld')
    asset_path = os.path.join(main_directory, 'assets')
    if(tile.standable):
        return os.path.join(asset_path, 'grass.png')
    else:
        return os.path.join(asset_path, 'stone.png')

def _get_entity_img(entity):
    main_directory = os.path.dirname('WizardvsWorld')
    asset_path = os.path.join(main_directory, 'assets')
    return os.path.join(asset_path, 'archer.png')
    
def quit_game(pygame):
    pygame.quit()
    sys.exit()