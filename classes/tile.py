class Tile:

    def __init__(self, col, row, standable):
        self._col = col
        self._row = row
        self._standable = standable  # bool
        # self._walls = walls #length-4 bool array [top, left, bottom, right] BREAK IN CASE OF DIRECTIONS
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

    def __repr__(self):
        return f'({self.row}, {self.col})'

    # @property
    # def walls(self):
    #   return self._walls

    @property
    def occupied(self):
        return self._occupied

    @occupied.setter
    def occupied(self, occupied):
        self._occupied = occupied