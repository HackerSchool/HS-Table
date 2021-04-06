# -*- coding: utf-8 -*-
import pygame
from Color import *

pygame.init()

#Get fonts
FONT_ORIGAMI = 'fonts/Origami.ttf'
FONT_RAJDHANI = 'fonts/Rajdhani-Medium.ttf'
FONT_RAJDHANI_BOLD = 'fonts/Rajdhani-Bold.ttf'

SCREEN_WIDTH = int(pygame.display.Info().current_w)
SCREEN_HEIGHT = int(pygame.display.Info().current_h)

SCREEN_WIDTH, SCREEN_HEIGHT = int(0.75 * SCREEN_WIDTH), int(0.75 * SCREEN_HEIGHT) #Tirar quando passar para a mesa

FPS = 60 #Sets a limit of FPS to be able to run better
clock = pygame.time.Clock()
clock.tick(FPS)

#Create texts
MAIN_MENU_TEXT = pygame.font.Font(FONT_ORIGAMI, int(115 / 1080 * SCREEN_HEIGHT))
MENU_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(115 / 1080 * SCREEN_HEIGHT))
LARGE_TEXT = pygame.font.Font(FONT_RAJDHANI, int(60 / 1440 * SCREEN_HEIGHT))
MEDIUM_TEXT = pygame.font.Font(FONT_RAJDHANI, int(45 / 1440 * SCREEN_HEIGHT))
MEDIUM_BOLD_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(45 / 1440 * SCREEN_HEIGHT))
SMALL_TEXT = pygame.font.Font(FONT_RAJDHANI, int(35 / 1440 * SCREEN_HEIGHT))
SMALL_BOLD_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(35 / 1440 * SCREEN_HEIGHT))
LABEL_TEXT = pygame.font.Font(FONT_RAJDHANI, int(85 / 1440 * SCREEN_HEIGHT))

MAIN_FONT = pygame.font.Font(FONT_ORIGAMI, int(SCREEN_HEIGHT/7))
SMALL_FONT = pygame.font.Font (FONT_RAJDHANI,int(SCREEN_HEIGHT/20))

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