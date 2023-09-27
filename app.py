import pygame


class GameWindow:
    def __init__(self, grid_size, cell_size, game):
        self.game = game
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.screen = None
        self.grid_matrix = [[None for _ in range(
            grid_size)] for _ in range(grid_size)]
        self.star_image = pygame.image.load('img/star.png')
        self.star_image = pygame.transform.scale(
            self.star_image, (self.cell_size, self.cell_size))
        self.setup_grid_colors()
        self.setup_display()

    def setup_display(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.grid_size * self.cell_size, self.grid_size * self.cell_size))
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
        self.screen.fill((255, 255, 255))
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
                    self.screen.blit(
                        cell_surface, (x * self.cell_size, y * self.cell_size))
        center_x = self.grid_size // 2
        center_y = self.grid_size // 2
        background_color = (255, 0, 0)
        cell_surface = pygame.Surface(
            (self.cell_size, self.cell_size), pygame.SRCALPHA)
        pygame.draw.rect(cell_surface, background_color,
                         (0, 0, self.cell_size, self.cell_size))
        self.screen.blit(self.star_image, (center_x * self.cell_size,
                                           center_y * self.cell_size))
