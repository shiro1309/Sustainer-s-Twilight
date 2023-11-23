import pygame
import sys

from settings import *

def handle_events(state, buttons, player=0, enemy=0):
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
        if pygame.sprite.collide_rect(player, enemy):
            return "collision"

    return None