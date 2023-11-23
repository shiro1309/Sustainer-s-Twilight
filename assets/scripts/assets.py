# assets.py
import pygame
import os

class AssetsLoader:
    def __init__(self):
        self.image_dict = {}
        self.animation_dict = {}

    def load_image(self, image_path):
        if image_path not in self.image_dict:
            image = pygame.image.load(image_path).convert_alpha()
            self.image_dict[image_path] = image
            return image
        else:
            return self.image_dict[image_path]

    def load_images(self, directory_path):
        image_paths = sorted([os.path.join(directory_path, filename) for filename in os.listdir(directory_path)])
        images = [self.load_image(image_path) for image_path in image_paths]
        return images

    def load_animation(self, sprite_sheet_path, frame_dimensions, num_frames, loop=True):
        animation_key = (sprite_sheet_path, frame_dimensions, num_frames, loop)
        if animation_key not in self.animation_dict:
            sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
            frames = []
            for i in range(num_frames):
                frame = pygame.Surface(frame_dimensions, pygame.SRCALPHA)
                frame.blit(sprite_sheet, (0, 0), (i * frame_dimensions[0], 0, frame_dimensions[0], frame_dimensions[1]))
                frames.append(frame)

            self.animation_dict[animation_key] = {
                'frames': frames,
                'current_frame': 0,
                'loop': loop
            }

        return self.animation_dict[animation_key]['frames']

    def get_animation_frame(self, sprite_sheet_path, frame_dimensions, num_frames, loop=True):
        animation_key = (sprite_sheet_path, frame_dimensions, num_frames, loop)
        animation_info = self.animation_dict.get(animation_key, None)

        if animation_info:
            return animation_info['frames'][animation_info['current_frame']]
        else:
            return None

    def update_animation_frame(self, sprite_sheet_path, frame_dimensions, num_frames, loop=True):
        animation_key = (sprite_sheet_path, frame_dimensions, num_frames, loop)
        animation_info = self.animation_dict.get(animation_key, None)

        if animation_info:
            if animation_info['loop'] or animation_info['current_frame'] < num_frames - 1:
                animation_info['current_frame'] = (animation_info['current_frame'] + 1) % num_frames
