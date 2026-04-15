"""
Автори: Клебанський Іван, Захарченко Артем, Маркграф Олександр, група ІПЗ-21
Головний модуль запуску гри Сапер.
Запускає меню вибору складності, після чого — гру.
"""
import pygame

from src.game import Game
from src.menu import Menu
import src.settings as settings

DIFFICULTY_CONFIGS = {
    'easy':   (8,  8,  10, 320, 370),
    'normal': (10, 10, 10, 400, 450),
    'medium': (12, 12, 20, 480, 530),
    'hard':   (16, 16, 40, 640, 690),
}

DIFFICULTY_LABEL = {
    'easy':   'Easy',
    'medium': 'Medium',
    'normal': 'Normal',
    'hard':   'Hard',
}


def apply_settings(difficulty: str) -> None:
    """Apply grid size, mine count and window dimensions for the chosen difficulty."""
    rows, cols, mines, w, h = DIFFICULTY_CONFIGS[difficulty]
    settings.ROWS, settings.COLS, settings.MINES = rows, cols, mines
    settings.WIDTH, settings.HEIGHT = w, h
    settings.CELL_SIZE = w // cols
    settings.STATUS_BAR_HEIGHT = h - rows * settings.CELL_SIZE


if __name__ == "__main__":
    pygame.init()

    while True:
        # Show difficulty selection menu (fixed 420×520 window)
        menu_screen = pygame.display.set_mode((420, 520))
        pygame.display.set_caption("Minesweeper")
        menu = Menu(menu_screen)
        difficulty = menu.run()

        # Apply settings and launch the game
        apply_settings(difficulty)
        label = DIFFICULTY_LABEL[difficulty]
        game = Game(title=f"{label} — Minesweeper", difficulty=difficulty)
        result = game.run()

        if result == "quit":
            break
        # result == "menu" → loop back to difficulty selection

    pygame.quit()