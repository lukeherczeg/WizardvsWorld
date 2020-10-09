import abc

from typing import List


class Phase(metaclass=abc.ABCMeta):
    """Represents a in-game phase"""

    @abc.abstractmethod
    def enter(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def exit(self):
        pass


class SubPhase(Phase):
    def enter(self):
        print('Entering subphase...')

    def update(self):
        print('Main Functions of subphase...')

    def exit(self):
        print('Exiting subphase...')


class PhaseOne(Phase):
    """Description of Phase 1"""
    movement: SubPhase = SubPhase()
    choice: SubPhase = SubPhase()
    attack: SubPhase = SubPhase()

    subphases: List[SubPhase] = [movement, choice, attack]

    def enter(self):
        print('Entering Phase 1...')
        self.subphases[0].enter()

    def update(self):
        print('Main Functions of Phase 1...')

    def exit(self):
        print('Exiting Phase 1...')


class PhaseTwo(Phase):
    """Description of Phase 2"""

    def enter(self):
        print('Entering Phase 2...')

    def update(self):
        print('Main Functions of Phase 2...')

    def exit(self):
        print('Exiting Phase 2...')


class FSM:
    """Manages the actual flow of the game"""

    def __init__(self):
        self.phase_number = 0
        self.phases = [
            PhaseOne(),
            PhaseTwo()
        ]
        self.subphases = self.phases[self.phase_number].subphases
        self.current_phase = None
        self.current_subphase = None

    def next_subphase(self):
        """Transition to the next subphase"""

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

    def update_subphase(self):
        """Call update on current subphase and perform other relevant functions"""

        self.current_subphase.update()

    def update(self):
        """Call update on current phase and perform other relevant functions"""

        self.current_phase.update()


def test_fsm():
    """Quick unit test for the FSM"""
    fsm = FSM()
    for x in range(0, 5):
        fsm.next_phase()
        fsm.update()


if __name__ == '__main__':
    test_fsm()
