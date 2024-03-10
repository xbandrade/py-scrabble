import re
from collections import Counter


class Player:
    def __init__(self, id=1, is_bot=False) -> None:
        self.tiles = []
        self.score = 0
        self.id = id
        self.best_words = []
        self.previous_play = None
        self.previous_draw = None
        self.previous_score = 0
        self.show_tiles = False
        self.is_bot = is_bot

    def __str__(self) -> str:
        return str(self.id)

    def __int__(self) -> int:
        return self.id

    def __eq__(self, other):
        if isinstance(other, Player):
            return self == other
        if isinstance(other, int):
            return self.id == other
        return False

    def __lt__(self, other):
        return self.score < other.score

    def draw_tiles(self, bag) -> None:
        draw = []
        while (bag and len(self.tiles) < 7):
            draw.append(bag.pop())
            self.tiles.append(draw[-1])
        self.previous_draw = draw

    def has_tiles(self, word_chars) -> bool:
        word = ''.join(word_chars)
        counter = Counter(self.tiles)
        word = re.sub(r'\*(\w)', r'*\1', word)
        for letter in word_chars:
            counter[letter if '*' not in letter else '*'] -= 1
            if counter[letter] < 0:
                return False
        return True

    def remove_tiles(self, tiles) -> None:
        for tile in tiles:
            if '*' in tile:
                tile = '*'
            self.tiles.remove(tile)
