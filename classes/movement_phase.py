from GameManager import Phase


class PlayerMovementPhase(Phase):

    def enter(self):
        print('Entering Phase 1...')

    def update(self):
        print('Main Functions of Phase 1...')

    def exit(self):
        print('Exiting Phase 1...')
