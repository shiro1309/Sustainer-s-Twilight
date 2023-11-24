# main.py
import pygame

from assets.scripts.entity import Entity, Player
from assets.scripts.startscreen import *
from assets.scripts.enemy import Enemy
from assets.scripts.events import handle_events
from assets.scripts.utils import draw_buttons, Button
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
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(WIDTH // 2, HEIGHT // 2, "assets/sprites/Sprite-0001.png", (16,16), animation_names=["idle", "walk"])
        self.enemy = Enemy(80,80, self.player, "assets/sprites/Sprite-0001.png", (16,16), animation_names=["idle", "walk"])
        self.all_sprites.add(self.player, self.enemy)
        
        self.show_start_screen()

    def events(self):
        if self.current_state == START_SCREEN:
            return handle_events(self.current_state, self.buttons, self.player, self.enemy)
        elif self.current_state == GAME_PLAY:
            return handle_events(self.current_state, [], self.player, self.enemy)
        elif self.current_state == GAME_MENU:
            return handle_events(self.current_state, self.menu_buttons, self.player, self.enemy)
        elif self.current_state == GAME_OVER:
            return handle_events(self.current_state, self.game_over_buttons)

    def delta_update(self):
        self.delta_time = self.clock.tick() / 1000.0  # Convert to seconds

    def update(self):
        self.delta_update()
        self.score += self.delta_time
        self.all_sprites.update(self.delta_time)

    def draw(self):
        self.game_screen.fill((125,125,125))
        for sprite in self.all_sprites:
                if hasattr(sprite, 'draw'):
                    sprite.draw(self.game_screen)
                else:
                    self.game_screen.blit(sprite.image, sprite.rect.topleft)
        pygame.display.flip()

    def run(self):
        while self.running:
            action = self.events()
            if action:
                self.handle_action(action)

            if self.current_state == GAME_PLAY:
                self.update()
                self.draw()

            elif self.current_state == GAME_MENU:
                 self.draw_game_menu()
                 self.delta_update()

            elif self.current_state == GAME_OVER:
                self.game_over_screen.draw(self.game_screen, self.game_over_buttons[0])

        pygame.quit()
        exit()

    def show_start_screen(self):
        for i in self.all_sprites:
            self.all_sprites.remove(i)
        self.current_state = START_SCREEN
        self.current_state = self.start_screen.run(self.current_state)  # Run the start screen
        self.current_state = GAME_PLAY
        self.delta_time = self.clock.tick(FPS) / 1000.0
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(WIDTH // 2, HEIGHT // 2, "assets/sprites/Sprite-0001.png", (16,16), animation_names=["idle", "walk"])
        self.enemy = Enemy(80, 80, self.player, "assets/sprites/Sprite-0001.png", (16,16), animation_names=["idle", "walk"])
        self.all_sprites.add(self.player, self.enemy)

    def show_game_menu(self):
        self.current_state = GAME_MENU
        # Add logic for displaying and handling the game menu options

    def draw_game_menu(self):
        self.game_screen.fill(BLACK)
        self.all_sprites.draw(self.game_screen)
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

if __name__ == "__main__":
    game = Game()
    game.run()