import os
import pygame
pygame.init()

from subprocess import call
from tic_tac_toe_main_menu import *
from assets.Color import *
from assets.Dimensions import *
from assets.Fonts import *
from assets.env_buttons_and_text import *
from assets.env_background import *
from assets.fade import *
from datetime import date

#Defining screen
Fullscreen = True
if Fullscreen == True:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
    SCREEN_WIDTH, SCREEN_HEIGHT = int(0.75 * SCREEN_WIDTH), int(0.75 * SCREEN_HEIGHT)
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#TURN OFF PC MENU
def turnoff_system_menu(turnoff_system):

    def setup_turnoff_system_menu(turnoff_system):
        
        text_surf, text_rectangle = text_objects('Are you sure you want to ' + str(turnoff_system) + ' the system?', LARGE_TEXT, WHITE)
        text_rectangle.center = ((SCREEN_WIDTH // 3.27), (SCREEN_HEIGHT // 5))
        SCREEN.blit(text_surf, text_rectangle)

    display_background(SCREEN, False, True, 122)
    turnoffmenu = True
    while turnoffmenu:
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        if turnoff_system == 'Shutdown':
            setup_turnoff_system_menu(turnoff_system)

            if env_button(SCREEN, False, 'Y E S', MEDIUM_TEXT, MEDIUM_BOLD_TEXT, *QUESTION_ENV_BUTTONS_LAYOUT[0], 2, 2, click):
                pygame.time.delay(100)
                #call("sudo shutdown -h now", shell = True) #Raspberry pi

            elif env_button(SCREEN, False, 'N O', MEDIUM_TEXT, MEDIUM_BOLD_TEXT, *QUESTION_ENV_BUTTONS_LAYOUT[1], 2, 2, click):
                pygame.time.delay(100)
                main_env(False)

        elif turnoff_system == 'Restart':
            setup_turnoff_system_menu(turnoff_system)

            if env_button(SCREEN, False, 'Y E S', MEDIUM_TEXT, MEDIUM_BOLD_TEXT, *QUESTION_ENV_BUTTONS_LAYOUT[0], 2, 2, click):
                pygame.time.delay(100)
                #call("sudo shutdown -r now", shell = True) #Raspberry pi

            elif env_button(SCREEN, False, 'N O', MEDIUM_TEXT, MEDIUM_BOLD_TEXT, *QUESTION_ENV_BUTTONS_LAYOUT[1], 2, 2, click):
                pygame.time.delay(100)
                main_env(False)

        pygame.display.update()


#SETTINGS MENU
def env_settings_menu():
    display_background(SCREEN, True, False, 15)

    settingsmenu = True
    while settingsmenu:
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        if env_button(SCREEN, False, 'S H U T D O W N', MEDIUM_TEXT, MEDIUM_BOLD_TEXT, *SETTINGS_ENV_BUTTONS_LAYOUT[0], 2, 2, click):
            pygame.time.delay(100)
            turnoff_system_menu('Shutdown')

        elif env_button(SCREEN, False, 'R E S T A R T', MEDIUM_TEXT, MEDIUM_BOLD_TEXT, *SETTINGS_ENV_BUTTONS_LAYOUT[1], 2, 2, click):
            pygame.time.delay(100)
            turnoff_system_menu('Restart')

        elif env_button(SCREEN, False, 'R E T U R N', MEDIUM_TEXT, MEDIUM_BOLD_TEXT, *SETTINGS_ENV_BUTTONS_LAYOUT[2], 2, 2, click):
            pygame.time.delay(100)
            main_env(False)

    pygame.display.update()

#Add date and time here
"""def date_and_time():
    pygame.draw.rect(SCREEN, GREY, (int(SCREEN_WIDTH / 1.355), int(SCREEN_HEIGHT * 0.935), int(1 / 4 * SCREEN_WIDTH), int(50 / 1440 * SCREEN_HEIGHT)))
    
    while True:
        time = datetime.now()"""

#MAIN ENVIRONMENT
def main_env(fading):
    display_background(SCREEN, False, False, 0)
    pygame.draw.rect(SCREEN, LIGHT_GREEN, (int(SCREEN_WIDTH * 0.32), int(SCREEN_HEIGHT * 0.10), int(SCREEN_WIDTH * 0.35), int(SCREEN_WIDTH // 15)), 1)
    #date_and_time()

    def start_game(game):
        fadeout_screen(SCREEN, 255)
        playing = True
        while playing:
            quit_game = game()
            if quit_game == True:
                break
        main_env(False)

    envmenu = True
    while envmenu:
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        if env_button(SCREEN, False, 'H', HS_TEXT, HS_TEXT, *MAIN_ENV_BUTTONS_LAYOUT[0], 2, 2, click):
            pygame.time.delay(100)
            env_settings_menu()

        elif env_button(SCREEN, True, 'TIC TAC TOE', SMALL_TEXT, SMALL_BOLD_TEXT, *MAIN_ENV_BUTTONS_LAYOUT[1], 2, 6, click):
            pygame.time.delay(100)
            start_game(galo_main_menu)

        elif env_button(SCREEN, True, 'SNOOKER', SMALL_TEXT, SMALL_BOLD_TEXT, *MAIN_ENV_BUTTONS_LAYOUT[2], 2, 6, click):
            pygame.time.delay(100)
            #start_game()

    pygame.display.update()


#STARTUP HERE

#fadein_screen(SCREEN, 255)
main_env(True)