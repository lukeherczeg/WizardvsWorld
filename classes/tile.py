import os

class Tile:

    def __init__(self, row, col, standable, image=None):

        self._col = col
        self._row = row
        self._standable = standable #bool
        # self._walls = walls #length-4 bool array [top, left, bottom, right] BREAK IN CASE OF DIRECTIONS
        self._occupied = False
        self._image = self._get_tile_img()

    @property
    def col(self):
        return self._col

    @property
    def row(self):
        return self._row

    @property
    def standable(self):
        return self._standable

    # @property
    # def walls(self):
        #   return self._walls

    @property
    def occupied(self):
        return self._occupied

    @occupied.setter
    def occupied(self, occupied):
        self._occupied = occupied

    @property
    def image(self):
        return self._image

    def _get_tile_img(self):
        main_directory = os.path.dirname('WizardvsWorld')
        asset_path = os.path.join(main_directory, 'assets')
        if(self._standable):
            return os.path.join(asset_path, 'grass.png')
        else:
            return os.path.join(asset_path, 'stone.png')
        
