from collections import Counter, defaultdict, deque
from random import randint, random, shuffle
from typing import LiteralString

from src.boardcell import BoardCell
from src.bot import Bot
from src.player import Player
from src.tile import Tile
from src.trie import Trie
from src.utils import get_end_pos, get_word_path


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
        self.board = [[BoardCell() for _ in range(15)] for _ in range(15)]
        self.bag = None
        self.vs_bot = vs_bot
        self.player1 = self.player2 = None
        self.current_player = None
        self.previous_played_tiles = None
        self.tiles_on_board = 0
        self.previous_play_info = {}
        self.unseen_tiles = Counter(self.initial_tiles)
        self.winner = None
        self.play_memo = set()
        self.passes_counter = 0
        self.start_game()

    def start_game(self) -> None:
        self.set_multipliers()
        shuffle(self.initial_tiles)
        self.bag = deque([Tile(letter, self.values[letter])
                          for letter in self.initial_tiles])
        self.initial_tiles.sort()
        self.player1 = Player(1) if not self.vs_bot else Bot(1)
        self.player2 = Player(2)
        self.draw_tiles(self.player1)
        self.draw_tiles(self.player2)
        self.current_player = self.player1

    def draw_tiles(self, player, num=7) -> None:
        draw = []
        tiles = player.tiles
        left = num
        while self.bag and left > 0:
            tile = self.bag.pop()
            draw.append(tile)
            tiles.append(tile)
            tile.where = f'p{player}'
            left -= 1
        player.previous_draw = draw
        return num - left

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
        if (end[0] - start[0] + 1 != len(word) and
                end[1] - start[1] + 1 != len(word)):
            raise ValueError('Palavra ou posições inválidas')
        word_path, _ = get_word_path(start, len(word), start[1] == end[1])
        word_multiplier, score = 1, 0
        for i, (a, b) in enumerate(word_path):
            mult = self.board[a][b].letter_multiplier
            score += self.values.get(word[i], 0) * mult
            word_multiplier = max(
                word_multiplier, self.board[a][b].word_multiplier)
        return score * word_multiplier

    def show_tiles(self, player=0) -> None:
        if player < 2:
            print(f'Player 1: {self.player1.get_tiles()}')
        if player in (0, 2):
            print(f'Player 2: {self.player2.get_tiles()}')

    def show_bag(self) -> None:
        counter = Counter(map(str, self.bag))
        print('Bolsa de palavras:\n|', end='')
        for letter, count in sorted(counter.items()):
            print(f' {letter}: {count}', end=' |')
        print()

    def print_board(self) -> None:
        for i in range(15):
            print(' '.join(map(str, self.board[i])))

    def show_scores(self) -> None:
        print(f'Player 1: {self.player1.score} pontos')
        print(f'Player 2: {self.player2.score} pontos')

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

    def find_invalid_words(self, path, get_all_words=True) -> list:
        word = self.get_word_from_board(path[0], path[-1])
        if not self.trie.search(word):
            return [word]
        invalid_words = []
        down = path[0][1] == path[-1][1]
        for i, j in path:
            _, word = self.get_full_word(
                (i, j), str(self.board[i][j]), not down)
            if len(word) < 2:
                continue
            if not self.trie.search(word):
                if not get_all_words:
                    return [word]
                invalid_words.append(word)
        return invalid_words

    def challenge(self) -> bool:
        opponent = self.get_player(3 - self.current_player.id)
        if not self.current_player.can_challenge:
            print('Desafio inválido')
            return False
        if not opponent.previous_play:
            print('O oponente não jogou nenhuma palavra')
            return False
        path = opponent.previous_play
        invalid_words = self.find_invalid_words(path)
        self.passes_counter += 1
        if self.passes_counter >= 6:
            self.forfeit()
            return False
        if invalid_words:
            print('Desafio aceito! Palavras inválidas: '
                  f'{', '.join(invalid_words)}')
            self.previous_play_info = {
                'challenge_ok': 'aceito',
                'challenged_player': opponent.id,
                'challenger': 3 - opponent.id,
                'invalid_words': invalid_words
            }
            self.undo_play(opponent)
            self.set_challenge_flags()
            return True
        print('Desafio recusado, a jogada anterior foi válida!')
        self.switch_current_player()
        self.previous_play_info = {
            'challenge_ok': 'rejeitado',
            'challenger': 3 - opponent.id,
            'challenged_player': opponent.id
        }
        return False

    def forfeit(self) -> None:
        player = self.current_player
        opponent = self.get_player(3 - player.id)
        player_hand_score = sum(map(int, player.tiles))
        opponent_hand_score = sum(map(int, opponent.tiles))
        player.score += player_hand_score
        opponent.score += opponent_hand_score
        self.winner = max(self.player1, self.player2)
        print('Fim da partida por repetição de passes')
        print(f'Player {self.winner} venceu!')

    def exchange_tiles(self) -> bool:
        player = self.current_player
        tiles = player.tiles
        tiles_on_hand = tiles[:]
        drawn_tiles = self.draw_tiles(player, len(tiles_on_hand))
        if drawn_tiles == 0:
            print('Troca inválida\n')
            self.previous_play_info = {'exchange_ok': 'inválida'}
            return False
        player.remove_tiles(tiles_on_hand[:drawn_tiles])
        self.move_tiles_to_bag(tiles_on_hand[:drawn_tiles])
        print(f'Player {player} trocou de peças com sucesso\n')
        self.previous_play_info = {'exchange_ok': 'válida'}
        player.show_tiles = False
        self.switch_current_player()
        self.set_challenge_flags()
        self.passes_counter += 1
        if self.passes_counter >= 6:
            self.forfeit()
            return False
        return True

    def move_tiles_to_bag(self, tiles) -> None:
        for tile in tiles:
            self.bag.append(tile)
            tile.where = 'bag'
        shuffle(self.bag)

    def set_challenge_flags(self, p1=False, p2=False) -> None:
        self.player1.can_challenge = p1
        self.player2.can_challenge = p2

    def get_word_from_board(self, start, end) -> LiteralString:
        word = []
        down = start[1] == end[1]
        length = (end[1] - start[1] or end[0] - start[0]) + 1
        word_path, _ = get_word_path(start, length, down)
        for i, j in word_path:
            if not self.board[i][j].is_occupied:
                raise ValueError(f'Word path inválido: {word_path}')
            word.append(f'{self.board[i][j]}')
        return ''.join(word)

    def undo_play(self, player) -> bool:
        if not player.previous_draw:
            print('Não há nenhuma jogada anterior\n')
            return False
        player.remove_tiles(player.previous_draw)
        self.move_tiles_to_bag(player.previous_draw)
        player.previous_draw = None
        for i, j in self.previous_played_tiles:
            tile = self.board[i][j].clear()
            player.add_tile(tile)
            self.tiles_on_board -= 1
        player.score = player.previous_score
        self.update_unseen_tiles()
        return True

    def get_extra_score(self, path) -> int:
        extra_score = 0
        down = path[0][1] == path[-1][1]
        for i, j in path:
            start, word = self.get_full_word(
                (i, j), str(self.board[i][j]), not down)
            if len(word) < 2:
                continue
            end = get_end_pos(start, len(word), not down)
            extra_score += self.get_word_score(word, start, end)
        return extra_score

    def get_full_word(self, start, word, down=True) -> tuple:
        full_word = word.split()
        if down:
            y = start[1]
            start_x = start[0]
            end_x = start[0] + len(word) - 1
            for i in range(end_x + 1, 15):
                if not self.board[i][y].is_occupied:
                    break
                full_word.append(f'{self.board[i][y]}')
            for i in range(start_x - 1, -1, -1):
                if not self.board[i][y].is_occupied:
                    break
                start = (i, y)
                full_word.insert(0, f'{self.board[i][y]}')
            return start, ''.join(full_word)
        x = start[0]
        start_y = start[1]
        end_y = start[1] + len(word) - 1
        for i in range(end_y + 1, 15):
            if not self.board[x][i].is_occupied:
                break
            full_word.append(f'{self.board[x][i]}')
        for i in range(start_y - 1, -1, -1):
            if not self.board[x][i].is_occupied:
                break
            start = (x, i)
            full_word.insert(0, f'{self.board[x][i]}')
        return start, ''.join(full_word)

    def get_best_words(self, player, start, down, on_board) -> list:
        x, y = start
        min_size = max(on_board) if on_board else 0
        max_size = 15 - x if down else 15 - y
        if max_size < min_size:
            return [('', 0)]
        valid_words = self.trie.find_valid_words(
            player, on_board, min_size, max_size)[:10]
        best_words = []
        for word in valid_words:
            path, end = get_word_path(start, len(word), down)
            score = self.get_word_score(word, start, end)
            score += self.get_extra_score(path)
            best_words.append((word, score))
        best_words = sorted(best_words, key=lambda x: (-x[1], x[0]))
        player.best_words = best_words
        return best_words or [('', 0)]

    def bot_play(self) -> None:
        if not self.current_player.is_bot:
            raise ValueError('Player não é um bot')
        bot = self.current_player
        if self.tiles_on_board == 0:
            down = random() < 0.5
            word, _ = self.get_best_words(bot, (7, 7), down, None)[0]
            if not word:
                print('O bot não encontrou palavras válidas.')
                print('Realizando troca de peças\n')
                self.exchange_tiles()
                return
            start = ((randint(7 - len(word) + 1, 7), 7)
                     if down else (7, randint(7 - len(word) + 1, 7)))
            self.play_word(word, start, down)
            return
        current_best_play = ('', 0, (7, 7), False)  # word, score, start, down
        for i, j in self.get_all_occupied_tiles():
            down = False
            for k in range(max(0, j - 7), j + 1):
                if (i, k, down) in self.play_memo:
                    continue
                path = self.get_valid_path_to_play((i, k), down)
                on_board = self.get_occupied_tiles_positions_from_path(path)
                best_plays = self.get_best_words(bot, (i, k), down, on_board)
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
                best_plays = self.get_best_words(bot, (k, j), down, on_board)
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
        self.exchange_tiles()

    def get_current_best_play(self, current_best, play, x, y, down) -> tuple:
        word, _ = play
        temp_tiles = []
        i, j = x, y
        for letter in word:
            cell = self.board[i][j]
            if not cell.is_occupied:
                tile = Tile(letter, self.values[letter])
                cell.place_tile(tile)
                if letter.isupper():
                    tile.blank_letter = letter
                temp_tiles.append(cell)
            if cell.is_occupied and letter != f'{cell.tile}':
                return current_best
            i += down
            j += not down
            if i >= 15 or j >= 15:
                self.undo_temp_plays(temp_tiles)
                return current_best
        start, full_word = self.get_full_word((x, y), word, down)
        path, end_pos = get_word_path(start, len(full_word), down)
        score = self.get_word_score(full_word, start, end_pos)
        score += self.get_extra_score(path)
        invalid_words = self.find_invalid_words(path, get_all_words=False)
        self.undo_temp_plays(temp_tiles)
        if invalid_words:
            return current_best
        return max(current_best, (play[0], score, start, down),
                   key=lambda k: k[1])

    def undo_temp_plays(self, temp_tiles) -> None:
        for cell in temp_tiles:
            cell.clear()

    def get_all_occupied_tiles(self) -> list:
        return [(i, j) for i in range(15) for j in range(15)
                if self.board[i][j].is_occupied]

    def get_occupied_tiles_positions_from_path(self, path) -> dict:
        return {p: f'{self.board[x][y]}' for p, (x, y) in enumerate(path)
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
            letter = self.board[i][j].tile.letter
            self.unseen_tiles[letter] -= 1

    def play_word(self, word, start, down=True) -> bool:
        player = self.current_player
        opponent = self.get_player(3 - player.id)
        start, word = self.get_full_word(start, word, down)
        word_path, end = get_word_path(start, len(word), down)
        if end[0] > 14 or end[1] > 14:
            print('Posição inválida')
            return False
        if self.tiles_on_board == 0:
            if (7, 7) not in word_path:
                print('A primeira palavra deve passar pelo centro (7, 7)')
                return False
        elif not self.are_tiles_touching(word_path):
            print('Sua palavra deve tocar em uma palavra já jogada')
            return False
        tiles_to_add = {}
        for i, (a, b) in enumerate(word_path):
            letter = word[i]
            if self.board[a][b].is_occupied:
                if str(self.board[a][b]) != letter:
                    print('Posição ocupada por outra letra')
                    print(f'Palavra: {word}, wordpath: {word_path}')
                    return False
                continue
            tiles_to_add[(a, b)] = letter
        if not player.has_tiles(tiles_to_add.values()):
            print('Você não possui as letras para jogar esta palavra')
            return False
        for (a, b), letter in tiles_to_add.items():
            tile = player.retrieve_tile(letter)
            self.board[a][b].place_tile(tile)
            if letter.isupper():
                tile.blank_letter = letter
        self.update_unseen_tiles()
        word_score = self.get_word_score(word, start, end)
        player.previous_score = player.score
        play_score = word_score + self.get_extra_score(word_path)
        if len(tiles_to_add) == 7:  # bingo extra score
            play_score += 50
        player.score += play_score
        self.tiles_on_board += len(tiles_to_add)
        self.previous_played_tiles = tiles_to_add.keys()
        print(f'Jogador {player} jogou > {word} < por '
              f'{play_score} pontos')
        self.draw_tiles(player, len(tiles_to_add))
        self.show_tiles(1)
        self.show_tiles(2)
        player.previous_play = word_path
        self.switch_current_player()
        self.previous_play_info = {
            'player': player.id,
            'word': word,
            'play_score': play_score
        }
        player.show_tiles = False
        player.can_challenge = False
        opponent.can_challenge = True
        if len(self.bag) == 0 and not player.tiles:
            opponent_hand_score = sum(map(int, opponent.tiles))
            player.score += opponent_hand_score
            self.winner = max(self.player1, self.player2)
            print(f'Player {self.winner} venceu!')
        self.passes_counter = 0
        return True
