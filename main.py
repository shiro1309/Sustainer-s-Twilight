# main.py
import pygame
import random
import time
import sys

from assets.scripts.entity import Entity, Player
from assets.scripts.startscreen import *
from assets.scripts.enemy import Enemy
#from assets.scripts.events import handle_events
from assets.scripts.utils import draw_buttons, Button, draw_text, load_level, Chunk
from assets.scripts.gameover import GameOverScreen
from assets.scripts.camera import Camera

from assets.scripts.settings import *
# import everything from settings.py

# Initialize pygame
pygame.init()

# Main game class
class Game:
    def __init__(self):
        self.buttons = [
            Button("Start", (WIDTH // 2 - 50, HEIGHT // 2 - 70, 100, 40), "start", WHITE),
            Button("Shop", (WIDTH // 2 - 50, HEIGHT // 2 - 20, 100, 40), "shop", WHITE),
            Button("Options", (WIDTH // 2 - 50, HEIGHT // 2 + 30, 100, 40), "options", WHITE),
            Button("Quit", (WIDTH // 2 - 50, HEIGHT // 2 + 80, 100, 40), "quit", WHITE),
        ]
        self.menu_buttons = [
            Button("Resume", (WIDTH // 2 - 50, HEIGHT // 2 - 70, 100, 40), "resume", WHITE),
            Button("Options", (WIDTH // 2 - 50, HEIGHT // 2 - 20, 100, 40), "options", WHITE),
            Button("Quit", (WIDTH // 2 - 50, HEIGHT // 2 + 30, 100, 40), "quit", WHITE),
        ]
        self.game_over_buttons = [
            Button("Return to Menu", (WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 40), "return_to_menu", WHITE)
        ]

        self.game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.start_screen = StartScreen(self.buttons, self.game_screen)  # Create an instance of the StartScreen
        pygame.display.set_caption("Sustainer's Twilight")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = START_SCREEN
        self.score = 0
        self.enemy_group = pygame.sprite.Group()
        self.player = Player(WIDTH // 2, HEIGHT // 2, "assets/sprites/Sprite-0001.png", (16,16), animation_names=["idle", "walk"])
        self.fps = 0
        self.start_time = time.time()
        self.camera = Camera(WIDTH, HEIGHT)
        #self.enemy = Enemy(80,80, self.player, "assets/sprites/Sprite-0001.png", (16,16), animation_names=["idle", "walk"])
        #self.enemy_group.add(self.enemy)
        
        self.show_start_screen()

    def events(self):
        if self.current_state == START_SCREEN:
            return self.handle_events(self.current_state, self.buttons, self.delta_time, self.player, self.enemy_group)
        elif self.current_state == GAME_PLAY:
            return self.handle_events(self.current_state, [], self.delta_time, self.player, self.enemy_group)
        elif self.current_state == GAME_MENU:
            return self.handle_events(self.current_state, self.menu_buttons, self.delta_time, self.player, self.enemy_group)
        elif self.current_state == GAME_OVER:
            return self.handle_events(self.current_state, self.game_over_buttons, self.delta_time)

    def delta_update(self):
        self.delta_time = time.time() - self.start_time  # Convert to seconds
        self.start_time = time.time()

    def update(self):
        self.clock.tick()
        self.local_scroll = [0,0]
        self.delta_update()
        self.score += self.delta_time
        self.local_scroll = self.player.update(self.delta_time, self.enemy_group, self.local_scroll, self.global_scroll, apply_scroll=True)
        self.global_scroll[0] += self.local_scroll[0]
        self.global_scroll[1] += self.local_scroll[1]
        print(self.global_scroll)
        self.enemy_group.update(self.delta_time, self.local_scroll)


    def draw(self):
        self.game_screen.fill((125,125,125))
        for row in self.map:
            for chunk in row:
                
                if (chunk.x + chunk.width + self.global_scroll[0] > 0 and chunk.x + self.global_scroll[0] < WIDTH) and (chunk.y + chunk.height + self.global_scroll[1] > 0 and chunk.y + self.global_scroll[1] < HEIGHT):
                    #print(chunk.id)
                    chunk.draw(self.game_screen, self.global_scroll)

        for enemy in self.enemy_group:
            enemy.update_img()
            if (enemy.rect.x + enemy.rect.width > 0 and enemy.rect.x < WIDTH) and (enemy.rect.y + enemy.rect.height > 0 and enemy.rect.y < HEIGHT):    
                if hasattr(enemy, 'draw'):
                    enemy.draw(self.game_screen)
                else:
                    self.game_screen.blit(enemy.image, enemy.rect.topleft)
        
        self.player.draw(self.game_screen)
        self.get_fps()
        draw_text(str(self.fps),100,50,(255,255,255), pygame.font.Font(None, 36), self.game_screen)
        if self.current_state == GAME_PLAY:
            pygame.display.flip()

    def get_fps(self):
        try:
            self.fps = int(1 / self.delta_time)
        except ZeroDivisionError:
            self.fps = self.fps

    def handle_events(self, state, buttons, delta_time=0, player=0, enemies=0):
        self.comulativ_time += delta_time * 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        return button.action

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == GAME_PLAY:
                        return "pause"
                    elif state == GAME_MENU:
                        return "resume"
        
        if state == GAME_PLAY:
            self.attacking_enemy_damage = 0
            if len(enemies) >= 1:
                for enemy in enemies:
                    if player.rect.colliderect(enemy.rect):
                        if enemy.attack_timer + 200 < self.comulativ_time:
                            enemy.attack_timer = self.comulativ_time
                            self.attacking_enemy_damage = enemy.damage
                            return "collision"

        return None

    def run(self):
        komulativ_time = 0.0
        while self.running:
            action = self.events()
            if action:
                self.handle_action(action)

            if self.current_state == GAME_PLAY:
                self.update()
                self.draw()
                
                if komulativ_time > 1 / SPAWN_RATE:
                    komulativ_time = 0.0
                    self.spawn_enemy()
                else:
                    komulativ_time += self.delta_time

            elif self.current_state == GAME_MENU:
                 self.draw_game_menu()
                 self.delta_update()

            elif self.current_state == GAME_OVER:
                self.game_over_screen.draw(self.game_screen, self.game_over_buttons[0])

        pygame.quit()
        exit()

    def show_start_screen(self):
        for i in self.enemy_group:
            self.enemy_group.remove(i)
        self.current_state = START_SCREEN
        self.current_state = self.start_screen.run(self.current_state)  # Run the start screen
        self.current_state = GAME_PLAY
        self.delta_update()
        self.score = 0
        self.enemy_group = pygame.sprite.Group()
        self.player = Player(WIDTH // 2, HEIGHT // 2, "assets/sprites/Sprite-0001.png", (16,16), animation_names=["idle", "walk"])
        self.enemy = Enemy(80, 80, self.player, "assets/sprites/Sprite-0001.png", (16,16), animation_names=["idle", "walk"])
        self.enemy_group.add(self.enemy)
        self.attacking_enemy_damage = 0
        self.comulativ_time = 0.0
        self.global_scroll = [0,0]
        self.local_scroll = [0,0]
        self.level = load_level("assets/maps/worldone.json")
        self.tile_image = pygame.image.load('assets/sprites/tile.png')

        self.chunk_size = 16
        self.tile_size = 16
        self.map_width = 10
        self.map_height = 10
        self.map = [[Chunk(self.tile_image, self.chunk_size, self.tile_size, x * self.chunk_size * self.tile_size, y * self.chunk_size * self.tile_size) for x in range(self.map_width)] for y in range(self.map_height)]
        
        self.start_time = time.time()

    def show_game_menu(self):
        self.current_state = GAME_MENU
        # Add logic for displaying and handling the game menu options

    def draw_game_menu(self):
        self.draw()
        draw_buttons(self.menu_buttons, self.game_screen)
        pygame.display.flip()

    def handle_action(self, action):
        # ----------- this section has been moved ----------- #
        # ----------- handles the main menu actions ----------- #
        #if self.current_state == START_SCREEN:
        #    if action == "start":
        #        print("Transition to game")
        #    elif action == "shop":
        #        print("Transition to shop")
        #    elif action == "options":
        #        print("Transition to options")
        #    elif action == "quit":
        #        self.running = False

        # ----------- handles the game play actions ----------- #
        if self.current_state == GAME_PLAY:
            if action == "pause":
                self.show_game_menu()
            if action == "collision":
                self.player.take_damage(self.attacking_enemy_damage)
                if self.player.health_bar.health <= 0:
                    self.current_state = GAME_OVER
                    self.game_over_screen = GameOverScreen(self.score)

        # ----------- handles the in game menu actions ----------- #
        elif self.current_state == GAME_MENU:
            if action == "resume":
                print("Resume game")
                self.current_state = GAME_PLAY
                for sprite in self.enemy_group:
                    if hasattr(sprite, 'ani_resume'):
                        sprite.ani_resume(self.game_screen)

            elif action == "options":
                print("Transition to options")
            elif action == "quit":
                print("run savings script for the game")
                print("check states for new achivments")
                print("go back into main menu and prepere for a restart of the game")
                self.show_start_screen()

        # ----------- handles the game over actions ----------- #
        elif self.current_state == GAME_OVER:
            if action == "return_to_menu":
                print("run savings script for the game")
                print("check states for new achivments")
                print("go back into main menu and prepere for a restart of the game")
                self.show_start_screen()

    def spawn_enemy(self):
        # Randomly determine the initial position of the enemy
        up = random.choice([0,1])
        if up == 0:
            x = random.randint(0, WIDTH)
            y = random.choice([0,1]) * HEIGHT
        else:
            x = random.choice([0,1]) * WIDTH
            y = random.randint(0, HEIGHT)

        # Create a new enemy instance and add it to the sprite group
        new_enemy = Enemy(x, y, self.player, "assets/sprites/Sprite-0001.png", (16,16), animation_names=["idle", "walk"])
        self.enemy_group.add(new_enemy)

if __name__ == "__main__":
    game = Game()
    game.run()