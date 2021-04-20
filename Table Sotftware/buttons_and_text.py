import pygame
from assets.Color import *
from assets.Fonts import *
from assets.Dimensions import *

FPS = 60 #Sets a limit of FPS to be able to run better
clock = pygame.time.Clock()
clock.tick(FPS)

#Create buttons (according to screen size)
BUTTON_WIDTH = int(SCREEN_WIDTH * 0.8 // 3)
BUTTON_HEIGHT = int(SCREEN_HEIGHT * 5 // 55)

SMALL_BUTTON_WIDTH = int(70)
SMALL_BUTTON_HEIGHT = int(70)

MAIN_MENU_BUTTONS_LAYOUT = [((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 5 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
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

#Define rendered text of button (returns rendered text and it's image dimensions)
def text_objects(text, font, colour):
    text_surface = font.render(text, True, colour) #antialias = True
    text_area = text_surface.get_rect()

    return text_surface, text_area

#Define button style
def button(SCREEN, text, x, y, w, h, click, inactive_button = LIGHT_GREEN, active_button = DARK_GREEN, text_colour = BLACK):
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