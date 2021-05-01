#NOTE: NA ALTURA DE TESTAR NA MESA: 
# - COLOCAR FULLSCREEN = True (linha 26)
# - DEFINIR LIMITE PARA NÚMERO DE BOARDSIZE

import pygame
pygame.init()

from assets.Color import *
from tic_tac_toe import *
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

#Default variable names
NPLAYERS = 2
BOARDSIZE = 3
NROUNDS = 3
BOT_DIFF = 0
NBOTS = 1
difficulty = 'E A S Y'

#CHOOSING SETTINGS MENU
def choose_galo_settings_menu(settings_type):
    
    def setup_choose_galo_settings_menu(settings_type):
        SCREEN.fill(GREY)
        
        if settings_type == 'number of players':
            text_surf, text_rectangle = text_objects('Select the ' +  str(settings_type) + ' (max of 9) ...', LARGE_TEXT, WHITE)
        else:
            text_surf, text_rectangle = text_objects('Select the ' +  str(settings_type) + ' ...', LARGE_TEXT, WHITE)

        text_rectangle.center = ((SCREEN_WIDTH // 3.27), (SCREEN_HEIGHT // 5))
        SCREEN.blit(text_surf, text_rectangle)
        
        pygame.display.update()

    def choose_settings(settings_display):
        pygame.draw.rect(SCREEN, LIGHT_GREEN, (int(SCREEN_WIDTH // 2.72), int(SCREEN_HEIGHT * 4 // 12), int(SCREEN_WIDTH * 0.8 // 3), int(70)), int(1))
        pygame.draw.rect(SCREEN, GREY, (int(SCREEN_WIDTH // 2.66), int(SCREEN_HEIGHT * 4.1 // 12), int(SCREEN_WIDTH * 0.75 // 3), int(85 / 1440 * SCREEN_HEIGHT)))

        text_surf, text_rectangle = text_objects(str(settings_display), LABEL_TEXT, WHITE)
        text_rectangle.center = (int(SCREEN_WIDTH // 2), int(SCREEN_HEIGHT // 2.67))
        SCREEN.blit(text_surf, text_rectangle)

    def changes_done(settings_display, change):
        pygame.draw.rect(SCREEN, GREY, (int(SCREEN_WIDTH / 1.355), int(SCREEN_HEIGHT * 0.935), int(1 / 4 * SCREEN_WIDTH), int(50 / 1440 * SCREEN_HEIGHT)))
        
        text_surf, text_rectangle = text_objects('Succesfully changed ' + str(settings_display) + ' to ' + str(change), SMALL_TEXT, WHITE)
        text_rectangle.center = (int(SCREEN_WIDTH / 1.16), int(SCREEN_HEIGHT * 0.95))
        SCREEN.blit(text_surf, text_rectangle)
        pygame.display.update()
        pygame.time.delay(1000)

    setup_choose_galo_settings_menu(settings_type)
    
    #Define current variable values in the interface
    if settings_type == 'number of players':
        global NPLAYERS
        num_players = NPLAYERS
        choose_settings(num_players)
    elif settings_type == 'number of rounds':
        global NROUNDS
        num_rounds = NROUNDS
        choose_settings(num_rounds)
    elif settings_type == 'board size':
        global BOARDSIZE
        num_board = BOARDSIZE
        choose_settings(num_board)
    elif settings_type == 'bot difficulty':
        global BOT_DIFF
        global difficulty
        difficulty = str(difficulty)
        num_diff = BOT_DIFF
        choose_settings(difficulty)
    elif settings_type == 'number of bot players':
        global NBOTS
        num_bots = NBOTS
        choose_settings(num_bots)

    settingsmenu = True
    while settingsmenu:
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if button(SCREEN,' - ', *CHOOSE_SET_BUTTONS_LAYOUT[0], click):
            pygame.time.delay(100)
            
            if settings_type == 'number of players':
                if num_players <= 2:
                    pass
                elif num_players > 1:
                    num_players -= 1
                choose_settings(num_players)

            elif settings_type == 'number of rounds':
                if num_rounds <= 1:
                    pass
                elif num_rounds > 1:
                    num_rounds -= 1
                choose_settings(num_rounds)

            elif settings_type == 'board size':
                if num_board <= 3:
                    pass
                elif num_board > 3:
                    num_board -= 1
                choose_settings(num_board)

            elif settings_type == 'bot difficulty':
                if difficulty == 'E A S Y':
                    num_diff = 0
                elif difficulty == 'M E D I U M':
                    difficulty = 'E A S Y'
                    num_diff = 0
                elif difficulty == 'H A R D':
                    difficulty = 'M E D I U M'
                    num_diff = 1
                choose_settings(difficulty)

            elif settings_type == 'number of bot players':
                if num_bots > NPLAYERS or num_bots <= 1:
                    pass
                elif num_bots < NPLAYERS:
                    num_bots -= 1
                choose_settings(num_bots)

        elif button(SCREEN,' + ', *CHOOSE_SET_BUTTONS_LAYOUT[1], click):
            pygame.time.delay(100)
            
            if settings_type == 'number of players':
                if num_players >= 9:
                    pass
                elif num_players < 9:
                    num_players += 1
                choose_settings(num_players)
            
            elif settings_type == 'number of rounds':
                num_rounds += 1
                choose_settings(num_rounds)

            elif settings_type == 'board size':
                num_board += 1
                choose_settings(num_board)

            elif settings_type == 'bot difficulty':
                if difficulty == 'E A S Y':
                    difficulty = 'M E D I U M'
                    num_diff = 1
                elif difficulty == 'M E D I U M':
                    difficulty = 'H A R D'
                    num_diff = 2
                elif difficulty == 'H A R D':
                    num_diff = 2 
                choose_settings(difficulty)  

            elif settings_type == 'number of bot players':
                if num_bots >= NPLAYERS - 1:
                    pass
                elif num_bots < NPLAYERS - 1 or num_bots <= 1:
                    num_bots += 1
                choose_settings(num_bots)

        elif button(SCREEN,'C O N F I R M ', *CHOOSE_SET_BUTTONS_LAYOUT[2], click):
            pygame.time.delay(100)

            if settings_type == 'number of players':
                NPLAYERS = int(num_players)
                changes_done(settings_type, NPLAYERS)
                return NPLAYERS

            elif settings_type == 'number of rounds':
                NROUNDS = int(num_rounds)
                changes_done(settings_type, NROUNDS)
                return NROUNDS

            elif settings_type == 'board size':
                BOARDSIZE = int(num_board)
                changes_done(settings_type, BOARDSIZE)
                return BOARDSIZE

            elif settings_type == 'bot difficulty':
                BOT_DIFF = int(num_diff)
                diff_changed = difficulty.replace(' ', '').lower()
                changes_done(settings_type, diff_changed)
                return BOT_DIFF
            
            elif settings_type == 'number of bot players':
                NBOTS = int(num_bots)
                changes_done(settings_type, NBOTS)
                playgame = True
                return NBOTS, playgame

        elif button(SCREEN,'R E T U R N', *CHOOSE_SET_BUTTONS_LAYOUT[3], click):
            pygame.time.delay(100)
            if settings_type == 'number of players':
                return
            
            elif settings_type == 'number of rounds':
                return

            elif settings_type == 'board size':
                return
            
            elif settings_type == 'bot difficulty':
                return

            elif settings_type == 'number of bot players':
                playgame = False
                return NBOTS, playgame

        pygame.display.update()


#SETTINGS MENU
def setup_galo_settings_menu():
    SCREEN.fill(GREY)

    text_surf, text_rectangle = text_objects('SETTINGS', MENU_TEXT, WHITE)
    text_rectangle.center = (int(SCREEN_WIDTH // 2), int(SCREEN_HEIGHT // 4))
    SCREEN.blit(text_surf, text_rectangle)

    pygame.display.update()

def galo_settings_menu():
    setup_galo_settings_menu()
    
    settingsmenu = True
    while settingsmenu:
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        if button(SCREEN,'N U M B E R  O F  P L A Y E R S', *SETTINGS_BUTTONS_LAYOUT[0], click):
            pygame.time.delay(100)
            NPLAYERS = choose_galo_settings_menu('number of players')
            settingsmenu = False
            galo_settings_menu()
            return NPLAYERS

        elif button(SCREEN,'N U M B E R  O F  R O U N D S', *SETTINGS_BUTTONS_LAYOUT[1], click):
            pygame.time.delay(100)
            NROUNDS = choose_galo_settings_menu('number of rounds')
            settingsmenu = False
            galo_settings_menu()
            return NROUNDS

        elif button(SCREEN,'B O A R D  S I Z E', *SETTINGS_BUTTONS_LAYOUT[2], click):
            pygame.time.delay(100)
            BOARDSIZE = choose_galo_settings_menu('board size')
            settingsmenu = False
            galo_settings_menu()
            return BOARDSIZE
        
        elif button(SCREEN,'B O T  D I F F I C U L T Y', *SETTINGS_BUTTONS_LAYOUT[3], click):
            pygame.time.delay(100)
            BOT_DIFF = choose_galo_settings_menu('bot difficulty')
            settingsmenu = False
            galo_settings_menu()
            return BOT_DIFF

        elif button(SCREEN,'R E T U R N', *SETTINGS_BUTTONS_LAYOUT[4], click):
            pygame.time.delay(100)
            return

        pygame.display.update()  


#START GAME MENU
def setup_galo_start_game():
    SCREEN.fill(GREY)

    text_surf, text_rectangle = text_objects('START GAME', MENU_TEXT, WHITE)
    text_rectangle.center = (int(SCREEN_WIDTH // 2), int(SCREEN_HEIGHT // 4))
    SCREEN.blit(text_surf, text_rectangle)

    pygame.display.update()

def galo_start_game():
    setup_galo_start_game()

    startgame = True
    while startgame:
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if button(SCREEN,'P L A Y E R S  V S  P L A Y E R S', *START_GAME_BUTTONS_LAYOUT[0], click):
            pygame.time.delay(100)
            while True:
                if (galo (NPLAYERS, BOARDSIZE, NROUNDS) != -1):
                    break
            return

        elif button(SCREEN,'P L A Y E R S  V S  B O T S', *START_GAME_BUTTONS_LAYOUT[1], click):
            pygame.time.delay(100)
            NBOTS, playgame = choose_galo_settings_menu('number of bot players')
            if playgame == False:
                return 
            else:
                while True:
                    if (galo_BOT (NPLAYERS, BOARDSIZE, NROUNDS, BOT_DIFF, NBOTS) != -1):
                        break 
            return

        elif button(SCREEN,'R E T U R N', *START_GAME_BUTTONS_LAYOUT[2], click):
            pygame.time.delay(100)
            return
            
        pygame.display.update()


#MAIN MENU
def setup_galo_main_menu():
    SCREEN.fill(GREY)
    
    text_surf, text_rectangle = text_objects('TIC-TAC-TOE', MAIN_MENU_TEXT, WHITE)
    text_rectangle.center = (int(SCREEN_WIDTH // 2), int(SCREEN_HEIGHT // 4))
    SCREEN.blit(text_surf, text_rectangle)
    
    text_surf, text_rectangle = text_objects('Created by the HS Table team', SMALL_TEXT, WHITE)
    text_rectangle.center = (int(SCREEN_WIDTH / 1.11), int(SCREEN_HEIGHT * 0.95))
    SCREEN.blit(text_surf, text_rectangle)
    pygame.display.update()

def galo_main_menu():
    setup_galo_main_menu()
    quit_game = False
    
    mainmenu = True
    while mainmenu:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        if button(SCREEN,'S T A R T  G A M E', *MAIN_MENU_BUTTONS_LAYOUT[0], click):
            pygame.time.delay(100)
            galo_start_game()
            mainmenu = False

        elif button(SCREEN,'S E T T I N G S', *MAIN_MENU_BUTTONS_LAYOUT[1], click):
            pygame.time.delay(100)
            galo_settings_menu()
            mainmenu = False

        elif button(SCREEN,'Q U I T   G A M E', *MAIN_MENU_BUTTONS_LAYOUT[2], click):
            pygame.time.delay(100)
            #Default variable names (cada vez que se inicia o jogo as variáveis terão sempre os valores default)
            global NPLAYERS
            global NROUNDS
            global BOARDSIZE
            global NBOTS
            global BOT_DIFF
            global difficulty
            NPLAYERS = 2
            BOARDSIZE = 3
            NROUNDS = 3
            BOT_DIFF = 0
            NBOTS = 1
            quit_game = True
            fadeout_screen(SCREEN, 255)
            return quit_game

        pygame.display.update()


pygame.display.set_caption('TIC-TAC-TOE')