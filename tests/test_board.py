import unittest

from src.board import Board
from src.settings import MINES, ROWS, COLS


class BoardTests(unittest.TestCase):
    def test_first_click_is_safe(self):
        board = Board()
        board.initialize(0, 0)

        self.assertFalse(board.grid[0][0].is_mine)

    def test_exact_mine_count_is_placed(self):
        board = Board()
        board.initialize(0, 0)
        mine_count = sum(cell.is_mine for row in board.grid for cell in row)

        self.assertEqual(mine_count, MINES)

    def test_toggle_flag_changes_state(self):
        board = Board()
        board.toggle_flag(1, 1)
        self.assertTrue(board.grid[1][1].is_flagged)
        board.toggle_flag(1, 1)
        self.assertFalse(board.grid[1][1].is_flagged)

    def test_reveal_all_mines_reveals_only_mines(self):
        board = Board()
        board.initialize(0, 0)
        board.reveal_all_mines()

        for row in range(ROWS):
            for col in range(COLS):
                cell = board.grid[row][col]
                if cell.is_mine:
                    self.assertTrue(cell.is_revealed)

    def test_check_win_when_all_safe_cells_revealed(self):
        board = Board()
        board.initialize(0, 0)

        for row in board.grid:
            for cell in row:
                if not cell.is_mine:
                    cell.is_revealed = True

        self.assertTrue(board.check_win())


if __name__ == "__main__":
    unittest.main()
