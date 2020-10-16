from assets.image_loader import *
from classes.phase import Phase
from classes.user_interface import Button
from draw import quit_game

class StartScreen(Phase):
    def __init__(self):
        # Fonts
        self.__button_font = pygame.font.Font('freesansbold.ttf', 24)

        # Images
        self.__logo_splash = pygame.transform.scale(LOGO_PNG, (1000, 600))

        # Buttons (Make them appear under the icons)
        self.__buttons = []
        self.__buttons.append(Button(WINDOW_WIDTH // 4 - 60, 7 * WINDOW_HEIGHT // 8, 100, 50, 'Start', BRIGHT_RED, RED, self.complete)) #TODO: CALL START GAME FUNCTION IN GAME.PY
        self.__buttons.append(Button(3 * WINDOW_WIDTH // 4, 7 * WINDOW_HEIGHT // 8, 100, 50, 'Quit', BRIGHT_RED, RED, quit_game))

        # Completion
        self.__completed = None

    def complete(self):
        self.__completed = True

    def enter(self):
        print('Entering start...')
        self.__completed = False

    def update(self):
        SCREEN.fill(BLACK)
        SCREEN.blit(self.__logo_splash, (0, 0))

        for button in self.__buttons:
            button.update()

        pygame.display.update()

        if self.__completed:
            return True
        else:
            return False

    def exit(self):
        pass