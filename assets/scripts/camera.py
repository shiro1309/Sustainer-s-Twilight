import pygame

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        x = max(-(self.width), x)  # right
        y = min(0, y)  # top
        y = max(-(self.height), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)