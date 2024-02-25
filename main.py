import pygame

from src import GameWindow, Scrabble, Trie


def main() -> None:
    pygame.init()
    trie = Trie()
    trie.populate_from_file('words_ptbr.txt')
    app = GameWindow(15, 48)
    running = True
    while running:
        if app.go_to_menu:
            app.go_to_menu = False
            vs_bot = app.run_main_menu()
            if vs_bot is None:
                running = False
                break
            game = Scrabble(trie, vs_bot=vs_bot)
            app.game = game
            app.draw_grid_colors()
        app.draw_grid()
        app.handle_events()
        app.draw_info_section()
        app.draw_board_tiles()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
