import pygame
import sys
from assets.scripts.utils import load_sprites, Animation  # Assuming you have your spritesheet loader function

# Initialize pygame
pygame.init()

# Set up window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animation Example")
clock = pygame.time.Clock()

# Load player sprites
player_sprites = load_sprites("assets\sprites\Sprite-0001.png", (16,16), ["walk", "jump"])
player_animation = Animation(player_sprites, image_duration=24, loop=True)

# Set initial position of player
player_x, player_y = WIDTH // 2, HEIGHT // 2
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the animation
    player_animation.update()
    clock.tick(60)

    # Clear the screen
    screen.fill((125,125,125))

    # Get the current frame of the animation
    current_frame = player_animation.img()

    # Draw the current frame to the screen at the player's position
    screen.blit(current_frame, (player_x, player_y))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
