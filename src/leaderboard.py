"""Leaderboard screen for viewing top scores by difficulty."""
import pygame

from .scores import get_leaderboard

DIFFICULTIES = [
    ("Easy", "easy"),
    ("Normal", "normal"),
    ("Medium", "medium"),
    ("Hard", "hard"),
]

BG = (24, 26, 36)
CARD_IDLE = (40, 44, 62)
CARD_HOVER = (58, 90, 168)
CARD_BORDER = (70, 80, 120)
TEXT_WHITE = (235, 235, 245)
TEXT_SUB = (150, 155, 180)
TEXT_GOLD = (255, 200, 60)


class Leaderboard:
    """Display saved scores and allow switching difficulty tabs."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font_title = pygame.font.SysFont(None, 48)
        self.font_entry = pygame.font.SysFont(None, 24)
        self.font_small = pygame.font.SysFont(None, 20)
        self.selected_difficulty = 0
        self.buttons: list[pygame.Rect] = []
        self._build_layout()

    def _build_layout(self) -> None:
        """Build tab buttons using the current screen width."""
        tab_width = 90
        gap = 8
        total_width = len(DIFFICULTIES) * tab_width + (len(DIFFICULTIES) - 1) * gap
        start_x = (self.screen.get_width() - total_width) // 2

        self.buttons = []
        for index in range(len(DIFFICULTIES)):
            x = start_x + index * (tab_width + gap)
            self.buttons.append(pygame.Rect(x, 72, tab_width, 40))

    def run(self) -> str:
        """Block until the user returns to the main menu."""
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            hovered = next(
                (
                    index
                    for index, rect in enumerate(self.buttons)
                    if rect.collidepoint(mouse_x, mouse_y)
                ),
                -1,
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_m):
                    return "menu"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if hovered >= 0:
                        self.selected_difficulty = hovered
                    elif mouse_y >= self.screen.get_height() - 50:
                        return "menu"

            self._draw()

    def _draw(self) -> None:
        self.screen.fill(BG)

        title = self.font_title.render("Leaderboard", True, TEXT_GOLD)
        self.screen.blit(title, title.get_rect(center=(self.screen.get_width() // 2, 34)))

        self._draw_tabs()
        self._draw_scores()

        hint = self.font_small.render("ESC or M - back", True, TEXT_SUB)
        self.screen.blit(
            hint,
            hint.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 20)),
        )

        pygame.display.flip()

    def _draw_tabs(self) -> None:
        for index, (label, _difficulty_key) in enumerate(DIFFICULTIES):
            rect = self.buttons[index]
            is_selected = index == self.selected_difficulty
            background = CARD_HOVER if is_selected else CARD_IDLE

            pygame.draw.rect(self.screen, background, rect, border_radius=8)
            pygame.draw.rect(
                self.screen,
                CARD_BORDER,
                rect,
                width=2 if is_selected else 1,
                border_radius=8,
            )

            text = self.font_entry.render(label, True, TEXT_WHITE)
            self.screen.blit(text, text.get_rect(center=rect.center))

    def _draw_scores(self) -> None:
        difficulty_key = DIFFICULTIES[self.selected_difficulty][1]
        leaderboard = get_leaderboard(difficulty_key)

        if not leaderboard:
            empty_state = self.font_entry.render("No scores yet", True, TEXT_SUB)
            self.screen.blit(
                empty_state,
                empty_state.get_rect(center=(self.screen.get_width() // 2, 220)),
            )
            return

        medals = ["#1", "#2", "#3"]
        start_y = 150
        line_height = 40
        time_x = self.screen.get_width() - 110

        for position, entry in enumerate(leaderboard[:5]):
            y = start_y + position * line_height
            rank_label = medals[position] if position < 3 else f"#{position + 1}"
            rank_surface = self.font_entry.render(rank_label, True, TEXT_WHITE)
            name_surface = self.font_entry.render(entry.get("name", "Unknown")[:15], True, TEXT_WHITE)
            time_surface = self.font_entry.render(f"{entry['time']}s", True, TEXT_GOLD)

            self.screen.blit(rank_surface, (42, y))
            self.screen.blit(name_surface, (108, y))
            self.screen.blit(time_surface, (time_x, y))
