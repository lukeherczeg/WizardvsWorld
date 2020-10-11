import os
import pygame
import sys
import wsl

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
    block_size = 40  # Set the size of the grid block
    for x in range(WINDOW_WIDTH):
        for y in range(WINDOW_HEIGHT):
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)


if __name__ == "__main__":
    main()
