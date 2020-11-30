class Spell:
    """Spells are used by wizards and mages to augment their Attack"""
    def __init__(self, name, description, uses, spell_range, power, aoe=0, exclude=False, effect=None, impact=None):
        self._name = name               # Name of spell for the menu
        self._description = description # Description of the spell for the menu
        self._max_uses = uses           # Maximum uses of this spell per level
        self._current_uses = uses       # How many uses of the spell are left this level
        self._range = spell_range       # Spell range in tiles (Named this way to avoid shadowing stl range).
        self._power = power             # Spell power -- Can be damaging (Positive Value) or healing (Negative Value)
        self._aoe = aoe                 # The depth of tiles around a target that are affected by the spell
        self._exclude_self = exclude    # Determines if the caster is excluded from the spell's AoE
        self._effect = effect           # On cast effect
        self._impact = impact           # On attack hit effect

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def max_uses(self):
        return self._max_uses

    @property
    def current_uses(self):
        return self._current_uses

    @property
    def range(self):
        return self._range

    @property
    def power(self):
        return self._power

    @property
    def aoe(self):
        return self._aoe

    @property
    def exclude_self(self):
        return self._exclude_self

    @range.setter
    def range(self, new_range):
        self._range = new_range

    def replenish(self):
        """Set spell uses to max"""
        self._current_uses = self._max_uses

    def can_cast(self):
        """Returns True if spell has uses left, False otherwise"""
        if self._current_uses > 0:
            return True
        else:
            return False

    def cast(self, target):
        """Cast the spell effect"""
        if self._current_uses > 0:
            if self._effect is not None:
                if target is not None:
                    self._effect(target)
                else:
                    self._effect()

    def expend_use(self):
        """Decrement the spell uses if there are any"""
        if self._current_uses > 0:
            self._current_uses -= 1

    def on_hit(self, target):
        """Any effects that are dependant on the spell hitting the enemy"""
        if self._impact is not None and target is not None:
            self._impact(target)
