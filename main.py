# import pygame

from scrabble import Scrabble
from trie import Trie


def main():
    # pygame.init()
    # screen = pygame.display.set_mode((800, 600))
    # pygame.display.set_caption('Scrabble')
    # running = True
    info = '''
        Input order: [word] [row(1-indexed)] [column(1-indexed)]
        [direction: (h)orizontal/(v)ertical]
    '''
    def msg(x): return f'Player {x}: [palavra] [linha] [coluna] [h/v] -> '
    current_player = 1
    trie = Trie()
    trie.populate_from_file('words_ptbr.txt')
    game = Scrabble(trie)
    game.print_board()
    game.show_tiles()
    game.show_best_words(1)
    game.show_best_words(2)
    game.show_scores()
    while (c := input(msg(current_player))) != 'q':
        if c == 'info':
            print(info)
            continue
        word, row, col, direction = c.split(' ')
        try:
            row, col = int(row), int(col)
        except ValueError:
            print('Valor inválido')
            continue
        direction = direction.lower() in ('v', 'vertical', 'ver', 'down', 'd')
        valid_play = game.play_word(
            current_player, word, (row - 1, col - 1), direction)
        if valid_play:
            game.print_board()
            game.show_tiles()
            game.show_best_words(1)
            game.show_best_words(2)
            game.show_scores()
            current_player = 3 - current_player
        else:
            print('Jogada inválida')
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False

    # pygame.quit()


if __name__ == '__main__':
    main()
