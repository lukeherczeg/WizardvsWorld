import pygame
import sys
import wsl
import classes.fsm
import classes.entity
import phases.movement_phase

from classes.grid import Grid

wsl.set_display_to_host()

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
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

    player = classes.entity.Player(GRID)

    fsm = classes.fsm.FSM()
    fsm.add_phase(phases.movement_phase.PlayerMovementPhase(player, GRID))
    fsm.next_phase()

    while True:
        draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def draw_grid():
    for y in range(GRID.GRID_HEIGHT):
        for x in range(GRID.GRID_WIDTH):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)

    pygame.display.update()


if __name__ == "__main__":
    main()
