# entity.py
import pygame
import math

from assets.scripts.utils import load_sprites, Animation
from assets.scripts.settings import * 

class Entity(pygame.sprite.Sprite):
    def __init__(self, width, height, color, x, y):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_frect()
        self.rect.x = x
        self.rect.y = y
        

    def update(self):
        pass  # Add specific update logic in derived classes

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

class Player(Entity):
    def __init__(self, x, y, sprite_sheet_path, size, animation_names):
        super().__init__(size[0], size[1], (255, 255, 255), x, y)
        self.sprite_dict = load_sprites(sprite_sheet_path, size, animation_names)
        self.animation = Animation(self.sprite_dict, 8)
        self.image = self.animation.img()
        self.animation.set_animation("walk")
        self.speed = 5

    def update(self, delta_time):
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_LEFT] and self.rect.x > 0:
            dx -= 1
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            dx += 1
        if keys[pygame.K_UP] and self.rect.y > 0:
            dy -= 1
        if keys[pygame.K_DOWN] and self.rect.y < HEIGHT - self.rect.height:
            dy += 1

        # Calculate the length of the movement vector
        magnitude = (dx**2 + dy**2)**0.5

        # Avoid division by zero
        if magnitude == 0:
            return

        # Normalize the movement vector
        normalized_dx = dx / magnitude
        normalized_dy = dy / magnitude
        
        x = self.rect.x
        y = self.rect.y

        # Move the player with equal speed in both directions
        self.rect.x += normalized_dx * self.speed * delta_time * FPS
        self.rect.y += normalized_dy * self.speed * delta_time * FPS

        #print(num)

    def draw(self, screen):
        #pygame.draw.rect(screen, (0,0,0), self.rect)
        self.animation.update()
        self.image = self.animation.img()
        screen.blit(self.image, (self.rect.x, self.rect.y))