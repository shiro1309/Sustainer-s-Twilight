# HealthBar.py
import pygame
from assets.scripts.utils import translate

class VariabelBar:
    def __init__(self, x, y, width, height, max_value, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_value = max_value
        self.color = color

    def update(self):
        pass
    
    def draw(self):
        pass

class HealthBar(VariabelBar):
    def __init__(self, x, y, width, height, health):
        super().__init__(x, y, width, height, health, (255,0,0))
        self.health = health

    def update(self, damage):
        self.health -= damage

    def draw(self, screen):
        # Outer rectangle (background)
        outer_rect = pygame.Rect(self.x - 1, self.y - 1, self.width + 2, self.height + 2)
        pygame.draw.rect(screen, (0,0,0), outer_rect)

        # Inner rectangle (health bar)
        #inner_rect_width = self.h
        inner_rect = pygame.Rect(self.x, self.y, self.health, self.height)
        pygame.draw.rect(screen, (0,255,0), inner_rect)
        
class ProgressBar(VariabelBar):
    def __init__(self, x, y, width, height, value):
        super().__init__(x, y, width, height, value, (0,0,255))
        self.value = 0
        self.level = 0
        
    def update(self, value):
        self.value += value
        if self.value >= int(0.002*self.level**2 + 2*self.level + 30):
            self.max_value = 0.002*self.level**2 + 2*self.level + 30
            self.value = 0
            self.level += 1
        return 0
        
    def draw(self, screen):
        outer_rect = pygame.Rect(self.x - 1, self.y - 1, self.width + 2, self.height + 2)
        pygame.draw.rect(screen, (0,0,0), outer_rect)

        # Inner rectangle (health bar)
        #inner_rect_width = self.h
        inner_rect = pygame.Rect(self.x, self.y, translate(self.value, 0, self.max_value, 0, self.width), self.height)
        pygame.draw.rect(screen, (0,255,0), inner_rect)