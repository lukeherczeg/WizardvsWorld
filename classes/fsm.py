from classes.movement_phase import PlayerMovementPhase
from GameManager import PhaseTwo


class FSM:
    """Manages the actual flow of the game"""

    def __init__(self, player, grid):
        self.phase_number = 0
        self.phases = [
            PlayerMovementPhase(player, grid),
            PhaseTwo()
        ]
        self.current_phase = None

    def next_phase(self):
        """Transition to the next phase"""

        # Starting the game
        if self.current_phase is None:
            self.phase_number = 0
            self.current_phase = self.phases[0]
            self.current_phase.enter()
            return

        # Other transitions
        self.current_phase.exit()
        self.phase_number += 1
        if self.phase_number == len(self.phases):
            self.phase_number = 0
        self.current_phase = self.phases[self.phase_number]
        self.current_phase.enter()

    def update(self):
        """Call update on current phase and perform other relevant functions"""

        self.current_phase.update()

    def test_fsm(self):
        """Quick unit test for the FSM"""
        self.next_phase()
        # for x in range(0, 5):
        #   fsm.next_phase()
        #   fsm.update()
