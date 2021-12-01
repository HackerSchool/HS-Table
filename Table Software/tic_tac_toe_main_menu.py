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

def galo_settings_menu_setup(settings):
    SCREEN.fill(GREY)
    text_surf, text_rectangle = text_objects('Select the ' + settings + ' settings ...', LARGE_TEXT, WHITE)
    text_rectangle.center = ((SCREEN_WIDTH * 0.20), (SCREEN_HEIGHT * 0.10))
    SCREEN.blit(text_surf, text_rectangle)
    pygame.display.update()

def choose_settings(settings_display, init_rect_position, rect_height):
    def draw_display(x_position, y_position):
        pygame.draw.rect(SCREEN, LIGHT_GREEN, (x_position, y_position, int(SCREEN_WIDTH // 5 + 5), int(SCREEN_HEIGHT * 0.9 // 12)), 1)
        pygame.draw.rect(SCREEN, GREY, (x_position + 1, y_position + 1, int(SCREEN_WIDTH // 5 - 1), int(SCREEN_HEIGHT * 0.8 // 12)))

    rect_position = init_rect_position
    for setting in settings_display:
        draw_display(int(SCREEN_WIDTH * 0.50 + SCREEN_HEIGHT * 0.9 // 12), int((SCREEN_HEIGHT // 6.5) * rect_position))
        text_surf, text_rectangle = text_objects(str(setting), LABEL_TEXT, WHITE)
        text_rectangle.center = (int((SCREEN_WIDTH * 0.50 + SCREEN_HEIGHT * 0.9 // 12) + (int(SCREEN_WIDTH // 5 + 5)// 2)), (int(SCREEN_HEIGHT // 6.5) * rect_position) + int(SCREEN_HEIGHT * 0.9 // 12) // 2)
        SCREEN.blit(text_surf, text_rectangle)
        rect_position += rect_height
    
    pygame.display.update()

def write_settings(name, x_position, y_position):
    text_surf, text_rectangle = text_objects(name, LARGE_TEXT, WHITE)
    text_rectangle.center = (x_position, y_position)
    SCREEN.blit(text_surf, text_rectangle)

def changes_done():
    fadeout_screen(SCREEN)
    dots = ['.', '..', '...']
    repeat = 2
    for dot in dots * repeat:
        pygame.draw.rect(SCREEN, BLACK, (int(SCREEN_WIDTH * 0.75), int(SCREEN_HEIGHT * 0.935), int(1 / 4 * SCREEN_WIDTH), int(50 / 1440 * SCREEN_HEIGHT)))
        text_surf, text_rectangle = text_objects('Starting game' + dot, MEDIUM_TEXT, WHITE)
        text_rectangle.center = (int(SCREEN_WIDTH * 0.90), int(SCREEN_HEIGHT * 0.95))
        SCREEN.blit(text_surf, text_rectangle)
        pygame.display.update()
        pygame.time.delay(250)
        
#BOT SETTINGS MENU
def galo_bot_settings_menu():

    #Define current variable values in the interface for bot settings
    global playgame
    global difficulty
    global BOT_DIFF
    num_diff = BOT_DIFF
    global NBOTS
    num_bots = NBOTS
    settings_display = [difficulty, num_bots]
    galo_settings_menu_setup('bot')
    write_settings('Bot Difficulty:', int(SCREEN_WIDTH * 0.50 - 340), int(SCREEN_HEIGHT // 6.5 * 1.5) + int(SCREEN_HEIGHT * 0.9 // 12) // 2)
    write_settings('Number of Bots:', int(SCREEN_WIDTH * 0.50 - 320), int(SCREEN_HEIGHT // 6.5 * 2.5) + int(SCREEN_HEIGHT * 0.9 // 12) // 2)
    choose_settings(settings_display, 1.5, 1)

    settingsmenu = True
    while settingsmenu:
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        # Bot difficulty
        if button(SCREEN,' - ', *CHOOSE_SET_BUTTONS_LAYOUT[6], click):
            #pygame.time.delay(100)
            if difficulty == 'E A S Y':
                num_diff = 0
            elif difficulty == 'M E D I U M':
                difficulty = 'E A S Y'
                num_diff = 0
            elif difficulty == 'H A R D':
                difficulty = 'M E D I U M'
                num_diff = 1
            settings_display[0] = difficulty
            choose_settings(settings_display, 1.5, 1)

        elif button(SCREEN,' + ', *CHOOSE_SET_BUTTONS_LAYOUT[7], click):
            #pygame.time.delay(100)
            if difficulty == 'E A S Y':
                difficulty = 'M E D I U M'
                num_diff = 1
            elif difficulty == 'M E D I U M':
                difficulty = 'H A R D'
                num_diff = 2
            elif difficulty == 'H A R D':
                num_diff = 2 
            settings_display[0] = difficulty
            choose_settings(settings_display, 1.5, 1)

        # Number of bot players
        if button(SCREEN,' - ', *CHOOSE_SET_BUTTONS_LAYOUT[8], click):
            #pygame.time.delay(100)
            if num_bots > NPLAYERS or num_bots <= 1:
                pass
            elif num_bots < NPLAYERS:
                num_bots -= 1
            settings_display[1] = num_bots
            choose_settings(settings_display, 1.5, 1)

        elif button(SCREEN,' + ', *CHOOSE_SET_BUTTONS_LAYOUT[9], click):
            #pygame.time.delay(100)
            if num_bots >= NPLAYERS - 1:
                pass
            elif num_bots < NPLAYERS - 1 or num_bots <= 1:
                num_bots += 1
            settings_display[1] = num_bots
            choose_settings(settings_display, 1.5, 1)

        if button(SCREEN,'C O N F I R M ', *CHOOSE_SET_BUTTONS_LAYOUT[12], click):
            #pygame.time.delay(100)
            BOT_DIFF = int(num_diff)
            NBOTS = int(num_bots)
            playgame = True
            changes_done()
            return BOT_DIFF, NBOTS, playgame

        elif button(SCREEN,'R E T U R N', *CHOOSE_SET_BUTTONS_LAYOUT[13], click):
            #pygame.time.delay(100)
            playgame = False
            return BOT_DIFF, NBOTS, playgame
    
        pygame.display.update()


#GENERAL SETTINGS MENU
def galo_general_settings_menu(bot_settings):
    #Define current variable values in the interface for general settings
    global NPLAYERS
    num_players = NPLAYERS
    global NROUNDS
    num_rounds = NROUNDS
    global BOARDSIZE
    num_board = BOARDSIZE
    settings_display = [num_players, num_rounds, num_board]

    galo_settings_menu_setup('general')
    write_settings('Number of Players:', int(SCREEN_WIDTH * 0.50 - 300), int(SCREEN_HEIGHT // 6.5 * 1.2) + int(SCREEN_HEIGHT * 0.9 // 12) // 2)
    write_settings('Number of Rounds:', int(SCREEN_WIDTH * 0.50 - 300), int(SCREEN_HEIGHT // 6.5 * 2.2) + int(SCREEN_HEIGHT * 0.9 // 12) // 2)
    write_settings('Board Size:', int(SCREEN_WIDTH * 0.50 - 355), int(SCREEN_HEIGHT // 6.5 * 3.2) + int(SCREEN_HEIGHT * 0.9 // 12) // 2)
    choose_settings(settings_display, 1.2, 1)

    settingsmenu = True
    while settingsmenu:
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        # Number of players
        if button(SCREEN,' - ', *CHOOSE_SET_BUTTONS_LAYOUT[0], click):
            #pygame.time.delay(100)
            if num_players <= 2:
                pass
            elif num_players > 1:
                num_players -= 1
            settings_display[0] = num_players
            choose_settings(settings_display, 1.2, 1)

        elif button(SCREEN,' + ', *CHOOSE_SET_BUTTONS_LAYOUT[1], click):
            #pygame.time.delay(100)
            if num_players >= 9:
                pass
            elif num_players < 9:
                num_players += 1
            settings_display[0] = num_players
            choose_settings(settings_display, 1.2, 1)

        # Number of rounds
        if button(SCREEN,' - ', *CHOOSE_SET_BUTTONS_LAYOUT[2], click):
            #pygame.time.delay(100)
            if num_rounds <= 1:
                pass
            elif num_rounds > 1:
                num_rounds -= 1
            settings_display[1] = num_rounds
            choose_settings(settings_display, 1.2, 1)

        elif button(SCREEN,' + ', *CHOOSE_SET_BUTTONS_LAYOUT[3], click):
            #pygame.time.delay(100)
            num_rounds += 1
            settings_display[1] = num_rounds
            choose_settings(settings_display, 1.2, 1)

        # Board size
        if button(SCREEN,' - ', *CHOOSE_SET_BUTTONS_LAYOUT[4], click):
            #pygame.time.delay(100)
            if num_board <= 3:
                pass
            elif num_board > 3:
                num_board -= 1
            settings_display[2] = num_board
            choose_settings(settings_display, 1.2, 1)

        elif button(SCREEN,' + ', *CHOOSE_SET_BUTTONS_LAYOUT[5], click):
            #pygame.time.delay(100)
            num_board += 1
            settings_display[2] = num_board
            choose_settings(settings_display, 1.2, 1)

        if bot_settings == True:
            if button(SCREEN, 'N E X T', *CHOOSE_SET_BUTTONS_LAYOUT[10], click):
                #pygame.time.delay(100)
                global BOT_DIFF
                global NBOTS
                NPLAYERS = int(num_players)
                NROUNDS = int(num_rounds)
                BOARDSIZE = int(num_board)
                BOT_DIFF, NBOTS, playgame = galo_bot_settings_menu()
                if playgame == True:
                    return NPLAYERS, NROUNDS, BOARDSIZE, playgame
                else:
                    settingsmenu = False
                    galo_general_settings_menu(True)
                    return NPLAYERS, NROUNDS, BOARDSIZE, playgame
        else:
            if button(SCREEN, 'C O N F I R M', *CHOOSE_SET_BUTTONS_LAYOUT[10], click):
                #pygame.time.delay(100)
                NPLAYERS = int(num_players)
                NROUNDS = int(num_rounds)
                BOARDSIZE = int(num_board)
                playgame = True
                changes_done()
                return NPLAYERS, NROUNDS, BOARDSIZE, playgame

        if button(SCREEN,'R E T U R N', *CHOOSE_SET_BUTTONS_LAYOUT[11], click):
            #pygame.time.delay(100)
            playgame = False
            return NPLAYERS, NROUNDS, BOARDSIZE, playgame
    
        pygame.display.update()


#MAIN MENU
def galo_main_menu():

    SCREEN.fill(GREY)
    text_surf, text_rectangle = text_objects('TIC-TAC-TOE', MAIN_MENU_TEXT, WHITE)
    text_rectangle.center = (int(SCREEN_WIDTH // 2), int(SCREEN_HEIGHT // 4))
    SCREEN.blit(text_surf, text_rectangle)
    text_surf, text_rectangle = text_objects('Created by the HS Table team', SMALL_TEXT, WHITE)
    text_rectangle.center = (int(SCREEN_WIDTH / 1.11), int(SCREEN_HEIGHT * 0.95))
    SCREEN.blit(text_surf, text_rectangle)

    global NPLAYERS
    global NROUNDS
    global BOARDSIZE
    global NBOTS
    global BOT_DIFF
    global difficulty
    quit_game = False
    
    mainmenu = True
    while mainmenu:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        if button(SCREEN,'P L A Y E R S  V S  P L A Y E R S', *MAIN_MENU_BUTTONS_LAYOUT[0], click):
            #pygame.time.delay(100)
            NPLAYERS, NROUNDS, BOARDSIZE, playgame = galo_general_settings_menu(False)
            if playgame == False:
                NPLAYERS = 2
                BOARDSIZE = 3
                NROUNDS = 3
                BOT_DIFF = 0
                NBOTS = 1
                difficulty = 'E A S Y'
            else:
                while True:
                    if (galo (NPLAYERS, BOARDSIZE, NROUNDS) != -1):
                        NPLAYERS = 2
                        BOARDSIZE = 3
                        NROUNDS = 3
                        BOT_DIFF = 0
                        NBOTS = 1
                        difficulty = 'E A S Y'
                        break
            mainmenu = False

        elif button(SCREEN,'P L A Y E R S  V S  B O T S', *MAIN_MENU_BUTTONS_LAYOUT[1], click):
            #pygame.time.delay(100)
            NPLAYERS, NROUNDS, BOARDSIZE, playgame = galo_general_settings_menu(True)
            if playgame == False:
                NPLAYERS = 2
                BOARDSIZE = 3
                NROUNDS = 3
                BOT_DIFF = 0
                NBOTS = 1
                difficulty = 'E A S Y'
            else:
                while True:
                    if (galo_BOT (NPLAYERS, BOARDSIZE, NROUNDS, BOT_DIFF, NBOTS) != -1):
                        NPLAYERS = 2
                        BOARDSIZE = 3
                        NROUNDS = 3
                        BOT_DIFF = 0
                        NBOTS = 1
                        difficulty = 'E A S Y'
                        break 
            mainmenu = False

        elif button(SCREEN,'Q U I T   G A M E', *MAIN_MENU_BUTTONS_LAYOUT[2], click):
            #pygame.time.delay(100)
            #Default variable names (cada vez que se inicia o jogo as variáveis terão sempre os valores default)
            NPLAYERS = 2
            BOARDSIZE = 3
            NROUNDS = 3
            BOT_DIFF = 0
            NBOTS = 1
            quit_game = True
            fadeout_screen(SCREEN)
            return quit_game

        pygame.display.update()


pygame.display.set_caption('TIC-TAC-TOE')