import pygame

from .board import Board
from .settings import CELL_SIZE, COLS, FPS, HEIGHT, ROWS, WIDTH


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)

        self.board = Board()
        self.running = True
        self.game_over = False
        self.win = False

    def draw(self):
        self.screen.fill((200, 200, 200))

        for r in range(ROWS):
            for c in range(COLS):
                cell = self.board.grid[r][c]
                x = c * CELL_SIZE
                y = r * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

                if cell.is_revealed:
                    pygame.draw.rect(self.screen, (220, 220, 220), rect)

                    if cell.is_mine:
                        pygame.draw.circle(self.screen, (255, 0, 0), rect.center, CELL_SIZE // 4)
                    elif cell.neighbor_mines > 0:
                        text = self.font.render(str(cell.neighbor_mines), True, (0, 0, 255))
                        self.screen.blit(text, (x + CELL_SIZE // 3, y + CELL_SIZE // 4))
                else:
                    pygame.draw.rect(self.screen, (140, 140, 140), rect)

                    if cell.is_flagged:
                        text = self.font.render("F", True, (255, 140, 0))
                        self.screen.blit(text, (x + CELL_SIZE // 3, y + CELL_SIZE // 4))

                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        if self.game_over:
            message = "You Win!" if self.win else "Game Over!"
            text = self.font.render(message, True, (0, 0, 0))
            self.screen.blit(text, (WIDTH // 2 - 70, HEIGHT - 35))

        pygame.display.flip()

    def handle_left_click(self, pos):
        if self.game_over:
            return

        x, y = pos
        if y >= ROWS * CELL_SIZE:
            return

        col = x // CELL_SIZE
        row = y // CELL_SIZE

        cell = self.board.grid[row][col]

        if cell.is_flagged:
            return

        if cell.is_mine:
            self.board.reveal_all_mines()
            self.game_over = True
            self.win = False
        else:
            self.board.reveal_cell(row, col)
            if self.board.check_win():
                self.game_over = True
                self.win = True

    def handle_right_click(self, pos):
        if self.game_over:
            return

        x, y = pos
        if y >= ROWS * CELL_SIZE:
            return

        col = x // CELL_SIZE
        row = y // CELL_SIZE
        self.board.toggle_flag(row, col)

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_left_click(event.pos)
                    elif event.button == 3:
                        self.handle_right_click(event.pos)

            self.draw()

        pygame.quit()
