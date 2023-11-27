# main.py
import pygame
import random
import time

from assets.scripts.entity import Entity, Player
from assets.scripts.startscreen import *
from assets.scripts.enemy import Enemy
from assets.scripts.events import handle_events
from assets.scripts.utils import draw_buttons, Button, draw_text
from assets.scripts.gameover import GameOverScreen

from assets.scripts.settings import *

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
        #self.enemy = Enemy(80,80, self.player, "assets/sprites/Sprite-0001.png", (16,16), animation_names=["idle", "walk"])
        #self.enemy_group.add(self.enemy)
        
        self.show_start_screen()

    def events(self):
        if self.current_state == START_SCREEN:
            return handle_events(self.current_state, self.buttons, self.player, self.enemy_group)
        elif self.current_state == GAME_PLAY:
            return handle_events(self.current_state, [], self.player, self.enemy_group)
        elif self.current_state == GAME_MENU:
            return handle_events(self.current_state, self.menu_buttons, self.player, self.enemy_group)
        elif self.current_state == GAME_OVER:
            return handle_events(self.current_state, self.game_over_buttons)

    def delta_update(self):
        self.delta_time = time.time() - self.start_time  # Convert to seconds
        self.start_time = time.time()

    def update(self):
        self.delta_update()
        self.score += self.delta_time
        self.player.update(self.delta_time)
        self.enemy_group.update(self.delta_time)

    def draw(self):
        self.game_screen.fill((125,125,125))
        for sprite in self.enemy_group:
                if hasattr(sprite, 'draw'):
                    sprite.draw(self.game_screen)
                else:
                    self.game_screen.blit(sprite.image, sprite.rect.topleft)
        self.player.draw(self.game_screen)
        self.get_fps()
        draw_text(str(self.fps),100,50,(255,255,255), pygame.font.Font(None, 36), self.game_screen)
        pygame.display.flip()

    def get_fps(self):
        try:
            self.fps = int(1 / self.delta_time)
        except ZeroDivisionError:
            self.fps = self.fps

    def run(self):
        while self.running:
            action = self.events()
            if action:
                self.handle_action(action)

            if self.current_state == GAME_PLAY:
                self.update()
                self.draw()

                if random.random() < .01:
                    self.spawn_enemy()

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
        self.start_time = time.time()

    def show_game_menu(self):
        self.current_state = GAME_MENU
        # Add logic for displaying and handling the game menu options

    def draw_game_menu(self):
        self.game_screen.fill(BLACK)
        self.enemy_group.draw(self.game_screen)
        self.player.draw(self.game_screen)
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