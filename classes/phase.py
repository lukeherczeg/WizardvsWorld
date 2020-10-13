import abc

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
