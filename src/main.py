"""Main entry point for Minesweeper."""
import pygame

from src.game import Game
from src.leaderboard import Leaderboard
from src.menu import Menu
import src.settings as settings

DIFFICULTY_CONFIGS = {
    "easy": (8, 8, 10, 320, 370),
    "normal": (10, 10, 10, 400, 450),
    "medium": (12, 12, 20, 480, 530),
    "hard": (16, 16, 40, 640, 690),
}

DIFFICULTY_LABELS = {
    "easy": "Easy",
    "normal": "Normal",
    "medium": "Medium",
    "hard": "Hard",
}


def apply_settings(difficulty: str) -> None:
    """Apply board size, mine count, and window dimensions for a difficulty."""
    rows, cols, mines, width, height = DIFFICULTY_CONFIGS[difficulty]
    settings.ROWS = rows
    settings.COLS = cols
    settings.MINES = mines
    settings.WIDTH = width
    settings.HEIGHT = height
    settings.CELL_SIZE = width // cols
    settings.STATUS_BAR_HEIGHT = height - rows * settings.CELL_SIZE


if __name__ == "__main__":
    pygame.init()

    while True:
        menu_screen = pygame.display.set_mode((420, 520))
        pygame.display.set_caption("Minesweeper")
        menu = Menu(menu_screen)
        choice = menu.run()

        if choice == "leaderboard":
            leaderboard = Leaderboard(menu_screen)
            leaderboard.run()
            continue

        difficulty = choice
        apply_settings(difficulty)
        label = DIFFICULTY_LABELS[difficulty]
        game = Game(title=f"{label} - Minesweeper", difficulty=difficulty)
        result = game.run()

        if result == "quit":
            break

    pygame.quit()
