# Проєктування гри

## Діаграма діяльності

```mermaid
flowchart TD
    A[Старт гри] --> B[Ініціалізація вікна і поля]
    B --> C[Очікування дії гравця]
    C --> D{Тип дії}
    D -->|Лівий клік| E[Відкрити клітинку]
    D -->|Правий клік| F[Перемкнути прапорець]
    D -->|R| G[Перезапустити гру]
    E --> H{Міна?}
    H -->|Так| I[Показати всі міни]
    I --> J[Поразка]
    H -->|Ні| K{Порожня клітинка?}
    K -->|Так| L[Рекурсивно відкрити сусідів]
    K -->|Ні| M[Показати число]
    L --> N{Усі безпечні клітинки відкриті?}
    M --> N
    F --> C
    G --> B
    N -->|Так| O[Перемога]
    N -->|Ні| C
```

## Діаграма класів

```mermaid
classDiagram
    class Cell {
        +int row
        +int col
        +bool is_mine
        +bool is_revealed
        +bool is_flagged
        +int neighbor_mines
    }

    class Board {
        +list grid
        +bool initialized
        +initialize(first_row, first_col)
        +place_mines(excluded_row, excluded_col)
        +calculate_numbers()
        +count_neighbor_mines(row, col)
        +reveal_cell(row, col)
        +toggle_flag(row, col)
        +reveal_all_mines()
        +check_win()
        +count_flags()
    }

    class Game {
        +screen
        +clock
        +font
        +board
        +running
        +game_over
        +win
        +draw()
        +draw_status()
        +reset()
        +handle_left_click(pos)
        +handle_right_click(pos)
        +run()
    }

    Board --> Cell : contains
    Game --> Board : manages
```

## Короткі проєктні рішення

- `Cell` зберігає лише стан однієї клітинки.
- `Board` відповідає за всю ігрову логіку та перевірки.
- `Game` відповідає за `pygame`, події та відображення.
- Ініціалізація мін відкладена до першого ходу, щоб перший клік був безпечним.

