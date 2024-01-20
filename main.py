import pygame

from src import GameWindow, Scrabble, Trie


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
        app.draw_grid()
        app.handle_events()
        app.draw_info_section()
        app.draw_board_tiles()
        app.draw_arrow()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
