import random

from .cell import Cell
from . import settings


class Board:
    """Manages the Minesweeper grid, mine placement, and game logic."""

    def __init__(self) -> None:
        self.grid: list[list[Cell]] = [
            [Cell(r, c) for c in range(settings.COLS)]
            for r in range(settings.ROWS)
        ]
        self.initialized: bool = False

    def _iter_neighbors(self, row: int, col: int):
        """Yield (r, c) tuples for all valid neighbors of a cell."""
        for r in range(max(0, row - 1), min(settings.ROWS, row + 2)):
            for c in range(max(0, col - 1), min(settings.COLS, col + 2)):
                if (r, c) != (row, col):
                    yield r, c

    def initialize(self, first_row: int, first_col: int) -> None:
        """Place mines and calculate numbers. Safe for the first clicked cell."""
        if self.initialized:
            return
        self.place_mines(first_row, first_col)
        self.calculate_numbers()
        self.initialized = True

    def place_mines(self, excluded_row: int, excluded_col: int) -> None:
        """Randomly place mines, avoiding the excluded cell."""
        positions: set[tuple[int, int]] = set()
        while len(positions) < settings.MINES:
            r = random.randint(0, settings.ROWS - 1)
            c = random.randint(0, settings.COLS - 1)
            if (r, c) == (excluded_row, excluded_col):
                continue
            positions.add((r, c))

        for r, c in positions:
            self.grid[r][c].is_mine = True

    def calculate_numbers(self) -> None:
        """Calculate neighbor mine counts for all non-mine cells."""
        for r in range(settings.ROWS):
            for c in range(settings.COLS):
                if not self.grid[r][c].is_mine:
                    self.grid[r][c].neighbor_mines = self.count_neighbor_mines(r, c)

    def count_neighbor_mines(self, row: int, col: int) -> int:
        """Return the number of mines adjacent to (row, col)."""
        return sum(
            1 for r, c in self._iter_neighbors(row, col)
            if self.grid[r][c].is_mine
        )

    def reveal_cell(self, row: int, col: int) -> None:
        """Reveal a cell; recursively reveal neighbors if it has no adjacent mines."""
        cell = self.grid[row][col]

        if cell.is_revealed or cell.is_flagged:
            return

        cell.is_revealed = True

        if cell.is_mine:
            return

        if cell.neighbor_mines == 0:
            for r, c in self._iter_neighbors(row, col):
                if not self.grid[r][c].is_revealed:
                    self.reveal_cell(r, c)

    def toggle_flag(self, row: int, col: int) -> None:
        """Toggle the flag state of an unrevealed cell."""
        cell = self.grid[row][col]
        if not cell.is_revealed:
            cell.is_flagged = not cell.is_flagged

    def reveal_all_mines(self) -> None:
        """Reveal all mine cells (called on game over)."""
        for row in self.grid:
            for cell in row:
                if cell.is_mine:
                    cell.is_revealed = True

    def check_win(self) -> bool:
        """Return True if all non-mine cells are revealed."""
        return all(
            cell.is_revealed
            for row in self.grid
            for cell in row
            if not cell.is_mine
        )

    def count_flags(self) -> int:
        """Return the total number of flagged cells."""
        return sum(cell.is_flagged for row in self.grid for cell in row)

    def count_neighbor_flags(self, row: int, col: int) -> int:
        """Return the number of flagged cells adjacent to (row, col)."""
        return sum(
            1 for r, c in self._iter_neighbors(row, col)
            if self.grid[r][c].is_flagged
        )

    def chord_cell(self, row: int, col: int) -> None:
        """Auto-reveal neighbors when flag count matches the cell number."""
        cell = self.grid[row][col]

        if not cell.is_revealed or cell.neighbor_mines == 0:
            return

        if self.count_neighbor_flags(row, col) == cell.neighbor_mines:
            for r, c in self._iter_neighbors(row, col):
                if not self.grid[r][c].is_flagged and not self.grid[r][c].is_revealed:
                    self.reveal_cell(r, c)