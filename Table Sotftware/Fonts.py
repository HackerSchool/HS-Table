import pygame
from assets.Dimensions import *

FONT_ORIGAMI = 'assets/fonts/Origami.ttf'
FONT_RAJDHANI = 'assets/fonts/Rajdhani-Medium.ttf'
FONT_RAJDHANI_BOLD = 'assets/fonts/Rajdhani-Bold.ttf'

#Create texts
MAIN_MENU_TEXT = pygame.font.Font(FONT_ORIGAMI, int(115 / 1080 * SCREEN_HEIGHT))
LARGE_MIDDLE_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(115 / 1080 * SCREEN_HEIGHT))
MENU_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(115 / 1080 * SCREEN_HEIGHT))
LARGE_TEXT = pygame.font.Font(FONT_RAJDHANI, int(60 / 1440 * SCREEN_HEIGHT))
MEDIUM_TEXT = pygame.font.Font(FONT_RAJDHANI, int(45 / 1440 * SCREEN_HEIGHT))
MEDIUM_BOLD_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(45 / 1440 * SCREEN_HEIGHT))
SMALL_TEXT = pygame.font.Font(FONT_RAJDHANI, int(35 / 1440 * SCREEN_HEIGHT))
SMALL_BOLD_TEXT = pygame.font.Font(FONT_RAJDHANI_BOLD, int(35 / 1440 * SCREEN_HEIGHT))
LABEL_TEXT = pygame.font.Font(FONT_RAJDHANI, int(85 / 1440 * SCREEN_HEIGHT))
HS_TEXT = pygame.font.Font(FONT_ORIGAMI, int(100 / 1440 * SCREEN_HEIGHT))

MAIN_FONT = pygame.font.Font(FONT_ORIGAMI, int(SCREEN_HEIGHT/7))
SMALL_FONT = pygame.font.Font (FONT_RAJDHANI,int(SCREEN_HEIGHT/20))

SMALL_TEXT_ONE = pygame.font.Font(FONT_RAJDHANI, int(SCREEN_HEIGHT/27))