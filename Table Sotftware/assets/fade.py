import pygame
from assets.Color import *
from assets.Dimensions import *
from assets.env_buttons_and_text import *

def fadeout_screen(SCREEN, opacity):
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade.fill(BLACK)
    for i in range(0, opacity):
        fade.set_alpha(i)
        SCREEN.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)

def fadein_screen(SCREEN, opacity):
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade.fill(BLACK)
    for i in range(0, opacity):
        fade.set_alpha(opacity - i)
        SCREEN.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)

"""
def fadeout_button(SCREEN, opacity)
def fadein_button(SCREEN, opacity):
"""