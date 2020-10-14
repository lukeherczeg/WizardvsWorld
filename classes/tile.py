class Tile:

    def __init__(self, col, row, standable):

        self._col = col
        self._row = row
        self._standable = standable #bool
        self._occupied = False

    @property
    def col(self):
        return self._col

    @property
    def row(self):
        return self._row

    @property
    def standable(self):
        return self._standable

    @property
    def occupied(self):
        return self._occupied

    @occupied.setter
    def occupied(self, occupied):
        self._occupied = occupied
