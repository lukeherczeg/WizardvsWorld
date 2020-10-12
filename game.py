import pygame
import sys
import wsl

from classes.grid import Grid

wsl.set_display_to_host()

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (200, 0, 0)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1000
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BLOCK_SIZE = 40 # Set the size of the grid block
GRID = Grid(WINDOW_WIDTH // BLOCK_SIZE, WINDOW_HEIGHT // BLOCK_SIZE)

print(f'Grid Width: {GRID.GRID_WIDTH}; Grid Height: {GRID.GRID_HEIGHT}')


def main():
    pygame.init()
    clock = pygame.time.Clock()
    SCREEN.fill(BLACK)
    draw_button_2 = False

    # Main game loop
    while True:
        draw_grid()
        button = pygame.Rect(0, 0, 39, 39)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button.collidepoint(event.pos):
                        button2 = pygame.Rect(0, 40, 39, 39)
                        draw_button_2 = True

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(SCREEN, WHITE, button)
        if draw_button_2:
            pygame.draw.rect(SCREEN, BLACK, button)
            pygame.draw.rect(SCREEN, WHITE, button2)

        pygame.display.update()


def draw_grid():
    for x in range(GRID.GRID_WIDTH):
        for y in range(GRID.GRID_HEIGHT):
            color = RED
            if GRID.is_valid_tile(x, y):
                color = WHITE

            rect = pygame.Rect(y * BLOCK_SIZE, x * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, color, rect, 1)


if __name__ == "__main__":
    main()
