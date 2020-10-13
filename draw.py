import sys
import os
from classes.grid import Grid

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1000
BLOCK_SIZE = 40
X_MOVEMENT_SPEED = 2
Y_MOVEMENT_SPEED = 2

def init(pygame):
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.fill(BLACK)
    grid = Grid(WINDOW_WIDTH // BLOCK_SIZE, WINDOW_HEIGHT // BLOCK_SIZE)
    return screen, grid

def redraw(pygame, screen, grid, entities):
    draw_grid(pygame, screen, grid)
    draw_characters(pygame, screen, entities)

def draw_grid(pygame, screen, grid):
    for _, col in enumerate(grid.game_map):
        for _, tile in enumerate(col):
            tile_img = pygame.image.load(_get_tile_img(tile)).convert()
            tile_rect = tile_img.get_rect()
            tile_rect = tile_rect.move([tile.col * BLOCK_SIZE, tile.row * BLOCK_SIZE])
            screen.blit(tile_img, tile_rect)
    pygame.display.flip()

def draw_tile(pygame, screen, tile):
    tile_img = pygame.image.load(_get_tile_img(tile)).convert()
    tile_rect = tile_img.get_rect()
    tile_rect = tile_rect.move([tile.col * BLOCK_SIZE, tile.row * BLOCK_SIZE])
    screen.blit(tile_img, tile_rect)
    pygame.display.flip()

def draw_characters(pygame, screen, entities):
    for entity in entities:
        entity_img = pygame.image.load(_get_entity_img(None)).convert_alpha()
        entity_rect = entity_img.get_rect()
        entity_rect = entity_rect.move([entity.get_position().col * BLOCK_SIZE, entity.get_position().row * BLOCK_SIZE])
        screen.blit(entity_img, entity_rect)

    pygame.display.flip()

def move_player(pygame, screen, grid, entity, oldPos):
    target_x, target_y = entity.get_position().col, entity.get_position().row
    old_x, old_y = oldPos
    entity_img = pygame.image.load(_get_entity_img(entity)).convert_alpha()
    entity_rect = entity_img.get_rect()
    while(old_x != target_x or old_y != target_y):
        if old_x < target_x:
            entity_rect = entity_rect.move([X_MOVEMENT_SPEED, 0])
            old_x = old_x + 1
        elif old_x > target_x:
            entity_rect = entity_rect.move([-X_MOVEMENT_SPEED, 0])
            old_x = old_x - 1
        if old_y < target_y:
            entity_rect = entity_rect.move([0, Y_MOVEMENT_SPEED])
            old_y = old_y + 1
        elif old_y > target_y:
            entity_rect = entity_rect.move([0, -Y_MOVEMENT_SPEED])
            old_y = old_y - 1
        print(old_x, old_y)
        entity_rect = entity_rect.move([old_x, old_y])
        draw_grid(pygame,screen, grid)
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