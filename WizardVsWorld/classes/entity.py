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
        self.tiles = [self.currentTile]
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
        self.spellbook = None # Populated by self.refresh_spell()
        self.prepared_spell = None # Keeps track of current spell to cast (jank)
        self.refresh_spells()
        self.tiles = None
        self.healing = False

    def level_up(self, new_level):
        self.level = new_level
        self.max_health += 15
        self.health = self.max_health
        self.attack += 5
        self.defense += 1
        self.refresh_spells()

    def boost_attack(self):
        """End of level boost for attack"""
        self.attack += 5
        self.refresh_spells()

    def boost_health(self):
        """End of level boost for health"""
        self.health += 15
        self.refresh_spells()

    def boost_movement(self):
        """End of level boost for movement"""
        self.max_movement += 1
        self.refresh_spells()

    def decrease_health(self, health):
        """Decrease the health of player by a certain amount; Clamped at 0 and Max Health. Can be used for healing"""
        self.health -= health
        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health < 0:
            self.health = 0

    def get_name(self):
        return "The Wizard"

    def heal(self, target):
        self.healing = True
        target.health = target.max_health

    def refresh_spells(self):
        """Called to initialize the spellbook and to refresh between levels (Rescales spells to current stats)"""
        self.spellbook = [
            # Example Spell
            # Spell(
            #   'Name',                     # Name of Spell
            #   'Description Goes Here',    # Description
            #   0,                          # Max Uses
            #   self.range,                 # Range
            #   self.attack,                # Spell Power (Positive for Damage, Negative for Healing)
            #   aoe=self.creep,             # AoE of the Spell (Default = 0)
            #   exclude=True,               # Exclude the caster from AoE
            #   effect=some_function,       # On cast effect
            #   impact=other_function       # On hit effect
            #),
            Spell(
                'Fireball',
                'Basic Fireball.',
                999,
                self.range,
                self.attack
            ),
            Spell(
                'Heal',
                'Heal to full.',
                self.uses,
                0,
                -self.max_health,
                effect=self.heal
            ),
            Spell(
                'Greater Fireball',
                f'Cast a stronger fireball with AoE of {self.creep}',
                self.uses,
                self.range + 1,
                self.attack + 5 * (self.level + 1),
                aoe=self.creep,
                exclude=True
            ),
            Spell(
                'Flame Nova',
                f'A cloak of flames with AoE of {self.creep}',
                self.uses,
                0,
                50 + self.attack + 2 * (self.level + 1),
                aoe=self.creep,
                exclude=True
            )
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

    def __init__(self):
        super()
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
        self.crit_chance = 8
        self.range = 3

    def get_name(self):
        return "Great Marksman"


class WizardKing(Boss):
    range = 2

    def __init__(self, level):
        super().__init__()
        self.max_movement = 0
        self.health = 45 + (level * 6)
        self.max_health = self.health
        self.attack = 35 + (level * 6)
        self.defense = 10 + (level * 3)
        self.crit._chance = 7
        self.range = 2

    def get_name(self):
        return "Wizard King"