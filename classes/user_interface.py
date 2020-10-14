from draw import *

class Button:
    # Inspired by the tutorial at https://pythonprogramming.net/pygame-button-function/
    def __init__(self, pos_x, pos_y, width, height, text, color_active, color_inactive, on_click = None):
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__width = width
        self.__height = height
        self.__text = text
        self.__color_active = color_active
        self.__color_inactive = color_inactive
        self.__on_click = on_click

        button_font = pygame.font.Font('freesansbold.ttf', 24)
        self.__button_text = button_font.render(text, True, WHITE)
        self.__button_rect = self.__button_text.get_rect()
        self.__button_rect.center = (pos_x + (width // 2), (pos_y + (height // 2)))

    def update(self):
        mouse = pygame.mouse.get_pos()
        is_pressed = pygame.mouse.get_pressed()

        # Button is being hovered
        if self.__pos_x + self.__width > mouse[0] > self.__pos_x and self.__pos_y + self.__height > mouse[1] > self.__pos_y:
            pygame.draw.rect(SCREEN, self.__color_active, (self.__pos_x, self.__pos_y, self.__width, self.__height))

            if is_pressed[0] == 1 and self.__on_click is not None:
                self.__on_click()
        # Button isn't hovered
        else:
            pygame.draw.rect(SCREEN, self.__color_inactive, (self.__pos_x, self.__pos_y, self.__width, self.__height))

        SCREEN.blit(self.__button_text, self.__button_rect)