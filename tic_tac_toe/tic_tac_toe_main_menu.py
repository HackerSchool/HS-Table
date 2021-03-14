"""
SELFNOTES:

font.render(text, antialias, color, background = None): draws text on a new surface

get_rect: Obtain dimensions of rendered text image with width and height attributes

pygame.time.get_ticks(): get time in miliseconds since pygame.init() was called

pygame.draw.rect(screen, colour, (x, y, width, height), thickness): draws a rectangle
    x and y: coordinates of the upper left hand corner
    width and height: button dimensions
    thickness: line thickness (= 0 for filled rectangle)

MIGHT HAVE TO ADD ANTI-ALIASING - CREATE A FUNCTION FOR IT USING MODULE gfxdraw


pygame.key.get_pressed(): 
    
"""

import os
import pygame

FPS = 60 #Sets a limit of FPS to be able to run better

#Colours
BLACK = (0, 0, 0)
LIGHT_BLACK = (20, 20, 20)
GREY = (28, 27, 27)
WHITE = (207, 207, 207)
LIGHT_GREEN = (109, 215, 143)
DARK_GREEN = (79, 161, 106)

#Get fonts
FONT_ORIGAMI = 'assets/fonts/Origami.ttf'
FONT_AZONIX = 'assets/fonts/Azonix.otf'
FONT_AZONIX_BOLD = 'assets/fonts/Azonix_bold.otf'
FONT_RAJDHANI = 'assets/fonts/Rajdhani-Medium.ttf'
FONT_RAJDHANI_BOLD = 'assets/fonts/Rajdhani-Bold.ttf'


#DEFINING SCREEN, BUTTONS, TEXT AND LAYOUTS

#Create screen
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1' #Centers the window screen

SCREEN_WIDTH = int(pygame.display.Info().current_w)
SCREEN_HEIGHT = int(pygame.display.Info().current_h)
FULLSCREEN = True
if FULLSCREEN == True:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
    SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT = int(0.50 * SCREEN_WIDTH), int(0.50 * SCREEN_HEIGHT)
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Create buttons (according to screen size)
BUTTON_WIDTH = int(SCREEN_WIDTH * 0.8 // 3)
BUTTON_HEIGHT = int(SCREEN_HEIGHT * 5 // 70)

BUTTONS_LAYOUT = [((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 3.5 // 9, BUTTON_WIDTH, BUTTON_HEIGHT),
                   ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 4.5 // 9, BUTTON_WIDTH, BUTTON_HEIGHT),
                   ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 5.5 // 9, BUTTON_WIDTH, BUTTON_HEIGHT),
                   ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 6.5 // 9, BUTTON_WIDTH, BUTTON_HEIGHT)] 

#Create texts
MENU_TEXT = pygame.font.Font(FONT_ORIGAMI, int(115 / 1080 * SCREEN_HEIGHT))
BIG_TEXT = pygame.font.Font(FONT_RAJDHANI, int(40 / 1080 * SCREEN_HEIGHT))
MEDIUM_TEXT = pygame.font.Font(FONT_RAJDHANI, int(35 / 1440 * SCREEN_HEIGHT))
MEDIUM_BOLD_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(35 / 1440 * SCREEN_HEIGHT))
SMALL_TEXT = pygame.font.Font(FONT_RAJDHANI, int(25 / 1440 * SCREEN_HEIGHT))
SMALL_BOLD_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(25 / 1440 * SCREEN_HEIGHT))
EVEN_SMALLER_TEXT = pygame.font.Font(FONT_RAJDHANI, int(20 / 1440 * SCREEN_HEIGHT))


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

#PERSONALIZED GAME MENU
def setup_personalized_menu():
    SCREEN.fill(GREY)
    text_surf, text_rect = text_objects('PERSONALIZED GAME', MENU_TEXT, WHITE)
    text_rect.center = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 4))
    SCREEN.blit(text_surf, text_rect)
    
    text_surf, text_rect = text_objects('Choose the number of players:', MENU_TEXT, WHITE)
    text_rect.center = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 4))
    SCREEN.blit(text_surf, text_rect)
    pygame.display.update()

def personalized_menu():
    setup_personalized_menu()
    pers_menu = True
    while pers_menu:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True


   
"""
#PAUSE MENU
def setup_pause_menu(background):
    SCREEN.blit(background, (0,0))
    background = SCREEN.copy()
    text_surf, text_rect = text_objects('PAUSED', MENU_TEXT, WHITE)
    text_rect.center = (int(SCREEN_WIDTH // 2), int(SCREEN_HEIGHT // 4)))
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


#MAIN MENU
def setup_main_menu():
    SCREEN.fill(GREY)

    text_surf, text_rect = text_objects('TIC-TAC-TOE', MENU_TEXT, WHITE)
    text_rect.center = (int(SCREEN_WIDTH // 2), int(SCREEN_HEIGHT // 4))
    SCREEN.blit(text_surf, text_rect)
    
    text_surf, text_rect = text_objects('Created by the HS Table team', MEDIUM_TEXT, WHITE)
    text_rect.center = (int(SCREEN_WIDTH / 1.11), int(SCREEN_HEIGHT * 0.95))
    SCREEN.blit(text_surf, text_rect)
    pygame.display.update()

def main_menu():
    setup_main_menu()
    start_game = False

    #Create main menu game loop
    mainmenu = True
    while mainmenu:
        click = False
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        #SELFNOTE: ONLY QUIT GAME BUTTON IS WORKING
        if button('DEFAULT GAME (2 PLAYERS)', *BUTTONS_LAYOUT[0], click):
            start_game = True
        elif button('PERSONALIZED GAME', *BUTTONS_LAYOUT[1], click):
            pass
        elif button('SETTINGS', *BUTTONS_LAYOUT[2], click):
            pass
        elif button('QUIT GAME', *BUTTONS_LAYOUT[3], click):
            exit()

        #if start_game:
            #MISSING CODE HERE

        pygame.display.update(BUTTONS_LAYOUT)


pygame.display.set_caption('TIC-TAC-TOE')
clock = pygame.time.Clock()
main_menu()