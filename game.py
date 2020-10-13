import os
import pygame
import sys
import wsl
import classes.fsm
import classes.grid
import classes.entity

wsl.set_display_to_host()
print("Distro:\t", wsl.get_wsl_distro())
print("Host:\t", wsl.get_wsl_host())
print("Display:", os.environ['DISPLAY'])

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1000
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


def main():
    pygame.init()
    clock = pygame.time.Clock()
    SCREEN.fill(BLACK)
    draw_button_2 = False
    draw_grid()

    grid = classes.grid.Grid()
    grid.print_map_data()

    player = classes.entity.Player(grid)

    fsm = classes.fsm.FSM(player, grid)
    fsm.test_fsm()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def draw_grid():
    block_size = 40  # Set the size of the grid block
    for x in range(int(WINDOW_WIDTH / block_size)):
        for y in range(int(WINDOW_HEIGHT / block_size)):
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)
    pygame.display.update()


if __name__ == "__main__":
    main()
