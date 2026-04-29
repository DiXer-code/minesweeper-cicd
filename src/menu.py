"""Difficulty selection menu for Minesweeper."""
import pygame

from .scores import get_best_time

DIFFICULTIES = [
    ("Easy", "easy", "8x8 | 10 mines"),
    ("Normal", "normal", "10x10 | 10 mines"),
    ("Medium", "medium", "12x12 | 20 mines"),
    ("Hard", "hard", "16x16 | 40 mines"),
]

MENU_W, MENU_H = 420, 520
BUTTON_W, BUTTON_H = 300, 68
GAP = 14

BG = (24, 26, 36)
CARD_IDLE = (40, 44, 62)
CARD_HOVER = (58, 90, 168)
CARD_BORDER = (70, 80, 120)
TEXT_WHITE = (235, 235, 245)
TEXT_SUB = (150, 155, 180)
TEXT_RECORD = (90, 200, 120)
ACCENT_GOLD = (255, 200, 60)


class Menu:
    """Render the start menu and return the selected action."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font_title = pygame.font.SysFont(None, 54)
        self.font_sub = pygame.font.SysFont(None, 26)
        self.font_btn = pygame.font.SysFont(None, 38)
        self.font_desc = pygame.font.SysFont(None, 24)
        self.hovered = -1
        self.leaderboard_btn_hovered = False
        self.buttons: list[pygame.Rect] = []
        self.leaderboard_rect: pygame.Rect | None = None
        self._build_layout()

    def _build_layout(self) -> None:
        total_height = len(DIFFICULTIES) * (BUTTON_H + GAP) - GAP
        start_y = (MENU_H - total_height) // 2 + 24
        self.buttons = []

        for index in range(len(DIFFICULTIES)):
            x = (MENU_W - BUTTON_W) // 2
            y = start_y + index * (BUTTON_H + GAP)
            self.buttons.append(pygame.Rect(x, y, BUTTON_W, BUTTON_H))

        self.leaderboard_rect = pygame.Rect((MENU_W - 200) // 2, MENU_H - 78, 200, 46)

    def run(self) -> str:
        """Block until the player picks a difficulty or the leaderboard."""
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.hovered = next(
                (
                    index
                    for index, rect in enumerate(self.buttons)
                    if rect.collidepoint(mouse_x, mouse_y)
                ),
                -1,
            )
            self.leaderboard_btn_hovered = bool(
                self.leaderboard_rect and self.leaderboard_rect.collidepoint(mouse_x, mouse_y)
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for index, rect in enumerate(self.buttons):
                        if rect.collidepoint(event.pos):
                            return DIFFICULTIES[index][1]
                    if self.leaderboard_rect and self.leaderboard_rect.collidepoint(event.pos):
                        return "leaderboard"

            self._draw()

    def _draw(self) -> None:
        self.screen.fill(BG)

        title = self.font_title.render("Minesweeper", True, TEXT_WHITE)
        self.screen.blit(title, title.get_rect(center=(MENU_W // 2, 52)))

        subtitle = self.font_sub.render("Choose a difficulty", True, TEXT_SUB)
        self.screen.blit(subtitle, subtitle.get_rect(center=(MENU_W // 2, 90)))

        for index, (label, key, description) in enumerate(DIFFICULTIES):
            rect = self.buttons[index]
            hovered = index == self.hovered
            background = CARD_HOVER if hovered else CARD_IDLE

            pygame.draw.rect(self.screen, background, rect, border_radius=12)
            pygame.draw.rect(self.screen, CARD_BORDER, rect, width=1, border_radius=12)

            label_surface = self.font_btn.render(label, True, TEXT_WHITE)
            self.screen.blit(
                label_surface,
                label_surface.get_rect(midleft=(rect.x + 22, rect.centery - 10)),
            )

            description_surface = self.font_desc.render(description, True, TEXT_SUB)
            self.screen.blit(
                description_surface,
                description_surface.get_rect(midleft=(rect.x + 22, rect.centery + 14)),
            )

            best_time = get_best_time(key)
            if best_time is not None:
                badge_text = f"Best {best_time}s"
                badge_surface = self.font_desc.render(
                    badge_text,
                    True,
                    ACCENT_GOLD if hovered else TEXT_RECORD,
                )
                self.screen.blit(
                    badge_surface,
                    badge_surface.get_rect(midright=(rect.right - 18, rect.centery)),
                )

        if self.leaderboard_rect is not None:
            background = CARD_HOVER if self.leaderboard_btn_hovered else CARD_IDLE
            pygame.draw.rect(
                self.screen,
                background,
                self.leaderboard_rect,
                border_radius=10,
            )
            pygame.draw.rect(
                self.screen,
                CARD_BORDER,
                self.leaderboard_rect,
                width=1,
                border_radius=10,
            )
            leaderboard_surface = self.font_desc.render(
                "View leaderboard",
                True,
                TEXT_WHITE if self.leaderboard_btn_hovered else TEXT_SUB,
            )
            self.screen.blit(
                leaderboard_surface,
                leaderboard_surface.get_rect(center=self.leaderboard_rect.center),
            )

        hint = self.font_desc.render("R - restart | M - menu", True, TEXT_SUB)
        self.screen.blit(hint, hint.get_rect(center=(MENU_W // 2, MENU_H - 18)))

        pygame.display.flip()
