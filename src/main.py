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

if __name__ == "__main__":
    game = Game()
    game.run()
