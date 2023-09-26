import re
from collections import Counter


class Player:
    def __init__(self, id=1):
        self.tiles = []
        self.score = 0
        self.id = id
        self.best_words = []

    def __str__(self):
        return str(self.id)

    def draw_tiles(self, bag):
        while (bag and len(self.tiles) < 7):
            self.tiles.append(bag.popleft())

    def has_tiles(self, word_chars):
        word = ''.join(word_chars)
        print('>>>>', re.sub(r'\*(\w)', r'[\1]', word))
        counter = Counter(self.tiles)
        word = re.sub(r'\*(\w)', r'*\1', word)
        print('word: ', word)
        for letter in word_chars:
            counter[letter] -= 1
            if counter[letter] < 0:
                return False
        return True

    def remove_tiles(self, tiles):
        for tile in tiles:
            if '*' in tile:
                tile = '*'
            self.tiles.remove(tile)
