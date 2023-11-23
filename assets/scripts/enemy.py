# enemy.py
import pygame
from settings import WHITE, FPS

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))  # Red color for the enemy
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
        self.player = player

    def update(self, delta):
        # Simple AI: Move towards the player in a straight line
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = pygame.math.Vector2(dx, dy).length()
        
        if distance > 0:
            self.rect.x += (dx / distance) * self.speed * delta * FPS
            self.rect.y += (dy / distance) * self.speed * delta * FPS
