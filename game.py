import pygame
import draw
import wsl
from classes.entity import Enemy


wsl.set_display_to_host()

def main():

    pygame.init()
    screen, grid = draw.init(pygame)

    draw.draw_grid(pygame, screen, grid)
    draw.draw_characters(pygame, screen, [Enemy(), Enemy()])

    while True:
        # button = pygame_inst.Rect(0, 0, 39, 39)
        for event in pygame.event.get():
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 1:
            #         if button.collidepoint(event.pos):
            #             button2 = pygame.Rect(0, 40, 39, 39)
            #             draw_button_2 = True

            if event.type == pygame.QUIT:
                draw.quit_game(pygame)

        # pygame.draw.rect(SCREEN, WHITE, button)




if __name__ == "__main__":
    main()

