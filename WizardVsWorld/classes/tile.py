from WizardVsWorld.classes.const import TileTexture, TileTint


class Tile:
    _texture_type: TileTexture
    tint: TileTint

    def __init__(self, col, row, standable=True, texture_type=TileTexture.NONE, win_tile=False):
        self._col = col
        self._row = row
        self._standable = standable
        self._occupied = False
        self._texture_type = texture_type
        self.tint = TileTint.NONE
        self.win_tile = win_tile

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

    @standable.setter
    def standable(self, value):
        self._standable = value
