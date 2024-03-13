class Tile:
    def __init__(self, letter='', value=0, blank_letter=None, pos=(15, 15)):
        self.where = 'bag'
        self.letter = letter
        self.is_blank = letter == '*'
        self.blank_letter = blank_letter
        self.value = value
        self.pos = pos

    def __str__(self):
        return self.blank_letter or self.letter

    def __int__(self):
        return self.value

    def __lt__(self, other):
        return self.letter < other.letter
