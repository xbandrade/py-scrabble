import pygame

from app import GameWindow
from scrabble import Scrabble
from trie import Trie


def main() -> None:
    trie = Trie()
    trie.populate_from_file('words_ptbr.txt')
    game = Scrabble(trie)
    game.print_board()
    game.show_scores()
    game.show_tiles()
    running = True
    app = GameWindow(15, 48, game)
    while running:
        app.handle_events()
        app.draw_grid()
        app.draw_info_section()
        app.draw_board_tiles()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
