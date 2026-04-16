import random

from .cell import Cell
from . import settings

class Board:
    def __init__(self):
        self.grid = [[Cell(r, c) for c in range(settings.COLS)] for r in range(settings.ROWS)]
        self.initialized = False

    def initialize(self, first_row: int, first_col: int):
        if self.initialized:
            return
        self.place_mines(first_row, first_col)
        self.calculate_numbers()
        self.initialized = True

    def place_mines(self, excluded_row: int, excluded_col: int):
        positions = set()
        while len(positions) < settings.MINES:
            r = random.randint(0, settings.ROWS - 1)
            c = random.randint(0, settings.COLS - 1)
            if (r, c) == (excluded_row, excluded_col):
                continue
            positions.add((r, c))

        for r, c in positions:
            self.grid[r][c].is_mine = True

    def calculate_numbers(self):
        for r in range(settings.ROWS):
            for c in range(settings.COLS):
                if self.grid[r][c].is_mine:
                    continue
                self.grid[r][c].neighbor_mines = self.count_neighbor_mines(r, c)

    def count_neighbor_mines(self, row: int, col: int) -> int:
        count = 0
        for r in range(max(0, row - 1), min(settings.ROWS, row + 2)):
            for c in range(max(0, col - 1), min(settings.COLS, col + 2)):
                if (r, c) != (row, col) and self.grid[r][c].is_mine:
                    count += 1
        return count

    def reveal_cell(self, row, col):
        cell = self.grid[row][col]

        if cell.is_revealed or cell.is_flagged:
            return

        cell.is_revealed = True

        if cell.is_mine:
            return

        if cell.neighbor_mines == 0:
            for r in range(max(0, row - 1), min(settings.ROWS, row + 2)):
                for c in range(max(0, col - 1), min(settings.COLS, col + 2)):
                    if not self.grid[r][c].is_revealed:
                        self.reveal_cell(r, c)

    def toggle_flag(self, row, col):
        cell = self.grid[row][col]
        if not cell.is_revealed:
            cell.is_flagged = not cell.is_flagged

    def reveal_all_mines(self):
        for row in self.grid:
            for cell in row:
                if cell.is_mine:
                    cell.is_revealed = True

    def check_win(self):
        for row in self.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def count_flags(self) -> int:
        return sum(cell.is_flagged for row in self.grid for cell in row)

    def count_neighbor_flags(self, row: int, col: int) -> int:
        """Рахує кількість прапорців навколо вказаної клітинки."""
        count = 0
        for r in range(max(0, row - 1), min(settings.ROWS, row + 2)):
            for c in range(max(0, col - 1), min(settings.COLS, col + 2)):
                if self.grid[r][c].is_flagged:
                    count += 1
        return count

    def chord_cell(self, row: int, col: int):
        """Автоматично відкриває сусідів, якщо кількість прапорців збігається з цифрою."""
        cell = self.grid[row][col]
        
        # Працює лише для відкритих клітинок з цифрами
        if not cell.is_revealed or cell.neighbor_mines == 0:
            return

        # Якщо кількість прапорців навколо дорівнює цифрі в клітинці
        if self.count_neighbor_flags(row, col) == cell.neighbor_mines:
            for r in range(max(0, row - 1), min(settings.ROWS, row + 2)):
                for c in range(max(0, col - 1), min(settings.COLS, col + 2)):
                    # Відкриваємо всі закриті клітинки без прапорців
                    if not self.grid[r][c].is_flagged and not self.grid[r][c].is_revealed:
                        self.reveal_cell(r, c)