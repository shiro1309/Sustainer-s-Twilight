import pygame
import time

def draw_text(text, x, y, color, font, surf):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        surf.blit(text_surface, text_rect)

def draw_buttons(buttons, surf):
    for button in buttons:
        pygame.draw.rect(surf, (200, 200, 200), button.rect)
        draw_text(button.text, button.rect.centerx, button.rect.centery, button.color, button.font, surf)

def load_sprites(sprite_sheet_path, sprite_size, animation_names):
    sprite_sheets = {}
    sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()

    for i, name in enumerate(animation_names):
        sprites = []
        for x in range(sprite_sheet.get_width() // sprite_size[0]):
            print(x * sprite_size[0], i * sprite_size[1], sprite_size[0], sprite_size[1])
            sprite = pygame.Surface.subsurface(sprite_sheet, (x * sprite_size[0], i * sprite_size[1], sprite_size[0], sprite_size[1]))
            sprites.append(sprite)
        
        sprite_sheets[name] = sprites
    return sprite_sheets

class Animation:
    def __init__(self, sprite_dict, image_duration=1, loop=True):
        self.sprite_dict = sprite_dict
        self.image_duration = 1 / image_duration
        self.loop = loop
        self.current_animation = list(sprite_dict.keys())[0]  # Set the default animation to the first one
        self.frame = 0
        self.done = False
        self.animation_sum = 0
        self.animation_start = time.time()

    def update(self):
        #print(time.time() - self.animation_start, self.animation_sum + self.image_duration)
        if time.time() - self.animation_start >= self.animation_sum + self.image_duration:
            self.animation_sum += self.image_duration
            self.animate()

    def set_animation(self, animation_name):
        if animation_name in self.sprite_dict:
            self.current_animation = animation_name
            self.frame = 0
            self.done = False
            self.animation_start = time.time()

    def copy(self):
        return Animation(self.sprite_dict, self.image_duration, self.loop)

    def animate(self):
        if self.loop:
            self.frame = (self.frame + 1) % (len(self.sprite_dict[self.current_animation]))
        else:
            self.frame = min(self.frame + 1, len(self.sprite_dict[self.current_animation]) - 1)
            if self.frame == len(self.sprite_dict[self.current_animation]) - 1:
                self.done = True

    def img(self):
        return self.sprite_dict[self.current_animation][self.frame]

class Button:
    def __init__(self, text, rect, action, color):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.action = action
        self.color = color
        self.font = pygame.font.Font(None, 36)

