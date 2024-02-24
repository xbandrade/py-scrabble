import pygame


class GameWindow:
    def __init__(self, grid_size, cell_size, game=None):
        self.game = game
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.info_width = 400
        self.border_thickness = 3
        self.screen = None
        self.word_start_cell = None
        self.current_cell = None
        self.letters_matrix = {}
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
        self.go_to_menu = True
        self.can_challenge = False
        self.active_button = 1
        self.get_font = lambda size: pygame.font.SysFont(None, size)
        self.font = self.get_font(36)
        self.medium_font = self.get_font(24)
        self.small_font = self.get_font(18)
        self.font_color = (0, 0, 0)
        self.fill_color = (94, 63, 51)
        self.title_color = (200, 200, 200)
        self.setup()

    def setup(self) -> None:
        total_width = (self.grid_size * self.cell_size +
                       self.info_width + self.border_thickness)
        self.screen = pygame.display.set_mode(
            (total_width, (self.grid_size * self.cell_size +
                           self.border_thickness // 2)))
        pygame.display.set_caption('Scrabble')
        self.grid_matrix = [[None for _ in range(
            self.grid_size)] for _ in range(self.grid_size)]
        self.star_image = pygame.image.load('assets/images/star.png')
        self.star_image = pygame.transform.scale(
            self.star_image, (self.cell_size, self.cell_size))
        self.arrow_image = pygame.image.load('assets/images/arrow.png')
        self.arrow_image = pygame.transform.scale(
            self.arrow_image, (self.cell_size, self.cell_size))
        self.arrow_image.set_colorkey((255, 255, 255))
        self.arrow_img_right = pygame.transform.rotate(self.arrow_image, 180)
        self.arrow_img_down = pygame.transform.rotate(self.arrow_image, 90)
        self.letters_accents = [
            'á', 'é', 'í', 'ó', 'ú', 'ã', 'õ', 'â', 'ê', 'ô',
            'Á', 'É', 'Í', 'Ó', 'Ú', 'Ã', 'Õ', 'Â', 'Ê', 'Ô']

    def draw_start_screen_buttons(self):
        big_font = pygame.font.Font(
            'assets/fonts/RobotoSlab-ExtraBold.ttf', 84)
        button_font = pygame.font.Font(
            'assets/fonts/RobotoSlab-ExtraBold.ttf', 26)
        screen_width, _ = self.screen.get_size()
        title = big_font.render('SCRABBLE', True, self.title_color)
        title_img = pygame.image.load('assets/images/title.png')
        button_img = pygame.image.load('assets/images/gui.png')
        title_y = 100
        button_y = 170
        button_margin = 20
        button_width, button_height = button_img.get_rect().size
        center_x = screen_width // 2
        title_rect = title.get_rect(center=(center_x, title_y))
        bot_button = pygame.Rect(
            center_x - button_width // 2,
            button_y, button_width, button_height)
        player_button = pygame.Rect(
            center_x - button_width // 2,
            button_y + button_height + button_margin,
            button_width, button_height)
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        button_color = (80, 80, 80)
        button_color_hover = (130, 90, 90)
        button_color_click = (150, 150, 150)
        current_color = button_color
        self.screen.blit(button_img, bot_button)
        self.screen.blit(button_img, player_button)
        if bot_button.collidepoint(mouse_pos):
            current_color = button_color_hover
            if mouse_clicked:
                current_color = button_color_click
        vs_bot_text = button_font.render(
            'Player vs Bot', True, current_color)
        current_color = button_color
        if player_button.collidepoint(mouse_pos):
            current_color = button_color_hover
            if mouse_clicked:
                current_color = button_color_click
        vs_player_text = button_font.render(
            'Player vs Player', True, current_color)
        bot_text_rect = vs_bot_text.get_rect(center=bot_button.center)
        player_text_rect = vs_player_text.get_rect(center=player_button.center)
        self.screen.blit(title_img, title_rect)
        self.screen.blit(vs_bot_text, bot_text_rect)
        self.screen.blit(vs_player_text, player_text_rect)
        return bot_button, player_button

    def run_main_menu(self) -> bool | None:
        opponent = None
        vs_bot = None
        button_pressed = False
        width, _ = self.screen.get_size()
        bg = pygame.image.load('assets/images/bg2.png')
        scaled_bg = pygame.transform.smoothscale(
            bg, (width, int(bg.get_height() * width / bg.get_width())))
        self.screen.fill(self.fill_color)
        scaled_bg.set_alpha(10)
        while not opponent:
            self.screen.blit(scaled_bg, (0, 0))
            bot_button, player_button = self.draw_start_screen_buttons()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if (bot_button.collidepoint(mouse_pos) or
                            player_button.collidepoint(mouse_pos)):
                        button_pressed = True
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if (button_pressed and (
                            bot_button.collidepoint(mouse_pos) or
                            player_button.collidepoint(mouse_pos))):
                        vs_bot = bot_button.collidepoint(mouse_pos)
                        opponent = True
                    button_pressed = False
            pygame.display.flip()
        return vs_bot

    def show_start_menu(self):
        bot_button, player_button = self.draw_start_screen_buttons()
        opponent = None
        while not opponent:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    opponent = True
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if bot_button.collidepoint(mouse_pos):
                        vs_bot = True
                        opponent = True
                    elif player_button.collidepoint(mouse_pos):
                        vs_bot = False
                        opponent = True
        return vs_bot

    def draw_grid_colors(self) -> None:
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

    def draw_grid(self) -> None:
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

    def draw_arrow(self) -> None:
        if self.current_cell:
            x, y = self.current_cell
            arrow_image = (self.arrow_img_down if self.arrow_down
                           else self.arrow_img_right)
            self.screen.blit(arrow_image, (
                x * self.cell_size, y * self.cell_size))

    def draw_board_tiles(self) -> None:
        self.color_change_counter += 1
        if self.color_change_counter >= 7:
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
                    value_text = self.small_font.render(
                        str(self.game.values[letter.lower()]), True, (0, 0, 0))
                    value_rect = value_text.get_rect(
                        center=(self.cell_size * .8, self.cell_size * .8))
                    background_surface.blit(letter_text, letter_rect)
                    background_surface.blit(value_text, value_rect)
                    self.screen.blit(background_surface, (
                        self.cell_size * j, self.cell_size * i))
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
        if self.blink_counter >= 8:
            self.blink_counter = 0
            self.color_change_counter = 0
            self.tile_rgb = 100
            self.play_ok = 0
            self.current_word = []
            self.word_start_cell = self.current_cell = None
            return

    def switch_button_click(self, click) -> None:
        player = self.game.current_player.id
        self.button1_clicking = click if player == 1 else self.button1_clicking
        self.button2_clicking = click if player == 2 else self.button2_clicking

    def is_show_tiles_button_pressed(self) -> bool:
        if int(self.game.current_player) == 1:
            return self.button1_clicking
        return self.button2_clicking

    def draw_show_tiles_button(self, button_y, text, active=False) -> None:
        if self.game.winner:
            return
        button_width = 200
        left = (self.grid_size * self.cell_size +
                (self.info_width - button_width) / 2)
        button_rect = pygame.Rect(left, button_y, button_width, 40)
        button_text = self.medium_font.render(text, True, (255, 255, 255))
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

    def draw_menu_button(self) -> None:
        button_width = 100
        left = (self.grid_size * self.cell_size +
                (self.info_width - button_width) / 2)
        button_rect = pygame.Rect(left, 10, button_width, 30)
        button_text = self.medium_font.render(
            'Menu', True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        mouse_pos = pygame.mouse.get_pos()
        button_pressed = pygame.mouse.get_pressed()[0]
        button_hovered = button_rect.collidepoint(mouse_pos)
        if button_pressed and button_hovered:
            self.on_click_menu()
        if self.challenge_clicking:
            pygame.draw.rect(self.screen, (100, 200, 200), button_rect)
        elif button_hovered:
            pygame.draw.rect(self.screen, (100, 158, 158), button_rect)
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), button_rect)
        self.screen.blit(button_text, button_text_rect)

    def draw_challenge_button(self, height) -> None:
        button_width = 100
        left = (self.grid_size * self.cell_size +
                (self.info_width - button_width) / 2)
        button_rect = pygame.Rect(left, height - 45, button_width, 40)
        button_text = self.medium_font.render(
            'Desafiar', True, (255, 255, 255))
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

    def on_click_menu(self) -> None:
        self.go_to_menu = True

    def on_click_challenge(self) -> None:
        self.game.challenge()
        self.can_challenge = False

    def draw_unseen_tiles(self, info_rect) -> None:
        if self.game.winner:
            winner_rect = self.get_label_rect(
                info_rect, 0, 10, 30, (100, 100, 100),
                f'Player {self.game.winner} venceu!', 28
            )
            self.screen.blit(*winner_rect)
            return
        unseen_text_counter = [
            f'{k}{v.upper()}'
            for v, k in self.game.unseen_tiles.items()
            if k != 0
        ]
        unseen_list = []
        for i in range(0, len(unseen_text_counter), 10):
            unseen_list.append(' '.join(unseen_text_counter[i:i + 10]))
        pad = 10
        for unseen_str in unseen_list:
            unseen_letters_rect = self.get_label_rect(
                info_rect, 0, pad, 70, (100, 100, 100),
                unseen_str, 28
            )
            self.screen.blit(*unseen_letters_rect)
            pad += 25

    def get_label_rect(self, rect, padx, pady, height, color, text, font=36):
        font = self.get_font(font)
        obj_rect = pygame.Rect(
            rect.left + padx, rect.centery + pady, self.info_width, height)
        obj_text = font.render(text, True, color)
        obj_text_rect = obj_text.get_rect(center=obj_rect.center)
        return obj_text, obj_text_rect

    def draw_info_section(self) -> None:
        grid_width = self.grid_size * self.cell_size + self.border_thickness
        info_rect = pygame.Rect(
            grid_width, 0, self.info_width, self.screen.get_height())
        pygame.draw.rect(self.screen, (200, 200, 200), info_rect)
        current_player_text_rect = self.get_label_rect(
            info_rect, 0, -135, 30, (10, 100, 100),
            f'Jogador atual: Player {self.game.current_player}'
        )
        if self.game.previous_play_info:
            if 'challenge' in self.game.previous_play_info:
                previous_play_text = (
                    'Desafio do Player ' +
                    f'{self.game.previous_play_info['challenger']} ' +
                    f'{self.game.previous_play_info['challenge_ok']}'
                )
            else:
                previous_player = self.game.previous_play_info.get('player')
                previous_word = self.game.previous_play_info.get('word')
                previous_play_score = self.game.previous_play_info.get(
                    'play_score')
                previous_play_text = (
                    f'Player {previous_player} | {previous_word} | ' +
                    f'{previous_play_score}'
                )
        else:
            previous_play_text = 'Nenhuma palavra foi jogada'
        previous_play_text_rect = self.get_label_rect(
            info_rect, 0, -105, 50, (0, 100, 0), previous_play_text)
        unseen_label_rect = self.get_label_rect(
            info_rect, 0, -15, 70, (50, 50, 50), 'Letras não jogadas:')
        self.screen.blit(*current_player_text_rect)
        self.screen.blit(*previous_play_text_rect)
        if not self.game.winner:
            self.screen.blit(*unseen_label_rect)
            if self.can_challenge:
                self.draw_challenge_button(info_rect.centery)
        self.draw_menu_button()
        self.draw_unseen_tiles(info_rect)
        self.draw_player_info()

    def draw_player_info(self) -> None:
        player1_tiles = self.game.player1.tiles
        player2_tiles = self.game.player2.tiles
        tile_size = 40
        tile_spacing = 5
        player_x = self.grid_size * self.cell_size + self.cell_size
        player1_y = self.screen.get_height() - (tile_size + tile_spacing) - 10
        player2_y = 50
        p1_rect = pygame.Rect(self.grid_size * self.cell_size,
                              player1_y - tile_size - 10, self.info_width, 30)
        p1_text = self.font.render(
            f'Player 1 - {self.game.player1.score} pontos',
            True, (180, 100, 100))
        p1_text_rect = p1_text.get_rect(center=p1_rect.center)
        active = self.game.winner or self.game.current_player.id == 1
        self.draw_show_tiles_button(
            p1_rect.y - self.cell_size, 'Exibir Letras', active)
        p2_rect = pygame.Rect(self.grid_size * self.cell_size,
                              player2_y + tile_size + 10, self.info_width, 30)
        p2_text = self.font.render(
            f'Player 2 - {self.game.player2.score} pontos',
            True, (100, 100, 180))
        p2_text_rect = p2_text.get_rect(center=p2_rect.center)
        active = self.game.winner or self.game.current_player.id == 2
        self.draw_show_tiles_button(
            p2_rect.y + self.cell_size, 'Exibir Letras', active)
        self.screen.blit(p1_text, p1_text_rect)
        self.screen.blit(p2_text, p2_text_rect)
        for tile in sorted(player2_tiles):
            tile_rect = pygame.Rect(player_x, player2_y, tile_size, tile_size)
            pygame.draw.rect(self.screen, (0, 0, 128), tile_rect)
            show_tile = tile.upper() if self.game.player2.show_tiles else ''
            value = (str(self.game.values[tile.lower()])
                     if self.game.player2.show_tiles else '')
            letter_text = self.font.render(show_tile, True, (200, 200, 200))
            letter_rect = letter_text.get_rect(center=tile_rect.center)
            value_text = self.small_font.render(value, True, (255, 255, 255))
            value_rect = value_text.get_rect(center=(
                tile_rect.x + tile_rect.height * .85,
                tile_rect.y + tile_rect.width * .85))
            self.screen.blit(letter_text, letter_rect)
            self.screen.blit(value_text, value_rect)
            player_x += tile_size + tile_spacing
        player_x = self.grid_size * self.cell_size + self.cell_size
        for tile in sorted(player1_tiles):
            tile_rect = pygame.Rect(player_x, player1_y, tile_size, tile_size)
            pygame.draw.rect(self.screen, (128, 0, 0), tile_rect)
            show_tile = tile.upper() if self.game.player1.show_tiles else ''
            value = (str(self.game.values[tile.lower()])
                     if self.game.player1.show_tiles else '')
            letter_text = self.font.render(show_tile, True, (200, 200, 200))
            letter_rect = letter_text.get_rect(center=tile_rect.center)
            value_text = self.small_font.render(value, True, (255, 255, 255))
            value_rect = value_text.get_rect(center=(
                tile_rect.x + tile_rect.height * .85,
                tile_rect.y + tile_rect.width * .85))
            self.screen.blit(letter_text, letter_rect)
            self.screen.blit(value_text, value_rect)
            player_x += tile_size + tile_spacing

    def handle_events(self) -> None:
        if self.game.current_player.is_bot:
            print('O bot está fazendo uma jogada')
            self.game.bot_play()
            self.game.print_board()
            self.color_change_counter = 0
            if self.game.winner:
                self.game.player1.show_tiles = True
                self.game.player2.show_tiles = True
            self.active_button = self.game.current_player.id
            self.can_challenge = True
            best1 = self.game.get_best_words()[0]
            best2 = self.game.get_best_words(2)[0]
            print(f'P1 melhor palavra: {best1}\nP2 melhor palavra: {best2}')
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
                    if (grid_x, grid_y) == self.current_cell:
                        self.arrow_down = not self.arrow_down
                    else:
                        self.arrow_down = False
                        self.word_start_cell = (grid_x, grid_y)
                        self.current_cell = self.word_start_cell
                else:
                    self.word_start_cell = self.current_cell = None
            if event.type == pygame.KEYDOWN and self.word_start_cell:
                if (self.current_cell and
                    (event.unicode.isalpha() or
                     event.unicode in self.letters_accents)):
                    if self.is_blank:
                        self.current_word.append(f'*{event.unicode.lower()}')
                        self.is_blank = False
                    else:
                        self.current_word.append(event.unicode.lower())
                    if ((self.current_cell[0] >= self.grid_size - 1 and
                         not self.arrow_down) or
                        (self.current_cell[1] >= self.grid_size and
                            self.arrow_down)):
                        self.current_cell = None
                    elif self.arrow_down:
                        self.current_cell = (
                            self.current_cell[0], self.current_cell[1] + 1)
                    else:
                        self.current_cell = (
                            self.current_cell[0] + 1, self.current_cell[1])
                elif event.key == pygame.K_SPACE:
                    self.is_blank = True
                elif event.key == pygame.K_BACKSPACE:
                    if not self.current_word:
                        continue
                    self.current_word.pop()
                    if self.arrow_down:
                        if not self.current_cell:
                            self.current_cell = (self.word_start_cell[0], 14)
                        else:
                            self.current_cell = (
                                self.current_cell[0], self.current_cell[1] - 1)
                    else:
                        if not self.current_cell:
                            self.current_cell = (14, self.word_start_cell[1])
                        else:
                            self.current_cell = (
                                self.current_cell[0] - 1, self.current_cell[1])
                    self.is_blank = False
                elif event.key == pygame.K_ESCAPE:
                    self.word_start_cell = self.current_cell = None
                    self.current_word = []
                elif event.key == pygame.K_RETURN and self.current_word:
                    word = ''.join(self.current_word)
                    start = (self.word_start_cell[1], self.word_start_cell[0])
                    play_ok = self.game.play_word(word, start, self.arrow_down)
                    self.play_ok = 1 if play_ok else -1
                    self.game.print_board()
                    self.color_change_counter = 0
                    if self.game.winner:
                        self.game.player1.show_tiles = True
                        self.game.player2.show_tiles = True
                    elif play_ok:
                        self.active_button = self.game.current_player.id
                        self.can_challenge = True
                    best1 = self.game.get_best_words()[0]
                    best2 = self.game.get_best_words(2)[0]
                    print(f'P1 melhor palavra: {best1}\n'
                          f'P2 melhor palavra: {best2}')
