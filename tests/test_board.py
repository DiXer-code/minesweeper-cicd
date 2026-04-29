import pytest

from src.board import Board
from src.cell import Cell
from src.settings import MINES


@pytest.fixture
def board() -> Board:
    return Board()


def plant_mines(board: Board, positions: set[tuple[int, int]]) -> None:
    for row in board.grid:
        for cell in row:
            cell.is_mine = False
            cell.is_revealed = False
            cell.is_flagged = False
            cell.neighbor_mines = 0

    for row, col in positions:
        board.grid[row][col].is_mine = True

    board.calculate_numbers()


def test_cell_defaults_are_initialized() -> None:
    cell = Cell(2, 3)

    assert cell.row == 2
    assert cell.col == 3
    assert not cell.is_mine
    assert not cell.is_revealed
    assert not cell.is_flagged
    assert cell.neighbor_mines == 0


def test_cell_repr_contains_coordinates() -> None:
    cell = Cell(1, 4)

    assert "Cell(1,4)" in repr(cell)


def test_initialize_keeps_first_click_safe_and_places_exact_mines(board: Board) -> None:
    board.initialize(0, 0)

    mine_count = sum(cell.is_mine for row in board.grid for cell in row)

    assert board.initialized is True
    assert not board.grid[0][0].is_mine
    assert mine_count == MINES


@pytest.mark.parametrize(
    ("row", "col", "expected_count"),
    [
        (0, 0, 3),
        (5, 5, 8),
    ],
)
def test_iter_neighbors_returns_expected_positions(
    board: Board,
    row: int,
    col: int,
    expected_count: int,
) -> None:
    neighbors = list(board._iter_neighbors(row, col))

    assert len(neighbors) == expected_count
    assert (row, col) not in neighbors


def test_calculate_numbers_counts_adjacent_mines(board: Board) -> None:
    plant_mines(board, {(0, 1), (1, 0), (1, 2)})

    assert board.grid[1][1].neighbor_mines == 3
    assert board.grid[0][0].neighbor_mines == 2


def test_reveal_cell_recursively_reveals_empty_area(board: Board) -> None:
    plant_mines(board, set())

    board.reveal_cell(0, 0)

    assert all(cell.is_revealed for row in board.grid for cell in row)


def test_reveal_cell_does_not_open_flagged_cell(board: Board) -> None:
    board.toggle_flag(1, 1)

    board.reveal_cell(1, 1)

    assert board.grid[1][1].is_flagged is True
    assert board.grid[1][1].is_revealed is False


def test_reveal_all_mines_reveals_only_mines(board: Board) -> None:
    mine_positions = {(0, 0), (2, 2), (4, 4)}
    plant_mines(board, mine_positions)

    board.reveal_all_mines()

    for row_index, row in enumerate(board.grid):
        for col_index, cell in enumerate(row):
            if (row_index, col_index) in mine_positions:
                assert cell.is_revealed is True
            else:
                assert cell.is_revealed is False


def test_toggle_flag_only_changes_hidden_cells(board: Board) -> None:
    board.toggle_flag(1, 1)
    board.grid[1][1].is_revealed = True

    board.toggle_flag(1, 1)

    assert board.grid[1][1].is_flagged is True


def test_check_win_returns_true_when_all_safe_cells_are_revealed(board: Board) -> None:
    plant_mines(board, {(0, 0), (0, 1)})

    for row in board.grid:
        for cell in row:
            if not cell.is_mine:
                cell.is_revealed = True

    assert board.check_win() is True


def test_count_flags_returns_total_number_of_flags(board: Board) -> None:
    board.toggle_flag(0, 0)
    board.toggle_flag(1, 1)
    board.toggle_flag(2, 2)

    assert board.count_flags() == 3


def test_count_neighbor_flags_counts_only_adjacent_flags(board: Board) -> None:
    board.toggle_flag(4, 4)
    board.toggle_flag(4, 5)
    board.toggle_flag(9, 9)

    assert board.count_neighbor_flags(5, 5) == 2


def test_chord_cell_reveals_unflagged_neighbors_when_flags_match(board: Board) -> None:
    mine_positions = {(0, 0), (0, 1)}
    plant_mines(board, mine_positions)
    board.grid[1][1].is_revealed = True

    for row, col in mine_positions:
        board.grid[row][col].is_flagged = True

    board.chord_cell(1, 1)

    for row, col in board._iter_neighbors(1, 1):
        cell = board.grid[row][col]
        if (row, col) in mine_positions:
            assert cell.is_revealed is False
        else:
            assert cell.is_revealed is True


def test_chord_cell_does_nothing_when_flag_count_does_not_match(board: Board) -> None:
    plant_mines(board, {(0, 0), (0, 1)})
    board.grid[1][1].is_revealed = True
    board.grid[0][0].is_flagged = True

    board.chord_cell(1, 1)

    assert board.grid[1][0].is_revealed is False
