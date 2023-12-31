# enemy.py
import pygame
import math

from assets.scripts.settings import WHITE, FPS
from assets.scripts.utils import load_sprites, Animation
from assets.scripts.entity import Crystal

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player, sprite_sheet_path, size, animation_names):
        self.sprite_dict = load_sprites(sprite_sheet_path, size, animation_names)
        super().__init__()
        self.animation = Animation(self.sprite_dict, 8)
        self.image = self.animation.img()
        self.rect = self.image.get_frect()
        self.rect.center = (x, y)
        self.speed = 2
        self.player = player
        self.health = 100
        #self.lifespan = 4  # Lifespan in seconds
        self.spawn_time = pygame.time.get_ticks()
        self.damage = 5
        self.attack_timer = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta):
        # Simple AI: Move towards the player in a straight line
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery

        # Normalize the direction vector (make its length 1)
        magnitude = (dx**2 + dy**2)**0.5
        if magnitude != 0:
            normalized_direction = (dx / magnitude, dy / magnitude)

            # Move the enemy towards the player using the normalized direction
            self.rect.x += normalized_direction[0] * self.speed * delta * FPS
            self.rect.y += normalized_direction[1] * self.speed * delta * FPS
        #current_time = pygame.time.get_ticks()
        #elapsed_time = (current_time - self.spawn_time) / 1000  # Convert milliseconds to seconds

        #if elapsed_time >= self.lifespan:
        #    self.handle_death()
    
    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.image)

    def update_img(self):
        self.animation.update()

    def calculate_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def draw(self, screen, offset=(0,0)):
        #pygame.draw.rect(screen, (0,0,0), self.rect)
        self.update_img()
        self.image = self.animation.img()
        screen.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))

    def take_damage(self, damage, knockback_direction, knockback_distance, crystal_list):
        self.health -= damage
        self.rect.x += knockback_direction[0] * knockback_distance
        self.rect.y += knockback_direction[1] * knockback_distance
        
        if self.health <= 0:
            self.health = 0  # Ensure health doesn't go below zero
            crystal_list.add(Crystal(self.rect.x, self.rect.y))
            self.handle_death()
            return 

    def handle_death(self):
        # Code to handle enemy death (e.g., play death animation, remove from groups, etc.)
        self.kill()

