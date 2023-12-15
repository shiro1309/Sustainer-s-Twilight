# HealthBar.py
import pygame

class HealthBar:
    def __init__(self, x, y, width, height, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = health
        self.health = health

    def update(self, damage):
        self.health -= damage

    def draw(self, surface):
        # Outer rectangle (background)
        outer_rect = pygame.Rect(self.x - 1, self.y - 1, self.width + 2, self.height + 2)
        pygame.draw.rect(surface, (0,0,0), outer_rect)

        # Inner rectangle (health bar)
        #inner_rect_width = self.h
        inner_rect = pygame.Rect(self.x, self.y, self.health, self.height)
        pygame.draw.rect(surface, (0,255,0), inner_rect)