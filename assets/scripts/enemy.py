# enemy.py
import pygame
import math

from assets.scripts.settings import WHITE, FPS
from assets.scripts.utils import load_sprites, Animation

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player, sprite_sheet_path, size, animation_names):
        self.sprite_dict = load_sprites(sprite_sheet_path, size, animation_names)
        super().__init__()
        self.animation = Animation(self.sprite_dict, 8)
        self.image = self.animation.img()
        self.rect = self.image.get_frect()
        print(self.rect.size)
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

        # Move the enemy towards the player using the normalized direction
        self.rect.x += normalized_direction[0] * self.speed * delta * FPS
        self.rect.y += normalized_direction[1] * self.speed * delta * FPS
    
    def calculate_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), self.rect)
        #self.animation.update()
        #self.image = self.animation.img()
        #screen.blit(self.image, (self.rect.x, self.rect.y))

