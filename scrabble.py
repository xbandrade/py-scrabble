import random
import re
from collections import Counter, defaultdict, deque

from player import Player
from trie import Trie


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


class Scrabble:
    def __init__(self, trie: Trie):
        self.values = {
            'a': 1, 'b': 3, 'c': 2, 'ç': 3, 'd': 2, 'e': 1, 'f': 4,
            'g': 4, 'h': 4, 'i': 1, 'j': 5, 'l': 2, 'm': 1, 'n': 3,
            'o': 1, 'p': 2, 'q': 6, 'r': 1, 's': 1, 't': 1,
            'u': 1, 'v': 4, 'x': 8, 'z': 8,
        }
        self.initial_tiles = list(
            'a' * 14 + 'b' * 3 + 'c' * 4 + 'ç' * 2 + 'd' * 5 + 'e' * 11 +
            'f' * 2 + 'g' * 2 + 'h' * 2 + 'i' * 10 + 'j' * 2 + 'l' * 5 +
            'm' * 6 + 'n' * 4 + 'o' * 10 + 'p' * 4 + 'q' * 1 + 'r' * 6 +
            's' * 8 + 't' * 5 + 'u' * 7 + 'v' * 2 + 'x' * 1 + 'z' * 1 +
            '*' * 3
        )
        self.trie = trie
        self.board = [[BoardSquare() for _ in range(15)] for _ in range(15)]
        self.bag = None
        self.player1 = None
        self.player2 = None
        self.current_player = None
        self.previous_played_tiles = None
        self.tiles_on_board = 0
        self.center = (7, 7)
        self.previous_play_info = {}
        self.start_game()

    def start_game(self):
        self.set_multipliers()
        random.shuffle(self.initial_tiles)
        self.bag = deque(self.initial_tiles)
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.player1.draw_tiles(self.bag)
        self.player2.draw_tiles(self.bag)
        self.current_player = self.player1

    def set_multipliers(self):
        tw = [(0, 0), (0, 14), (14, 0), (14, 14),
              (0, 7), (7, 0), (7, 14), (14, 7)]
        dw = [(7, 7), (1, 1), (2, 2), (3, 3), (4, 4),
              (10, 10), (11, 11), (12, 12), (13, 13),
              (1, 13), (2, 12), (3, 11), (4, 10),
              (10, 4), (11, 3), (12, 2), (13, 1)]
        tl = [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13),
              (9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 9)]
        dl = [(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7),
              (3, 14), (6, 2), (6, 6), (6, 8), (6, 12), (7, 3),
              (7, 11), (8, 2), (8, 6), (8, 8), (8, 12), (11, 0),
              (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11)]
        for a, b in tw:
            self.board[a][b].word_multiplier = 3
        for a, b in dw:
            self.board[a][b].word_multiplier = 2
        for a, b in tl:
            self.board[a][b].letter_multiplier = 3
        for a, b in dl:
            self.board[a][b].letter_multiplier = 2

    def get_word_score(self, word, start_pos, end_pos):
        word = self.split_word(word)
        if (end_pos[0] - start_pos[0] + 1 != self.len(word) and
                end_pos[1] - start_pos[1] + 1 != self.len(word)):
            raise ValueError('Palavra ou posições inválidas')
        if start_pos[0] == end_pos[0]:
            word_path = [(start_pos[0], i)
                         for i in range(start_pos[1], end_pos[1] + 1)]
        else:
            word_path = [(i, start_pos[1])
                         for i in range(start_pos[0], end_pos[0] + 1)]
        word_multiplier, score = 1, 0
        for i, (a, b) in enumerate(word_path):
            mult = self.board[a][b].letter_multiplier
            score += self.values.get(word[i].lower(), 0) * mult
            word_multiplier *= self.board[a][b].word_multiplier
        return score * word_multiplier

    def find_valid_words(self, player=1, on_board=None):
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
                    letters.append(f'[{letter}]')
                    letter_freq['*'] -= 1
                    backtrack(child, letters, letter_freq)
                    letters.pop()
                    letter_freq['*'] += 1

        letter_freq = defaultdict(int)
        player_tiles = (self.player1.tiles if player == 1
                        else self.player2.tiles)
        for letter in player_tiles:
            letter_freq[letter.lower()] += 1
        root = self.trie.root
        letters = []
        backtrack(root, letters, letter_freq)
        return sorted(valid_words, key=lambda x: (-len(x), x))

    def clear_word(self, word):
        if isinstance(word, list):
            word = ''.join(word)
        return word.replace('[', '').replace(']', '').replace('*', '')

    def len(self, word):
        if isinstance(word, list):
            word = ''.join(word)
        word = self.clear_word(word)
        return len(word)

    def show_best_words(self, player=1, start_tile=(7, 7), down=True):
        player = self.player1 if player == 1 else self.player2
        valid_words = self.find_valid_words(player.id)[:20]
        start = start_tile
        best_words = []
        for word in valid_words:
            if not down:
                best_words.append((word, self.get_word_score(
                    word, start, (start[0], start[1] + self.len(word) - 1))))
            else:
                best_words.append((word, self.get_word_score(
                    word, start, (start[0] + self.len(word) - 1, start[1]))))
        best_words.sort(key=lambda x: (-x[1], x[0]))
        player.best_words = []
        print(f'\nMelhores palavras player {player}: ')
        for i, (word, score) in enumerate(best_words[:10]):
            print(f'{word} - {score}', end=' | ')
            if i > 0 and i % 5 == 0:
                print()
            player.best_words.append((word, score))
        print()

    def split_word(self, word):
        if isinstance(word, list):
            word = ''.join(word)
        word = re.sub(r'\[(\w)\]', r'*\1', word)
        split_result = []
        i = 0
        while i < len(word):
            if word[i] == '*':
                split_result.append('*' + word[i + 1])
                i += 2
            else:
                split_result.append(word[i])
                i += 1
        return split_result

    def join_word(self, word):
        return re.sub(r'\*(\w)', r'[\1]', ''.join(word))

    def show_tiles(self, player=0):
        if player < 2:
            print(f'Player 1: {self.player1.tiles}')
        if player in (0, 2):
            print(f'Player 2: {self.player2.tiles}')

    def show_bag(self):
        counter = Counter(self.bag)
        print('Bolsa de palavras:\n|', end='')
        for letter, count in sorted(counter.items()):
            print(f' {letter}: {count}', end=' |')
        print()

    def print_board(self):
        for i in range(15):
            print(' '.join(map(str, self.board[i])))

    def show_scores(self):
        print(f'Pontuação player 1: {self.player1.score}')
        print(f'Pontuação player 2: {self.player2.score}')

    def get_player(self, id):
        return self.player1 if str(id) == '1' else self.player2

    def tiles_touching(self, word_path):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for (a, b) in word_path:
            if self.board[a][b].is_occupied:
                return True
            for (dx, dy) in directions:
                x, y = a + dx, b + dy
                if (0 <= x <= 14 and 0 <= y <= 14 and
                        self.board[x][y].is_occupied):
                    return True
        return False

    def switch_current_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def challenge(self, current_player):
        player = self.player1 if current_player == 2 else self.player2
        if not player.previous_play:
            print('O oponente não jogou nenhuma palavra')
            return False
        path = player.previous_play
        prev_word = self.get_word_from_board(path[0], path[-1])
        invalid_words = []
        if not self.trie.search(prev_word):
            invalid_words.append(prev_word)
        if path[0][0] == path[-1][0]:
            for i, j in path:
                x = i
                while x > 0 and self.board[x - 1][j].is_occupied:
                    x -= 1
                start = (x, j)
                x = i
                while x < 14 and self.board[x + 1][j].is_occupied:
                    x += 1
                end = (x, j)
                if start == end:
                    continue
                word = self.get_word_from_board(start, end)
                if not self.trie.search(word):
                    invalid_words.append(word)
        else:
            for i, j in path:
                y = j
                while y > 0 and self.board[i][y - 1].is_occupied:
                    y -= 1
                start = (i, y)
                y = j
                while y < 14 and self.board[i][y + 1].is_occupied:
                    y += 1
                end = (i, y)
                if start == end:
                    continue
                word = self.get_word_from_board(start, end)
                if not self.trie.search(word):
                    invalid_words.append(word)
        if invalid_words:
            print('Desafio aceito! Palavras inválidas: '
                  f'{", ".join(invalid_words)}')
            self.undo_play(player)
            return True
        print('Desafio recusado, a jogada anterior foi válida!')
        self.switch_current_player()
        return False

    def get_word_from_board(self, start, end):
        word = []
        if start[0] == end[0]:
            word_path = [(start[0], start[1] + i) for i in range(
                abs(start[1] - end[1]) + 1)]
        else:
            word_path = [(start[0] + i, start[1]) for i in range(
                abs(start[0] - end[0]) + 1)]
        for i, j in word_path:
            c = self.board[i][j].letter
            word.append(
                c if c != '*' else f'[{self.board[i][j].blank_letter}]')
        return ''.join(word)

    def undo_play(self, player):
        if not player.previous_draw:
            print('Não há nenhuma jogada anterior\n')
            return False
        for tile in player.previous_draw:
            self.bag.insert(random.randint(0, len(self.bag)), tile)
        player.previous_draw = None
        for i, j in self.previous_played_tiles:
            letter = self.board[i][j].letter
            player.tiles.append(letter)
            self.board[i][j].clear_square()
        return True

    def get_extra_score(self, path):
        extra_score = 0
        if path[0][0] == path[-1][0]:
            for i, j in path:
                above_occupied = self.board[i - 1][j].is_occupied
                below_occupied = self.board[(i + 1) % 15][j].is_occupied
                if ((i == 0 and not below_occupied) or
                        (i == 14 and not above_occupied)):
                    continue
                if ((i == 0 and below_occupied) or
                        (i < 14 and below_occupied and not above_occupied)):
                    start = (i, j)
                    x = i
                    while x < 14 and self.board[x + 1][j].is_occupied:
                        x += 1
                    end = (x, j)
                    word = self.get_word_from_board(start, end)
                    extra_score += self.get_word_score(word, start, end)
                    continue
                if ((i == 14 and above_occupied) or
                        (i > 0 and above_occupied and not below_occupied)):
                    end = (i, j)
                    x = i
                    while x > 0 and self.board[x - 1][j].is_occupied:
                        x -= 1
                    start = (x, j)
                    word = self.get_word_from_board(start, end)
                    extra_score += self.get_word_score(word, start, end)
        else:
            for i, j in path:
                left_occupied = self.board[i][j - 1].is_occupied
                right_occupied = self.board[i][(j + 1) % 15].is_occupied
                if ((j == 0 and not right_occupied) or
                        (j == 14 and not left_occupied)):
                    continue
                if ((j == 0 and right_occupied) or
                        (j < 14 and right_occupied and not left_occupied)):
                    start = (i, j)
                    y = j
                    while y < 14 and self.board[i][y + 1].is_occupied:
                        y += 1
                    end = (i, y)
                    word = self.get_word_from_board(start, end)
                    extra_score += self.get_word_score(word, start, end)
                    continue
                if ((j == 14 and left_occupied) or
                        (j > 0 and left_occupied and not right_occupied)):
                    end = (i, j)
                    y = j
                    while y > 0 and self.board[i][y - 1].is_occupied:
                        y -= 1
                    start = (i, y)
                    word = self.get_word_from_board(start, end)
                    extra_score += self.get_word_score(word, start, end)
        return extra_score

    def play_word(self, word, start_pos, down=True):
        player = self.current_player
        word = self.split_word(word)
        if not player.has_tiles(word):
            print('Você não possui as letras para jogar esta palavra')
            return False
        if down:
            end_pos = (start_pos[0] + len(word) - 1, start_pos[1])
            word_path = [(i, start_pos[1]) for i in range(
                start_pos[0], end_pos[0] + 1)]
        else:
            end_pos = (start_pos[0], start_pos[1] + len(word) - 1)
            word_path = [(start_pos[0], i) for i in range(
                start_pos[1], end_pos[1] + 1)]
        if end_pos[0] > 14 or end_pos[1] > 14:
            print('Posição inválida')
            return False
        if self.tiles_on_board == 0:
            if self.center not in word_path:
                print('A primeira palavra deve passar pelo centro (8, 8)')
                return False
        elif not self.tiles_touching(word_path):
            print('Sua palavra deve tocar em uma palavra já jogada')
            return False
        tiles_to_add = {}
        for i, (a, b) in enumerate(word_path):
            tile = word[i]
            if self.board[a][b].is_occupied and str(self.board[a][b]) != tile:
                print('Posição ocupada por outra letra')
                return False
            tiles_to_add[(a, b)] = tile
        for (a, b), tile in tiles_to_add.items():
            self.board[a][b].set_letter(tile)
        word_score = self.get_word_score(word, start_pos, end_pos)
        player.previous_score = player.score
        play_score = word_score + self.get_extra_score(word_path)
        player.score += play_score
        self.tiles_on_board += len(tiles_to_add)
        self.previous_played_tiles = tiles_to_add.keys()
        try:
            player.remove_tiles(word)
        except ValueError:
            print('Jogada inválida!')
            return False
        print(f'Jogador {player} jogou > {self.join_word(word)} < por '
              f'{play_score} pontos')
        player.draw_tiles(self.bag)
        player.previous_play = word_path
        self.switch_current_player()
        self.previous_play_info = {
            'player': player.id,
            'word': self.join_word(word),
            'play_score': play_score
        }
        player.show_tiles = False
        return True
