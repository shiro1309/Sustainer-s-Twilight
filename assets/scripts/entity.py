# entity.py
import pygame

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


class Player(Entity):
    def __init__(self, x, y, sprite_sheet_path, size, animation_names):
        super().__init__(50, 50, (255, 255, 255), x, y)
        self.sprite_dict = load_sprites(sprite_sheet_path, size, animation_names)
        self.animation = Animation(self.sprite_dict, 8)
        self.image = self.animation.img()
        self.animation.set_animation("walk")
        self.speed = 5

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed * delta_time * FPS
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed * delta_time * FPS
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed * delta_time * FPS
        if keys[pygame.K_DOWN] and self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += self.speed * delta_time * FPS

    def draw(self, screen):
        self.animation.update()
        self.image = self.animation.img()
        screen.blit(self.image, (self.rect.x, self.rect.y))