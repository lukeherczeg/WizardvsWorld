from const import TextureType


class Tile:
    _texture_type: TextureType

    def __init__(self, col, row, standable, texture_type=TextureType.NONE):
        self._col = col
        self._row = row
        self._standable = standable #bool
        self._occupied = False
        self._texture_type = texture_type

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

    @property
    def occupied(self):
        return self._occupied

    @property
    def texture_type(self):
        return self._texture_type

    @occupied.setter
    def occupied(self, occupied):
        self._occupied = occupied
