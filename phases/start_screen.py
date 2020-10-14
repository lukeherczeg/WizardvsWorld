from classes.phase import Phase
from classes.user_interface import *

class StartScreen(Phase):
    def __init__(self):
        # Fonts
        self.__title_font = pygame.font.Font('freesansbold.ttf', 72)
        self.__button_font = pygame.font.Font('freesansbold.ttf', 24)

        # Title Attributes
        self.__title = self.__title_font.render('Wizard Vs. World', True, BLUE)
        self.__title_box = self.__title.get_rect()
        self.__title_box.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        # Buttons
        self.__buttons = []
        self.__buttons.append(Button(WINDOW_WIDTH // 4 - 100, 2 * WINDOW_HEIGHT // 3, 100, 50, 'Start', BRIGHT_RED, RED)) #TODO: CALL START GAME FUNCTION IN GAME.PY
        self.__buttons.append(Button(3 * WINDOW_WIDTH // 4, 2 * WINDOW_HEIGHT // 3, 100, 50, 'Quit', BRIGHT_RED, RED, quit_game))

    def enter(self):
        pass

    def update(self):
        SCREEN.fill(WHITE)
        SCREEN.blit(self.__title, self.__title_box)

        for button in self.__buttons:
            button.update()

        pygame.display.update()

    def exit(self):
        pass