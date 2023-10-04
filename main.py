import pygame

from app import GameWindow
from scrabble import Scrabble
from trie import Trie


def menu(game, trie):
    info = '''
        Ordem de input: [palavra] [linha(1-indexed)] [coluna(1-indexed)]
        [direção: (h)orizontal/(v)ertical]
    '''
    def msg(x): return f'Player {x}: [palavra] [linha] [coluna] [h/v] -> '
    current_player = 1
    while (c := input(msg(current_player))) != 'q':
        if c == 's':
            game.show_bag()
            game.show_tiles()
            game.show_best_words(1)
            game.show_best_words(2)
            game.show_scores()
            game.print_board()
            continue
        elif c == 'c':
            challenge_accepted = game.challenge(current_player)
            if not challenge_accepted:
                current_player = 3 - current_player
            continue
        if c.startswith('info'):
            print(info)
            continue
        elif c.startswith('-- '):  # Exchange
            _, exchange = c.split(' ')
            player = game.get_player(current_player)
            valid_play = player.exchange_tiles(exchange, game.bag)
        else:
            try:
                word, row, col, direction = c.split(' ')
                row, col = int(row), int(col)
            except ValueError:
                print('Valor inválido\n')
                continue
            direction = direction.lower() in (
                'v', 'vertical', 'ver', 'down', 'd')
            word = trie.clear_word(word)
            valid_play = game.play_word(
                current_player, word, (row - 1, col - 1), direction)
        if valid_play:
            game.print_board()
            game.show_scores()
            current_player = 3 - current_player
        else:
            print('Jogada inválida\n')


def main():
    trie = Trie()
    trie.populate_from_file('words_ptbr.txt')
    game = Scrabble(trie)
    game.print_board()
    game.show_scores()
    running = True
    app = GameWindow(15, 48, game)
    while running:
        app.handle_events()
        app.draw_info_section()
        app.draw_grid()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
