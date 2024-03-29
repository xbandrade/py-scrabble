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
        self.current_word = []
        self.arrow_down = False
        self.is_blank = False
        self.tile_rgb = 100
        self.color_sum = -5
        self.color_change_counter = 0
        self.played_word_blink_counter = 0
        self.play_ok = 0
        self.button_down = False
        self.go_to_menu = True
        self.active_button = 1
        self.game_button_rects = []
        self.get_font = lambda size: pygame.font.Font(
            'assets/fonts/RobotoSlab-ExtraBold.ttf', size)
        self.font = self.get_font(26)
        self.small_font = self.get_font(12)
        self.setup()

    def setup(self) -> None:
        self.grid_width = (self.grid_size * self.cell_size +
                           self.border_thickness)
        total_width = self.grid_width + self.info_width
        self.screen = pygame.display.set_mode(
            (total_width, (self.grid_size * self.cell_size +
                           self.border_thickness // 2)))
        pygame.display.set_caption('Scrabble')
        pygame.display.set_icon(pygame.image.load('assets/images/icon.png'))
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
        width, _ = self.screen.get_size()
        bg = pygame.image.load('assets/images/bg2.png')
        self.background = pygame.transform.smoothscale(
            bg, (width, int(bg.get_height() * width / bg.get_width())))
        self.button_font = pygame.font.Font(
            'assets/fonts/RobotoSlab-ExtraBold.ttf', 24)
        self.small_button_font = pygame.font.Font(
            'assets/fonts/RobotoSlab-ExtraBold.ttf', 18)
        self.title_img = pygame.image.load('assets/images/title.png')
        self.button_img = pygame.image.load('assets/images/button.png')
        self.exchange_img = pygame.image.load('assets/images/exchange.png')
        self.exchange_img = pygame.transform.scale(self.exchange_img, (55, 55))
        self.exchange_hover = pygame.transform.scale(
            self.exchange_img, (52, 52))
        self.letters_accents = [
            'á', 'é', 'í', 'ó', 'ú', 'ã', 'õ', 'â', 'ê', 'ô',
            'Á', 'É', 'Í', 'Ó', 'Ú', 'Ã', 'Õ', 'Â', 'Ê', 'Ô']

    def draw_background(self, alpha=200, area=None):
        x, y = area.topleft if area else (0, 0)
        if area:
            self.fill_area(self.grid_width, self.screen.get_height(), (x, y))
        self.background.set_alpha(alpha)
        self.screen.blit(self.background, (x, y), area)

    def draw_button(self, rect, text, mouse_pos, mouse_clicked, resize=1):
        button_color = (80, 80, 80)
        button_color_hover = (130, 90, 90)
        button_color_click = (150, 150, 150)
        current_color = button_color
        button_image = self.button_img
        if resize != 1:
            width = int(button_image.get_width() * resize)
            height = int(button_image.get_height() * resize)
            button_image = pygame.transform.scale(
                button_image, (width, height))
        self.screen.blit(button_image, rect)
        if rect.collidepoint(mouse_pos):
            current_color = button_color_hover
            if mouse_clicked:
                self.button_down = True
                current_color = button_color_click
        font = self.button_font if resize > .7 else self.small_button_font
        button_text = font.render(text, True, current_color)
        text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, text_rect)

    def draw_start_screen_buttons(self):
        screen_width, _ = self.screen.get_size()
        title_y = 100
        button_y = 170
        button_margin = 20
        button_width, button_height = self.button_img.get_rect().size
        center_x = screen_width // 2
        title_rect = self.title_img.get_rect(center=(center_x, title_y))
        bot_button_rect = pygame.Rect(
            center_x - button_width // 2,
            button_y, button_width, button_height)
        player_button_rect = pygame.Rect(
            center_x - button_width // 2,
            button_y + button_height + button_margin,
            button_width, button_height)
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        self.draw_button(bot_button_rect, 'Player vs Bot',
                         mouse_pos, mouse_clicked)
        self.draw_button(player_button_rect, 'Player vs Player',
                         mouse_pos, mouse_clicked)
        self.screen.blit(self.title_img, title_rect)
        return bot_button_rect, player_button_rect

    def fill_area(self, width, height, pos, color=(220, 220, 220)):
        fill_surface = pygame.Surface((width, height))
        fill_surface.fill(color)
        self.screen.blit(fill_surface, pos)

    def run_main_menu(self) -> bool | None:
        opponent = None
        vs_bot = None
        button_pressed = False
        while not opponent:
            self.draw_background()
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
        self.button_down = False
        return vs_bot

    def draw_grid_colors(self) -> None:
        for i in range(len(self.game.board)):
            for j in range(len(self.game.board[0])):
                self.grid_matrix[i][j] = (220, 220, 220, 255)
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
        self.fill_area(self.grid_width, self.screen.get_height(), (0, 0))
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

    def draw_arrow(self) -> None:
        if self.current_cell:
            x, y = self.current_cell
            arrow_image = (self.arrow_img_down if self.arrow_down
                           else self.arrow_img_right)
            self.screen.blit(arrow_image, (
                x * self.cell_size, y * self.cell_size))

    def draw_board_tiles(self) -> None:
        self.color_change_counter += 1
        if self.color_change_counter >= 5:
            self.color_change_counter = 0
            self.tile_rgb += self.color_sum + abs(self.play_ok) * 10
            self.tile_rgb = min(255, self.tile_rgb)
            if self.tile_rgb >= 125 or self.tile_rgb <= 75:
                self.color_sum *= -1
            if self.play_ok:
                self.color_sum = abs(self.color_sum)
                self.played_word_blink_counter += 1
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
                    if cell.tile.blank_letter:
                        font_color = (70, 155, 70)
                    letter = f'{cell}'.upper()
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
            # for letter in ''.join(self.current_word).upper():
            for letter in ''.join(self.current_word):
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
                if letter.isupper():
                    is_blank = True
                    font_color = (255, 112, 112)
                letter_text = self.font.render(
                    letter.upper(), True, font_color)
                letter_rect = letter_text.get_rect(
                    center=(self.cell_size // 2, self.cell_size // 2))
                background_surface.blit(letter_text, letter_rect)
                self.screen.blit(background_surface, (start_x, start_y))
                start_x += step_x
                start_y += step_y
                if is_blank:
                    is_blank = False
                    font_color = (220, 220, 220)
        if not self.play_ok:
            self.draw_arrow()
        if self.played_word_blink_counter >= 5:
            self.played_word_blink_counter = 0
            self.color_change_counter = 0
            self.tile_rgb = 100
            self.play_ok = 0
            self.current_word = []
            self.word_start_cell = self.current_cell = None
            return

    def draw_show_tiles_button(self, button_y, text, active=False) -> None:
        if self.game.winner or not active or self.game.current_player.is_bot:
            return
        if self.game_button_click(.85, button_y, text):
            self.button_down = False
            self.game.current_player.show_tiles = True
        if self.game.current_player.show_tiles:
            self.draw_exchange_button(button_y)

    def draw_exchange_button(self, button_y):
        exchange_width, exchange_height = self.exchange_img.get_rect().size
        button_width, _ = self.button_img.get_rect().size
        button_rect = pygame.Rect(
            self.grid_width + (self.info_width + button_width) // 2,
            button_y + 5, exchange_width, exchange_height)
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        button_hovered = button_rect.collidepoint(mouse_pos)
        if button_hovered and not mouse_clicked:
            self.screen.blit(self.exchange_hover, button_rect)
            return
        if mouse_clicked and button_hovered:
            exchange_ok = self.game.exchange_tiles()
            if exchange_ok:
                print('Troca de peças feita com sucesso')
        self.screen.blit(self.exchange_img, button_rect)

    def draw_menu_button(self) -> None:
        if self.game_button_click(.4, 10, 'Menu'):
            self.button_down = False
            self.go_to_menu = True

    def draw_challenge_button(self, height) -> None:
        if self.game_button_click(.6, height - 55, 'Desafiar'):
            self.button_down = False
            self.game.challenge()

    def game_button_click(self, resize, top, text) -> bool:
        button_resize = resize
        button_width, button_height = self.button_img.get_rect().size
        button_width *= button_resize
        button_height *= button_resize
        left = self.grid_width + (self.info_width - button_width) // 2
        button_rect = pygame.Rect(left, top, button_width, button_height)
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        button_hovered = button_rect.collidepoint(mouse_pos)
        self.draw_button(button_rect, text, mouse_pos,
                         mouse_clicked, button_resize)
        if button_rect not in self.game_button_rects:
            self.game_button_rects.append(button_rect)
        return self.button_down and button_hovered and not mouse_clicked

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
                info_rect, 0, pad, 70, (70, 70, 70),
                unseen_str, 22
            )
            self.screen.blit(*unseen_letters_rect)
            pad += 25

    def draw_tiles_in_bag(self, info_rect) -> None:
        tiles_in_bag = self.get_label_rect(
            info_rect, 0, 100, 50, (40, 40, 40),
            f'Bolsa de Letras: {len(self.game.bag)}', 22
        )
        self.screen.blit(*tiles_in_bag)

    def get_label_rect(self, rect, padx, pady, height, color, text, font=24):
        font = self.get_font(font)
        obj_rect = pygame.Rect(
            rect.left + padx, rect.centery + pady, self.info_width, height)
        obj_text = font.render(text, True, color)
        obj_text_rect = obj_text.get_rect(center=obj_rect.center)
        return obj_text, obj_text_rect

    def draw_info_section(self) -> None:
        info_rect = pygame.Rect(
            self.grid_width, 0, self.info_width, self.screen.get_height())
        self.draw_background(150, info_rect)
        current_player_text_rect = self.get_label_rect(
            info_rect, 0, -135, 30, (10, 100, 100),
            f'Jogador atual: Player {self.game.current_player}')
        if self.game.previous_play_info:
            if 'challenge_ok' in self.game.previous_play_info:
                previous_play_text = (
                    'Desafio do Player ' +
                    f'{self.game.previous_play_info['challenger']} ' +
                    f'{self.game.previous_play_info['challenge_ok']}')
            elif 'exchange_ok' in self.game.previous_play_info:
                previous_play_text = (
                    'Troca do player ' +
                    f'{3 - self.game.current_player.id} ' +
                    f'{self.game.previous_play_info['exchange_ok']}')
            else:
                previous_player = self.game.previous_play_info.get('player')
                previous_word = self.game.previous_play_info.get('word')
                previous_play_score = self.game.previous_play_info.get(
                    'play_score')
                previous_play_text = (
                    f'Player {previous_player} | {previous_word} | ' +
                    f'{previous_play_score}')
        else:
            previous_play_text = 'Nenhuma palavra foi jogada'
        previous_play_text_rect = self.get_label_rect(
            info_rect, 0, -105, 50, (0, 100, 0), previous_play_text)
        unseen_label_rect = self.get_label_rect(
            info_rect, 0, -25, 70, (50, 50, 50), 'Letras não jogadas:')
        self.screen.blit(*current_player_text_rect)
        self.screen.blit(*previous_play_text_rect)
        if not self.game.winner:
            self.screen.blit(*unseen_label_rect)
            if (self.game.player1.can_challenge or
                    self.game.player2.can_challenge):
                self.draw_challenge_button(info_rect.centery)
        self.draw_menu_button()
        self.draw_unseen_tiles(info_rect)
        self.draw_tiles_in_bag(info_rect)
        self.draw_player_info()
        mouse_pos = pygame.mouse.get_pos()
        if self.button_down and all(
                not rect.collidepoint(mouse_pos)
                for rect in self.game_button_rects):
            self.button_down = False

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
            True, (180, 40, 40))
        p1_text_rect = p1_text.get_rect(center=p1_rect.center)
        active = self.game.winner or self.game.current_player.id == 1
        self.draw_show_tiles_button(
            p1_rect.y - 2 * self.cell_size, 'Mostrar Letras', active)
        p2_rect = pygame.Rect(self.grid_size * self.cell_size,
                              player2_y + tile_size + 10, self.info_width, 30)
        p2_text = self.font.render(
            f'Player 2 - {self.game.player2.score} pontos',
            True, (40, 40, 180))
        p2_text_rect = p2_text.get_rect(center=p2_rect.center)
        active = self.game.winner or self.game.current_player.id == 2
        self.draw_show_tiles_button(
            p2_rect.y + self.cell_size, 'Mostrar Letras', active)
        self.screen.blit(p1_text, p1_text_rect)
        self.screen.blit(p2_text, p2_text_rect)
        for tile in sorted(player2_tiles[:7]):
            tile_rect = pygame.Rect(player_x, player2_y, tile_size, tile_size)
            pygame.draw.rect(self.screen, (0, 0, 128), tile_rect)
            show_tile = str(tile).upper(
            ) if self.game.player2.show_tiles else ''
            value = f'{int(tile)}' if self.game.player2.show_tiles else ''
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
        for tile in sorted(player1_tiles[:7]):
            tile_rect = pygame.Rect(player_x, player1_y, tile_size, tile_size)
            pygame.draw.rect(self.screen, (128, 0, 0), tile_rect)
            show_tile = str(tile).upper(
            ) if self.game.player1.show_tiles else ''
            value = f'{int(tile)}' if self.game.player1.show_tiles else ''
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
        if self.game.current_player.is_bot and not self.game.winner:
            print('O bot está fazendo uma jogada')
            self.game.show_tiles(1)
            self.game.show_tiles(2)
            self.game.bot_play()
            self.game.print_board()
            self.game.show_bag()
            self.color_change_counter = 0
            self.active_button = self.game.current_player.id
        if self.game.winner:
            self.game.player1.show_tiles = True
            self.game.player2.show_tiles = True
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
            if (event.type == pygame.KEYDOWN and self.word_start_cell and
                    not self.game.winner):
                if (self.current_cell and (event.unicode.isalpha() or
                                           event.unicode in self.letters_accents)):  # noqa
                    letter = event.unicode
                    self.current_word.append(
                        letter.upper() if self.is_blank else letter.lower())
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
                    self.is_blank = False
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
                    self.game.show_bag()
                    self.color_change_counter = 0
                    if play_ok:
                        self.active_button = self.game.current_player.id
