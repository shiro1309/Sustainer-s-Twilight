# start_screen.py
import pygame
from settings import *
from scripts.events import handle_events
from scripts.utils import draw_buttons, Button


class StartScreen:
    def __init__(self, buttons, screen):
        self.screen = screen
        pygame.display.set_caption("Sustainer's Twilight - Start Screen")
        self.clock = pygame.time.Clock()
        self.running = True
        self.buttons = buttons


    def run(self, state):
        self.running = True
        self.state = state
        while self.running:
            self.screen.fill((0, 0, 0))  # Set background color
            # Draw buttons
            draw_buttons(self.buttons, self.screen)

            pygame.display.flip()

            action = handle_events("start_screen", self.buttons)
            if action:
                self.handle_action(action)

            self.clock.tick(30)  # Set a lower frame rate for the start screen
        return self.state

    def handle_action(self, action):
        if action == "start":
            #print("Transition to game")
            self.state = GAME_PLAY
            self.running = False
        elif action == "shop":
            print("Transition to shop")
        elif action == "options":
            print("Transition to options")
        elif action == "quit":
            pygame.quit()
            exit()
