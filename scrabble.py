import random
from collections import defaultdict, deque

from player import Player
from trie import Trie


class Scrabble:
    def __init__(self, trie: Trie):
        self.values = {
            'A': 1, 'B': 3, 'C': 2, 'Ç': 3, 'D': 2, 'E': 1, 'F': 4,
            'G': 4, 'H': 4, 'I': 1, 'J': 5, 'L': 2, 'M': 1, 'N': 3,
            'O': 1, 'P': 2, 'Q': 6, 'R': 1, 'S': 1, 'T': 1,
            'U': 1, 'V': 4, 'X': 8, 'Z': 8,
        }
        self.initial_tiles = list(
            'A' * 14 + 'B' * 3 + 'C' * 4 + 'Ç' * 2 + 'D' * 5 + 'E' * 11 +
            'F' * 2 + 'G' * 2 + 'H' * 2 + 'I' * 10 + 'J' * 2 + 'L' * 5 +
            'M' * 6 + 'N' * 4 + 'O' * 10 + 'P' * 4 + 'Q' * 1 + 'R' * 6 +
            'S' * 8 + 'T' * 5 + 'U' * 7 + 'V' * 2 + 'X' * 1 + 'Z' * 1 +
            '*' * 3
        )
        self.trie = trie
        self.board = [['-' for _ in range(15)] for _ in range(15)]
        self.bag = None
        self.player1 = None
        self.player2 = None
        self.start_game()

    def start_game(self):
        random.shuffle(self.initial_tiles)
        self.bag = deque(self.initial_tiles)
        self.player1 = Player()
        self.player2 = Player()
        self.player1.draw_tiles(self.bag)
        self.player2.draw_tiles(self.bag)
        print(f'Player 1: {self.player1.tiles}')
        print(f'Player 2: {self.player2.tiles}')

    def get_word_score(self):
        score = 0
        for letter in self.word:
            score += self.values.get(letter.upper(), 0)
        return score

    def find_valid_words(self, player_tiles, on_board=None):
        valid_words = []

        def backtrack(node, letters, letter_freq):
            if node.is_word:
                valid_words.append(''.join(letters))
            for letter, child in node.children.items():
                if letter_freq[letter] > 0:
                    letters.append(letter)
                    letter_freq[letter] -= 1
                    backtrack(child, letters, letter_freq)
                    letters.pop()
                    letter_freq[letter] += 1
            if letter_freq['*'] > 0:
                for letter, child in node.children.items():
                    letters.append(letter)
                    letter_freq['*'] -= 1
                    backtrack(child, letters, letter_freq)
                    letters.pop()
                    letter_freq['*'] += 1

        letter_freq = defaultdict(int)
        for letter in player_tiles:
            letter_freq[letter.lower()] += 1
        print(letter_freq)
        root = self.trie.root
        letters = []
        backtrack(root, letters, letter_freq)
        return sorted(valid_words, key=lambda x: (-len(x), x))
