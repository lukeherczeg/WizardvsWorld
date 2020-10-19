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

        # Button selected with Arrow Keys
        self.__selection = 0
        self.__buttons[0].select()

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

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Select Left
                if event.key == pygame.K_LEFT and self.__selection > 0:
                    self.__buttons[self.__selection].unselect()
                    self.__selection -= 1
                    self.__buttons[self.__selection].select()
                # Select Right
                elif event.key == pygame.K_RIGHT and self.__selection < len(self.__buttons) - 1:
                    self.__buttons[self.__selection].unselect()
                    self.__selection += 1
                    self.__buttons[self.__selection].select()
                # Confirm Selection
                elif event.key == pygame.K_RETURN:
                    self.__buttons[self.__selection].on_click()
            elif event.type == pygame.QUIT:
                quit_game()

        if self.__completed:
            return True
        else:
            return False

    def exit(self):
        pass