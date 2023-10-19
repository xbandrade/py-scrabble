import pygame


class GameWindow:
    def __init__(self, grid_size, cell_size, game):
        pygame.init()
        self.game = game
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.info_width = 400
        self.border_thickness = 3
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
        self.curr_cell = None
        self.current_word = []
        self.arrow_down = False
        self.is_blank = False
        self.tile_rgb = 100
        self.color_sum = -5
        self.color_change_counter = 0
        self.blink_counter = 0
        self.play_ok = 0
        self.button1_clicking = False
        self.button2_clicking = False
        self.challenge_clicking = False
        self.can_challenge = False
        self.active_button = 1
        self.letters_accents = [
            'á', 'é', 'í', 'ó', 'ú', 'ã', 'õ', 'â', 'ê', 'ô',
            'Á', 'É', 'Í', 'Ó', 'Ú', 'Ã', 'Õ', 'Â', 'Ê', 'Ô']
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 28)
        self.font_color = (0, 0, 0)
        self.setup_grid_colors()
        self.setup_display()

    def setup_display(self):
        total_width = (self.grid_size * self.cell_size +
                       self.info_width + self.border_thickness)
        self.screen = pygame.display.set_mode(
            (total_width, (self.grid_size * self.cell_size +
                           self.border_thickness // 2)))
        pygame.display.set_caption('Scrabble')

    def setup_grid_colors(self):
        for i in range(len(self.game.board)):
            for j in range(len(self.game.board[0])):
                wm = self.game.board[i][j].word_multiplier
                lm = self.game.board[i][j].letter_multiplier
                if wm == 2:
                    self.grid_matrix[i][j] = (255, 0, 0, 52)
                elif wm == 3:
                    self.grid_matrix[i][j] = (255, 0, 0, 150)
                if lm == 2:
                    self.grid_matrix[i][j] = (0, 0, 255, 72)
                elif lm == 3:
                    self.grid_matrix[i][j] = (0, 0, 255, 180)

    def draw_grid(self):
        self.screen.fill((220, 220, 220))
        border_color = (25, 25, 25)
        border_width = 2
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                color = self.grid_matrix[x][y]
                if color:
                    cell_surface = pygame.Surface((
                        self.cell_size, self.cell_size),
                        pygame.SRCALPHA)
                    pygame.draw.rect(cell_surface, color, (
                        0, 0, self.cell_size, self.cell_size))
                    self.screen.blit(cell_surface, (
                        x * self.cell_size, y * self.cell_size))
                pygame.draw.rect(self.screen, border_color, (
                    x * self.cell_size, y * self.cell_size,
                    self.cell_size, self.cell_size), border_width)
        center_x = self.grid_size // 2
        center_y = self.grid_size // 2
        background_color = (255, 0, 0)
        cell_surface = pygame.Surface(
            (self.cell_size, self.cell_size), pygame.SRCALPHA)
        pygame.draw.rect(cell_surface, background_color,
                         (0, 0, self.cell_size, self.cell_size))
        self.screen.blit(self.star_image, (center_x * self.cell_size,
                                           center_y * self.cell_size))
        xy_max_pos = self.grid_size * self.cell_size
        pygame.draw.line(self.screen, (0, 0, 0), (0, 0), (
            0, self.screen.get_height()), self.border_thickness)
        pygame.draw.line(self.screen, (0, 0, 0), (xy_max_pos, 0), (
            xy_max_pos, self.screen.get_height()), self.border_thickness)
        pygame.draw.line(self.screen, (0, 0, 0), (0, 0), (
            xy_max_pos, 0), self.border_thickness)
        pygame.draw.line(self.screen, (0, 0, 0), (0, xy_max_pos), (
            xy_max_pos, xy_max_pos), self.border_thickness)
        if not self.play_ok:
            self.draw_arrow()

    def draw_arrow(self):
        if self.curr_cell:
            x, y = self.curr_cell
            arrow_image = (self.arrow_img_down if self.arrow_down
                           else self.arrow_img_right)
            self.screen.blit(arrow_image, (
                x * self.cell_size, y * self.cell_size))

    def draw_board_tiles(self):
        self.color_change_counter += 1
        if self.color_change_counter >= (20 if not self.play_ok else 10):
            self.color_change_counter = 0
            self.tile_rgb += self.color_sum + abs(self.play_ok) * 10
            self.tile_rgb = min(255, self.tile_rgb)
            if self.tile_rgb >= 125 or self.tile_rgb <= 75:
                self.color_sum *= -1
            if self.play_ok:
                self.color_sum = abs(self.color_sum)
                self.blink_counter += 1
        match self.play_ok:
            case -1:
                tile_color = (225, self.tile_rgb - 30, self.tile_rgb - 30)
            case 0:
                tile_color = (self.tile_rgb, self.tile_rgb, self.tile_rgb)
            case 1:
                tile_color = (self.tile_rgb - 30, 225, self.tile_rgb - 30)
            case _:
                tile_color = (0, 0, 0)
        font_color = (120, 120, 120)
        for i in range(len(self.game.board)):
            for j in range(len(self.game.board[0])):
                cell = self.game.board[i][j]
                if cell.is_occupied:
                    offset = 3
                    border_width = 2
                    background_surface = pygame.Surface(
                        (self.cell_size - offset, self.cell_size - offset))
                    background_surface.fill((182, 182, 182))
                    pygame.draw.rect(
                        background_surface, (220, 220, 220),
                        (0, 0, background_surface.get_width(),
                         background_surface.get_height()),
                        border_width
                    )
                    if cell.blank_letter:
                        letter = cell.blank_letter.upper()
                        font_color = (70, 155, 70)
                    else:
                        letter = cell.letter.upper()
                    letter_text = self.font.render(letter, True, font_color)
                    letter_rect = letter_text.get_rect(
                        center=(self.cell_size // 2, self.cell_size // 2))
                    background_surface.blit(letter_text, letter_rect)
                    self.screen.blit(background_surface, (
                        self.cell_size * j, self.cell_size * i))
                    if cell.blank_letter:
                        font_color = (120, 120, 120)
        if self.current_word:
            start_x, start_y = self.word_start_cell
            start_x *= self.cell_size
            start_y *= self.cell_size
            step_x, step_y = (0, self.cell_size) if self.arrow_down else (
                self.cell_size, 0)
            font_color = (220, 220, 220)
            is_blank = False
            for letter in ''.join(self.current_word).upper():
                if letter == '*':
                    is_blank = True
                    continue
                offset = 3
                border_width = 2
                background_surface = pygame.Surface(
                    (self.cell_size - offset, self.cell_size - offset))
                background_surface.fill(tile_color)
                pygame.draw.rect(
                    background_surface, (20, 20, 20),
                    (0, 0, background_surface.get_width(),
                     background_surface.get_height()),
                    border_width
                )
                if is_blank:
                    font_color = (255, 112, 112)
                letter_text = self.font.render(letter, True, font_color)
                letter_rect = letter_text.get_rect(
                    center=(self.cell_size // 2, self.cell_size // 2))
                background_surface.blit(letter_text, letter_rect)
                self.screen.blit(background_surface, (start_x, start_y))
                start_x += step_x
                start_y += step_y
                if is_blank:
                    is_blank = False
                    font_color = (220, 220, 220)
        if self.blink_counter >= 12:
            self.blink_counter = 0
            self.color_change_counter = 0
            self.tile_rgb = 100
            self.play_ok = 0
            self.current_word = []
            self.word_start_cell = self.curr_cell = None
            return

    def switch_button_click(self, click):
        if self.game.current_player == 1:
            self.button1_clicking = click
        else:
            self.button2_clicking = click

    def is_show_tiles_button_pressed(self):
        if self.game.current_player == 1:
            return self.button1_clicking
        return self.button2_clicking

    def draw_show_tiles_button(self, button_y, text, active=False) -> None:
        button_width = 200
        left = (self.grid_size * self.cell_size +
                (self.info_width - button_width) / 2)
        button_rect = pygame.Rect(left, button_y, button_width, 40)
        button_text = self.small_font.render(text, True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        if not active:
            pygame.draw.rect(self.screen, (72, 72, 72), button_rect)
            self.screen.blit(button_text, button_text_rect)
            return
        mouse_pos = pygame.mouse.get_pos()
        button_pressed = pygame.mouse.get_pressed()[0]
        if not self.is_show_tiles_button_pressed():
            button_hovered = button_rect.collidepoint(mouse_pos)
        else:
            button_hovered = False
        if button_pressed and button_hovered:
            self.switch_button_click(True)
        if not button_pressed and self.is_show_tiles_button_pressed():
            self.on_click_show_tiles()
            self.switch_button_click(False)
        if self.is_show_tiles_button_pressed():
            pygame.draw.rect(self.screen, (0, 200, 0), button_rect)
        elif button_hovered:
            pygame.draw.rect(self.screen, (0, 128, 0), button_rect)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect)
        self.screen.blit(button_text, button_text_rect)

    def draw_challenge_button(self, height):
        button_width = 100
        left = (self.grid_size * self.cell_size +
                (self.info_width - button_width) / 2)
        button_rect = pygame.Rect(left, height, button_width, 40)
        button_text = self.small_font.render('Desafiar', True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        mouse_pos = pygame.mouse.get_pos()
        button_pressed = pygame.mouse.get_pressed()[0]
        button_hovered = button_rect.collidepoint(mouse_pos)
        if not self.challenge_clicking:
            button_hovered = button_rect.collidepoint(mouse_pos)
        else:
            button_hovered = False
        if button_pressed and button_hovered:
            self.challenge_clicking = True
        if not button_pressed and self.challenge_clicking:
            self.on_click_challenge()
            self.challenge_clicking = False
        if self.challenge_clicking:
            pygame.draw.rect(self.screen, (0, 200, 200), button_rect)
        elif button_hovered:
            pygame.draw.rect(self.screen, (0, 158, 158), button_rect)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect)
        self.screen.blit(button_text, button_text_rect)

    def on_click_show_tiles(self) -> None:
        self.game.current_player.show_tiles = True

    def on_click_challenge(self) -> None:
        self.game.challenge()
        self.can_challenge = False

    def draw_info_section(self) -> None:
        grid_width = self.grid_size * self.cell_size + self.border_thickness
        info_rect = pygame.Rect(
            grid_width, 0, self.info_width, self.screen.get_height())
        pygame.draw.rect(self.screen, (200, 200, 200), info_rect)
        curr_player_rect = pygame.Rect(
            info_rect.left, info_rect.centery - 45, self.info_width, 30)
        curr_player_text = self.font.render(
            f'Jogador atual: Player {self.game.current_player}',
            True, (10, 100, 100))
        curr_text_rect = curr_player_text.get_rect(
            center=curr_player_rect.center)
        prev_play_rect = pygame.Rect(
            info_rect.left, info_rect.centery - 15, self.info_width, 30)
        if self.game.previous_play_info:
            if 'challenge' in self.game.previous_play_info:
                prev_play_text = self.font.render(
                    'Desafio do Player '
                    f'{self.game.previous_play_info['challenger']} '
                    f'{self.game.previous_play_info['challenge_ok']}',
                    True, (0, 100, 0)
                )
            else:
                prev_player = self.game.previous_play_info.get('player')
                prev_word = self.game.previous_play_info.get('word')
                prev_play_score = self.game.previous_play_info.get(
                    'play_score')
                prev_play_text = self.font.render(
                    f'Player {prev_player} | {prev_word} | {prev_play_score}',
                    True, (0, 100, 0))
        else:
            prev_play_text = self.font.render(
                'Nenhuma palavra foi jogada', True, (0, 100, 0))
        prev_text_rect = prev_play_text.get_rect(center=prev_play_rect.center)
        self.screen.blit(curr_player_text, curr_text_rect)
        self.screen.blit(prev_play_text, prev_text_rect)
        if self.can_challenge:
            self.draw_challenge_button(info_rect.centery + 20)
        self.draw_player_info()

    def draw_player_info(self) -> None:
        player1_tiles = self.game.player1.tiles
        player2_tiles = self.game.player2.tiles
        tile_size = 40
        tile_spacing = 5
        player_x = self.grid_size * self.cell_size + self.cell_size
        player1_y = (self.screen.get_height() -
                     (tile_size + tile_spacing) - 10)
        player2_y = 10
        p1_rect = pygame.Rect(self.grid_size * self.cell_size,
                              player1_y - tile_size - 10, self.info_width, 30)
        p1_text = self.font.render(
            f'Player 1 - {self.game.player1.score} pontos',
            True, (180, 100, 100))
        p1_text_rect = p1_text.get_rect(center=p1_rect.center)
        active = self.game.current_player.id == 1
        self.draw_show_tiles_button(
            p1_rect.y - self.cell_size, 'Exibir Letras', active)
        self.screen.blit(p1_text, p1_text_rect)
        p2_rect = pygame.Rect(self.grid_size * self.cell_size,
                              player2_y + tile_size + 10, self.info_width, 30)
        p2_text = self.font.render(
            f'Player 2 - {self.game.player2.score} pontos',
            True, (100, 100, 180))
        p2_text_rect = p2_text.get_rect(center=p2_rect.center)
        active = self.game.current_player.id == 2
        self.draw_show_tiles_button(
            p2_rect.y + self.cell_size, 'Exibir Letras', active)
        self.screen.blit(p2_text, p2_text_rect)
        for tile in sorted(player2_tiles):
            tile_rect = pygame.Rect(player_x, player2_y, tile_size, tile_size)
            pygame.draw.rect(self.screen, (0, 0, 128), tile_rect)
            show_tile = tile.upper() if self.game.player2.show_tiles else ''
            letter_text = self.font.render(show_tile, True, (200, 200, 200))
            letter_rect = letter_text.get_rect(center=tile_rect.center)
            self.screen.blit(letter_text, letter_rect)
            player_x += tile_size + tile_spacing
        player_x = self.grid_size * self.cell_size + self.cell_size
        for tile in sorted(player1_tiles):
            tile_rect = pygame.Rect(player_x, player1_y, tile_size, tile_size)
            pygame.draw.rect(self.screen, (128, 0, 0), tile_rect)
            show_tile = tile.upper() if self.game.player1.show_tiles else ''
            letter_text = self.font.render(show_tile, True, (200, 200, 200))
            letter_rect = letter_text.get_rect(center=tile_rect.center)
            self.screen.blit(letter_text, letter_rect)
            player_x += tile_size + tile_spacing

    def blink_tiles(self) -> None:
        font_color = (120, 120, 120)
        self.color_change_counter += 1
        if self.color_change_counter >= 35:
            self.color_change_counter = 0
            self.tile_rgb += self.color_sum
            if self.tile_rgb <= 50 or self.tile_rgb >= 220:
                self.tile_rgb = 100
                self.play_ok = 0
                return
        if self.current_word:
            start_x, start_y = self.word_start_cell
            start_x *= self.cell_size
            start_y *= self.cell_size
            step_x, step_y = (0, self.cell_size) if self.arrow_down else (
                self.cell_size, 0)
            font_color = (220, 220, 220)
            is_blank = False
            for letter in ''.join(self.current_word).upper():
                if letter == '*':
                    is_blank = True
                    continue
                offset = 3
                border_width = 2
                background_surface = pygame.Surface(
                    (self.cell_size - offset, self.cell_size - offset))
                background_surface.fill((self.tile_rgb, 22, 22))
                pygame.draw.rect(
                    background_surface, (20, 20, 20),
                    (0, 0, background_surface.get_width(),
                     background_surface.get_height()),
                    border_width
                )
                if is_blank:
                    font_color = (255, 112, 112)
                letter_text = self.font.render(letter, True, font_color)
                letter_rect = letter_text.get_rect(
                    center=(self.cell_size // 2, self.cell_size // 2))
                background_surface.blit(letter_text, letter_rect)
                self.screen.blit(background_surface, (start_x, start_y))
                start_x += step_x
                start_y += step_y
                if is_blank:
                    is_blank = False
                    font_color = (220, 220, 220)

    def handle_events(self) -> None:
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
                    if (grid_x, grid_y) == self.curr_cell:
                        self.arrow_down = not self.arrow_down
                    else:
                        self.arrow_down = False
                        self.word_start_cell = (grid_x, grid_y)
                        self.curr_cell = self.word_start_cell
                else:
                    self.word_start_cell = self.curr_cell = None
            if event.type == pygame.KEYDOWN and self.word_start_cell:
                if (self.curr_cell and
                    (event.unicode.isalpha() or
                     event.unicode in self.letters_accents)):
                    if self.is_blank:
                        self.current_word.append(f'*{event.unicode.lower()}')
                        self.is_blank = False
                    else:
                        self.current_word.append(event.unicode.lower())
                    if ((self.curr_cell[0] >= self.grid_size - 1 and
                         not self.arrow_down) or
                        (self.curr_cell[1] >= self.grid_size and
                            self.arrow_down)):
                        self.curr_cell = None
                    elif self.arrow_down:
                        self.curr_cell = (
                            self.curr_cell[0], self.curr_cell[1] + 1)
                    else:
                        self.curr_cell = (
                            self.curr_cell[0] + 1, self.curr_cell[1])
                elif event.key == pygame.K_SPACE:
                    self.is_blank = True
                elif event.key == pygame.K_BACKSPACE:
                    if not self.current_word:
                        continue
                    self.current_word.pop()
                    if self.arrow_down:
                        if not self.curr_cell:
                            self.curr_cell = (self.word_start_cell[0], 14)
                        else:
                            self.curr_cell = (
                                self.curr_cell[0], self.curr_cell[1] - 1)
                    else:
                        if not self.curr_cell:
                            self.curr_cell = (14, self.word_start_cell[1])
                        else:
                            self.curr_cell = (
                                self.curr_cell[0] - 1, self.curr_cell[1])
                    self.is_blank = False
                elif event.key == pygame.K_ESCAPE:
                    self.word_start_cell = self.curr_cell = None
                    self.current_word = []
                elif event.key == pygame.K_RETURN and self.current_word:
                    word = ''.join(self.current_word)
                    start = (self.word_start_cell[1], self.word_start_cell[0])
                    play_ok = self.game.play_word(word, start, self.arrow_down)
                    self.play_ok = 1 if play_ok else -1
                    self.game.print_board()
                    self.color_change_counter = 0
                    if play_ok:
                        self.active_button = self.game.current_player.id
                        self.can_challenge = True
