from collections import Counter, defaultdict, deque
from random import randint, random, shuffle
from typing import LiteralString

from src.boardsquare import BoardSquare
from src.bot import Bot
from src.player import Player
from src.trie import Trie
from src.utils import (clear_word, get_end_pos, get_word_path, word_join,
                       word_len, word_split)


class Scrabble:
    def __init__(self, trie: Trie, vs_bot=False):
        self.values = defaultdict(int, {
            'a': 1, 'b': 3, 'c': 2, 'ç': 3, 'd': 2, 'e': 1, 'f': 4,
            'g': 4, 'h': 4, 'i': 1, 'j': 5, 'l': 2, 'm': 1, 'n': 3,
            'o': 1, 'p': 2, 'q': 6, 'r': 1, 's': 1, 't': 1,
            'u': 1, 'v': 4, 'x': 8, 'z': 8, '*': 0
        })
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
        self.vs_bot = vs_bot
        self.player1 = self.player2 = None
        self.current_player = None
        self.previous_played_tiles = None
        self.tiles_on_board = 0
        self.center = (7, 7)
        self.previous_play_info = {}
        self.unseen_tiles = Counter(self.initial_tiles)
        self.winner = None
        self.play_memo = set()
        self.start_game()

    def start_game(self) -> None:
        self.set_multipliers()
        shuffle(self.initial_tiles)
        self.bag = deque(self.initial_tiles)
        self.initial_tiles.sort()
        self.player1 = Player(1) if not self.vs_bot else Bot(1)
        self.player2 = Player(2)
        self.player1.draw_tiles(self.bag)
        self.player2.draw_tiles(self.bag)
        self.current_player = self.player1

    def set_multipliers(self) -> None:
        triple_word = [(0, 0), (0, 14), (14, 0), (14, 14),
                       (0, 7), (7, 0), (7, 14), (14, 7)]
        double_word = [(7, 7), (1, 1), (2, 2), (3, 3), (4, 4),
                       (10, 10), (11, 11), (12, 12), (13, 13),
                       (1, 13), (2, 12), (3, 11), (4, 10),
                       (10, 4), (11, 3), (12, 2), (13, 1)]
        triple_letter = [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13),
                         (9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 9)]
        double_letter = [(0, 3), (0, 11), (2, 6), (2, 8), (3, 0),
                         (3, 7), (3, 14), (6, 2), (6, 6), (6, 8),
                         (6, 12), (7, 3), (7, 11), (8, 2), (8, 6),
                         (8, 8), (8, 12), (11, 0), (11, 7), (11, 14),
                         (12, 6), (12, 8), (14, 3), (14, 11)]
        for a, b in triple_word:
            self.board[a][b].word_multiplier = 3
        for a, b in double_word:
            self.board[a][b].word_multiplier = 2
        for a, b in triple_letter:
            self.board[a][b].letter_multiplier = 3
        for a, b in double_letter:
            self.board[a][b].letter_multiplier = 2

    def get_word_score(self, word, start, end) -> int:
        word = word_split(word)
        if (end[0] - start[0] + 1 != word_len(word) and
                end[1] - start[1] + 1 != word_len(word)):
            raise ValueError('Palavra ou posições inválidas')
        if start[0] == end[0]:
            word_path = [(start[0], i)
                         for i in range(start[1], end[1] + 1)]
        else:
            word_path = [(i, start[1])
                         for i in range(start[0], end[0] + 1)]
        word_multiplier, score = 1, 0
        for i, (a, b) in enumerate(word_path):
            mult = self.board[a][b].letter_multiplier
            score += self.values.get(word[i].lower(), 0) * mult
            word_multiplier *= self.board[a][b].word_multiplier
        return score * word_multiplier

    def show_tiles(self, player=0) -> None:
        if player < 2:
            print(f'Player 1: {self.player1.tiles}')
        if player in (0, 2):
            print(f'Player 2: {self.player2.tiles}')

    def show_bag(self) -> None:
        counter = Counter(self.bag)
        print('Bolsa de palavras:\n|', end='')
        for letter, count in sorted(counter.items()):
            print(f' {letter}: {count}', end=' |')
        print()

    def print_board(self) -> None:
        for i in range(15):
            print(' '.join(map(str, self.board[i])))

    def show_scores(self) -> None:
        print(f'Pontuação player 1: {self.player1.score}')
        print(f'Pontuação player 2: {self.player2.score}')

    def get_player(self, id) -> Player:
        return self.player1 if id == 1 else self.player2

    def are_tiles_touching(self, word_path) -> bool:
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

    def switch_current_player(self) -> None:
        self.current_player = self.get_player(3 - self.current_player.id)

    def find_invalid_words(self, word_path) -> list:
        word = self.get_word_from_board(word_path[0], word_path[-1])
        if not self.trie.search(clear_word(word)):
            return [word]
        invalid_words = []
        if word_path[0][0] == word_path[-1][0]:  # horizontal
            for i, j in word_path:
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
                if not self.trie.search(clear_word(word)):
                    invalid_words.append(word)
            return invalid_words
        for i, j in word_path:  # vertical
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
            if not self.trie.search(clear_word(word)):
                invalid_words.append(word)
        return invalid_words

    def challenge(self) -> bool:
        player = self.player1 if self.current_player.id == 2 else self.player2
        if not player.previous_play:
            print('O oponente não jogou nenhuma palavra')
            return False
        path = player.previous_play
        prev_word = self.get_word_from_board(path[0], path[-1])
        invalid_words = []
        if not self.trie.search(clear_word(prev_word)):
            invalid_words.append(prev_word)
        invalid_words += self.find_invalid_words(path)
        if invalid_words:
            print('Desafio aceito! Palavras inválidas: '
                  f'{', '.join(invalid_words)}')
            self.previous_play_info = {
                'challenge': True,
                'challenge_ok': 'aceito',
                'challenged_player': player.id,
                'challenger': 3 - player.id,
                'invalid_words': invalid_words
            }
            self.undo_play(player)
            self.set_challenge_flags()
            return True
        print('Desafio recusado, a jogada anterior foi válida!')
        self.switch_current_player()
        self.previous_play_info = {
            'challenge': True,
            'challenge_ok': 'rejeitado',
            'challenger': 3 - player.id,
            'challenged_player': player.id
        }
        return False

    def forfeit(self) -> None:
        player = self.current_player
        opponent = self.get_player(3 - player.id)
        print(f'Player {player} perdeu a partida')
        print(f'Player {opponent} venceu!')

    def exchange_tiles(self, tiles) -> bool:
        player = self.current_player
        if (len(tiles) > len(self.bag) or
                not all(t in player.tiles for t in tiles)):
            print('Troca inválida\n')
            self.previous_play_info = {
                'exchange': True,
                'exchange_ok': 'inválida',
            }
            return False
        tiles_on_hand = tiles[:]
        player.remove_tiles(tiles)
        player.draw_tiles(self.bag)
        for tile in tiles_on_hand:
            self.bag.insert(randint(0, len(self.bag)), tile)
        print(f'Player {player} trocou de peças com sucesso\n')
        self.previous_play_info = {
            'exchange': True,
            'exchange_ok': 'válida',
        }
        player.show_tiles = False
        self.switch_current_player()
        self.set_challenge_flags()
        return True

    def set_challenge_flags(self, p1=False, p2=False) -> None:
        self.player1.can_challenge = p1
        self.player2.can_challenge = p2

    def get_word_from_board(self, start, end) -> LiteralString:
        word = []
        if start[0] == end[0]:
            word_path = [(start[0], start[1] + i) for i in range(
                abs(start[1] - end[1]) + 1)]
        else:
            word_path = [(start[0] + i, start[1]) for i in range(
                abs(start[0] - end[0]) + 1)]
        for i, j in word_path:
            c = self.board[i][j].blank_letter or self.board[i][j].letter
            word.append(c)
        return ''.join(word)

    def undo_play(self, player) -> bool:
        if not player.previous_draw:
            print('Não há nenhuma jogada anterior\n')
            return False
        player.remove_tiles(player.previous_draw)
        for tile in player.previous_draw:
            self.bag.insert(randint(0, len(self.bag)), tile)
        player.previous_draw = None
        for i, j in self.previous_played_tiles:
            letter = self.board[i][j].letter
            player.tiles.append(letter)
            self.board[i][j].clear_square()
            self.tiles_on_board -= 1
        player.score = player.previous_score
        self.update_unseen_tiles()
        return True

    def get_extra_score(self, path) -> int:
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
            return extra_score
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

    def get_full_word(self, start, word, down=True) -> tuple:
        full_word = word.split()
        if down:
            end_x = start[0] + word_len(word) - 1
            end_y = start[1]
            start_x = start[0]
            for i in range(end_x + 1, 15):
                if not self.board[i][end_y].is_occupied:
                    break
                full_word.append(self.board[i][end_y].blank_letter or
                                 self.board[i][end_y].letter)
            for i in range(start_x - 1, -1, -1):
                if not self.board[i][end_y].is_occupied:
                    break
                start = (i, end_y)
                full_word.insert(0, (self.board[i][end_y].blank_letter or
                                     self.board[i][end_y].letter))
            return start, ''.join(full_word)
        end_x = start[0]
        end_y = start[1] + word_len(word) - 1
        start_y = start[1]
        for i in range(end_y + 1, 15):
            if not self.board[end_x][i].is_occupied:
                break
            full_word.append(self.board[end_x][i].blank_letter or
                             self.board[end_x][i].letter)
        for i in range(start_y - 1, -1, -1):
            if not self.board[end_x][i].is_occupied:
                break
            start = (end_x, i)
            full_word.insert(0, (self.board[end_x][i].blank_letter or
                                 self.board[end_x][i].letter))
        return start, ''.join(full_word)

    def find_valid_words(self, player, on_board=None, min_size=0, max_size=15) -> list:  # noqa
        def dfs(node, letters, letter_freq):
            if node.is_word and min_size <= len(letters) <= max_size:
                valid_words.append(''.join(letters))
            if (index := len(letters)) in on_board:
                if (letter := on_board[index]) in node.children:
                    letters.append(letter)
                    dfs(node.children[letter], letters, letter_freq)
                    letters.pop()
                return
            for letter, child in node.children.items():
                if letter_freq[letter] > 0:
                    letters.append(letter)
                    letter_freq[letter] -= 1
                    dfs(child, letters, letter_freq)
                    letters.pop()
                    letter_freq[letter] += 1
            if letter_freq['*'] > 0:
                for letter, child in node.children.items():
                    letters.append(f'[{letter}]')
                    letter_freq['*'] -= 1
                    dfs(child, letters, letter_freq)
                    letters.pop()
                    letter_freq['*'] += 1

        valid_words = []
        if not on_board:
            on_board = {}
        letter_freq = defaultdict(int)
        for letter in player.tiles:
            letter_freq[letter.lower()] += 1
        dfs(self.trie.root, [], letter_freq)
        return sorted(valid_words, key=lambda x: (-len(x), x))

    def get_best_words(self, player, start, down, on_board) -> list:
        player = self.get_player(player)
        x, y = start
        min_size = max(on_board) if on_board else 0
        max_size = 15 - x if down else 15 - y
        if max_size < min_size:
            return [('', 0)]
        valid_words = self.find_valid_words(
            player, on_board, min_size, max_size)[:10]
        best_words = []
        for word in valid_words:
            end = get_end_pos(start, word_len(word), down)
            score = self.get_word_score(word, start, end)
            best_words.append((word, score))
        best_words = sorted(best_words, key=lambda x: (-x[1], x[0]))
        player.best_words = []
        return best_words or [('', 0)]

    def bot_play(self) -> None:
        if not self.current_player.is_bot:
            raise ValueError('Player não é um bot')
        word, _ = self.get_best_words(
            self.current_player.id, (7, 7), random() < .5, None)[0]
        if not word:
            print('O bot não encontrou palavras válidas.')
            print('Realizando troca de peças\n')
            self.exchange_tiles(self.current_player.tiles)
            return
        if self.tiles_on_board == 0:
            down = random() < 0.5
            start_pos = ((randint(7 - len(word) + 1, 7), 7)
                         if down else (7, randint(7 - len(word) + 1, 7)))
            self.play_word(word, start_pos, down)
            return
        current_best_play = ('', 0, (7, 7), False)  # word, score, start, down
        for i, j in self.get_all_occupied_tiles():
            down = False
            for k in range(max(0, j - 7), j + 1):
                if (i, k, down) in self.play_memo:
                    continue
                path = self.get_valid_path_to_play((i, k), down)
                on_board = self.get_occupied_tiles_positions_from_path(path)
                best_plays = self.get_best_words(1, (i, k), down, on_board)
                if len(best_plays[0][0]) > len(on_board):
                    current_best_play = self.get_current_best_play(
                        current_best_play, best_plays[0], i, k, down)
                self.play_memo.add((i, k, down))
            down = True
            for k in range(max(0, i - 7), i + 1):
                if (k, j, down) in self.play_memo:
                    continue
                path = self.get_valid_path_to_play((k, j), down)
                on_board = self.get_occupied_tiles_positions_from_path(path)
                best_plays = self.get_best_words(1, (k, j), down, on_board)
                if len(best_plays[0][0]) > len(on_board):
                    current_best_play = self.get_current_best_play(
                        current_best_play, best_plays[0], k, j, down)
                self.play_memo.add((k, j, down))
        word, _, (x, y), down = current_best_play
        self.play_memo.clear()
        if (word and ((down and len(word) + x < 15) or
                      (not down and len(word) + y < 15))):
            if self.play_word(word, (x, y), down):
                return
        print('O bot não encontrou jogadas válidas')
        opponent = self.get_player(3 - self.current_player.id)
        if opponent.previous_play and random() < 0.1:
            print('O bot está desafiando o player\n')
            if self.challenge():
                print('Desafio aceito!\n')
            return
        print('Realizando troca de peças\n')
        self.exchange_tiles(self.current_player.tiles)

    def get_current_best_play(self, current_best, play, x, y, down) -> tuple:
        word, _ = play
        word = clear_word(word)
        temp_tiles = []
        i, j = x, y
        for letter in word:
            tile = self.board[i][j]
            if not tile.is_occupied:
                tile.set_letter(letter)
                temp_tiles.append(tile)
            if (tile.is_occupied and letter not in (
                    tile.letter, tile.blank_letter)):
                return current_best
            i += down
            j += not down
            if i >= 15 or j >= 15:
                self.undo_temp_plays(temp_tiles)
                return current_best
        start, full_word = self.get_full_word((x, y), word, down)
        end_pos = get_end_pos(start, word_len(full_word), down)
        score = self.get_word_score(full_word, start, end_pos)
        path = get_word_path(start, down, full_word)[0]
        invalid_words = self.find_invalid_words(path)
        self.undo_temp_plays(temp_tiles)
        if invalid_words:
            return current_best
        return max(current_best, (play[0], score, start, down),
                   key=lambda k: k[1])

    def undo_temp_plays(self, temp_tiles) -> None:
        for tile in temp_tiles:
            tile.clear_square()

    def get_all_occupied_tiles(self) -> list:
        return [(i, j) for i in range(15) for j in range(15)
                if self.board[i][j].is_occupied]

    def get_occupied_tiles_positions_from_path(self, path) -> dict:
        return {p: self.board[x][y].letter for p, (x, y) in enumerate(path)
                if self.board[x][y].is_occupied}

    def get_valid_path_to_play(self, start, down) -> list:
        path = []
        left = 7
        x, y = start
        while 0 <= x < 15 and 0 <= y < 15:
            if not self.board[x][y].is_occupied:
                left -= 1
            if left < 0:
                break
            path.append((x, y))
            x += down
            y += not down
        return path

    def update_unseen_tiles(self) -> None:
        self.unseen_tiles = Counter(self.initial_tiles)
        for i, j in self.get_all_occupied_tiles():
            self.unseen_tiles[self.board[i][j].letter] -= 1

    def play_word(self, word, start_pos, down=True) -> bool:
        player = self.current_player
        opponent = self.get_player(3 - player.id)
        start_pos, word = self.get_full_word(start_pos, word, down)
        word = word_split(word)
        word_path, end_pos = get_word_path(start_pos, down, word)
        if end_pos[0] > 14 or end_pos[1] > 14:
            print('Posição inválida')
            return False
        if self.tiles_on_board == 0:
            if self.center not in word_path:
                print('A primeira palavra deve passar pelo centro (7, 7)')
                return False
        elif not self.are_tiles_touching(word_path):
            print('Sua palavra deve tocar em uma palavra já jogada')
            return False
        tiles_to_add = {}
        not_on_board = []
        for i, (a, b) in enumerate(word_path):
            tile = word[i]
            if self.board[a][b].is_occupied:
                if str(self.board[a][b]) != tile:
                    print('Posição ocupada por outra letra')
                    return False
            else:
                not_on_board.append(tile)
                tiles_to_add[(a, b)] = tile
        if not player.has_tiles(not_on_board):
            print('Você não possui as letras para jogar esta palavra')
            return False
        for (a, b), tile in tiles_to_add.items():
            self.board[a][b].set_letter(tile)
        self.update_unseen_tiles()
        word_score = self.get_word_score(word, start_pos, end_pos)
        player.previous_score = player.score
        play_score = word_score + self.get_extra_score(word_path)
        if len(not_on_board) == 7:
            play_score += 50
        player.score += play_score
        self.tiles_on_board += len(tiles_to_add)
        self.previous_played_tiles = tiles_to_add.keys()
        try:
            player.remove_tiles(not_on_board)
        except ValueError:
            print('Jogada inválida!')
            return False
        print(f'Jogador {player} jogou > {word_join(word)} < por '
              f'{play_score} pontos')
        player.draw_tiles(self.bag)
        print(self.player1.tiles)
        print(self.player2.tiles)
        player.previous_play = word_path
        self.switch_current_player()
        self.previous_play_info = {
            'player': player.id,
            'word': word_join(word),
            'play_score': play_score
        }
        player.show_tiles = False
        player.can_challenge = False
        opponent.can_challenge = True
        if len(self.bag) == 0 and not player.tiles:
            opponent_hand_score = sum(
                self.values.get(c, 0) for c in opponent.tiles)
            player.score += opponent_hand_score
            self.winner = max(self.player1, self.player2)
            print(f'Player {self.winner} venceu!')
        return True
