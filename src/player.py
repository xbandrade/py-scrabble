from collections import Counter

from src.tile import Tile


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
        self.can_challenge = False

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

    def add_tile(self, tile) -> None:
        self.tiles.append(tile)
        tile.where = f'p{self}'

    def get_tiles(self) -> None:
        return [f'{tile}' for tile in self.tiles]

    def has_tiles(self, word_chars) -> bool:
        word = [c if c.islower() else '*' for c in word_chars]
        counter = Counter(map(str, self.tiles))
        for letter in word:
            counter[letter] -= 1
            if counter[letter] < 0:
                return False
        return True

    def remove_tiles(self, tiles_to_remove) -> None:
        self.tiles = [
            tile for tile in self.tiles if tile not in tiles_to_remove]

    def retrieve_tile(self, letter) -> Tile:
        if letter.isupper():
            letter = '*'
        tile_to_remove = [tile for tile in self.tiles if str(tile) == letter]
        if not tile_to_remove:
            raise ValueError(f'Player {self} does not have tile {letter}')
        self.tiles.remove(tile_to_remove[0])
        return tile_to_remove[0]
