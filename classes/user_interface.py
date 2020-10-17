from assets.image_loader import pygame, SCREEN, RED, WHITE, WINDOW_HEIGHT, WINDOW_WIDTH
from draw import quit_game


class Button:
    # Inspired by the tutorial at https://pythonprogramming.net/pygame-button-function/
    def __init__(self, pos_x, pos_y, width, height, text, color_active, color_inactive, on_click=None):
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
        if self.__pos_x + self.__width > mouse[0] > self.__pos_x and self.__pos_y + self.__height > mouse[
            1] > self.__pos_y:
            pygame.draw.rect(SCREEN, self.__color_active, (self.__pos_x, self.__pos_y, self.__width, self.__height))

            # Check for clicks
            if is_pressed[0] and self.__on_click is not None:
                self.__on_click()
        # Button isn't hovered
        else:
            pygame.draw.rect(SCREEN, self.__color_inactive, (self.__pos_x, self.__pos_y, self.__width, self.__height))

        SCREEN.blit(self.__button_text, self.__button_rect)


class MessageBox:
    """A Message Box that is dismissed with Enter or Click"""

    # TODO: PUT A DARK TRANSPARENT OVERLAY ON THE TOP OF THE SCREEN TO FOCUS PLAYER
    def __init__(self, message):
        self.__font = pygame.font.Font('freesansbold.ttf', 24)
        self.__lines = self.split(message, 80)  # 80 Characters Max in a line
        self.__lines.append('Press ENTER to continue...')
        self.__rendered_lines = [self.__font.render(line, True, WHITE) for line in self.__lines]
        self.draw_message_box()
        self.confirm()

    def draw_message_box(self):
        """Draw the message box over the bottom third of the screen"""
        length = len(self.__rendered_lines)

        # Build the Dialogue Box
        pygame.draw.rect(SCREEN, RED, (0, 2 * WINDOW_HEIGHT // 3, WINDOW_WIDTH, WINDOW_HEIGHT))
        text_lines = [
            pygame.draw.rect(SCREEN, RED, (20, 2 * WINDOW_HEIGHT // 3 + (offset * 45 + 20), WINDOW_WIDTH - 20, 20))
            for offset in range(length)]

        # Render to the screen
        for x in range(length):
            SCREEN.blit(self.__rendered_lines[x], text_lines[x])

        pygame.display.update()

    @staticmethod
    def confirm():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return True
                elif event.type == pygame.QUIT:
                    quit_game()

    @staticmethod
    def split(long_string, length):
        """Split the message into up to length char lines"""
        lines = []
        words = long_string.split(' ')
        line = ''
        while len(words) != 0:
            if line == '':
                line = words.pop(0)
            elif len(line) + len(words[0]) + 1 < length:
                line += ' ' + words.pop(0)
            else:
                lines.append(line)
                line = ''
        lines.append(line)
        return lines
