import os
import pygame
from subprocess import call
#import tic_tac_toe_main_menu

FPS = 60 #Sets a limit of FPS to be able to run better

#Colours
BLACK = (0, 0, 0)
LIGHT_BLACK = (20, 20, 20)
GREY = (28, 27, 27)
WHITE = (207, 207, 207)
LIGHT_GREEN = (109, 215, 143)
DARK_GREEN = (79, 161, 106)

#Load fonts
FONT_ORIGAMI = 'assets/fonts/Origami.ttf'
FONT_RAJDHANI = 'assets/fonts/Rajdhani-Medium.ttf'
FONT_RAJDHANI_BOLD = 'assets/fonts/Rajdhani-Bold.ttf'

#DEFINING SCREEN, BUTTONS, TEXT AND LAYOUTS
#Create screen
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1' #Centers the window screen

SCREEN_WIDTH = int(pygame.display.Info().current_w)
SCREEN_HEIGHT = int(pygame.display.Info().current_h)
print(SCREEN_WIDTH, SCREEN_HEIGHT)

Fullscreen = True
if Fullscreen == True:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
    SCREEN_WIDTH, SCREEN_HEIGHT = int(0.75 * SCREEN_WIDTH), int(0.75 * SCREEN_HEIGHT)
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Load images
def display_background():
    BACKGROUND_IMAGE = pygame.image.load("assets/images/Logo_HS_Table 1.png")
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
    SCREEN.blit(BACKGROUND_IMAGE, [0,0])  

#Create buttons (according to screen size)
APP_BUTTON_WIDTH = int(170)
APP_BUTTON_HEIGHT = int(170)

