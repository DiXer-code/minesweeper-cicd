import random
from cell import Cell
from settings import ROWS, COLS, MINES


class Board:
    def __init__(self):
        self.grid = [[Cell(r, c) for c in range(COLS)] for r in range(ROWS)]
        self.place_mines()
        self.calculate_numbers()

    def place_mines(self):
        positions = set()
        while len(positions) < MINES:
            r = random.randint(0, ROWS - 1)
            c = random.randint(0, COLS - 1)
            positions.add((r, c))

        for r, c in positions:
            self.grid[r][c].is_mine = True

    def calculate_numbers(self):
        for r in range(ROWS):
            for c in range(COLS):
                if self.grid[r][c].is_mine:
                    continue
                self.grid[r][c].neighbor_mines = self.count_neighbor_mines(r, c)

    def count_neighbor_mines(self, row, col):
        count = 0
        for r in range(max(0, row - 1), min(ROWS, row + 2)):
            for c in range(max(0, col - 1), min(COLS, col + 2)):
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
            for r in range(max(0, row - 1), min(ROWS, row + 2)):
                for c in range(max(0, col - 1), min(COLS, col + 2)):
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