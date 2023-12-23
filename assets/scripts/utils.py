import pygame
import time
import os
import json

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
            sprite = pygame.Surface.subsurface(sprite_sheet, (x * sprite_size[0], i * sprite_size[1], sprite_size[0], sprite_size[1]))
            sprites.append(sprite)
        
        sprite_sheets[name] = sprites
    return sprite_sheets

def load_file(path):
    with open(path, 'r') as file:
        return file.read()

def inside_render_box(rect, global_width, global_height, scroll=(0,0)):
    return (rect.x + rect.width + scroll[0] > 0 and rect.x + scroll[0] < global_width) and (rect.y + rect.height + scroll[1] > 0 and rect.y + scroll[1] < global_height)
    

def load_files(path):
    files = []
    for file in os.listdir(path):
        with open(file, 'r') as f:
            files.append(f.read())

def load_level(path):
    with open(path, 'r') as file:
        level_data = json.load(file)
    return level_data


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

    def ani_resume(self):
        self.animation_start = time.time()

    def img(self):
        return self.sprite_dict[self.current_animation][self.frame]

class Button:
    def __init__(self, text, rect, action, color):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.action = action
        self.color = color
        self.font = pygame.font.Font(None, 36)

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen, global_scroll=(0,0)):
        screen.blit(self.image, (self.rect.x + global_scroll[0], self.rect.y + global_scroll[1]))

class Chunk:
    def __init__(self, id, image, chunk_size, tile_size, x, y, spawn_enemy, can_walk, prerender=False):
        self.id = id
        self.x = x
        self.y = y
        self.id = "x:"+str(x//256)+", y:"+str(y//256)
        self.width = chunk_size * tile_size
        self.height = chunk_size * tile_size
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.tiles = pygame.sprite.Group()
        self.spawn_enemy = spawn_enemy
        self.can_walk = can_walk
        
        for i in range(chunk_size):
            for j in range(chunk_size):
                if prerender:
                    tile = Tile(image, i * tile_size, j * tile_size)
                else:
                    tile = Tile(image, x + i * tile_size, y + j * tile_size)
                self.tiles.add(tile)

        self.prerender = None
    
    def draw(self, screen, global_scroll=(0,0)):
        for tile in self.tiles:
            tile.draw(screen, global_scroll)

    def draw_prerender(self, screen, global_scroll=(0,0), resize=False):
        if self.prerender is None:
            # Create a new Surface for the pre-rendered image
            self.prerender = pygame.Surface((self.width, self.height))

            # Draw each tile onto the pre-rendered image
            for tile in self.tiles:
                #self.prerender.blit(tile.image, (tile.rect.x * 16, tile.rect.y * 16))
                tile.draw(self.prerender)

        # Draw the pre-rendered image onto the screen
        screen.blit(self.prerender, (self.x + global_scroll[0], self.y + global_scroll[1]))

class MetaChunk:
    def __init__(self, chunks):
        self.chunks = chunks
        
        self.prerender = None
        
        self.x = min(chunk.x for chunk in chunks)
        self.y = min(chunk.y for chunk in chunks)
        self.width = max(chunk.x + chunk.width for chunk in chunks) - self.x
        self.height = max(chunk.y + chunk.height for chunk in chunks) - self.y
    
    def draw(self, screen, global_scroll=(0,0)):
        for chunk in self.chunks:
            chunk.draw(screen, global_scroll)
            
    def draw_prerender(self, screen, global_scroll=(0,0)):
        if self.prerender is None:
            # Create a new Surface for the pre-rendered image
            self.prerender = pygame.Surface((self.width, self.height))

            # Draw each tile onto the pre-rendered image
            for chunk in self.chunks:
                #self.prerender.blit(tile.image, (tile.rect.x * 16, tile.rect.y * 16))
                chunk.draw_prerender(self.prerender)

        # Draw the pre-rendered image onto the screen
        screen.blit(self.prerender, (self.x + global_scroll[0], self.y + global_scroll[1]))
       
def resize_surface(surface, new_width, new_height):
    # Create a new surface with the desired size
        new_surface = pygame.Surface((new_width, new_height))

        # Scale the pre-rendered surface to the new size
        scaled_surface = pygame.transform.scale(surface, (new_width, new_height))

        # Replace the old surface with the new one
        surface = scaled_surface

        return surface
    
def scale_surface_to_height(surface, new_height):
    # Get the current size of the surface
    width, height = surface.get_size()

    # Calculate the new width while maintaining the aspect ratio
    new_width = int(new_height * width / height)

    # Scale the surface to the new size
    scaled_surface = pygame.transform.scale(surface, (new_width, new_height))

    return scaled_surface

class AttributePiece:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y

    def apply_effect(self, player):
        if self.type == 'knockback':
            player.knockback += 1
        elif self.type == 'attack':
            player.attack += 1
        elif self.type == "barrier_size":
            player.max_attack_range += 15    
        
        elif self.type == 'barrier':
            player.barrier = True
        elif self.type == "dash_attack":
            player.dash_attack = True
        # Add more types as needed
