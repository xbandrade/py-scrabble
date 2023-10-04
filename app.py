import pygame


class GameWindow:
    def __init__(self, grid_size, cell_size, game):
        pygame.init()
        self.game = game
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.info_width = 400
        self.screen = None
        self.grid_matrix = [[None for _ in range(
            grid_size)] for _ in range(grid_size)]
        self.letters_matrix = {}
        self.star_image = pygame.image.load('img/star.png')
        self.star_image = pygame.transform.scale(
            self.star_image, (self.cell_size, self.cell_size))
        self.arrow_image = pygame.image.load('img/arrow.png')
        self.arrow_image = pygame.transform.scale(
            self.arrow_image, (self.cell_size, self.cell_size))
        self.arrow_image.set_colorkey((255, 255, 255))
        self.arrow_img_right = pygame.transform.rotate(self.arrow_image, 180)
        self.arrow_img_down = pygame.transform.rotate(self.arrow_image, 90)
        self.word_start_cell = None
        self.word_curr_cell = None
        self.current_word = []
        self.arrow_down = False
        self.letters_accents = [
            'á', 'é', 'í', 'ó', 'ú', 'ã', 'õ', 'â', 'ê', 'ô',
            'Á', 'É', 'Í', 'Ó', 'Ú', 'Ã', 'Õ', 'Â', 'Ê', 'Ô']
        self.font = pygame.font.SysFont(None, 36)
        self.font_color = (0, 0, 0)
        self.setup_grid_colors()
        self.setup_display()

    def setup_display(self):
        total_width = self.grid_size * self.cell_size + self.info_width
        self.screen = pygame.display.set_mode(
            (total_width, self.grid_size * self.cell_size))
        pygame.display.set_caption('Scrabble')

    def setup_grid_colors(self):
        for i in range(len(self.game.board)):
            for j in range(len(self.game.board[0])):
                wm = self.game.board[i][j].word_multiplier
                lm = self.game.board[i][j].letter_multiplier
                if wm == 2:
                    self.grid_matrix[i][j] = (255, 0, 0, 72)
                elif wm == 3:
                    self.grid_matrix[i][j] = (255, 0, 0, 196)
                if lm == 2:
                    self.grid_matrix[i][j] = (0, 0, 255, 72)
                elif lm == 3:
                    self.grid_matrix[i][j] = (0, 0, 255, 196)

    def draw_grid(self):
        self.screen.fill((220, 220, 220))
        for x in range(0, self.screen.get_width(), self.cell_size):
            pygame.draw.line(self.screen, (0, 0, 0), (x, 0),
                             (x, self.screen.get_height()))
        for y in range(0, self.screen.get_height(), self.cell_size):
            pygame.draw.line(self.screen, (0, 0, 0), (0, y),
                             (self.screen.get_width(), y))
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                pygame.draw.rect(self.screen, (25, 25, 25), (
                    x * self.cell_size, y * self.cell_size,
                    self.cell_size, self.cell_size), 1)
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                color = self.grid_matrix[x][y]
                if color is not None:
                    cell_surface = pygame.Surface(
                        (self.cell_size, self.cell_size), pygame.SRCALPHA)
                    pygame.draw.rect(cell_surface, color,
                                     (0, 0, self.cell_size, self.cell_size))
                    self.screen.blit(cell_surface, (
                        x * self.cell_size, y * self.cell_size))
        center_x = self.grid_size // 2
        center_y = self.grid_size // 2
        background_color = (255, 0, 0)
        cell_surface = pygame.Surface(
            (self.cell_size, self.cell_size), pygame.SRCALPHA)
        pygame.draw.rect(cell_surface, background_color,
                         (0, 0, self.cell_size, self.cell_size))
        self.screen.blit(self.star_image, (center_x * self.cell_size,
                                           center_y * self.cell_size))
        if self.word_curr_cell is not None:
            x, y = self.word_curr_cell
            arrow_image = (self.arrow_img_down if self.arrow_down
                           else self.arrow_img_right)
            self.screen.blit(arrow_image, (
                x * self.cell_size, y * self.cell_size))
        info_rect = pygame.Rect(self.grid_size * self.cell_size,
                                0, self.info_width, self.screen.get_height())
        pygame.draw.rect(self.screen, (200, 200, 200), info_rect)
        if self.current_word:
            start_x, start_y = self.word_start_cell
            start_x *= self.cell_size
            start_y *= self.cell_size
            step_x, step_y = (0, self.cell_size) if self.arrow_down else (
                self.cell_size, 0)
            for letter in ''.join(self.current_word).upper():
                offset = 3
                border_width = 2
                background_surface = pygame.Surface(
                    (self.cell_size - offset, self.cell_size - offset))
                background_surface.fill((192, 192, 192))
                pygame.draw.rect(
                    background_surface, (100, 100, 100),
                    (0, 0, background_surface.get_width(),
                     background_surface.get_height()),
                    border_width
                )
                letter_text = self.font.render(letter, True, self.font_color)
                letter_rect = letter_text.get_rect(
                    center=(self.cell_size // 2, self.cell_size // 2))
                background_surface.blit(letter_text, letter_rect)
                self.screen.blit(background_surface, (start_x, start_y))
                start_x += step_x
                start_y += step_y

    def draw_info_section(self):
        info_rect = pygame.Rect(0, 0, self.info_width,
                                self.screen.get_height())
        pygame.draw.rect(self.screen, (200, 200, 200), info_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                self.current_word = []
                if (0 <= x < self.grid_size * self.cell_size and
                        0 <= y < self.grid_size * self.cell_size):
                    grid_x = x // self.cell_size
                    grid_y = y // self.cell_size
                    if (grid_x, grid_y) == self.word_curr_cell:
                        self.arrow_down = not self.arrow_down
                    else:
                        self.arrow_down = False
                        self.word_start_cell = (grid_x, grid_y)
                        self.word_curr_cell = self.word_start_cell
                else:
                    self.word_start_cell = self.word_curr_cell = None
            if event.type == pygame.KEYDOWN and self.word_start_cell:
                if (self.word_curr_cell and
                    (event.unicode.isalpha() or
                     event.unicode in self.letters_accents)):
                    self.current_word.append(event.unicode.lower())
                    if 14 in self.word_curr_cell:
                        self.word_curr_cell = None
                    elif self.arrow_down:
                        self.word_curr_cell = (
                            self.word_curr_cell[0], self.word_curr_cell[1] + 1
                        )
                    else:
                        self.word_curr_cell = (
                            self.word_curr_cell[0] + 1, self.word_curr_cell[1]
                        )
                elif event.key == pygame.K_ESCAPE:
                    self.word_start_cell = self.word_curr_cell = None
                    self.current_word = []
