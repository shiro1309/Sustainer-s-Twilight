import pygame
import json
import math
from assets.scripts.utils import load_chunk_data, Chunk, MetaChunk, save_chunk_data

def make_chunk(image, size, enemy, walk, prerender):
    li = []
    for i in range(4):
        t = math.sqrt(4)
        w = 0
        if i >= 2:
            w = 1
        e = Chunk(i+1, image, size, int(i%2), w, enemy, walk, "assets/sprites/grass.png",prerender)
        li.append(e)
    return li
        

class Editor:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1200, 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.map = load_chunk_data("assets/maps/worldone.json")
        self.scroll = [0,0]
        # Load the map data
        self.clock = pygame.time.Clock()
        self.running = True
        self.movment = [False, False, False, False]
        self.metachunk_size = 256
        self.chunk_size = 128
        self.tile_size = 16
        self.meta_activ = False
        self.chunk_activ = False
        self.activ_meta_chunk = [0,0]
        self.clicking = False
        self.base_chunk_list = make_chunk(pygame.image.load("assets/sprites/grass.png").convert_alpha(), 8, True, True, True)
        #self.base_meta = MetaChunk(self.base_chunk_list, 2,0)
        self.images = [pygame.image.load("assets/sprites/grass.png").convert_alpha(), pygame.image.load("assets/sprites/water.png").convert_alpha()]
        
    def update(self):
        
        self.scroll[0] += (self.movment[2] - self.movment[0]) * 2
        self.scroll[1] += (self.movment[3] - self.movment[1]) * 2
        
        self.render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
    
    def draw(self):
        pygame.display.set_caption(f'{self.scroll}')
        self.screen.fill((0,0,0))
        for meta_chunk in self.map:
            meta_chunk.draw_prerender(self.screen, self.render_scroll)
        
        pygame.draw.rect(self.screen, (255,255,255), (self.activ_meta_chunk[0] * self.metachunk_size - self.scroll[0], 
                                                      self.activ_meta_chunk[1] * self.metachunk_size - self.scroll[1], 
                                                      self.metachunk_size, 
                                                      self.metachunk_size), 4)
        pygame.display.update()
    
    def handle_events(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        screen_value = self.screen.get_size()
        self.mouse_pos = (self.mouse_x, self.mouse_y)
        self.meta_chunk_pos = (int((self.mouse_x + self.scroll[0]) // self.metachunk_size), int((self.mouse_y + self.scroll[1]) // self.metachunk_size))
        self.chunk_pos = [int((self.mouse_x + self.scroll[0]) // self.chunk_size), int((self.mouse_y + self.scroll[1]) // self.chunk_size)]
        
        #if self.clicking:
        self.activ_meta_chunk = self.meta_chunk_pos
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicking = True
                if event.button == 3:
                    check = False
                    for meta_chunk in self.map:
                        if meta_chunk.id_x == self.meta_chunk_pos[0]:
                            if meta_chunk.id_y == self.meta_chunk_pos[1]:
                                self.map.remove(meta_chunk)
                                break
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.movment[2] = True
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.movment[1] = True
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.movment[0] = True
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.movment[3] = True
                if event.key == pygame.K_LSHIFT:
                    self.meta_activ = True
                if event.key == pygame.K_LCTRL and self.meta_activ:
                    self.chunk_activ = True
                if event.key == pygame.K_TAB:
                    check = False
                    for meta_chunk in self.map:
                        if meta_chunk.id_x == self.meta_chunk_pos[0]:
                            if meta_chunk.id_y == self.meta_chunk_pos[1]:
                                check = True
                                break
                    if check == False:
                        new_chunk_list = []
                        for i in range(len(self.base_chunk_list)):
                            new_chunk_list.append(self.base_chunk_list[i])
                        self.map.append(MetaChunk(new_chunk_list, self.meta_chunk_pos[0], self.meta_chunk_pos[1]))
                if event.key == pygame.K_u:
                    print(len(self.map))
                    for meta_chunk in self.map:
                        
                        was = False
                        if meta_chunk.id_x == self.meta_chunk_pos[0] and meta_chunk.id_y == self.meta_chunk_pos[1]:
                            # Loop over the chunks in the meta chunk
                            for chunk in meta_chunk.chunks:
                                # Check if the mouse is hovering over the chunk
                                if chunk.x == self.chunk_pos[0]%2 and chunk.y == self.chunk_pos[1]%2:
                                    print("found chunk")
                                    
                                    if chunk.can_walk:
                                        chunk.can_walk = False
                                        chunk.image = self.images[1]
                                        chunk.sprite = "assets/sprites/water.png"
                                        print("can't walk")
                                    else:
                                        chunk.can_walk = True
                                        chunk.image = self.images[0]
                                        chunk.sprite = "assets/sprites/grass.png"
                                        print("can walk")
                                    
                                    chunk.tile(True)
                                    was = True
                                if was:
                                    chunk.prerender = None
                        if was:
                            meta_chunk.prerender = None
                
                if event.key == pygame.K_o:
                    save_chunk_data("assets/maps/worldtwo.json", self.map)


            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.clicking = False
                    
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.movment[2] = False
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.movment[1] = False
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.movment[0] = False
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.movment[3] = False
                if event.key == pygame.K_LSHIFT:
                    self.meta_activ = False
                if event.key == pygame.K_LCTRL:
                    self.chunk_activ = False
        
        #print(self.meta_chunk_pos, self.chunk_pos)
        #print(len(self.map))
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()
            
if __name__ == '__main__':
    app = Editor()
    app.run()