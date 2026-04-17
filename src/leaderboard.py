"""
Leaderboard screen for viewing top scores per difficulty.
"""
import pygame
from . import settings
from .scores import get_leaderboard

DIFFICULTIES = [
    ("Easy",   "easy"),
    ("Normal", "normal"),
    ("Medium", "medium"),
    ("Hard",   "hard"),
]

# Colour palette
BG          = (24, 26, 36)
CARD_IDLE   = (40, 44, 62)
CARD_HOVER  = (58, 90, 168)
CARD_BORDER = (70, 80, 120)
TEXT_WHITE  = (235, 235, 245)
TEXT_SUB    = (150, 155, 180)
TEXT_GOLD   = (255, 200, 60)
MEDAL_GOLD  = (255, 215, 0)
MEDAL_SILVER = (192, 192, 192)
MEDAL_BRONZE = (205, 127, 50)


class Leaderboard:
    """Displays top scores for each difficulty."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font_title = pygame.font.SysFont(None, 48)
        self.font_difficulty = pygame.font.SysFont(None, 32)
        self.font_entry = pygame.font.SysFont(None, 24)
        self.font_small = pygame.font.SysFont(None, 20)
        self.selected_difficulty = 0
        self.buttons = []
        self._build_layout()

    def _build_layout(self) -> None:
        """Build tab buttons at the top."""
        tab_w = 90
        gap = 8
        total_w = len(DIFFICULTIES) * (tab_w + gap)
        start_x = (settings.WIDTH - total_w) // 2
        
        self.buttons = []
        for i in range(len(DIFFICULTIES)):
            x = start_x + i * (tab_w + gap)
            rect = pygame.Rect(x, 20, tab_w, 40)
            self.buttons.append(rect)

    def run(self) -> str:
        """Block until user goes back. Returns 'menu'."""
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            
            mx, my = pygame.mouse.get_pos()
            hovered = next(
                (i for i, r in enumerate(self.buttons) if r.collidepoint(mx, my)),
                -1
            )
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
                        return "menu"
                        
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if hovered >= 0:
                        self.selected_difficulty = hovered
                    elif my > 400:  # Back button area
                        return "menu"
            
            self._draw()

    def _draw(self) -> None:
        """Draw the leaderboard screen."""
        self.screen.fill(BG)
        
        # Title
        title = self.font_title.render("🏆 ТАБЛИЦЯ ЛІДЕРІВ", True, TEXT_GOLD)
        self.screen.blit(title, title.get_rect(center=(settings.WIDTH // 2, 10)))
        
        # Difficulty tabs
        self._draw_tabs()
        
        # Scores for selected difficulty
        self._draw_scores()
        
        # Back button hint
        hint = self.font_small.render("ESC або M — назад", True, TEXT_SUB)
        self.screen.blit(hint, hint.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT - 20)))
        
        pygame.display.flip()

    def _draw_tabs(self) -> None:
        """Draw difficulty tabs."""
        for i, (label, key) in enumerate(DIFFICULTIES):
            rect = self.buttons[i]
            is_selected = (i == self.selected_difficulty)
            
            color = CARD_HOVER if is_selected else CARD_IDLE
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            pygame.draw.rect(self.screen, CARD_BORDER, rect, width=2 if is_selected else 1, border_radius=8)
            
            text = self.font_entry.render(label, True, TEXT_WHITE)
            self.screen.blit(text, text.get_rect(center=rect.center))

    def _draw_scores(self) -> None:
        """Draw leaderboard entries for selected difficulty."""
        diff_key = DIFFICULTIES[self.selected_difficulty][1]
        leaderboard = get_leaderboard(diff_key)
        
        if not leaderboard:
            empty = self.font_entry.render("Немає записів", True, TEXT_SUB)
            self.screen.blit(empty, empty.get_rect(center=(settings.WIDTH // 2, 200)))
            return
        
        medals = ["🥇", "🥈", "🥉"]
        start_y = 90
        line_height = 40
        
        for pos, entry in enumerate(leaderboard[:5]):
            y = start_y + pos * line_height
            
            # Medal or position number
            if pos < 3:
                medal_text = self.font_entry.render(medals[pos], True, TEXT_WHITE)
            else:
                medal_text = self.font_entry.render(f"#{pos + 1}", True, TEXT_SUB)
            self.screen.blit(medal_text, (40, y))
            
            # Player name
            name = entry.get("name", "Невідомо")[:15]
            name_text = self.font_entry.render(name, True, TEXT_WHITE)
            self.screen.blit(name_text, (100, y))
            
            # Time
            time_str = f"{entry['time']}s"
            time_text = self.font_entry.render(time_str, True, TEXT_GOLD)
            self.screen.blit(time_text, (settings.WIDTH - 100, y))
