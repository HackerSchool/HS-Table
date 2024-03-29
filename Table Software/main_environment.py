import os
import pygame
pygame.init()

from subprocess import call
from tic_tac_toe_main_menu import *
from Snooker_main_menu import *
from assets.Color import *
from assets.Dimensions import *
from assets.Fonts import *
from assets.env_buttons_and_text import *
from assets.env_background import *
from assets.fade import *
from datetime import datetime
from time import time

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
                pygame.quit()
                #call("sudo shutdown -h now", shell = True) #Raspberry pi

            elif env_button(SCREEN, False, 'N O', MEDIUM_TEXT, MEDIUM_BOLD_TEXT, *QUESTION_ENV_BUTTONS_LAYOUT[1], 2, 2, click):
                pygame.time.delay(100)
                main_env()

        elif turnoff_system == 'Restart':
            setup_turnoff_system_menu(turnoff_system)

            if env_button(SCREEN, False, 'Y E S', MEDIUM_TEXT, MEDIUM_BOLD_TEXT, *QUESTION_ENV_BUTTONS_LAYOUT[0], 2, 2, click):
                pygame.time.delay(100)
                #call("sudo shutdown -r now", shell = True) #Raspberry pi

            elif env_button(SCREEN, False, 'N O', MEDIUM_TEXT, MEDIUM_BOLD_TEXT, *QUESTION_ENV_BUTTONS_LAYOUT[1], 2, 2, click):
                pygame.time.delay(100)
                main_env()

        pygame.display.update()


#SETTINGS MENU
def env_settings_menu():
    display_background(SCREEN, False, True, 122)

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
            main_env()

    pygame.display.update()

#Add date and time here
def date_and_time():
    #while True:
    time = datetime.now()
    string = str(time.strftime("%d/%m/%Y %H:%M"))
    segundos = int(time.strftime("%S"))

    text_w = SMALL_FONT.render(str(string), True,WHITE)

    pygame.draw.rect(SCREEN, MAIN_BACK, (int(SCREEN_WIDTH * 0.77 + 2.5), int(SCREEN_HEIGHT * 0.9 + 2.5), int(SCREEN_WIDTH // 4.5), int(SCREEN_HEIGHT // 11)))
    
    textwRect = text_w.get_rect()
    textwRect.center = (8.8 * SCREEN_WIDTH//10, 9.5 * SCREEN_HEIGHT//10)
    SCREEN.blit(text_w,textwRect)
    pygame.display.update()
    return segundos
        

#MAIN ENVIRONMENT
aux, itstime = 0, 0
def main_env():
    display_background(SCREEN, False, False, 0)
    pygame.draw.rect(SCREEN, LIGHT_GREEN, (int(SCREEN_WIDTH * 0.76), int(SCREEN_HEIGHT * 0.9 - 2.5), int(SCREEN_WIDTH // 4.2), int(SCREEN_HEIGHT - SCREEN_HEIGHT * 0.90)), 1)

    def start_game(game):
        fadeout_screen(SCREEN)
        playing = True
        while playing:
            quit_game = game()
            if quit_game == True:
                fadeout_screen(SCREEN)
                break
        main_env()

    envmenu = True
    prev = time()
    first = 1
    while envmenu:
        aux = time()
        istime = aux - prev
        if istime >= 60 or first:
            segundos = date_and_time()
            prev = aux - segundos            
            first = 0
        pygame.display.update()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if env_button(SCREEN, False, 'H', HS_TEXT, HS_TEXT, *MAIN_ENV_BUTTONS_LAYOUT[0], 2, 2, click):
            #pygame.time.delay(100)
            env_settings_menu()

        elif env_button(SCREEN, True, 'TIC TAC TOE', SMALL_TEXT, SMALL_BOLD_TEXT, *MAIN_ENV_BUTTONS_LAYOUT[1], 2, 6, click):
            #pygame.time.delay(100)
            start_game(galo_main_menu)

        elif env_button(SCREEN, True, 'SNOOKER', SMALL_TEXT, SMALL_BOLD_TEXT, *MAIN_ENV_BUTTONS_LAYOUT[2], 2, 6, click):
            #pygame.time.delay(100)
            start_game(snooker_main_menu)

    pygame.display.update()


fadein_screen(SCREEN)
main_env()