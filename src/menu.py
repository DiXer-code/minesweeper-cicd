"""
Difficulty selection menu screen for Minesweeper.
Draws a simple but clean UI with four difficulty buttons and a best-time hint.
"""
import pygame
from . import settings
from .scores import get_best_time

DIFFICULTIES = [
    ("Easy",   "easy",   "8×8  •  10 мін"),
    ("Normal", "normal", "10×10  •  10 мін"),
    ("Medium", "medium", "12×12  •  20 мін"),
    ("Hard",   "hard",   "16×16  •  40 мін"),
]

# Layout
MENU_W, MENU_H = 420, 520
BUTTON_W, BUTTON_H = 300, 68
GAP = 14

# Colour palette
BG          = (24, 26, 36)
CARD_IDLE   = (40, 44, 62)
CARD_HOVER  = (58, 90, 168)
CARD_BORDER = (70, 80, 120)
TEXT_WHITE  = (235, 235, 245)
TEXT_SUB    = (150, 155, 180)
TEXT_RECORD = (90, 200, 120)
ACCENT_GOLD = (255, 200, 60)


class Menu:
    """Renders the difficulty selection screen and returns the chosen difficulty key."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font_title  = pygame.font.SysFont(None, 54)
        self.font_sub    = pygame.font.SysFont(None, 26)
        self.font_btn    = pygame.font.SysFont(None, 38)
        self.font_desc   = pygame.font.SysFont(None, 24)
        self.hovered: int = -1
        self.buttons: list[pygame.Rect] = []
        self._build_layout()

    def _build_layout(self) -> None:
        total_h = len(DIFFICULTIES) * (BUTTON_H + GAP) - GAP
        start_y = (MENU_H - total_h) // 2 + 40
        for i in range(len(DIFFICULTIES)):
            x = (MENU_W - BUTTON_W) // 2
            y = start_y + i * (BUTTON_H + GAP)
            self.buttons.append(pygame.Rect(x, y, BUTTON_W, BUTTON_H))

    def run(self) -> str:
        """Block until the player picks a difficulty. Returns the difficulty key."""
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            mx, my = pygame.mouse.get_pos()
            self.hovered = next(
                (i for i, r in enumerate(self.buttons) if r.collidepoint(mx, my)),
                -1
            )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(self.buttons):
                        if rect.collidepoint(event.pos):
                            return DIFFICULTIES[i][1]
            self._draw()

    def _draw(self) -> None:
        self.screen.fill(BG)
        w = MENU_W

        # ── Title ─────────────────────────────────────────────
        title = self.font_title.render("💣  Minesweeper", True, TEXT_WHITE)
        self.screen.blit(title, title.get_rect(center=(w // 2, 52)))

        subtitle = self.font_sub.render("Оберіть рівень складності", True, TEXT_SUB)
        self.screen.blit(subtitle, subtitle.get_rect(center=(w // 2, 90)))

        # ── Buttons ───────────────────────────────────────────
        for i, (label, key, desc) in enumerate(DIFFICULTIES):
            rect = self.buttons[i]
            hovered = (i == self.hovered)

            # Card background
            bg_color = CARD_HOVER if hovered else CARD_IDLE
            pygame.draw.rect(self.screen, bg_color, rect, border_radius=12)
            pygame.draw.rect(self.screen, CARD_BORDER, rect, width=1, border_radius=12)

            # Difficulty label
            lbl = self.font_btn.render(label, True, TEXT_WHITE)
            self.screen.blit(lbl, lbl.get_rect(midleft=(rect.x + 22, rect.centery - 10)))

            # Grid / mines description
            dsf = self.font_desc.render(desc, True, TEXT_SUB)
            self.screen.blit(dsf, dsf.get_rect(midleft=(rect.x + 22, rect.centery + 14)))

            # Best time badge
            best = get_best_time(key)
            if best is not None:
                badge_text = f"⭐ {best}с"
                badge = self.font_desc.render(badge_text, True,
                                              ACCENT_GOLD if hovered else TEXT_RECORD)
                self.screen.blit(badge, badge.get_rect(midright=(rect.right - 18, rect.centery)))

        # ── Footer hint ───────────────────────────────────────
        hint = self.font_desc.render("R – рестарт гри   |   M – повернутись до меню", True, TEXT_SUB)
        self.screen.blit(hint, hint.get_rect(center=(w // 2, MENU_H - 22)))

        pygame.display.flip()
