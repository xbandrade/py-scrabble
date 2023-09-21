# import pygame

from scrabble import Scrabble
from trie import Trie


def main():
    # pygame.init()
    # screen = pygame.display.set_mode((800, 600))
    # pygame.display.set_caption('Scrabble')
    # running = True
    trie = Trie('words_ptbr.txt')
    game = Scrabble(trie)
    p1_tiles = game.player1.tiles
    p2_tiles = game.player2.tiles
    print('Palavras válidas para player 1: ', *game.find_valid_words(p1_tiles))
    print('Palavras válidas para player 2: ', *game.find_valid_words(p2_tiles))
    # while running:
    #     c = input('-> ')
    #     if c == 'q':
    #         running = False
    #     else:
    #         found = trie.is_word_valid(c)
    #         if found:
    #             print('Palavra válida!')
    #         else:
    #             print('Palavra inválida')
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False

    # pygame.quit()


if __name__ == '__main__':
    main()
