# game_over_screen.py
import pygame
from settings import WIDTH, HEIGHT, WHITE
from assets.scripts.utils import Button

class GameOverScreen:
    def __init__(self, score):
        self.end_time = 0
        self.score = score
    def handle_events(self, actions):
        for action in actions:
            if action == "return_to_menu":
                return True
        return False

    def draw(self, game_screen, button):
        game_screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        self.end_time = pygame.time.get_ticks()
        text = font.render(f"Game Over - Score: {int(round(self.score, 0))} seconds", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        game_screen.blit(text, text_rect)

        pygame.draw.rect(game_screen, (200, 200, 200), button.rect)
        self.draw_text(button.text, button.rect.centerx, button.rect.centery, game_screen)

        pygame.display.flip()

    def draw_text(self, text, x, y, game_screen):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x, y))
        game_screen.blit(text_surface, text_rect)
