# main.py
import pygame
from assets.scripts.utils import load_sprites
pygame.init()
screen = pygame.display.set_mode((200,200))

# Load sprites from a sprite sheet with individual sprite size (32x32)
# For this example, assume "walk" and "jump" are the animation names
player_animations = load_sprites("assets/Sprite-0001.png", (16, 16), animation_names=["walk", "jump"])
print(player_animations)
# Access sprites for the "walk" animation
walk_animation_sprites = player_animations["walk"]

# Access sprites for the "jump" animation
jump_animation_sprites = player_animations["jump"]

print(walk_animation_sprites, jump_animation_sprites)

# Use the sprites in your game
