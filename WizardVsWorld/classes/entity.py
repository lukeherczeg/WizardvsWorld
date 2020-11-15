from WizardVsWorld.classes.tile import Tile
from WizardVsWorld.classes.spell import Spell


# entity will have various shared data types
class Entity:
    currentTile: Tile = None
    health: int
    max_health: int
    attack: int  # these variables may change based on how we want to do combat
    defense: int
    max_movement: int = 5
    range: int
    crit_chance: int
    hit_chance: int
    level: int

    def __init__(self):
        self.damaged = False
        self.attacking = False

    def get_position(self):
        return self.currentTile

    # Gets health, defense, attack, attack range, critical chance, and movement.
    def get_character_stats(self):
        return self.health, self.defense, self.attack, self.range, self.crit_chance, self.hit_chance, self.max_movement

    def get_max_health(self):
        return self.max_health


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
        self.crit_chance = 25
        self.hit_chance = 95
        self.uses = 1 # Base uses for special spells
        self.creep = 1  # Base "creep" or spread of aoe spells
        self.spellbook = []
        self.refresh_spells()

    @property
    def spellbook(self):
        return self.spellbook

    @spellbook.setter
    def spellbook(self, spellbook):
        self.spellbook = spellbook

    def level_up(self, new_level):
        self.level = new_level
        self.max_health += 15
        self.health = self.max_health
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

    def get_name(self):
        return "The Wizard"

    def refresh_spells(self):
        """Called to initialize the spellbook and to refresh between levels (Rescales spells to current stats)"""
        self.spellbook = [
            Spell('Fireball', 999, self.range, self.attack),
            Spell('Heal', self.uses, 0, -self.max_health),
            Spell('Greater Fireball', self.uses, self.range + 1, self.attack + 5 * (self.level + 1), aoe=self.creep),
            Spell('Flame Barrier', self.uses, 0, self.attack + 5 * (self.level + 1), aoe= self.creep)
        ]


class Enemy(Entity):
    def __init__(self):
        super().__init__()
        self.attackable = False
        self.hit_chance = 80


class Knight(Enemy):
    def __init__(self, level):
        super().__init__()
        self.max_movement = 3
        self.health = 50 + (level * 5)
        self.max_health = self.health
        self.attack = 15 + (level * 2)
        self.defense = 5 + (level * 1)
        self.crit_chance = 5
        self.range = 1

    def get_name(self):
        return "Knight"


class Archer(Enemy):
    def __init__(self, level):
        super().__init__()
        self.max_movement = 4
        self.health = 30 + (level * 2)
        self.max_health = self.health
        self.attack = 10 + (level * 3)
        self.defense = 0 + (level * 1)
        self.crit_chance = 15
        self.range = 2

    def get_name(self):
        return "Archer"


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
        self.crit_chance = 5
        self.range = 1

    def get_name(self):
        return "Great Knight"


class GreatMarksman(Boss):
    range = 3

    def __init__(self, level):
        super().__init__()
        self.max_movement = 1
        self.health = 30 + (level * 4)
        self.max_health = self.health
        self.attack = 40 + (level * 4)
        self.defense = 0 + (level * 2)
        self.critical_chance = 8
        self.range = 3


class WizardKing(Boss):
    range = 2

    def __init__(self, level):
        super().__init__()
        self.max_movement = 0
        self.health = 45 + (level * 6)
        self.max_health = self.health
        self.attack = 35 + (level * 6)
        self.defense = 10 + (level * 3)
        self.critical_chance = 7
        self.range = 2