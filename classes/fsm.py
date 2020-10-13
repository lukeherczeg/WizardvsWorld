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

        # Starting the game
        if self.__current_phase is None:
            self.__phase_number = 0
            self.__current_phase = self.__phases[0]
            self.__current_phase.enter()
            return

        # Other transitions
        self.__current_phase.exit()
        self.__phase_number += 1
        if self.__phase_number == len(self.__phases):
            self.__phase_number = 0
        self.__current_phase = self.__phases[self.__phase_number]
        self.__current_phase.enter()

    def update(self):
        """Call update on current phase and perform other relevant functions"""
        self.__current_phase.update()
