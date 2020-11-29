from WizardVsWorld.classes.const import CRIT_MULTIPLIER
from WizardVsWorld.classes.draw import *
from WizardVsWorld.classes.tile import Tile
from WizardVsWorld.classes.entity import Entity, Enemy

from random import randint, randrange
from math import ceil


def get_aoe_tiles(caster, victim=None):
    aoe_tiles = []
    # Fetch AoE of a spell
    aoe = caster.prepared_spell.aoe

    # Calculate bounds of AoE
    lo = [victim.currentTile.row - aoe, victim.currentTile.col - aoe]  # lower [row, col] affected
    hi = [victim.currentTile.row + aoe, victim.currentTile.col + aoe]  # upper [row, col] affected

    for i in range(lo[0], hi[0] + 1):
        for j in range(lo[1], hi[1] + 1):
            if GRID.is_valid_tile(i, j):
                aoe_tiles.append(GRID.game_map[i][j])

    return aoe_tiles


def can_attack(attacker, victim):
    attackable_tiles = GRID.get_attack(attacker.currentTile.row, attacker.currentTile.col, attacker.range)
    if victim.currentTile in attackable_tiles:
        return True
    else:
        return False


def cast_spell(caster, target):
    """Casts the prepared spell"""
    # TODO: ANIMATE CASTING SPELLS OTHER THAN FIREBALL

    spell = caster.prepared_spell

    # Typically Buffs and defense spells
    if spell.range == 0:
        spell.cast(target)
        perform_aoe(caster, target, False)

    # If not cast on self, its susceptible to attack roll
    if spell.range > 0:
        spell.cast(target)
        perform_attack(caster, target, spell)


def entity_cleanup(victim, damage, crit):
    health_before_attack = victim.health
    victim.health -= damage
    victim.damaged = True
    animate_damage(victim, health_before_attack, crit)

    if victim.health <= 0:
        victim.currentTile.occupied = False
        ENTITIES.remove(victim)
        animate_death(victim)
    else:
        victim.damaged = False

    time.sleep(.3)


def perform_attack(attacker, victim, spell=None):
    attacker.attacking = True
    aoe_tiles = []
    if spell is not None and spell.name == "Greater Fireball":
        animate_attack(attacker, victim, spell.name)
        aoe_tiles = get_aoe_tiles(attacker, victim)
        draw_tinted_tiles(aoe_tiles, TileTint.FIRE)
    else:
        animate_attack(attacker, victim)
    attacker.attacking = False

    # Check if spell is being cast
    if spell is not None:
        damage_taken, crit = calculate_damage(attacker, victim, spell)
    else:
        damage_taken, crit = calculate_damage(attacker, victim)

    if damage_taken is None:
        animate_miss(victim)
        if spell is not None:
            # Clean aoe tiles
            clear_tinted_tiles(aoe_tiles)
        return

    if damage_taken < 0:
        damage_taken = 0

    entity_cleanup(victim, damage_taken, crit)

    if spell is not None:
        perform_aoe(attacker, victim, crit)

        # Clean aoe tiles
        aoe_tiles = get_aoe_tiles(attacker, victim)
        clear_tinted_tiles(aoe_tiles)


def calculate_damage(attacker, victim, spell=None, aoe=False, crit=False):
    """ Attack damage is calculated by picking a random number between [a little
        less than one's attack power] and [a little more than one's attack power]. """

    # Check if spell is being cast
    if spell is not None:
        attack_damage = (ceil(randrange(spell.power - randint(1, 3), spell.power + randint(1, 3))))
    else:
        attack_damage = (ceil(randrange(attacker.attack - randint(1, 3), attacker.attack + randint(1, 3))))

    chance = randint(0, 100)
    is_crit = False

    if aoe or chance <= attacker.hit_chance:
        if crit or chance <= attacker.crit_chance:
            critical_damage = ceil(attack_damage * CRIT_MULTIPLIER)
            damage = critical_damage - victim.defense
            is_crit = True
        else:
            damage = attack_damage - victim.defense
    else:
        damage = None

    return damage, is_crit


