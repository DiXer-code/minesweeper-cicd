"""
Name input dialog for saving player scores.
"""
import pygame

# Colour palette
BG          = (24, 26, 36)
DIALOG_BG   = (40, 44, 62)
DIALOG_BORDER = (70, 80, 120)
TEXT_WHITE  = (235, 235, 245)
TEXT_SUB    = (150, 155, 180)
TEXT_GOLD   = (255, 200, 60)


class NameInputDialog:
    """Dialog for entering player name after winning."""

    def __init__(self, screen: pygame.Surface, time_elapsed: int, difficulty: str) -> None:
        self.screen = screen
        self.time_elapsed = time_elapsed
        self.difficulty = difficulty
        self.player_name = ""
        self.max_name_length = 20
        self.font_title = pygame.font.SysFont(None, 48)
        self.font_text = pygame.font.SysFont(None, 32)
        self.font_small = pygame.font.SysFont(None, 24)

    def run(self) -> str:
        """Block until player enters name and confirms. Returns the name."""
        clock = pygame.time.Clock()
        
        while True:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Confirm name
                        return self.player_name.strip() or "Невідомо"
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif event.unicode.isprintable() and len(self.player_name) < self.max_name_length:
                        self.player_name += event.unicode
            
            self._draw()

    def _draw(self) -> None:
        """Draw name input dialog."""
        self.screen.fill(BG)
        
        # Overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Dialog box
        dialog_rect = pygame.Rect(80, 120, 240, 200)
        pygame.draw.rect(self.screen, DIALOG_BG, dialog_rect, border_radius=15)
        pygame.draw.rect(self.screen, DIALOG_BORDER, dialog_rect, width=2, border_radius=15)
        
        # Title
        title = self.font_title.render("🎉 Вітаємо!", True, TEXT_GOLD)
        self.screen.blit(title, title.get_rect(center=(self.screen.get_width() // 2, 140)))
        
        # Time display
        time_text = self.font_text.render(f"Час: {self.time_elapsed}с", True, TEXT_WHITE)
        self.screen.blit(time_text, time_text.get_rect(center=(self.screen.get_width() // 2, 190)))
        
        # Name input label
        label = self.font_small.render("Ваше ім'я:", True, TEXT_SUB)
        self.screen.blit(label, (100, 240))
        
        # Input field
        input_rect = pygame.Rect(100, 270, 200, 40)
        pygame.draw.rect(self.screen, TEXT_WHITE, input_rect, border_radius=5)
        pygame.draw.rect(self.screen, DIALOG_BORDER, input_rect, width=2, border_radius=5)
        
        # Input text with blinking cursor
        input_text = self.font_text.render(self.player_name + "|", True, (0, 0, 0))
        self.screen.blit(input_text, (110, 278))
        
        # Instructions
        instruction = self.font_small.render("Enter — готово", True, TEXT_SUB)
        self.screen.blit(instruction, instruction.get_rect(center=(self.screen.get_width() // 2, 350)))
        
        pygame.display.flip()
