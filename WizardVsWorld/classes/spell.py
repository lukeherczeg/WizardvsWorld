class Spell:
    def __init__(self, name, uses, spell_range, effect, aoe=0):
        self._name = name
        self._max_uses = uses
        self._current_uses = uses
        self._range = spell_range
        self._effect = effect
        self._aoe = aoe

    @property
    def name(self):
        return self._name

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
    def effect(self):
        return self._effect

    @property
    def aoe(self):
        return self._aoe

    @range.setter
    def range(self, new_range):
        self._range = new_range

    def replenish(self):
        """Set spell uses to max. Usually at beginning of level"""
        self._current_uses = self._max_uses

    def can_cast(self):
        """Returns True if spell has uses left, False otherwise"""
        if self._current_uses > 0:
            return True
        else:
            return False

    def cast(self):
        """Decrement _current_uses by 1 if the spell has any"""
        if self._current_uses > 0:
            self._current_uses -= 1