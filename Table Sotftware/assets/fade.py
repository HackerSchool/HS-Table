import pygame
from assets.Color import *
from assets.Dimensions import *
from assets.env_buttons_and_text import *

def draw(screen, TABLE_HEIGHT, TABLE_WIDTH):
    pygame.draw.rect(screen, GREY, (0, int(TABLE_HEIGHT), int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))
    pygame.draw.line(screen, BLUE_IST, (0, int(TABLE_HEIGHT + TABLE_HEIGHT/140 - 1)), (int(SCREEN_WIDTH), int(TABLE_HEIGHT + TABLE_HEIGHT/140 - 1)), int(TABLE_HEIGHT / 70))
    pygame.draw.line (screen, WHITE, ((SCREEN_WIDTH//19),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2) - TABLE_HEIGHT // 30), ((SCREEN_WIDTH//19),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2) + TABLE_HEIGHT // 30), TABLE_WIDTH // 120) #pause button
    pygame.draw.line (screen, WHITE, ((SCREEN_WIDTH//30),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2) - TABLE_HEIGHT // 30), ((SCREEN_WIDTH//30),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2) + TABLE_HEIGHT // 30),TABLE_WIDTH // 120)
   
    
    text_b = "Player 1 (No color): 0"
    text_r = "Player 2 (No color): 0"
    

    
    string_b = SMALL_FONT.render(str(text_b),True,WHITE)
    string_r = SMALL_FONT.render(str(text_r),True,WHITE)
    
    string_br = string_b.get_rect()
    string_rr = string_r.get_rect()
    
    string_br.center = (((SCREEN_WIDTH//2) - (SCREEN_WIDTH//5)),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2))
    string_rr.center = (((SCREEN_WIDTH//2) + (SCREEN_WIDTH//5)),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2))
    
    screen.blit(string_b,string_br)
    screen.blit(string_r,string_rr)

    text_a = "?"

    string_a = LARGE_MIDDLE_TEXT.render(str(text_a), True, WHITE)
    string_br = string_a.get_rect()
    string_br.center = ((9.5*SCREEN_WIDTH//10),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2))

    screen.blit(string_a,string_br)

def fadeout_screen(SCREEN):
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade.fill(BLACK)
    for i in range(0, 255, 2):
        fade.set_alpha(i)
        SCREEN.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

def fadein_screen(SCREEN):
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade.fill(BLACK)
    BACKGROUND_IMAGE = pygame.image.load("./assets/images/Logo_HS_Table.png").convert_alpha()
    for i in range(0, 255, 2):
        fade.set_alpha(255 - i)
        SCREEN.blit(BACKGROUND_IMAGE, [0,0])
        SCREEN.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

def fadein_snooker(screen, holes, balls, walls, TW, TH):
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade.fill((0, 0, 0))


    for i in range(0, 255, 2):
        fade.set_alpha(255 - i)


        screen.fill(DARK_GREEN)
        for hole in holes:
            hole.Render()
        for b in balls:
            b.Render()
            b.Move()
        for wall in walls:
            wall.Render()
        draw(screen, TH, TW)


        screen.blit(fade, (0, 0))
        pygame.display.flip()
        #pygame.time.delay(20)

def fadein_galo(screen, BOARDSIZE, dist, xo, yo, RONDAS, r, PLAYERS, wins, LARGURA, ALTURA):
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade.fill((0, 0, 0))


    for i in range(0, 255, 2):
        fade.set_alpha(255 - i)


        screen.fill(LIGHT_BLACK)    
        pygame.draw.line (screen, WHITE, ((LARGURA//19),(ALTURA//25)), ((LARGURA//19),(ALTURA//10)),10) #pause button
        pygame.draw.line (screen, WHITE, ((LARGURA//30),(ALTURA//25)), ((LARGURA//30),(ALTURA//10)),10)        
        for i in range (BOARDSIZE-1):
                pygame.draw.line (screen, LIGHT_GREEN, ((xo + (dist*i)), 50) ,((xo + (dist*i)),(ALTURA-50)),10) # linhas horizontais 
                pygame.draw.line (screen, LIGHT_GREEN, ((xo - dist), (yo + (dist*i))), ((xo + (BOARDSIZE-1)*dist),(yo + (dist*i))), 10) #linhas verticais
        
        if RONDAS > 1:
            string = "ROUND " + str(r+1) + " OF " + str(RONDAS)
            text_r = SMALL_FONT.render(str(string),True, WHITE)
            textrRect = text_r.get_rect()
            textrRect.center = ((LARGURA-(LARGURA//10)),(ALTURA//20))
            screen.blit(text_r,textrRect)
        
        for p in range (PLAYERS):
            texto = "PLAYER " + str(p+1) + ": " + str(wins[p])
            texto_r = SMALL_TEXT_ONE.render(str(texto),True, WHITE)
            texto_rect = texto_r.get_rect()
            if p == 0:
                texto_rect.center = ((LARGURA//13),(ALTURA//4))
            else:
                texto_rect.center = ((LARGURA//13),(ALTURA//4 + (p*40)))
            screen.blit (texto_r,texto_rect)


        screen.blit(fade, (0, 0))
        pygame.display.flip()
    pass

"""
def fadeout_button(SCREEN, opacity)
def fadein_button(SCREEN, opacity):
"""