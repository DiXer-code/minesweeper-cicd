import pygame

from .board import Board
from . import settings
from . import scores as scores_module

NUMBER_COLORS = {
    1: (0, 0, 255),
    2: (0, 128, 0),
    3: (255, 0, 0),
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 128, 128),
    7: (0, 0, 0),
    8: (128, 128, 128)
}


class Game:
    def __init__(self, title: str = "Minesweeper", difficulty: str = "normal") -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        # Window title reflects chosen difficulty
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)
        self.font_status = pygame.font.SysFont(None, 22)

        self.difficulty = difficulty
        self.board = Board()
        self.running = True
        self.game_over = False
        self.win = False
        self.start_time = 0
        self.time_elapsed = 0
        self.playing = False
        self.last_click_time = 0
        self.last_click_cell = None
        self.double_click_delay = 300

        self.is_new_best: bool = False
        self.best_time: int | None = scores_module.get_best_time(difficulty)

    def reset(self) -> None:
        self.board = Board()
        self.game_over = False
        self.win = False
        self.start_time = 0
        self.time_elapsed = 0
        self.playing = False
        self.last_click_time = 0
        self.last_click_cell = None
        self.is_new_best = False
        self.best_time = scores_module.get_best_time(self.difficulty)

    def _record_win(self) -> None:
        """Save the elapsed time and update the best-time cache."""
        self.is_new_best = scores_module.record_time(self.difficulty, self.time_elapsed)
        self.best_time = scores_module.get_best_time(self.difficulty)

    # ── Drawing ──────────────────────────────────────────────────────────────

    def draw(self) -> None:
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

    def _draw_cell(self, cell, x, y, rect) -> None:
        if cell.is_revealed:
            pygame.draw.rect(self.screen, (220, 220, 220), rect)
            self._draw_revealed_content(cell, x, y, rect)
            pygame.draw.rect(self.screen, (150, 150, 150), rect, 1)
        else:
            pygame.draw.rect(self.screen, (190, 190, 190), rect)
            pygame.draw.line(self.screen, (255, 255, 255), rect.topleft, rect.topright, 2)
            pygame.draw.line(self.screen, (255, 255, 255), rect.topleft, rect.bottomleft, 2)
            pygame.draw.line(self.screen, (100, 100, 100), rect.bottomleft, rect.bottomright, 2)
            pygame.draw.line(self.screen, (100, 100, 100), rect.topright, rect.bottomright, 2)

            if cell.is_flagged:
                self._draw_flag(rect)

    def _draw_revealed_content(self, cell, x, y, rect) -> None:
        if cell.is_mine:
            pygame.draw.rect(self.screen, (255, 100, 100), rect)
            pygame.draw.circle(self.screen, (0, 0, 0), rect.center, settings.CELL_SIZE // 4)
        elif cell.neighbor_mines > 0:
            color = NUMBER_COLORS.get(cell.neighbor_mines, (0, 0, 0))
            text = self.font.render(str(cell.neighbor_mines), True, color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def _draw_flag(self, rect) -> None:
        pole_rect = pygame.Rect(
            rect.centerx - 2,
            rect.top + settings.CELL_SIZE // 4,
            4,
            settings.CELL_SIZE // 2
        )
        pygame.draw.rect(self.screen, (0, 0, 0), pole_rect)
        flag_points = [
            (rect.centerx + 2,                    rect.top + settings.CELL_SIZE // 4),
            (rect.centerx + settings.CELL_SIZE // 3, rect.top + settings.CELL_SIZE // 3 + 2),
            (rect.centerx + 2,                    rect.top + settings.CELL_SIZE // 2),
        ]
        pygame.draw.polygon(self.screen, (255, 0, 0), flag_points)

    def draw_status(self) -> None:
        status_rect = pygame.Rect(
            0, settings.ROWS * settings.CELL_SIZE,
            settings.WIDTH, settings.STATUS_BAR_HEIGHT
        )
        pygame.draw.rect(self.screen, (210, 210, 210), status_rect)
        pygame.draw.line(self.screen, (128, 128, 128),
                         status_rect.topleft, status_rect.topright, 3)

        if self.playing:
            self.time_elapsed = (pygame.time.get_ticks() - self.start_time) // 1000

        if self.game_over:
            if self.win:
                best_note = " ★ НОВИЙ РЕКОРД!" if self.is_new_best \
                    else (f"  рекорд: {self.best_time}с" if self.best_time else "")
                message = f"Виграш! {self.time_elapsed}с{best_note}   R рестарт  M меню"
                color = (0, 130, 0)
            else:
                message = f"Поразка! {self.time_elapsed}с   R рестарт  M меню"
                color = (200, 0, 0)
        else:
            best_str = f"  |  Рекорд: {self.best_time}с" if self.best_time is not None else ""
            message = f"Прапорці: {self.board.count_flags()}/{settings.MINES}  Час: {self.time_elapsed}с{best_str}"
            color = (30, 30, 30)

        text = self.font_status.render(message, True, color)
        text_rect = text.get_rect(center=status_rect.center)
        self.screen.blit(text, text_rect)

    # ── Input handlers ───────────────────────────────────────────────────────

    def handle_left_click(self, pos) -> None:
        if self.game_over:
            return

        x, y = pos
        if y >= settings.ROWS * settings.CELL_SIZE:
            return

        col = min(x // settings.CELL_SIZE, settings.COLS - 1)
        row = min(y // settings.CELL_SIZE, settings.ROWS - 1)

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
                self._record_win()

    def handle_right_click(self, pos) -> None:
        if self.game_over:
            return

        x, y = pos
        if y >= settings.ROWS * settings.CELL_SIZE:
            return

        col = min(x // settings.CELL_SIZE, settings.COLS - 1)
        row = min(y // settings.CELL_SIZE, settings.ROWS - 1)
        self.board.toggle_flag(row, col)

    def handle_chording(self, pos) -> None:
        if self.game_over:
            return

        x, y = pos
        if y >= settings.ROWS * settings.CELL_SIZE:
            return

        col = min(x // settings.CELL_SIZE, settings.COLS - 1)
        row = min(y // settings.CELL_SIZE, settings.ROWS - 1)

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
            self._record_win()

    # ── Main loop ────────────────────────────────────────────────────────────

    def run(self) -> str:
        """Main game loop. Returns 'menu' or 'quit'."""
        while True:
            self.clock.tick(settings.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_m:
                        return "menu"

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        if y < settings.ROWS * settings.CELL_SIZE:
                            col = min(x // settings.CELL_SIZE, settings.COLS - 1)
                            row = min(y // settings.CELL_SIZE, settings.ROWS - 1)
                            current_cell = (row, col)
                            current_time = pygame.time.get_ticks()

                            if (current_time - self.last_click_time < self.double_click_delay
                                    and self.last_click_cell == current_cell):
                                self.handle_chording(event.pos)
                                self.last_click_time = 0
                            else:
                                self.handle_left_click(event.pos)
                                self.last_click_time = current_time
                                self.last_click_cell = current_cell
                        else:
                            self.handle_left_click(event.pos)

                    elif event.button == 3:
                        self.handle_right_click(event.pos)

            self.draw()
