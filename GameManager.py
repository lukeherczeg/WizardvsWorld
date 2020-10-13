from abc import abstractmethod, ABCMeta
from classes.enemyai import EnemyAI
from classes.entity import Player, Enemy, Archer


class Phase(metaclass=ABCMeta):
    """Represents a in-game phase"""

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def exit(self):
        pass


class PhaseOne(Phase):
    """Description of Phase 1"""

    def enter(self):
        print('Entering Phase 1...')

    def update(self):
        print('Main Functions of Phase 1...')

    def exit(self):
        print('Exiting Phase 1...')


class PhaseTwo(Phase):
    """Description of Phase 2"""

    def enter(self):
        print('Entering Phase 2...')
        player = Player()
        enemy = Enemy()
        ai = EnemyAI(player, enemy)
        ai.enemy_ai()
        enemy2 = Archer()
        ai = EnemyAI(player, enemy2)
        ai.enemy_ai()

    def update(self):
        print('Main Functions of Phase 2...')

    def exit(self):
        print('Exiting Phase 2...')

