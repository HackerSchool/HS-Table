import pygame
pygame.init()

from assets.Color import *
from Snooker import *
from assets.buttons_and_text import *
from assets.Dimensions import *
from assets.fade import *

#Defining screen
FULLSCREEN = True
if FULLSCREEN == True:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
    SCREEN_WIDTH, SCREEN_HEIGHT = int(0.75 * SCREEN_WIDTH), int(0.75 * SCREEN_HEIGHT)
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def snooker_main_menu():

    SCREEN.fill(GREY)
    text_surf, text_rectangle = text_objects('SNOOKER', MAIN_MENU_TEXT, WHITE)
    text_rectangle.center = (int(SCREEN_WIDTH // 2), int(SCREEN_HEIGHT // 4))
    SCREEN.blit(text_surf, text_rectangle)
    text_surf, text_rectangle = text_objects('Created by the HS Table team', SMALL_TEXT, WHITE)
    text_rectangle.center = (int(SCREEN_WIDTH / 1.11), int(SCREEN_HEIGHT * 0.95))
    SCREEN.blit(text_surf, text_rectangle)

    quit_game = False
    
    mainmenu = True
    while mainmenu:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        if button(SCREEN,'P L A Y E R  V S  P L A Y E R', *MAIN_MENU_BUTTONS_LAYOUT_4[0], click):
            playing = True
            while playing:
                quit_game = Snooker()
                if quit_game == True:
                    break          
            mainmenu = False

        elif button(SCREEN,'P L A Y E R  V S  B O T', *MAIN_MENU_BUTTONS_LAYOUT_4[1], click):
            playing = True
            while playing:
                quit_game = Snooker_BOT()
                if quit_game == True:
                    break          
            mainmenu = False 

        elif button(SCREEN,'B O T  V S  B O T', *MAIN_MENU_BUTTONS_LAYOUT_4[2], click):
            playing = True
            while playing:
                quit_game = Snooker_BOT(1)
                if quit_game == True:
                    break          
            mainmenu = False

        elif button(SCREEN,'Q U I T   G A M E', *MAIN_MENU_BUTTONS_LAYOUT_4[3], click):
            #Default variable names (cada vez que se inicia o jogo as variáveis terão sempre os valores default)
            quit_game = True
            fadeout_screen(SCREEN)
            return quit_game

        pygame.display.update()


pygame.display.set_caption('SNOOKER')