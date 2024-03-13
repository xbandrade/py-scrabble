class BoardCell:
    def __init__(self, tile=None):
        self.tile = tile
        self.letter_multiplier = 1
        self.word_multiplier = 1
        self.is_occupied = False

    def __str__(self):
        return f'{self.tile}' if self.tile else '-'

    def clear(self):
        tile = self.tile
        self.tile = None
        self.is_occupied = False
        return tile

    def place_tile(self, tile):
        self.tile = tile
        self.is_occupied = True
        tile.where = 'board'
