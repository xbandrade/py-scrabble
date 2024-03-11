class BoardSquare:
    def __init__(self, letter=''):
        self.letter = letter
        self.letter_multiplier = 1
        self.word_multiplier = 1
        self.blank_letter = None
        self.is_occupied = False

    def set_letter(self, letter):
        self.letter = letter
        self.is_occupied = True
        if '*' in letter:
            self.letter = '*'
            self.blank_letter = letter[1]

    def clear_square(self):
        self.letter = ''
        self.blank_letter = None
        self.is_occupied = False

    def __str__(self):
        if self.blank_letter:
            return self.blank_letter.upper()
        return self.letter or '-'
