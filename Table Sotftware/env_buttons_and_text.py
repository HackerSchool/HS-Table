import pygame

from assets.Color import *
from assets.Fonts import *
from assets.Dimensions import *

FPS = 60 #Sets a limit of FPS to be able to run better
clock = pygame.time.Clock()
clock.tick(FPS)

#Create buttons (according to screen size)
APP_BUTTON_WIDTH = int(170)
APP_BUTTON_HEIGHT = int(170)

ENV_SETTINGS_BUTTON_WIDTH = int(SCREEN_WIDTH * 0.8 // 3)
ENV_SETTINGS_BUTTON_HEIGHT = int(SCREEN_HEIGHT * 5 // 55)

ENV_SMALL_BUTTON_WIDTH = int(SCREEN_WIDTH * 0.8 // 10)
ENV_SMALL_BUTTON_HEIGHT = int(SCREEN_WIDTH * 0.8 // 10)

ENV_QUESTION_BUTTON_WIDTH = int(SCREEN_WIDTH * 0.8 // 3)
ENV_QUESTION_BUTTON_HEIGHT = int(SCREEN_HEIGHT * 5 // 55)

MAIN_ENV_BUTTONS_LAYOUT = [((SCREEN_WIDTH - ENV_SMALL_BUTTON_WIDTH) // 1.0005, SCREEN_HEIGHT * 10.9 // 12, ENV_SMALL_BUTTON_WIDTH, ENV_SMALL_BUTTON_HEIGHT),
                           ((SCREEN_WIDTH - APP_BUTTON_WIDTH) // 10, SCREEN_HEIGHT * 1 // 12, APP_BUTTON_WIDTH, APP_BUTTON_HEIGHT),
                           ((SCREEN_WIDTH - APP_BUTTON_WIDTH) // 3, SCREEN_HEIGHT * 1 // 12, APP_BUTTON_WIDTH, APP_BUTTON_HEIGHT)]

SETTINGS_ENV_BUTTONS_LAYOUT = [((SCREEN_WIDTH - ENV_SETTINGS_BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 5 // 12, ENV_SETTINGS_BUTTON_WIDTH, ENV_SETTINGS_BUTTON_HEIGHT),
                               ((SCREEN_WIDTH - ENV_SETTINGS_BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 7 // 12, ENV_SETTINGS_BUTTON_WIDTH, ENV_SETTINGS_BUTTON_HEIGHT),
                               ((SCREEN_WIDTH - ENV_SETTINGS_BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 9 // 12, ENV_SETTINGS_BUTTON_WIDTH, ENV_SETTINGS_BUTTON_HEIGHT),
                               ((SCREEN_WIDTH - ENV_SETTINGS_BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 10 // 12, ENV_SETTINGS_BUTTON_WIDTH, ENV_SETTINGS_BUTTON_HEIGHT)]

QUESTION_ENV_BUTTONS_LAYOUT = [((SCREEN_WIDTH - ENV_QUESTION_BUTTON_WIDTH) // 4.5, SCREEN_HEIGHT * 5 // 12, ENV_QUESTION_BUTTON_WIDTH, ENV_QUESTION_BUTTON_HEIGHT),
                               ((SCREEN_WIDTH - ENV_QUESTION_BUTTON_WIDTH) // 1.3, SCREEN_HEIGHT * 5 // 12, ENV_QUESTION_BUTTON_WIDTH, ENV_QUESTION_BUTTON_HEIGHT)]

#Define rendered text of button (returns rendered text and it's image dimensions)
def text_objects(text, font, colour):
    text_surface = font.render(text, True, colour) #antialias = True
    text_area = text_surface.get_rect()

    return text_surface, text_area

#Define button style
def env_button(SCREEN, text, x, y, w, h, click, inactive_button = LIGHT_GREEN, active_button = DARK_GREEN, text_colour = BLACK):
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

        elif text == 'TIC TAC TOE' or text == 'SNOOKER': #SELFNOTE: ADICIONAR RESTO DOS JOGOS AQUI
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

        elif text == 'TIC TAC TOE' or text == 'SNOOKER': #SELFNOTE: ADICIONAR RESTO DOS JOGOS AQUI
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