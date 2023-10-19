import re
from collections import Counter
from random import randint


class Player:
    def __init__(self, id=1) -> None:
        self.tiles = []
        self.score = 0
        self.id = id
        self.best_words = []
        self.previous_play = None
        self.previous_draw = None
        self.previous_score = 0
        self.show_tiles = False

    def __str__(self) -> str:
        return str(self.id)

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

    def exchange_tiles(self, tiles, bag) -> bool:
        if len(tiles) > len(bag) or not all(t in self.tiles for t in tiles):
            print('Troca inválida\n')
            return False
        tiles_on_hand = tiles[:]
        self.remove_tiles(tiles)
        self.draw_tiles(bag)
        for tile in tiles_on_hand:
            bag.insert(randint(0, len(bag)), tile)
        print(f'Player {self.id} trocou de peças com sucesso\n')
        return True
