import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (40, 40, 40)
CIRCLE_COLOR = (0, 255, 0)
OVERLAP_COLOR = (255, 0, 0)
CIRCLE_RADIUS = 50

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create the stationary circle
stationary_surface = pygame.Surface((5*2, 5*2), pygame.SRCALPHA)
pygame.draw.circle(stationary_surface, CIRCLE_COLOR, (5, 5), 5)
stationary_mask = pygame.mask.from_surface(stationary_surface)
stationary_rect = stationary_surface.get_rect(center=(WIDTH//2, HEIGHT//2))

# Game loop
running = True
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Create the moving circle
    moving_surface = pygame.Surface((CIRCLE_RADIUS*2, CIRCLE_RADIUS*2), pygame.SRCALPHA)
    pygame.draw.circle(moving_surface, CIRCLE_COLOR, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
    moving_mask = pygame.mask.from_surface(moving_surface)
    moving_rect = moving_surface.get_rect(center=pygame.mouse.get_pos())

    # Check for overlap
    offset_x = stationary_rect.x - moving_rect.x
    offset_y = stationary_rect.y - moving_rect.y
    print(moving_mask, stationary_mask)
    overlap = moving_mask.overlap(stationary_mask, (offset_x, offset_y))
    print(offset_x, offset_y)

    # Change the color of the moving circle if it overlaps with the stationary circle
    if overlap:
        pygame.draw.circle(moving_surface, OVERLAP_COLOR, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)

    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    screen.blit(stationary_surface, stationary_rect)
    screen.blit(moving_surface, moving_rect)

    # Flip the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()