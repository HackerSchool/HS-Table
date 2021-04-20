import os
import pygame
pygame.init()

from subprocess import call
from tic_tac_toe_main_menu import *
from assets.Color import *
from assets.Dimensions import *
from assets.Fonts import *
from assets.env_buttons_and_text import *
from assets.fade import *

#Defining screen
Fullscreen = True
if Fullscreen == True:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
    SCREEN_WIDTH, SCREEN_HEIGHT = int(0.75 * SCREEN_WIDTH), int(0.75 * SCREEN_HEIGHT)
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Load images
def display_background():
    BACKGROUND_IMAGE = pygame.image.load("./assets/images/Logo_HS_Table 1.png")
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
    SCREEN.blit(BACKGROUND_IMAGE, [0,0])  

#TURN OFF PC MENU
def turnoff_system_menu(turnoff_system):
    
    def setup_turnoff_system_menu(turnoff_system):
        display_background()

        text_surf, text_rectangle = text_objects('Are you sure you want to ' + str(turnoff_system) + ' the system?', LARGE_TEXT, WHITE)
        text_rectangle.center = ((SCREEN_WIDTH // 3.27), (SCREEN_HEIGHT // 5))
        SCREEN.blit(text_surf, text_rectangle)

    turnoffmenu = True
    while turnoffmenu:
        click = False
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        if turnoff_system == 'Shutdown':
            setup_turnoff_system_menu(turnoff_system)

            if env_button(SCREEN, 'Y E S', *QUESTION_ENV_BUTTONS_LAYOUT[0], click):
                pygame.time.delay(100)
                #call("sudo shutdown -h now", shell = True) #Raspberry pi

            elif env_button(SCREEN, 'N O', *QUESTION_ENV_BUTTONS_LAYOUT[1], click):
                pygame.time.delay(100)
                main_env()

        elif turnoff_system == 'Restart':
            setup_turnoff_system_menu(turnoff_system)

            if env_button(SCREEN, 'Y E S', *QUESTION_ENV_BUTTONS_LAYOUT[0], click):
                pygame.time.delay(100)
                #call("sudo shutdown -r now", shell=True) #Raspberry pi

            elif env_button(SCREEN, 'N O', *QUESTION_ENV_BUTTONS_LAYOUT[1], click):
                pygame.time.delay(100)
                main_env()

        elif turnoff_system == 'Hibernate':
            setup_turnoff_system_menu(turnoff_system)

            if env_button(SCREEN, 'Y E S', *QUESTION_ENV_BUTTONS_LAYOUT[0], click):
                pygame.time.delay(100)
                #Não encontrei comando de hibernar para o raspberry pi

            elif env_button(SCREEN, 'N O', *QUESTION_ENV_BUTTONS_LAYOUT[1], click):
                pygame.time.delay(100)
                main_env()

        pygame.display.update(QUESTION_ENV_BUTTONS_LAYOUT)


#SETTINGS MENU
def env_settings_menu():
    display_background()

    settingsmenu = True
    while settingsmenu:
        click = False
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        if env_button(SCREEN, 'H', *MAIN_ENV_BUTTONS_LAYOUT[0], click):
            pygame.time.delay(100)
            main_env()

        if env_button(SCREEN, 'S H U T D O W N', *SETTINGS_ENV_BUTTONS_LAYOUT[0], click):
            pygame.time.delay(100)
            turnoff_system_menu('Shutdown')

        elif env_button(SCREEN, 'R E S T A R T', *SETTINGS_ENV_BUTTONS_LAYOUT[1], click):
            pygame.time.delay(100)
            turnoff_system_menu('Restart')

        elif env_button(SCREEN, 'H I B E R N A T E', *SETTINGS_ENV_BUTTONS_LAYOUT[2], click):
            pygame.time.delay(100)
            turnoff_system_menu('Hibernate')

        pygame.display.update(MAIN_ENV_BUTTONS_LAYOUT)

#MAIN ENVIRONMENT
def main_env():
    display_background()

    envmenu = True
    while envmenu:
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        if env_button(SCREEN, 'H', *MAIN_ENV_BUTTONS_LAYOUT[0], click):
            pygame.time.delay(100)
            env_settings_menu()

        elif env_button(SCREEN, 'TIC TAC TOE', *MAIN_ENV_BUTTONS_LAYOUT[1], click):
            pygame.time.delay(100)
            fadeout_screen(SCREEN)
            galo_main_menu()

        elif env_button(SCREEN, 'SNOOKER', *MAIN_ENV_BUTTONS_LAYOUT[2], click):
            pygame.time.delay(1000)
            #snooker_main_menu()

    pygame.display.update(MAIN_ENV_BUTTONS_LAYOUT)

#fadein_screen(SCREEN, main_env) #Ainda não funciona
main_env()