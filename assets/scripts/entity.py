# entity.py
import pygame
import math

from assets.scripts.utils import load_sprites, Animation
from assets.scripts.settings import * 
from assets.scripts.healthbar import HealthBar

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
        self.attack_state = "cooldown"
        self.speed = 5
        self.health_bar = HealthBar(10, 10, 100, 20, 100)
        self.last_attack_time = 0
        self.attack_start_time = 0
        self.attacking = False
        self.attack_range = 0
        self.current_time = 0.0
        self.attack_color = (255,0,0,128)
        self.stationary_surface = pygame.Surface((5*2, 5*2), pygame.SRCALPHA)
        pygame.draw.circle(self.stationary_surface, (0,255,0), (5, 5), 5)
        self.stationary_mask = pygame.mask.from_surface(self.stationary_surface)
        self.stationary_rect = self.stationary_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.collected_pieces = []
        self.max_attack_range = 25

    def update(self, delta_time, enemy_group, local_scroll=[0,0], global_scroll=[0,0], apply_scroll=False):
        keys = pygame.key.get_pressed()
        self.attack(enemy_group, 25, 20, delta_time, global_scroll)

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
            return local_scroll

        # Normalize the movement vector
        normalized_dx = dx / magnitude
        normalized_dy = dy / magnitude

        # Move the player with equal speed in both directions
        if apply_scroll:
            local_scroll[0] = -(normalized_dx * self.speed * delta_time * FPS)
            local_scroll[1] = -(normalized_dy * self.speed * delta_time * FPS)
        else:
            self.rect.x += normalized_dx * self.speed * delta_time * FPS
            self.rect.y += normalized_dy * self.speed * delta_time * FPS
        return local_scroll


    def take_damage(self, damage):
        self.health_bar.update(damage)

    def attack(self, enemies, attack_damage, knockback_distance, delta_time, global_scroll=(0,0)):
        
        self.current_time += delta_time * 1000
        
        self.barrier_attack()
        
        self.attack_surface = pygame.Surface((int(self.attack_range * 2), int(self.attack_range * 2)), pygame.SRCALPHA)
        #self.attack_rect = pygame.FRect(self.rect.x - self.attack_range, self.rect.y - self.attack_range, self.rect.width + 2 * self.attack_range, self.rect.height + 2 * self.attack_range)
        self.attack_color = (255,0,0,128)
        pygame.draw.circle(self.attack_surface, self.attack_color, (int(self.attack_range), int(self.attack_range)), int(self.attack_range))
        attack_mask = pygame.mask.from_surface(self.attack_surface)
        self.attack_rect = self.attack_surface.get_rect(center=self.rect.center)
        
        self.attacking = True
        # Check for collisions with enemies
        for enemy in enemies:
            if self.attack_rect.colliderect(enemy.rect):
                enemy.update_mask()
                offset_x = enemy.rect.x - self.attack_rect.x
                offset_y = enemy.rect.y - self.attack_rect.y
                
                self.attack_color = (255,0,0,128)
                
                if attack_mask.overlap(enemy.mask, (int(offset_x), int(offset_y))):
                    
                    dx = enemy.rect.centerx - self.rect.centerx
                    dy = enemy.rect.centery - self.rect.centery
                    magnitude = (dx**2 + dy**2)**0.5
                    if magnitude != 0:
                        knockback_direction = (dx / magnitude, dy / magnitude)
                    else:
                        knockback_direction = (0, 0)

                    # Apply damage and knockback to enemy
                    enemy.take_damage(attack_damage, knockback_direction, knockback_distance)

    def barrier_attack(self):
        time_since_attack_start = self.current_time - self.attack_start_time
        #print(max_attack_range * (time_since_attack_start / 3000))

        if self.attack_state == 'growing':
            if time_since_attack_start > 3000: # 3 seconds
                self.attack_state = 'full size'
                self.attack_start_time = self.current_time
            else:
                self.attack_range = self.max_attack_range * (time_since_attack_start / 3000)

        elif self.attack_state == 'full size':
            if time_since_attack_start > 2000: # 2 seconds
                self.attack_state = 'shrinking'
                self.attack_start_time = self.current_time
            else:
                self.attack_range = self.max_attack_range

        elif self.attack_state == 'shrinking':
            if time_since_attack_start > 2000: # 2 seconds
                self.attack_state = 'cooldown'
                self.attack_start_time = self.current_time
            else:
                self.attack_range = self.max_attack_range * (1 - (time_since_attack_start / 2000))

        elif self.attack_state == 'cooldown':
            if time_since_attack_start > 2000: # 2 seconds
                self.attack_state = 'growing'
                self.attack_start_time = self.current_time
                self.attacking = False
                return # don't attack during cooldown
            else:
                self.attacking = False
                return # don't attack during cooldown
    
    def collect_piece(self, piece):
        # Add the piece to the player's collected pieces
        self.collected_pieces.append(piece)

        # Apply the effect of the piece
        piece.apply_effect(self)
    
    def draw(self, screen):
        #pygame.draw.rect(screen, (0,0,0), self.rect)
        if self.attacking:
            #pygame.draw.rect(screen, (0,0,0,50), self.attack_rect)
            #pygame.draw.rect(screen, (0,0,0,50), self.attack_rect)
            screen.blit(self.attack_surface, self.attack_rect)
        self.animation.update()
        self.image = self.animation.img()
        screen.blit(self.image, (self.rect.x, self.rect.y))
        self.health_bar.draw(screen)