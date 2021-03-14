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
FONT_ORIGAMI = 'fonts/Origami.ttf'
FONT_RAJDHANI = 'fonts/Rajdhani-Medium.ttf'
FONT_RAJDHANI_BOLD = 'fonts/Rajdhani-Bold.ttf'


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
    SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT = int(0.75 * SCREEN_WIDTH), int(0.75 * SCREEN_HEIGHT)
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Create buttons (according to screen size)
BUTTON_WIDTH = int(SCREEN_WIDTH * 0.8 // 3)
BUTTON_HEIGHT = int(SCREEN_HEIGHT * 5 // 55)

MAIN_BUTTONS_LAYOUT = [((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 5 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
                       ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 7 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
                       ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 9 // 12, BUTTON_WIDTH, BUTTON_HEIGHT)] 

NUM_PLAYERS_BUTTONS_LAYOUT = [((SCREEN_WIDTH - BUTTON_WIDTH) // 3.5, SCREEN_HEIGHT * 5 // 16, BUTTON_WIDTH, BUTTON_HEIGHT),
                              ((SCREEN_WIDTH - BUTTON_WIDTH) // 3.5, SCREEN_HEIGHT * 7 // 16, BUTTON_WIDTH, BUTTON_HEIGHT),
                              ((SCREEN_WIDTH - BUTTON_WIDTH) // 3.5, SCREEN_HEIGHT * 9 // 16, BUTTON_WIDTH, BUTTON_HEIGHT),
                              ((SCREEN_WIDTH - BUTTON_WIDTH) // 3.5, SCREEN_HEIGHT * 11 // 16, BUTTON_WIDTH, BUTTON_HEIGHT),
                              ((SCREEN_WIDTH - BUTTON_WIDTH) // 1.4, SCREEN_HEIGHT * 5 // 16, BUTTON_WIDTH, BUTTON_HEIGHT),
                              ((SCREEN_WIDTH - BUTTON_WIDTH) // 1.4, SCREEN_HEIGHT * 7 // 16, BUTTON_WIDTH, BUTTON_HEIGHT),
                              ((SCREEN_WIDTH - BUTTON_WIDTH) // 1.4, SCREEN_HEIGHT * 9 // 16, BUTTON_WIDTH, BUTTON_HEIGHT),
                              ((SCREEN_WIDTH - BUTTON_WIDTH) // 1.4, SCREEN_HEIGHT * 11 // 16, BUTTON_WIDTH, BUTTON_HEIGHT),
                              ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 10 // 12, BUTTON_WIDTH, BUTTON_HEIGHT)]

#Create texts
MAIN_MENU_TEXT = pygame.font.Font(FONT_ORIGAMI, int(115 / 1080 * SCREEN_HEIGHT))
MENU_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(115 / 1080 * SCREEN_HEIGHT))
LARGE_TEXT = pygame.font.Font(FONT_RAJDHANI, int(60 / 1440 * SCREEN_HEIGHT))
MEDIUM_TEXT = pygame.font.Font(FONT_RAJDHANI, int(45 / 1440 * SCREEN_HEIGHT))
MEDIUM_BOLD_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(45 / 1440 * SCREEN_HEIGHT))
SMALL_TEXT = pygame.font.Font(FONT_RAJDHANI, int(35 / 1440 * SCREEN_HEIGHT))
SMALL_BOLD_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(35 / 1440 * SCREEN_HEIGHT))


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

#SETTINGS MENU
def setup_settings_menu():
    SCREEN.fill(GREY)
    text_surf, text_rectangle = text_objects('Select the number of players...', LARGE_TEXT, WHITE)
    text_rectangle.center = ((SCREEN_WIDTH // 4), (SCREEN_HEIGHT // 5))
    SCREEN.blit(text_surf, text_rectangle)
    
    pygame.display.update()

def settings_menu():
    setup_settings_menu()

    def changes_done(numplayers):
        pygame.draw.rect(SCREEN, GREY, (int(SCREEN_WIDTH / 1.355), int(SCREEN_HEIGHT * 0.935), int(1 / 4 * SCREEN_WIDTH), int(50 / 1440 * SCREEN_HEIGHT)))
        
        text_surf, text_rectangle = text_objects('Succesfully changed number of players to '+ str(numplayers), SMALL_TEXT, WHITE)
        text_rectangle.center = (int(SCREEN_WIDTH / 1.16), int(SCREEN_HEIGHT * 0.95))
        SCREEN.blit(text_surf, text_rectangle)


    num_players_screen = True
    while num_players_screen:
        click = False
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        
        if button('2  P L A Y E R S', *NUM_PLAYERS_BUTTONS_LAYOUT[0], click):
            NPLAYERS = 2
            BOARDSIZE = 2
            pygame.time.delay(100)
            changes_done(2)

        if button('3  P L A Y E R S', *NUM_PLAYERS_BUTTONS_LAYOUT[1], click):
            NPLAYERS = 3
            BOARDSIZE = 3
            pygame.time.delay(100)
            changes_done(3)

        if button('4  P L A Y E R S', *NUM_PLAYERS_BUTTONS_LAYOUT[2], click):
            NPLAYERS = 4
            BOARDSIZE = 4
            pygame.time.delay(100)
            changes_done(4)

        if button('5  P L A Y E R S', *NUM_PLAYERS_BUTTONS_LAYOUT[3], click):
            NPLAYERS = 5
            BOARDSIZE = 5
            pygame.time.delay(100)
            changes_done(5)

        if button('6  P L A Y E R S', *NUM_PLAYERS_BUTTONS_LAYOUT[4], click):
            NPLAYERS = 6
            BOARDSIZE = 6
            pygame.time.delay(100)
            changes_done(6)
            
        if button('7  P L A Y E R S', *NUM_PLAYERS_BUTTONS_LAYOUT[5], click):
            NPLAYERS = 7
            BOARDSIZE = 7
            pygame.time.delay(100)
            changes_done(7)

        if button('8  P L A Y E R S', *NUM_PLAYERS_BUTTONS_LAYOUT[6], click):
            NPLAYERS = 8
            BOARDSIZE = 8
            pygame.time.delay(100)
            changes_done(8)

        if button('9  P L A Y E R S', *NUM_PLAYERS_BUTTONS_LAYOUT[7], click):
            NPLAYERS = 9
            BOARDSIZE = 9
            pygame.time.delay(100)
            changes_done(9)

        elif button('R E T U R N', *NUM_PLAYERS_BUTTONS_LAYOUT[8], click):
            pygame.time.delay(100)
            main_menu()
        
        pygame.display.update(NUM_PLAYERS_BUTTONS_LAYOUT)

    return NPLAYERS, BOARDSIZE

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
        
        if button('S T A R T  G A M E', *MAIN_BUTTONS_LAYOUT[0], click):
            pygame.time.delay(100)
            start_game = True

        elif button('S E T T I N G S', *MAIN_BUTTONS_LAYOUT[1], click):
            pygame.time.delay(100)
            settings_menu()

        elif button('Q U I T   G A M E', *MAIN_BUTTONS_LAYOUT[2], click):
            pygame.time.delay(100)
            exit()

        #if start_game:
            #CODE THAT STARTS THE GAME

        pygame.display.update(MAIN_BUTTONS_LAYOUT)


pygame.display.set_caption('TIC-TAC-TOE')
clock = pygame.time.Clock()
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