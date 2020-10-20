from phases.start_screen import StartScreen
import pygame
from draw import quit_game

# Example Phase
# class ExamplePhase(Phase):
#     """Description of Phase"""
#
#     def enter(self):
#         print('Entering Phase...')
#         player = Player()
#         enemy = Enemy()
#         ai = EnemyAI(player, enemy)
#         ai.enemy_ai()
#         enemy2 = Archer()
#         ai = EnemyAI(player, enemy2)
#         ai.enemy_ai()
#
#     def update(self):
#         print('Main Functions of Phase...')
#
#     def exit(self):
#         print('Exiting Phase...')


class FSM:
    """Manages the actual flow of the game"""

    def __init__(self):
        self.__phase_number = 0
        self.__phases = []
        self.__current_phase = None

    def add_phase(self, phase):
        self.__phases.append(phase)

    def next_phase(self):
        """Transition to the next phase"""
        self.__current_phase.exit()
        self.__phase_number += 1
        if self.__phase_number == len(self.__phases):
            self.__phase_number = 0
        self.__current_phase = self.__phases[self.__phase_number]
        self.__current_phase.enter()

    def update(self):
        """Call an update, then go to the next phase"""
        self.__current_phase.update()
        self.next_phase()

    def restart(self):
        """Restart the Game -- Call to start the box after adding states"""
        if not self.__phases:
            print('No phases were added before restart')

        start_screen = StartScreen()
        start_screen.enter()

        # Keep updating until the player starts or quits
        while not start_screen.update():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

        # Starting the game
        self.__phase_number = 0
        self.__current_phase = self.__phases[0]
        self.__current_phase.enter()