SETTINGS_BUTTON_WIDTH = int(SCREEN_WIDTH * 0.8 // 3)
SETTINGS_BUTTON_HEIGHT = int(SCREEN_HEIGHT * 5 // 55)

SMALL_BUTTON_WIDTH = int(80)
SMALL_BUTTON_HEIGHT = int(80)

QUESTION_BUTTON_WIDTH = int(SCREEN_WIDTH * 0.8 // 3)
QUESTION_BUTTON_HEIGHT = int(SCREEN_HEIGHT * 5 // 55)

MAIN_BUTTONS_LAYOUT = [((SCREEN_WIDTH - SMALL_BUTTON_WIDTH) // 1.0005, SCREEN_HEIGHT * 10.9 // 12, SMALL_BUTTON_WIDTH, SMALL_BUTTON_HEIGHT),
                       ((SCREEN_WIDTH - APP_BUTTON_WIDTH) // 10, SCREEN_HEIGHT * 1 // 12, APP_BUTTON_WIDTH, APP_BUTTON_HEIGHT),
                       ((SCREEN_WIDTH - APP_BUTTON_WIDTH) // 3, SCREEN_HEIGHT * 1 // 12, APP_BUTTON_WIDTH, APP_BUTTON_HEIGHT)]

SETTINGS_BUTTONS_LAYOUT = [((SCREEN_WIDTH - SETTINGS_BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 5 // 12, SETTINGS_BUTTON_WIDTH, SETTINGS_BUTTON_HEIGHT),
                           ((SCREEN_WIDTH - SETTINGS_BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 7 // 12, SETTINGS_BUTTON_WIDTH, SETTINGS_BUTTON_HEIGHT),
                           ((SCREEN_WIDTH - SETTINGS_BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 9 // 12, SETTINGS_BUTTON_WIDTH, SETTINGS_BUTTON_HEIGHT),
                           ((SCREEN_WIDTH - SETTINGS_BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 10 // 12, SETTINGS_BUTTON_WIDTH, SETTINGS_BUTTON_HEIGHT)]

QUESTION_BUTTONS_LAYOUT = [((SCREEN_WIDTH - QUESTION_BUTTON_WIDTH) // 4.5, SCREEN_HEIGHT * 5 // 12, QUESTION_BUTTON_WIDTH, QUESTION_BUTTON_HEIGHT),
                           ((SCREEN_WIDTH - QUESTION_BUTTON_WIDTH) // 1.3, SCREEN_HEIGHT * 5 // 12, QUESTION_BUTTON_WIDTH, QUESTION_BUTTON_HEIGHT)]

#Create texts
MAIN_MENU_TEXT = pygame.font.Font(FONT_ORIGAMI, int(115 / 1080 * SCREEN_HEIGHT))
LARGE_MIDDLE_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(115 / 1080 * SCREEN_HEIGHT))
LARGE_TEXT = pygame.font.Font(FONT_RAJDHANI, int(60 / 1440 * SCREEN_HEIGHT))
MEDIUM_TEXT = pygame.font.Font(FONT_RAJDHANI, int(45 / 1440 * SCREEN_HEIGHT))
MEDIUM_BOLD_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(45 / 1440 * SCREEN_HEIGHT))
SMALL_TEXT = pygame.font.Font(FONT_RAJDHANI, int(35 / 1440 * SCREEN_HEIGHT))
SMALL_BOLD_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(35 / 1440 * SCREEN_HEIGHT))
LABEL_TEXT = pygame.font.Font(FONT_RAJDHANI, int(85 / 1440 * SCREEN_HEIGHT))
HS_TEXT = pygame.font.Font(FONT_ORIGAMI, int(100 / 1440 * SCREEN_HEIGHT))

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
        if text == 'H':
            pygame.draw.rect(SCREEN, active_button, (x, y, w, h))
            text_surf, text_rectangle = text_objects(text, HS_TEXT, text_colour)
            text_rectangle.center = (int(x + w / 2), int(y + h / 2))
            SCREEN.blit(text_surf, text_rectangle)
            button_clicked = True

        elif text == 'TIC-TAC-TOE' or text == 'POLL GAME': #SELFNOTE: ADD REST OF GAMES HERE ONCE THEY'RE DONE
            pygame.draw.rect(SCREEN, active_button, (x, y, w, h))
            text_surf, text_rectangle = text_objects(text, SMALL_BOLD_TEXT, text_colour)
            text_rectangle.center = (int(x + w / 2), int(y + h / 1.2))
            SCREEN.blit(text_surf, text_rectangle)
            button_clicked = True

        else:
            pygame.draw.rect(SCREEN, active_button, (x, y, w, h))
            text_surf, text_rectangle = text_objects(text, MEDIUM_BOLD_TEXT, text_colour)
            text_rectangle.center = (int(x + w / 2), int(y + h / 2))
            SCREEN.blit(text_surf, text_rectangle)
            button_clicked = True

    else:
        if text == 'H':
            pygame.draw.rect(SCREEN, inactive_button, (x, y, w, h))
            text_surf, text_rectangle = text_objects(text, HS_TEXT, text_colour)
            text_rectangle.center = (int(x + w / 2), int(y + h / 2))
            SCREEN.blit(text_surf, text_rectangle)

        elif text == 'TIC-TAC-TOE' or text == 'POLL GAME': #SELFNOTE: ADD REST OF GAMES HERE ONCE THEY'RE DONE
            pygame.draw.rect(SCREEN, inactive_button, (x, y, w, h))
            text_surf, text_rectangle = text_objects(text, SMALL_TEXT, text_colour)
            text_rectangle.center = (int(x + w / 2), int(y + h / 1.2))
            SCREEN.blit(text_surf, text_rectangle)

        else:
            pygame.draw.rect(SCREEN, inactive_button, (x, y, w, h))
            text_surf, text_rectangle = text_objects(text, MEDIUM_TEXT, text_colour)
            text_rectangle.center = (int(x + w / 2), int(y + h / 2))
            SCREEN.blit(text_surf, text_rectangle)


    pygame.display.update()
    return button_clicked

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

            if button('Y E S', *QUESTION_BUTTONS_LAYOUT[0], click): #Desativei botão para não haver desligos acidentais de pc's
                pygame.time.delay(100)
                #os.system('shutdown /s /t 0') #Windows
                #call("sudo shutdown -h now", shell = True) #Raspberry pi

            elif button('N O', *QUESTION_BUTTONS_LAYOUT[1], click):
                pygame.time.delay(100)
                main_environment()

        elif turnoff_system == 'Restart':
            setup_turnoff_system_menu(turnoff_system)

            if button('Y E S', *QUESTION_BUTTONS_LAYOUT[0], click): #Desativei botão para não haver desligos acidentais de pc's
                pygame.time.delay(100)
                #os.system("shutdown /r /t 0") #Windows
                #call("sudo shutdown -r now", shell=True) #Raspberry pi

            elif button('N O', *QUESTION_BUTTONS_LAYOUT[1], click):
                pygame.time.delay(100)
                main_environment()

        elif turnoff_system == 'Hibernate':
            setup_turnoff_system_menu(turnoff_system)

            if button('Y E S', *QUESTION_BUTTONS_LAYOUT[0], click): #Desativei botão para não haver desligos acidentais de pc's
                pygame.time.delay(100)
                #os.system("shutdown /h /t 0") #Windows
                #Couldn't find any hibernate command for raspberry pi

            elif button('N O', *QUESTION_BUTTONS_LAYOUT[1], click):
                pygame.time.delay(100)
                main_environment()

        pygame.display.update(QUESTION_BUTTONS_LAYOUT)


#SETTINGS MENU  
def settings_menu():
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
        
        if button('H', *MAIN_BUTTONS_LAYOUT[0], click):
            pygame.time.delay(100)
            main_environment()

        if button('S H U T D O W N', *SETTINGS_BUTTONS_LAYOUT[0], click):
            pygame.time.delay(100)
            turnoff_system_menu('Shutdown')

        elif button('R E S T A R T', *SETTINGS_BUTTONS_LAYOUT[1], click):
            pygame.time.delay(100)
            turnoff_system_menu('Restart')

        elif button('H I B E R N A T E', *SETTINGS_BUTTONS_LAYOUT[2], click):
            pygame.time.delay(100)
            turnoff_system_menu('Hibernate')

        pygame.display.update(MAIN_BUTTONS_LAYOUT)


#MAIN ENVIRONMENT
def main_environment():
    display_background()

    envmenu = True
    while envmenu:
        click = False
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        if button('H', *MAIN_BUTTONS_LAYOUT[0], click):
            pygame.time.delay(100)
            settings_menu()

        elif button('TIC-TAC-TOE', *MAIN_BUTTONS_LAYOUT[1], click):
            pygame.time.delay(100)
            #tictactoe_mainmenu

        elif button('POLL GAME', *MAIN_BUTTONS_LAYOUT[2], click):
            pygame.time.delay(100)
            #pollgame_mainmenu

        pygame.display.update(MAIN_BUTTONS_LAYOUT)

clock = pygame.time.Clock()
main_environment()