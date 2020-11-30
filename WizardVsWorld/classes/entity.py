from WizardVsWorld.classes.tile import Tile
from WizardVsWorld.classes.spell import Spell
import WizardVsWorld.assets.image_loader
from math import modf

# entity will have various shared data types

def round_up_from(tiles, round_percentage):
    fraction, whole = modf(tiles)
    if fraction >= round_percentage:
        return whole + 1
    else:
        return whole

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
    shield_level: int = 0

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
        self.health = 200
        self.max_health = self.health
        self.attack = 30
        self.defense = 5
        self.range = 3
        self.selected = False
        self.level = 0
        self.crit_chance = 25
        self.hit_chance = 95

        # START SPELL STATS
        self.uses = 1  # Base uses for special spells
        self.creep = 1  # Base "creep" or spread of aoe spells
        self.shield_level = 0  # Increases chances of blocking all damage
        self.spellbook = None  # Populated by self.refresh_spell()
        self.prepared_spell = None  # Keeps track of current spell to cast (jank)
        self.refresh_spells()
        # END SPELL STATS

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
        self.attack += 10
        self.refresh_spells()

    def boost_health(self):
        """End of level boost for health"""
        self.health += 50
        self.refresh_spells()

    def boost_movement(self):
        """End of level boost for movement"""
        self.max_movement += 1
        self.refresh_spells()

    def boost_creep(self):
        """End of level boost for creep (Increases AoE)"""
        self.creep += 1
        self.refresh_spells()

    def boost_uses(self):
        """End of level boost for uses (increases Spell Charges)"""
        self.uses += 1
        self.refresh_spells()

    def boost_range(self):
        """End of level boost for range"""
        self.range += 1
        self.refresh_spells()

    def boost_shield(self):
        """End of level boost for spell shield -- increases chance of blocking damage"""
        if self.shield_level is None:
            self.shield_level = 1
        else:
            self.shield_level += 1
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
                exclude=False
            ),
            Spell(
                'Flame Nova',
                f'A cloak of flames with AoE of {self.creep}',
                self.uses,
                0,
                50 + self.attack + 2 * (self.level + 1),
                aoe=self.creep,
                exclude=True
            ),
            Spell(
                'Pass',
                'Do Nothing. Pass turn.',
                999,
                0,
                0,
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
        self.health = 55 + (level * 6)
        self.max_health = self.health
        self.attack = 20 + (level * 3)
        self.defense = 5 + (level * 5)
        self.crit_chance = 5
        self.range = 1

    def get_name(self):
        return "Knight"


class Archer(Enemy):
    def __init__(self, level):
        super().__init__()
        self.max_movement = 4
        self.health = 40 + (level * 4)
        self.max_health = self.health
        self.attack = 15 + (level * 4)
        self.defense = 0 + (level * 2)
        self.crit_chance = 15
        self.range = 2

    def get_name(self):
        return "Archer"


class Boss(Enemy):
    ranged: bool

    def __init__(self):
        super()
        super().__init__()

    def populate_tiles(self, height_tiles, width_tiles):
        self.tiles = [self.currentTile]
        for i in range(1, height_tiles):
            for j in range(0, width_tiles):
                WizardVsWorld.assets.image_loader.GRID.game_map[self.currentTile.row - i][
                    self.currentTile.col - j].standable = False
                self.tiles.append(
                    WizardVsWorld.assets.image_loader.GRID.game_map[self.currentTile.row - i][
                        self.currentTile.col - j])

    def get_dimensions(self):
        return self.height_tiles, self.width_tiles


class GreatKnight(Boss):
    range = 1

    def __init__(self, level):
        super().__init__()
        self.max_movement = 0
        self.health = 130 + (level * 5)
        self.max_health = self.health
        self.attack = 50 + (level * 2)
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
        self.health = 70 + (level * 4)
        self.max_health = self.health
        self.attack = 70 + (level * 4)
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
        self.creep = 1
        self.health = 200 + (level * 6)
        self.max_health = self.health
        self.attack = 75 + (level * 6)
        self.defense = 10 + (level * 3)
        self.crit_chance = 7
        self.level = level
        self.cutoff = 0.7
        self.range = 2
        self.uses = 99999
        self.spellbook = None  # Populated by self.refresh_spell()
        self.prepared_spell = None  # Keeps track of current spell to cast (jank)
        self.refresh_spells()
        self.height_tiles = 1 * (
                WizardVsWorld.assets.image_loader.WIZARDKING_RESCALESIZE // WizardVsWorld.assets.image_loader.BLOCK_SIZE)
        self.width_tiles = 0.5 * (
                WizardVsWorld.assets.image_loader.WIZARDKING_RESCALESIZE // WizardVsWorld.assets.image_loader.BLOCK_SIZE)
        self.width_tiles = int(round_up_from(self.width_tiles, self.cutoff))

    def get_name(self):
        return "Wizard King"

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
                'Dark Fireball',
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
                'Dark Greater Fireball',
                f'Cast a stronger fireball with AoE of {self.creep}',
                self.uses,
                self.range + 1,
                self.attack + 5 * (self.level + 1),
                aoe=self.creep,
                exclude=False
            ),
            Spell(
                'Dark Flame Nova',
                f'A cloak of flames with AoE of {self.creep}',
                self.uses,
                0,
                50 + self.attack + 2 * (self.level + 1),
                aoe=self.creep,
                exclude=True
            ),
            Spell(
                'Pass',
                'Do Nothing. Pass turn.',
                999,
                0,
                0,
            )
        ]
