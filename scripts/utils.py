import pygame

def draw_text(text, x, y, color, font, surf):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        surf.blit(text_surface, text_rect)

def draw_buttons(buttons, surf):
    for button in buttons:
        pygame.draw.rect(surf, (200, 200, 200), button.rect)
        draw_text(button.text, button.rect.centerx, button.rect.centery, button.color, button.font, surf)

class Button:
    def __init__(self, text, rect, action, color):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.action = action
        self.color = color
        self.font = pygame.font.Font(None, 36)