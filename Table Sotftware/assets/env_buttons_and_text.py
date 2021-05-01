import pygame

from assets.Color import *
from assets.Fonts import *
from assets.Dimensions import *
from assets.Fonts import *
from assets.fade import *

FPS = 60 #Sets a limit of FPS to be able to run better
clock = pygame.time.Clock()
clock.tick(FPS)

#Create buttons (according to screen size)
APP_BUTTON_WIDTH = int(SCREEN_WIDTH * 0.8 // 8)
APP_BUTTON_HEIGHT = int(SCREEN_WIDTH * 0.8 // 8)

ENV_SETTINGS_BUTTON_WIDTH = int(SCREEN_WIDTH * 0.8 // 3)
ENV_SETTINGS_BUTTON_HEIGHT = int(SCREEN_HEIGHT * 5 // 55)

ENV_SMALL_BUTTON_WIDTH = int(SCREEN_WIDTH // 14)
ENV_SMALL_BUTTON_HEIGHT = int(SCREEN_WIDTH // 14)

ENV_QUESTION_BUTTON_WIDTH = int(SCREEN_WIDTH * 0.8 // 3)
ENV_QUESTION_BUTTON_HEIGHT = int(SCREEN_HEIGHT * 5 // 55)

MAIN_ENV_BUTTONS_LAYOUT = [((SCREEN_WIDTH // 2) - (ENV_SMALL_BUTTON_WIDTH // 2), (SCREEN_HEIGHT * 0.80), ENV_SMALL_BUTTON_WIDTH, ENV_SMALL_BUTTON_HEIGHT),
                           ((SCREEN_WIDTH - APP_BUTTON_WIDTH) // 10, SCREEN_HEIGHT * 1 // 12, APP_BUTTON_WIDTH, APP_BUTTON_HEIGHT),
                           ((SCREEN_WIDTH - APP_BUTTON_WIDTH) // 3, SCREEN_HEIGHT * 1 // 12, APP_BUTTON_WIDTH, APP_BUTTON_HEIGHT)]

SETTINGS_ENV_BUTTONS_LAYOUT = [((SCREEN_WIDTH - ENV_SETTINGS_BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 3 // 12, ENV_SETTINGS_BUTTON_WIDTH, ENV_SETTINGS_BUTTON_HEIGHT),
                               ((SCREEN_WIDTH - ENV_SETTINGS_BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 5 // 12, ENV_SETTINGS_BUTTON_WIDTH, ENV_SETTINGS_BUTTON_HEIGHT),
                               ((SCREEN_WIDTH - ENV_SETTINGS_BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 7 // 12, ENV_SETTINGS_BUTTON_WIDTH, ENV_SETTINGS_BUTTON_HEIGHT),
                               ((SCREEN_WIDTH - ENV_SETTINGS_BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 9 // 12, ENV_SETTINGS_BUTTON_WIDTH, ENV_SETTINGS_BUTTON_HEIGHT)]

QUESTION_ENV_BUTTONS_LAYOUT = [((SCREEN_WIDTH - ENV_QUESTION_BUTTON_WIDTH) // 4.5, SCREEN_HEIGHT * 5 // 12, ENV_QUESTION_BUTTON_WIDTH, ENV_QUESTION_BUTTON_HEIGHT),
                               ((SCREEN_WIDTH - ENV_QUESTION_BUTTON_WIDTH) // 1.3, SCREEN_HEIGHT * 5 // 12, ENV_QUESTION_BUTTON_WIDTH, ENV_QUESTION_BUTTON_HEIGHT)]

#Define rendered text of button (returns rendered text and it's image dimensions)
def text_objects(text, font, colour):
    text_surface = font.render(text, True, colour) #antialias = True
    text_area = text_surface.get_rect()

    return text_surface, text_area

#Define button style
def env_button(SCREEN, game, text, notbold_font, bold_font, x, y, w, h, text_xposition, text_yposition, click, inactive_button = LIGHT_GREEN, active_button = DARK_GREEN, text_colour = BLACK):
    mouse = pygame.mouse.get_pos() #Store mouse coordinates into the variable
    button_clicked = False

    #Define button app symbols
    def button_symbol(SCREEN, active, text, w, h):
        if text == 'TIC TAC TOE':
            dist = int(w*(2 / 10))

            xo = ((SCREEN_WIDTH - w) // 10) + (w*(2 / 10)) # x de referência
            yo = (SCREEN_HEIGHT // 12) + (h*(3 / 10)) # y de referência
            
            if active == False:
                for i in range (1, 3):
                    pygame.draw.line (SCREEN, LIGHT_BLACK, (xo , (yo + dist*i)), ((xo + dist*3), (yo + dist*i)), 5) # linhas horizontais 
                    pygame.draw.line (SCREEN, LIGHT_BLACK, ((xo + dist*i), yo), ((xo + dist*i), (yo + dist*3)), 5) #linhas verticais
            else:
                for i in range (1, 3):
                    pygame.draw.line (SCREEN, LIGHT_BLACK, (xo , (yo + dist*i)), ((xo + dist*3), (yo + dist*i)), 7) # linhas horizontais 
                    pygame.draw.line (SCREEN, LIGHT_BLACK, ((xo + dist*i), yo), ((xo + dist*i), (yo + dist*3)), 7) #linhas verticais
    
        #elif text == 'SNOOKER':
        #Circulo preto grande
        #Circulo branco pequeno

    def draw_button(SCREEN, active, text, w, h, text_surf, text_rectangle, game):
        if game == True:
            #SCREEN.blit(text_surf, text_rectangle)
            SCREEN.blit(text_surf, text_rectangle, button_symbol(SCREEN, active, text, w, h))
        else:
            SCREEN.blit(text_surf, text_rectangle)

    #If button is clicked, button_clicked turns true and button changes to darker colour
    if x < mouse[0] < x + w and y < mouse[1] < y + h and click and pygame.time.get_ticks() > 100:
        button_clicked = True
        pygame.draw.rect(SCREEN, active_button, (x, y, w, h))
        text_surf, text_rectangle = text_objects(text, bold_font, text_colour)
        text_rectangle.center = (int(x + w / text_xposition), int(y + h / text_yposition))
        draw_button(SCREEN, True, text, w, h, text_surf, text_rectangle, game)

    else:
        pygame.draw.rect(SCREEN, inactive_button, (x, y, w, h))
        text_surf, text_rectangle = text_objects(text, notbold_font, text_colour)
        text_rectangle.center = (int(x + w / text_xposition), int(y + h / text_yposition))
        draw_button(SCREEN, False, text, w, h, text_surf, text_rectangle, game)

    pygame.display.update()
    return button_clicked