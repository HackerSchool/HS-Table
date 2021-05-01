import pygame
from assets.Dimensions import *
from assets.fade import *

#Load background
def display_background(SCREEN, fadeout, darker, opacity):
    BACKGROUND_IMAGE = pygame.image.load("./assets/images/Logo_HS_Table.png")
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
    SCREEN.blit(BACKGROUND_IMAGE, [0,0])

    if darker == True:
        BACKGROUND_IMAGE = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
        BACKGROUND_IMAGE.fill((0, 0, 0, opacity))
        SCREEN.blit(BACKGROUND_IMAGE, [0, 0])

    if fadeout == True:
        fadeout_screen(SCREEN, opacity)

    pygame.display.update()