def perform_aoe(attacker, victim, crit):
    """Check if any entities (not enemies) are in the spell's AoE"""
    spell = attacker.prepared_spell
    aoe_tiles = []
    if spell is not None and spell.aoe > 0:
        affected_entities = calculate_aoe(attacker, victim)
        if spell.name == "Flame Nova":
            attacker.attacking = True
            if len(affected_entities) > 0:
                # Here, we use player creep to draw fire
                # Tint surrounding tiles
                aoe_tiles = get_aoe_tiles(attacker, victim)
                aoe_tiles.remove(attacker.currentTile)
                draw_tinted_tiles(aoe_tiles, TileTint.FIRE)

        for entity in affected_entities:
            damage, is_crit = calculate_damage(attacker, entity, spell, True, crit)
            entity_cleanup(entity, damage, is_crit)
    attacker.attacking = False
    clear_tinted_tiles(aoe_tiles)


def calculate_aoe(caster, victim):
    """Returns a list of entities (not enemies) in the AoE of a spell"""
    affected_entities = []

    # Fetch AoE of a spell
    aoe = caster.prepared_spell.aoe

    # Calculate bounds of AoE
    lo = [victim.currentTile.row - aoe, victim.currentTile.col - aoe]  # lower [row, col] affected
    hi = [victim.currentTile.row + aoe, victim.currentTile.col + aoe]  # upper [row, col] affected

    # Check if any entities are in the AoE
    for entity in ENTITIES:
        if lo[0] <= entity.currentTile.row <= hi[0] and lo[1] <= entity.currentTile.col <= hi[1] \
                and entity is not victim:  # No double dipping
            affected_entities.append(entity)

    # Exclude caster from effects of spell
    if caster.prepared_spell.exclude_self:
        affected_entities = [entity for entity in affected_entities if entity is not caster]  # Yay listcomps!

    return affected_entities


class CounterAttack:
    enemy_tiles: [Tile]
    attacker: Entity
    victim: Entity

    def __init__(self, attacker, victim, enemy_tiles=None):
        self.attacker = attacker
        self.victim = victim
        self.enemy_tiles = enemy_tiles

    def counter_attack(self):
        self.attacker.attacking = True
        animate_attack(self.attacker, self.victim)
        self.attacker.attacking = False
        damage_taken, crit = calculate_damage(self.attacker, self.victim)

        if damage_taken is None:
            animate_miss(self.victim)
            if isinstance(self.attacker, Player):
                # Clear fire if fireball missed
                row = int(self.victim.get_position().row)
                col = int(self.victim.get_position().col)
                splash_of_fireball = GRID.get_attack(
                    row,
                    col,
                    self.attacker.creep + 1
                )
                clear_tinted_tiles(splash_of_fireball)
            return

        if damage_taken < 0:
            damage_taken = 0

        old_victim_health = self.victim.health
        self.victim.health -= damage_taken
        self.victim.damaged = True
        animate_damage(self.victim, old_victim_health, crit)

        time.sleep(.25)

        if isinstance(self.victim, Enemy):
            enemy = self.victim
            if enemy.health <= 0:
                enemy.health = 0
                enemy.currentTile.occupied = False
                ENTITIES.remove(enemy)
                animate_death(enemy)
            else:
                self.victim.damaged = False

        if isinstance(self.victim, Player):
            player = self.victim
            if player.health <= 0:
                player.health = 0
                ENTITIES.remove(player)
                animate_death(player)
                time.sleep(2)
                pygame.quit()
            else:
                self.victim.damaged = False

    def attempt_counter_attack(self):
        time.sleep(.5)
        if isinstance(self.attacker, Enemy):
            if can_attack(self.attacker, self.victim):
                self.counter_attack()
        else:
            self.counter_attack()
