from classes.tile import Tile


# entity will have various shared data types
class Entity:
    currentTile: Tile = None
    health: int
    max_health: int
    attack: int  # these variables may change based on how we want to do combat
    defense: int
    max_movement: int = 5
    range: int
    critical_chance: int
    level: int

    def __init__(self):
        self.damaged = False
        self.attacking = False

    def get_position(self):
        return self.currentTile


# each type of entity will have an "image" method that handles retrieving (but not printing assets)
# this method is responsible for taking in bools that will decipher which image of the character to retrieve

# the wizard will have methods and variables specific to the wizard
class Player(Entity):
    def __init__(self):
        super().__init__()
        self.health = 150
        self.max_health = self.health
        self.attack = 25
        self.defense = 5
        self.range = 3
        self.selected = False
        self.level = 0
        self.critical_chance = 25

    def level_up(self, new_level):
        self.level = new_level
        self.health += 15
        self.max_health = self.health
        self.attack += 5
        self.defense += 1

    def boost_attack(self):
        """End of level boost for attack"""
        self.attack += 5

    def boost_health(self):
        """End of level boost for health"""
        self.health += 15

    def boost_movement(self):
        """End of level boost for movement"""
        self.max_movement += 1


class Enemy(Entity):
    def __init__(self):
        super().__init__()
        self.attackable = False


class Knight(Enemy):
    def __init__(self, level):
        super().__init__()
        self.max_movement = 3
        self.health = 50 + (level * 5)
        self.max_health = self.health
        self.attack = 15 + (level * 2)
        self.defense = 5 + (level * 1)
        self.critical_chance = 5
        self.range = 1


class Archer(Enemy):
    def __init__(self, level):
        super().__init__()
        self.max_movement = 4
        self.health = 30 + (level * 2)
        self.max_health = self.health
        self.attack = 10 + (level * 3)
        self.defense = 0 + (level * 1)
        self.critical_chance = 15
        self.range = 2


class Boss(Enemy):
    ranged: bool
    tiles: [Tile]

    def __init__(self):
        super().__init__()


class GreatKnight(Boss):
    range = 1

    def __init__(self, level):
        super().__init__()
        self.max_movement = 0
        self.health = 60 + (level * 5)
        self.max_health = self.health
        self.attack = 20 + (level * 2)
        self.defense = 10 + (level * 1)
        self.critical_chance = 5
        self.range = 1
