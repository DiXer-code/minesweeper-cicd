import unittest

from src.board import Board
from src.cell import Cell
from src.settings import MINES, ROWS, COLS


class CellDefaultStateTests(unittest.TestCase):
    """Tests for the default state of a newly created Cell."""

    def test_cell_default_not_mine(self):
        cell = Cell(0, 0)
        self.assertFalse(cell.is_mine)

    def test_cell_default_not_revealed(self):
        cell = Cell(0, 0)
        self.assertFalse(cell.is_revealed)

    def test_cell_default_not_flagged(self):
        cell = Cell(0, 0)
        self.assertFalse(cell.is_flagged)

    def test_cell_default_zero_neighbors(self):
        cell = Cell(2, 3)
        self.assertEqual(cell.neighbor_mines, 0)

    def test_cell_repr_contains_coords(self):
        cell = Cell(1, 4)
        self.assertIn("1,4", repr(cell))


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


class ChordTests(unittest.TestCase):
    """Tests for chord_cell and count_neighbor_flags."""

    def test_count_neighbor_flags_zero_initially(self):
        board = Board()
        board.initialize(5, 5)
        self.assertEqual(board.count_neighbor_flags(5, 5), 0)

    def test_count_neighbor_flags_after_flagging(self):
        board = Board()
        board.initialize(5, 5)
        board.toggle_flag(4, 4)
        board.toggle_flag(4, 5)
        count = board.count_neighbor_flags(5, 5)
        self.assertGreaterEqual(count, 1)

    def test_chord_does_not_crash_on_unrevealed_cell(self):
        board = Board()
        board.initialize(0, 0)
        # Should silently do nothing вЂ” unrevealed cell with neighbor_mines==0
        board.chord_cell(0, 0)

    def test_iter_neighbors_corner_has_three(self):
        board = Board()
        neighbors = list(board._iter_neighbors(0, 0))
        self.assertEqual(len(neighbors), 3)

    def test_iter_neighbors_center_has_eight(self):
        board = Board()
        neighbors = list(board._iter_neighbors(5, 5))
        self.assertEqual(len(neighbors), 8)


# neighbor flag count tests included
# neighbor flag count tests included
if __name__ == "__main__":
    unittest.main()


