import pygame

from .board import Board
from . import settings

NUMBER_COLORS = {
    1: (0, 0, 255),       # Синій
    2: (0, 128, 0),       # Зелений
    3: (255, 0, 0),       # Червоний
    4: (0, 0, 128),       # Темно-синій
    5: (128, 0, 0),       # Бордовий
    6: (0, 128, 128),     # Бірюзовий
    7: (0, 0, 0),         # Чорний
    8: (128, 128, 128)    # Сірий
}

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)

        self.board = Board()
        self.running = True
        self.game_over = False
        self.win = False
        self.start_time = 0
        self.time_elapsed = 0
        self.playing = False
        self.playing = False
        self.last_click_time = 0
        self.last_click_cell = None
        self.double_click_delay = 300 

    def reset(self):
        self.board = Board()
        self.game_over = False
        self.win = False
        self.start_time = 0
        self.time_elapsed = 0
        self.playing = False
        self.last_click_time = 0
        self.last_click_cell = None

    def draw(self):
        self.screen.fill((200, 200, 200))

        for r in range(settings.ROWS):
            for c in range(settings.COLS):
                cell = self.board.grid[r][c]
                x = c * settings.CELL_SIZE
                y = r * settings.CELL_SIZE
                rect = pygame.Rect(x, y, settings.CELL_SIZE, settings.CELL_SIZE)
                self._draw_cell(cell, x, y, rect)

        self.draw_status()
        pygame.display.flip()

    def _draw_cell(self, cell, x, y, rect):
        if cell.is_revealed:
            # Відкрита клітинка
            pygame.draw.rect(self.screen, (220, 220, 220), rect)
            self._draw_revealed_content(cell, x, y, rect)
            pygame.draw.rect(self.screen, (150, 150, 150), rect, 1)
        else:
            # Закрита клітинка 3D
            pygame.draw.rect(self.screen, (190, 190, 190), rect)
            pygame.draw.line(self.screen, (255, 255, 255), rect.topleft, rect.topright, 2)
            pygame.draw.line(self.screen, (255, 255, 255), rect.topleft, rect.bottomleft, 2)
            pygame.draw.line(self.screen, (100, 100, 100), rect.bottomleft, rect.bottomright, 2)
            pygame.draw.line(self.screen, (100, 100, 100), rect.topright, rect.bottomright, 2)
            
            if cell.is_flagged:
                self._draw_flag(rect)

    def _draw_revealed_content(self, cell, x, y, rect):
        if cell.is_mine:
            pygame.draw.rect(self.screen, (255, 100, 100), rect)
            pygame.draw.circle(self.screen, (0, 0, 0), rect.center, settings.CELL_SIZE // 4)
        elif cell.neighbor_mines > 0:
            color = NUMBER_COLORS.get(cell.neighbor_mines, (0, 0, 0))
            text = self.font.render(str(cell.neighbor_mines), True, color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def _draw_flag(self, rect):
        pole_rect = pygame.Rect(rect.centerx - 2, rect.top + settings.CELL_SIZE // 4, 4, settings.CELL_SIZE // 2)
        pygame.draw.rect(self.screen, (0, 0, 0), pole_rect)
        
        flag_points = [
            (rect.centerx + 2, rect.top + settings.CELL_SIZE // 4),
            (rect.centerx + settings.CELL_SIZE // 3, rect.top + settings.CELL_SIZE // 3 + 2),
            (rect.centerx + 2, rect.top + settings.CELL_SIZE // 2)
        ]
        pygame.draw.polygon(self.screen, (255, 0, 0), flag_points)

    def draw_status(self):
        status_rect = pygame.Rect(0, settings.ROWS * settings.CELL_SIZE, settings.WIDTH, settings.STATUS_BAR_HEIGHT)
        pygame.draw.rect(self.screen, (210, 210, 210), status_rect)
        pygame.draw.line(self.screen, (128, 128, 128), status_rect.topleft, status_rect.topright, 3)

        if self.playing:
            self.time_elapsed = (pygame.time.get_ticks() - self.start_time) // 1000

        if self.game_over:
            message = f"Виграш! Час: {self.time_elapsed}с (R - Рестарт)" if self.win else f"Поразка! Час: {self.time_elapsed}с (R - Рестарт)"
            color = (0, 150, 0) if self.win else (200, 0, 0)
        else:
            message = f"Прапорці: {self.board.count_flags()} / {settings.MINES} | Час: {self.time_elapsed}с"
            color = (30, 30, 30)

        text = self.font.render(message, True, color)
        text_rect = text.get_rect(center=status_rect.center)
        self.screen.blit(text, text_rect)

    def handle_left_click(self, pos):
        if self.game_over:
            return

        x, y = pos
        if y >= settings.ROWS * settings.CELL_SIZE:
            return

        col = x // settings.CELL_SIZE
        row = y // settings.CELL_SIZE

        cell = self.board.grid[row][col]

        if cell.is_flagged:
            return

        if not self.board.initialized:
            self.board.initialize(row, col)
            cell = self.board.grid[row][col]
            self.start_time = pygame.time.get_ticks()
            self.playing = True

        if cell.is_mine:
            self.board.reveal_all_mines()
            self.game_over = True
            self.win = False
            self.playing = False 
        else:
            self.board.reveal_cell(row, col)
            if self.board.check_win():
                self.game_over = True
                self.win = True
                self.playing = False 

    def handle_right_click(self, pos):
        if self.game_over:
            return

        x, y = pos
        if y >= settings.ROWS * settings.CELL_SIZE:
            return

        col = x // settings.CELL_SIZE
        row = y // settings.CELL_SIZE
        self.board.toggle_flag(row, col)

    def handle_chording(self, pos):
        if self.game_over:
            return

        x, y = pos
        if y >= settings.ROWS * settings.CELL_SIZE:
            return

        col = x // settings.CELL_SIZE
        row = y // settings.CELL_SIZE

        self.board.chord_cell(row, col)

        for r in range(settings.ROWS):
            for c in range(settings.COLS):
                if self.board.grid[r][c].is_revealed and self.board.grid[r][c].is_mine:
                    self.board.reveal_all_mines()
                    self.game_over = True
                    self.win = False
                    self.playing = False
                    return

        if self.board.check_win():
            self.game_over = True
            self.win = True
            self.playing = False

    def run(self):
        while self.running:
            self.clock.tick(settings.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Лівий клік
                        x, y = event.pos
                        # Перевіряємо, чи клік був по ігровому полю (а не по статус-бару)
                        if y < settings.ROWS * settings.CELL_SIZE:
                            col = x // settings.CELL_SIZE
                            row = y // settings.CELL_SIZE
                            current_cell = (row, col)
                            current_time = pygame.time.get_ticks()

                            # Якщо це та сама клітинка і пройшло менше 300мс — це подвійний клік!
                            if current_time - self.last_click_time < self.double_click_delay and self.last_click_cell == current_cell:
                                self.handle_chording(event.pos)
                                self.last_click_time = 0 # Скидаємо, щоб уникнути потрійного кліку
                            else:
                                # Інакше це звичайний одинарний клік
                                self.handle_left_click(event.pos)
                                self.last_click_time = current_time
                                self.last_click_cell = current_cell
                        else:
                            # Клік по нижній панелі
                            self.handle_left_click(event.pos)
                            
                    elif event.button == 3: # Правий клік
                        self.handle_right_click(event.pos)

            self.draw()

        pygame.quit()