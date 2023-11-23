import time
from assets.scripts.assets import AssetsLoader  # Assuming this import is needed
from settings import ANIMATION_RATE

class Animation:
    def __init__(self, sprite_sheet_path, frame_dimensions, num_frames, image_duration=1, loop=True):
        self.frame_dimensions = frame_dimensions
        self.num_frames = num_frames
        self.image_duration = image_duration
        self.loop = loop
        self.frame = 0
        self.done = False
        self.animation_sum = 0
        self.animation_start = time.time()
        self.images = AssetsLoader().load_animation(sprite_sheet_path, frame_dimensions, num_frames, loop)

    def update(self):
        if time.time() - self.animation_start >= self.animation_sum + ANIMATION_RATE:
            self.animation_sum += ANIMATION_RATE
            self.animate()

    def copy(self):
        return Animation(self.sprite_sheet_path, self.frame_dimensions, self.num_frames, self.image_duration, self.loop)

    def animate(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.image_duration * self.num_frames)
            return
        self.frame = min(self.frame + 1, self.image_duration * self.num_frames - 1)
        if self.frame >= self.image_duration * self.num_frames - 1:
            self.done = True

    def img(self):
        return self.images[self.frame // self.image_duration]
