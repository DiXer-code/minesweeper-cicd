"""
Автори: Клебанський Іван, Захарченко Артем, Маркграф Олександр, група ІПЗ-21
Головний модуль запуску гри Сапер.
"""
import argparse
from src.game import Game
import src.settings as settings

def parse_args():
    parser = argparse.ArgumentParser(description="Гра Сапер (Minesweeper)")
    parser.add_argument(
        '--difficulty', 
        type=str, 
        choices=['easy', 'normal', 'hard'], 
        default='normal',
        help="Вибір складності гри"
    )
    return parser.parse_args()

def apply_settings(args):
    if args.difficulty == 'easy':
        settings.ROWS, settings.COLS, settings.MINES = 8, 8, 10
        settings.WIDTH, settings.HEIGHT = 320, 370
    elif args.difficulty == 'hard':
        settings.ROWS, settings.COLS, settings.MINES = 16, 16, 40
        settings.WIDTH, settings.HEIGHT = 640, 690
    else: # normal
        settings.ROWS, settings.COLS, settings.MINES = 10, 10, 10
        settings.WIDTH, settings.HEIGHT = 400, 450
        
    settings.CELL_SIZE = settings.WIDTH // settings.COLS
    settings.STATUS_BAR_HEIGHT = settings.HEIGHT - (settings.ROWS * settings.CELL_SIZE)

if __name__ == "__main__":
    args = parse_args()
    apply_settings(args)
    game = Game()
    game.run()