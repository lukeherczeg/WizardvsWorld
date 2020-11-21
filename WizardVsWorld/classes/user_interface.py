from WizardVsWorld.assets.image_loader import *
from WizardVsWorld.classes.draw import quit_game, draw_text_abs, total_refresh_drawing
from operator import attrgetter

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
        self.__selected = False

    def update(self):
        # Button is being hovered
        # TODO CENTER THE BUTTON HERE
        if self.__selected:
            pygame.draw.rect(SCREEN, self.__color_active,
                             (self.__pos_x, self.__pos_y, self.__width + 5, self.__height + 5))
        # Button isn't hovered
        else:
            pygame.draw.rect(SCREEN, self.__color_inactive, (self.__pos_x, self.__pos_y, self.__width, self.__height))

        SCREEN.blit(self.__button_text, self.__button_rect)

    def on_click(self):
        if self.__selected and self.__on_click is not None:
            self.__on_click()

    def select(self):
        self.__selected = True

    def unselect(self):
        self.__selected = False


class MessageBox:
    """A Message Box that is dismissed with Enter or Click"""

    # TODO: PUT A DARK TRANSPARENT OVERLAY ON THE TOP OF THE SCREEN TO FOCUS PLAYER
    def __init__(self, message):
        self.__lines = self.split(message, 75)  # 80 Characters Max in a line
        self.__lines.append('Press ENTER to continue...')
        self.draw_message_box()
        self.confirm()

    def draw_message_box(self):
        """Draw the message box over the bottom third of the screen"""
        length = len(self.__lines)

        # Build the Dialogue Box
        background = pygame.transform.scale(BACKGROUND_PNG, (WINDOW_WIDTH, WINDOW_HEIGHT // 3))
        rect = background.get_rect()
        rect.center = (WINDOW_WIDTH // 2, 2 * WINDOW_HEIGHT // 3 + 100)
        SCREEN.blit(background, rect)

        for offset in range(length):
            draw_text_abs(self.__lines[offset], 24, WINDOW_WIDTH // 2, 2 * WINDOW_HEIGHT // 3 + (offset * 45 + 35))

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


class SelectionMenu:
    """Overlay the current screen with selection menu.

    :param header: the title of the menu
    :param options: a list of 3-tuples: (name: str, description: str, on_click: function)

    """

    def __init__(self, header, options):
        self.header = header
        self.options = options
        if options:
            self.selected = 0
            self.last_selected = 0
        else:
            self.selected = None
            self.last_selected = None

    def add_option(self, option):
        self.options.append(option)

    def draw_menu(self, initialize=None):
        draw_text_abs(self.header, int(WINDOW_WIDTH * .036), WINDOW_WIDTH // 2, WINDOW_WIDTH // 20)
        option_number = 0
        for option in self.options:
            position = (WINDOW_WIDTH // 6, 100 * option_number + WINDOW_WIDTH // 10,
                        WINDOW_WIDTH - WINDOW_WIDTH // 3, int(WINDOW_WIDTH * .075))
            if option_number == self.selected:
                pygame.draw.rect(SCREEN, BRIGHT_RED, position)
            elif initialize is not None or (self.last_selected == option_number):
                pygame.draw.rect(SCREEN, RED, position)
            else:
                option_number += 1
                continue

            draw_text_abs(option[0], int(WINDOW_WIDTH * .018), WINDOW_WIDTH // 2,
                          100 * option_number + int(WINDOW_WIDTH * .115))
            draw_text_abs(option[1], int(WINDOW_WIDTH * .014), WINDOW_WIDTH // 2,
                          100 * option_number + int(WINDOW_WIDTH * .150))
            option_number += 1

    def await_response(self):
        self.draw_menu(True)
        while True:
            update = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if self.selected == len(self.options) - 1:
                        self.selected = 0
                        self.last_selected = len(self.options) - 1
                    else:
                        self.last_selected = self.selected
                        self.selected += 1
                    update = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if self.selected == 0:
                        self.selected = len(self.options) - 1
                        self.last_selected = 0
                    else:
                        self.last_selected = self.selected
                        self.selected -= 1
                    update = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.options[self.selected][2]()  # Call the on_click function of the option
                    total_refresh_drawing()
                    return True
                elif event.type == pygame.QUIT:
                    quit_game()

            if update:
                self.draw_menu()

class SpellMenu:
    """Overlay the current screen with selection menu.

    :param spells: a list of Spell Objects

    """

    def __init__(self, spells):
        longest_name = max(spells, key=attrgetter('name'))

        self.width = len(longest_name.name)
        self.height = len(spells)
        self.header = 'Choose a Spell'
        self.spells = spells

        self.selected = 0
        self.last_selected = 0

    def draw_menu(self, initialize=None):
        # Draw the menu header
        if initialize is not None:
            draw_text_abs(
                self.header,
                18,
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 8
            )

        spell_number = 0
        for spell in self.spells:
            position = (
                WINDOW_WIDTH // 20, # Left
                25 * spell_number + WINDOW_WIDTH * .020, # Top
                18 * (self.width + 5),  # Width
                25 # Height
            )
            if spell_number == self.selected:
                pygame.draw.rect(SCREEN, BRIGHT_RED, position)
            elif initialize is not None or (self.last_selected == spell_number):
                pygame.draw.rect(SCREEN, RED, position)
            else:
                spell_number += 1
                continue

            draw_text_abs(
                spell.name, # Text
                int(WINDOW_WIDTH * .018), # Font size
                (position[0] + position[2]) // 2, # Pos X
                20 * spell_number + int(WINDOW_WIDTH * .020) # Pos Y
            )

            spell_number += 1

    def await_response(self):
        self.draw_menu(True)
        while True:
            update = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if self.selected == len(self.spells) - 1:
                        self.selected = 0
                        self.last_selected = len(self.spells) - 1
                    else:
                        self.last_selected = self.selected
                        self.selected += 1
                    update = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if self.selected == 0:
                        self.selected = len(self.spells) - 1
                        self.last_selected = 0
                    else:
                        self.last_selected = self.selected
                        self.selected -= 1
                    update = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    total_refresh_drawing()
                    return self.selected
                elif event.type == pygame.QUIT:
                    quit_game()

            if update:
                self.draw_menu()

