#NOTE: NA ALTURA DE TESTAR NA MESA: 
# - REMOVER LINHAS 1 E 19 ('OS' DEIXA DE SER NECESSÁRIO)
# - COLOCAR FULLSCREEN = True (linha 26)
# - DEFINIR LIMITE PARA NÚMERO DE BOARDSIZE

import os
import pygame
from Color import *
from Galo import *

FPS = 60 #Sets a limit of FPS to be able to run better

#Get fonts
FONT_ORIGAMI = 'fonts/Origami.ttf'
FONT_RAJDHANI = 'fonts/Rajdhani-Medium.ttf'
FONT_RAJDHANI_BOLD = 'fonts/Rajdhani-Bold.ttf'

#DEFINING SCREEN, BUTTONS, TEXT AND LAYOUTS

#Create screen
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1' #Centers the window screen

SCREEN_WIDTH = int(pygame.display.Info().current_w)
SCREEN_HEIGHT = int(pygame.display.Info().current_h)
FULLSCREEN = False
if FULLSCREEN == True:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
    SCREEN_WIDTH, SCREEN_HEIGHT = int(0.75 * SCREEN_WIDTH), int(0.75 * SCREEN_HEIGHT)
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Create buttons (according to screen size)
BUTTON_WIDTH = int(SCREEN_WIDTH * 0.8 // 3)
BUTTON_HEIGHT = int(SCREEN_HEIGHT * 5 // 55)

SMALL_BUTTON_WIDTH = int(70)
SMALL_BUTTON_HEIGHT = int(70)

MAIN_BUTTONS_LAYOUT = [((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 5 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
                       ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 7 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
                       ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 9 // 12, BUTTON_WIDTH, BUTTON_HEIGHT)]

START_GAME_BUTTONS_LAYOUT = [((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 5 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
                             ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 7 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
                             ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 9 // 12, BUTTON_WIDTH, BUTTON_HEIGHT)]

SETTINGS_BUTTONS_LAYOUT = [((SCREEN_WIDTH - BUTTON_WIDTH) // 4, SCREEN_HEIGHT * 5 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
                           ((SCREEN_WIDTH - BUTTON_WIDTH) // 4, SCREEN_HEIGHT * 7 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
                           ((SCREEN_WIDTH - BUTTON_WIDTH) // 1.35, SCREEN_HEIGHT * 5 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
                           ((SCREEN_WIDTH - BUTTON_WIDTH) // 1.35, SCREEN_HEIGHT * 7 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
                           ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 9 // 12, BUTTON_WIDTH, BUTTON_HEIGHT)]

CHOOSE_SET_BUTTONS_LAYOUT = [((SCREEN_WIDTH - BUTTON_WIDTH) // 2.28, SCREEN_HEIGHT * 4 // 12, SMALL_BUTTON_WIDTH, SMALL_BUTTON_WIDTH),
                             ((SCREEN_WIDTH - BUTTON_WIDTH) // 1.16, SCREEN_HEIGHT * 4 // 12, SMALL_BUTTON_WIDTH, SMALL_BUTTON_WIDTH),
                             ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 7 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
                             ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 9 // 12, BUTTON_WIDTH, BUTTON_HEIGHT)]

NUM_ROUNDS_BUTTONS_LAYOUT = [((SCREEN_WIDTH - BUTTON_WIDTH) // 2.28, SCREEN_HEIGHT * 4 // 12, SMALL_BUTTON_WIDTH, SMALL_BUTTON_WIDTH),
                             ((SCREEN_WIDTH - BUTTON_WIDTH) // 1.16, SCREEN_HEIGHT * 4 // 12, SMALL_BUTTON_WIDTH, SMALL_BUTTON_WIDTH),
                             ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 7 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
                             ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 9 // 12, BUTTON_WIDTH, BUTTON_HEIGHT)]

#Create texts
MAIN_MENU_TEXT = pygame.font.Font(FONT_ORIGAMI, int(115 / 1080 * SCREEN_HEIGHT))
MENU_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(115 / 1080 * SCREEN_HEIGHT))
LARGE_TEXT = pygame.font.Font(FONT_RAJDHANI, int(60 / 1440 * SCREEN_HEIGHT))
MEDIUM_TEXT = pygame.font.Font(FONT_RAJDHANI, int(45 / 1440 * SCREEN_HEIGHT))
MEDIUM_BOLD_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(45 / 1440 * SCREEN_HEIGHT))
SMALL_TEXT = pygame.font.Font(FONT_RAJDHANI, int(35 / 1440 * SCREEN_HEIGHT))
SMALL_BOLD_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(35 / 1440 * SCREEN_HEIGHT))
LABEL_TEXT = pygame.font.Font(FONT_RAJDHANI, int(85 / 1440 * SCREEN_HEIGHT))

#BUTTONS AND TEXTS FUNCTIONS

#Define rendered text of button (returns rendered text and it's image dimensions)
def text_objects(text, font, colour):
    text_surface = font.render(text, True, colour) #antialias = True
    text_area = text_surface.get_rect()

    return text_surface, text_area

#Define button style
def button(text, x, y, w, h, click, inactive_button = LIGHT_GREEN, active_button = DARK_GREEN, text_colour = BLACK):
    mouse = pygame.mouse.get_pos() #Store mouse coordinates into the variable
    button_clicked = False

    #If button is clicked, button_clicked turns true and button changes to darker colour
    if x < mouse[0] < x + w and y < mouse[1] < y + h and click and pygame.time.get_ticks() > 100:
        pygame.draw.rect(SCREEN, active_button, (x, y, w, h))
        text_surf, text_rectangle = text_objects(text, MEDIUM_BOLD_TEXT, text_colour)
        text_rectangle.center = (int(x + w / 2), int(y + h / 2)) #Centers text on button
        SCREEN.blit(text_surf, text_rectangle)
        button_clicked = True

    else:
        pygame.draw.rect(SCREEN, inactive_button, (x, y, w, h))
        text_surf, text_rectangle = text_objects(text, MEDIUM_TEXT, text_colour)
        text_rectangle.center = (int(x + w / 2), int(y + h / 2)) #Centers text on button
        SCREEN.blit(text_surf, text_rectangle)

    pygame.display.update()
    return button_clicked

#CHOOSING SETTINGS MENU
def choose_settings_menu(settings_type):
    
    def setup_choose_settings_menu(settings_type):
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

    def changes_done(settings_display, number):
        pygame.draw.rect(SCREEN, GREY, (int(SCREEN_WIDTH / 1.355), int(SCREEN_HEIGHT * 0.935), int(1 / 4 * SCREEN_WIDTH), int(50 / 1440 * SCREEN_HEIGHT)))
        
        text_surf, text_rectangle = text_objects('Succesfully changed ' + str(settings_display) + ' to ' + str(number), SMALL_TEXT, WHITE)
        text_rectangle.center = (int(SCREEN_WIDTH / 1.16), int(SCREEN_HEIGHT * 0.95))
        SCREEN.blit(text_surf, text_rectangle)
        pygame.display.update()
        pygame.time.delay(1000)

    setup_choose_settings_menu(settings_type)
    if settings_type == 'number of players':
        num_players = 2
        choose_settings(num_players)
    elif settings_type == 'number of rounds':
        num_rounds = 3
        choose_settings(num_rounds)
    elif settings_type == 'board size':
        num_board = 3
        choose_settings(num_board)

    settingsmenu = True
    while settingsmenu:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if button(' - ', *CHOOSE_SET_BUTTONS_LAYOUT[0], click):
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

        elif button(' + ', *CHOOSE_SET_BUTTONS_LAYOUT[1], click):
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

        elif button('C O N F I R M ', *CHOOSE_SET_BUTTONS_LAYOUT[2], click):
            pygame.time.delay(100)

            if settings_type == 'number of players':
                global NPLAYERS
                NPLAYERS = int(num_players)
                changes_done(settings_type, NPLAYERS)
                return NPLAYERS

            elif settings_type == 'number of rounds':
                global NROUNDS
                NROUNDS = int(num_rounds)
                changes_done(settings_type, NROUNDS)
                return NROUNDS

            elif settings_type == 'board size':
                global BOARDSIZE
                BOARDSIZE = int(num_board)
                changes_done(settings_type, BOARDSIZE)
                return BOARDSIZE

        elif button('R E T U R N', *CHOOSE_SET_BUTTONS_LAYOUT[3], click):
            pygame.time.delay(100)
            if settings_type == 'number of players':
                return -1, -1
            
            elif settings_type == 'number of rounds':
                return -1

            elif settings_type == 'board size':
                return -1

        pygame.display.update(CHOOSE_SET_BUTTONS_LAYOUT)

    #return NPLAYERS, NROUNDS, BOARDSIZE
"""
#NUMBER OF PLAYERS MENU
def setup_nplayers_menu():
    SCREEN.fill(GREY)
    
    text_surf, text_rectangle = text_objects('Select the number of players (max of 9) ...', LARGE_TEXT, WHITE)
    text_rectangle.center = ((SCREEN_WIDTH // 3.27), (SCREEN_HEIGHT // 5))
    SCREEN.blit(text_surf, text_rectangle)
    
    pygame.display.update()

def nplayers_menu():
    setup_nplayers_menu()

    def choose_players(players_display):
        pygame.draw.rect(SCREEN, LIGHT_GREEN, (int(SCREEN_WIDTH // 2.72), int(SCREEN_HEIGHT * 4 // 12), int(SCREEN_WIDTH * 0.8 // 3), int(70)), int(1))
        pygame.draw.rect(SCREEN, GREY, (int(SCREEN_WIDTH // 2.66), int(SCREEN_HEIGHT * 4.1 // 12), int(SCREEN_WIDTH * 0.75 // 3), int(85 / 1440 * SCREEN_HEIGHT)))

        text_surf, text_rectangle = text_objects(str(players_display), LABEL_TEXT, WHITE)
        text_rectangle.center = (int(SCREEN_WIDTH // 2), int(SCREEN_HEIGHT // 2.67))
        SCREEN.blit(text_surf, text_rectangle)

    def changes_done(numplayers):
        pygame.draw.rect(SCREEN, GREY, (int(SCREEN_WIDTH / 1.355), int(SCREEN_HEIGHT * 0.935), int(1 / 4 * SCREEN_WIDTH), int(50 / 1440 * SCREEN_HEIGHT)))
        
        text_surf, text_rectangle = text_objects('Succesfully changed number of players to '+ str(numplayers), SMALL_TEXT, WHITE)
        text_rectangle.center = (int(SCREEN_WIDTH / 1.16), int(SCREEN_HEIGHT * 0.95))
        SCREEN.blit(text_surf, text_rectangle)
        pygame.display.update()
        pygame.time.delay(1000)

    num_players = 2
    nplayersmenu = True
    while nplayersmenu:
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        choose_players(num_players)
        if button(' - ', *NUM_PLAYERS_BUTTONS_LAYOUT[0], click):
            pygame.time.delay(100)
            
            if num_players <= 2:
                pass

            elif num_players > 1:
                num_players -= 1

            choose_players(num_players)

        elif button(' + ', *NUM_PLAYERS_BUTTONS_LAYOUT[1], click):
            pygame.time.delay(100)
            
            if num_players >= 9:
                pass

            elif num_players < 9:
                num_players += 1

            choose_players(num_players)

        elif button('C O N F I R M ', *NUM_PLAYERS_BUTTONS_LAYOUT[2], click):
            pygame.time.delay(100)
            NPLAYERS = int(num_players)
            BOARDSIZE = int(num_players) + 1 #devia-se adicionar uma opcaod e escolha mesmo para n depender do numero de jogadores

            changes_done(NPLAYERS)

            return NPLAYERS, BOARDSIZE


        elif button('R E T U R N', *NUM_PLAYERS_BUTTONS_LAYOUT[3], click):
            pygame.time.delay(100)
            return -1, -1

        pygame.display.update(NUM_PLAYERS_BUTTONS_LAYOUT)

    return NPLAYERS, BOARDSIZE

#NUMBER OF ROUNDS MENU
def setup_nrounds_menu():
    SCREEN.fill(GREY)

    text_surf, text_rectangle = text_objects('Select the number of rounds...', LARGE_TEXT, WHITE)
    text_rectangle.center = ((SCREEN_WIDTH // 4), (SCREEN_HEIGHT // 5))
    SCREEN.blit(text_surf, text_rectangle)
    
    pygame.display.update()

def nrounds_menu():
    setup_nrounds_menu()

    def choose_rounds(rounds_display):
        pygame.draw.rect(SCREEN, LIGHT_GREEN, (int(SCREEN_WIDTH // 2.72), int(SCREEN_HEIGHT * 4 // 12), int(SCREEN_WIDTH * 0.8 // 3), int(70)), int(1))
        pygame.draw.rect(SCREEN, GREY, (int(SCREEN_WIDTH // 2.66), int(SCREEN_HEIGHT * 4.1 // 12), int(SCREEN_WIDTH * 0.75 // 3), int(85 / 1440 * SCREEN_HEIGHT)))

        text_surf, text_rectangle = text_objects(str(rounds_display), LABEL_TEXT, WHITE)
        text_rectangle.center = (int(SCREEN_WIDTH // 2), int(SCREEN_HEIGHT // 2.67))
        SCREEN.blit(text_surf, text_rectangle)

    def changes_done(numrounds):
        pygame.draw.rect(SCREEN, GREY, (int(SCREEN_WIDTH / 1.355), int(SCREEN_HEIGHT * 0.935), int(1 / 4 * SCREEN_WIDTH), int(50 / 1440 * SCREEN_HEIGHT)))
        
        text_surf, text_rectangle = text_objects('Succesfully changed number of rounds to '+ str(numrounds), SMALL_TEXT, WHITE)
        text_rectangle.center = (int(SCREEN_WIDTH / 1.16), int(SCREEN_HEIGHT * 0.95))
        SCREEN.blit(text_surf, text_rectangle)
        pygame.display.update()
        pygame.time.delay(1000)

    num_rounds = 3
    nroundsmenu = True
    while nroundsmenu:
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        choose_rounds(num_rounds)
        if button(' - ', *NUM_ROUNDS_BUTTONS_LAYOUT[0], click):
            pygame.time.delay(100)
            
            if num_rounds <= 1:
                pass

            elif num_rounds > 1:
                num_rounds -= 1

            choose_rounds(num_rounds)

        elif button(' + ', *NUM_ROUNDS_BUTTONS_LAYOUT[1], click):
            pygame.time.delay(100)
            num_rounds += 1

            choose_rounds(num_rounds)

        elif button('C O N F I R M ', *NUM_ROUNDS_BUTTONS_LAYOUT[2], click):
            pygame.time.delay(100)
            NROUNDS = int(num_rounds)

            changes_done(NROUNDS)

            return NROUNDS

        elif button('R E T U R N', *NUM_ROUNDS_BUTTONS_LAYOUT[3], click):
            pygame.time.delay(100)
            return -1

        pygame.display.update(NUM_ROUNDS_BUTTONS_LAYOUT)

    return NROUNDS
"""

#SETTINGS MENU
def setup_settings_menu():
    SCREEN.fill(GREY)

    text_surf, text_rectangle = text_objects('SETTINGS', MENU_TEXT, WHITE)
    text_rectangle.center = (int(SCREEN_WIDTH // 2), int(SCREEN_HEIGHT // 4))
    SCREEN.blit(text_surf, text_rectangle)

    pygame.display.update()

def settings_menu():
    setup_settings_menu()
    
    settingsmenu = True
    while settingsmenu:
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        if button('N U M B E R  O F  P L A Y E R S', *SETTINGS_BUTTONS_LAYOUT[0], click):
            pygame.time.delay(100)
            NPLAYERS = choose_settings_menu('number of players')
            setup_settings_menu()

        elif button('N U M B E R  O F  R O U N D S', *SETTINGS_BUTTONS_LAYOUT[1], click):
            pygame.time.delay(100)
            NROUNDS = choose_settings_menu('number of rounds')
            setup_settings_menu()

        elif button('B O A R D  S I Z E', *SETTINGS_BUTTONS_LAYOUT[2], click):
            pygame.time.delay(100)
            BOARDSIZE = choose_settings_menu('board size')
            setup_settings_menu()
        
        elif button('B O T  S E T T I N G S', *SETTINGS_BUTTONS_LAYOUT[3], click):
            pygame.time.delay(100)
            #BOT_DIFF = choose_settings_menu('bot difficulty')
            #setup_settings_menu()

        elif button('R E T U R N', *SETTINGS_BUTTONS_LAYOUT[4], click):
            pygame.time.delay(100)
            main_menu()

        pygame.display.update(SETTINGS_BUTTONS_LAYOUT)
        
    return NPLAYERS, BOARDSIZE, NROUNDS, BOT_DIFF

#START GAME MENU
def setup_start_game():
    SCREEN.fill(GREY)

    text_surf, text_rectangle = text_objects('START GAME', MENU_TEXT, WHITE)
    text_rectangle.center = (int(SCREEN_WIDTH // 2), int(SCREEN_HEIGHT // 4))
    SCREEN.blit(text_surf, text_rectangle)

    pygame.display.update()

def start_game():
    setup_start_game()
    
    startgame = True
    while startgame:
        click = False
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #exit() #o exit dá me erros
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if button('P L A Y  W I T H  H U M A N S', *START_GAME_BUTTONS_LAYOUT[0], click):
            pygame.time.delay(100)
            galo(NPLAYERS, BOARDSIZE, NROUNDS)
            main_menu()

        elif button('P L A Y  W I T H  C P U', *START_GAME_BUTTONS_LAYOUT[1], click):
            pygame.time.delay(100)
            galo_BOT(NPLAYERS, BOARDSIZE, NROUNDS, 0)
            main_menu()

        elif button('R E T U R N', *START_GAME_BUTTONS_LAYOUT[2], click):
            pygame.time.delay(100)
            main_menu()

        pygame.display.update(START_GAME_BUTTONS_LAYOUT)

#MAIN MENU
def setup_main_menu():
    SCREEN.fill(GREY)

    text_surf, text_rectangle = text_objects('TIC-TAC-TOE', MAIN_MENU_TEXT, WHITE)
    text_rectangle.center = (int(SCREEN_WIDTH // 2), int(SCREEN_HEIGHT // 4))
    SCREEN.blit(text_surf, text_rectangle)
    
    text_surf, text_rectangle = text_objects('Created by the HS Table team', SMALL_TEXT, WHITE)
    text_rectangle.center = (int(SCREEN_WIDTH / 1.11), int(SCREEN_HEIGHT * 0.95))
    SCREEN.blit(text_surf, text_rectangle)
    pygame.display.update()

def main_menu():
    setup_main_menu()
    
    mainmenu = True
    while mainmenu:
        click = False
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #exit() #o exit dá me erros
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        if button('S T A R T  G A M E', *MAIN_BUTTONS_LAYOUT[0], click):
            pygame.time.delay(100)
            start_game()

        elif button('S E T T I N G S', *MAIN_BUTTONS_LAYOUT[1], click):
            pygame.time.delay(100)
            settings_menu()
            """if playersTemp != -1:
                players = playersTemp
            if boardsizeTemp != -1:
                boardsize = boardsizeTemp
            if rondasTemp != -1:
                rondas = rondasTemp
            main_menu()"""

        elif button('Q U I T   G A M E', *MAIN_BUTTONS_LAYOUT[2], click):
            pygame.time.delay(100)
            exit() # O exit dá me erro
            #pygame.quit()

        pygame.display.update(MAIN_BUTTONS_LAYOUT)


pygame.display.set_caption('TIC-TAC-TOE')
clock = pygame.time.Clock()
NPLAYERS = 2
BOARDSIZE = 3
NROUNDS = 3
BOT_DIFF = 0
main_menu()


"""
#PAUSE MENU
def setup_pause_menu(background):
    SCREEN.blit(background, (0,0))
    background = SCREEN.copy()
    text_surf, text_rectangle = text_objects('PAUSED', MENU_TEXT, WHITE)
    text_rectangle.center = (int(SCREEN_WIDTH // 2), int(SCREEN_HEIGHT // 4)))
    SCREEN.blit(text_surf, text_rect)
    pygame.display.update()
    
    return background

def pause_menu(player):
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA, 32)
    background.fill(*LIGHT_BLACK, 160)
    background = setup_pause_menu(background)

    paused = True
    while paused:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if button('RESUME GAME', *BUTTONS_LAYOUT[0], click):
            return 'Resume'
        elif button('RESTART GAME', *BUTTONS_LAYOUT[1], click):
            return 'Restart'
        elif button('RETURN TO MAIN MENU', *BUTTONS_LAYOUT[2], click):
            return 'Main Menu'
        elif button('QUIT GAME', *BUTTONS_LAYOUT[3], click):
            exit()
        pygame.display.update(button_layout_4)
"""