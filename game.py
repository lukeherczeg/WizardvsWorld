import pygame
import sys
import wsl
from classes.entity import Enemy
from classes.tile import Tile

import draw
from classes.fsm import FSM
from classes.entity import Player
from classes.grid import Grid
import phases.movement_phase

wsl.set_display_to_host()

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1000
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BLOCK_SIZE = 40  # Set the size of the grid block
GRID = Grid(WINDOW_WIDTH // BLOCK_SIZE, WINDOW_HEIGHT // BLOCK_SIZE)

print(f'Grid Width: {GRID.GRID_WIDTH}; Grid Height: {GRID.GRID_HEIGHT}')


def main():
    pygame.init()
    SCREEN.fill(BLACK)

    player = Player(GRID)
    fsm = FSM()
    
    pygame.init()
    screen, grid = draw.init(pygame)

    enemy = Enemy()

    draw.draw_grid(pygame, screen, grid)
    draw.draw_characters(pygame, screen, [Enemy()])
    oldPos = enemy.get_position().col, enemy.get_position().row
    enemy.currentTile = Tile(8,12,True)
    draw.move_player(pygame, screen, grid, enemy, oldPos)

    fsm.add_phase(phases.movement_phase.PlayerMovementPhase(player, GRID))
    fsm.next_phase()
    fsm.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                draw.quit_game(pygame)

        # pygame.draw.rect(SCREEN, WHITE, button)

if __name__ == "__main__":
    main()
