class Cell:
    """Represents a single cell on the Minesweeper board."""

    def __init__(self, row: int, col: int) -> None:
        self.row: int = row
        self.col: int = col
        self.is_mine: bool = False
        self.is_revealed: bool = False
        self.is_flagged: bool = False
        self.neighbor_mines: int = 0

    def __repr__(self) -> str:
        state = "M" if self.is_mine else str(self.neighbor_mines)
        flag = "F" if self.is_flagged else " "
        revealed = "O" if self.is_revealed else "."
        return f"Cell({self.row},{self.col})[{state}|{flag}|{revealed}]"
