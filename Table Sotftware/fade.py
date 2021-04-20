import pygame
from assets.Color import *
from assets.Dimensions import *

def fadeout_screen(SCREEN):
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade = fade.convert()
    fade.fill(BLACK)
    for i in range(0, 250):
        fade.set_alpha(i)
        SCREEN.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)

def fadein_screen(SCREEN, function):
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade = fade.convert()
    fade.fill(BLACK)
    for i in range(0, 300):
        fade.set_alpha(300 - i)
        function()
        SCREEN.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)