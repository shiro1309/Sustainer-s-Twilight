import pygame
import sys

from assets.scripts.settings import *

def handle_events(state, buttons, delta_time=0, player=0, enemies=0):
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
        if len(enemies) >= 1:
            for enemy in enemies:
                if player.rect.colliderect(enemy.rect):
                    if enemy.attack_timer + 200 < delta_time * 1000:
                        enemy.attack_timer = delta_time * 1000
                        return "collision", enemy.damage

    return None, None