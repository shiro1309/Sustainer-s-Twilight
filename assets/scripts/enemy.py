# enemy.py
import pygame
from settings import WHITE, FPS
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))  # Red color for the enemy
        self.rect = self.image.get_frect()
        self.rect.center = (x, y)
        self.speed = 2
        self.player = player

    def update(self, delta):
        # Simple AI: Move towards the player in a straight line
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery

        # Normalize the direction vector (make its length 1)
        magnitude = (dx**2 + dy**2)**0.5
        normalized_direction = (dx / magnitude, dy / magnitude)

        # Define the enemy's speed
        enemy_speed = 100

        # Move the enemy towards the player using the normalized direction
        self.rect.x += normalized_direction[0] * enemy_speed * delta
        self.rect.y += normalized_direction[1] * enemy_speed * delta
        print(normalized_direction[0] * enemy_speed * delta, normalized_direction[1] * enemy_speed * delta, self.rect.x, self.rect.y)
