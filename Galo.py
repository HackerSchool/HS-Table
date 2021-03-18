# -*- coding: utf-8 -*-
import pygame
from math import *
pygame.init()

NPLAYERS = 2             # definir o nº de jogadores
BOARDSIZE = 3            # definir o tamanho do board (BOARDSIZE*BOARDSIZE)

BLACK = (0, 0, 0)
LIGHT_BLACK = (20, 20, 20)
GREY = (28, 27, 27)
WHITE = (207, 207, 207)
LIGHT_GREEN = (109, 215, 143)
DARK_GREEN = (79, 161, 106)


LARGURA = 700
ALTURA = 500

dist = int ((ALTURA-100)/BOARDSIZE)          # distância entre duas linhas consecutivas (lado do quadrado)

if BOARDSIZE//2 != 0:
    xo = int ((LARGURA/2)-(dist/2)-((dist*(BOARDSIZE-3)/2))) # x da primeira linha vertical quando BOARDSIZE é ímpar
    yo = int ((ALTURA/2)-(dist/2)-((dist*(BOARDSIZE-3)/2))) # y da primeira linha vertical quando BOARDSIZE é ímpar
else:
    xo = int ((LARGURA/2) - (dist*(BOARDSIZE-2)/2)) # x da primeira linha vertical quando BOARDSIZE é par
    yo = int ((ALTURA/2) - (dist*(BOARDSIZE-2)/2)) # y da primeira linha vertical quando BOARDSIZE é par

# create the board (matriz BOARDSIZE x BOARDSIZE)
Board=[]
for i in range (BOARDSIZE):
    Board.append([-1 for i in range(BOARDSIZE)])

def makescreen():
    """ Inicializa o screen com a grade de jogo"""
    
    screen = pygame.display.set_mode((LARGURA,ALTURA))
    pygame.display.set_caption ("Jogo do Galo")
    screen.fill(LIGHT_BLACK)
    
    for i in range (BOARDSIZE-1):
            pygame.draw.line (screen, LIGHT_GREEN, ((xo + (dist*i)), 50) ,((xo + (dist*i)),(ALTURA-50)),10) # linhas horizontais 
            pygame.draw.line (screen, LIGHT_GREEN, ((xo - dist), (yo + (dist*i))), ((xo + (BOARDSIZE-1)*dist),(yo + (dist*i))), 10) #linhas verticais
    
    return screen

def convert(pos):
    x = xo
    y = yo
                 
    for c in range (BOARDSIZE): # percorrer todas as colunas
        if (pos[0] < x) or (c==BOARDSIZE-1): 
            for l in range(BOARDSIZE):
                if pos[1] < y:
                    break
                else:
                    y = y + dist # incrementar y para a próxima linha
            break     
        else:
            x = x + dist # incrementar x para a próxima coluna
            
    return c,l

def shapes(screen,player,c,l):
    
    # coordenadas do centro do quadrado
    xc = int(xo + (c*dist) - (dist/2)) 
    yc = int(yo + (l*dist) - (dist/2))
    
    # player 0: desenhar a cruz
    if player == 0:
        pygame.draw.line(screen,WHITE,(int(xc-(dist/2)+15),int(yc-(dist/2)+15)),
                                       (int(xc+(dist/2)-15),int(yc+(dist/2)-15)),5)
        pygame.draw.line(screen, WHITE,(int(xc-(dist/2)+15),int(yc+(dist/2)-15)),
                                       (int(xc+(dist/2)-15),int(yc-(dist/2)+15)),5)
   
    # player 1: desenhar a bola
    elif player == 1:
        pygame.draw.circle(screen, WHITE, (xc,yc), int((dist/2)-15))
        pygame.draw.circle(screen,LIGHT_BLACK,(xc,yc),int((dist/2)-19))
        
    else:
    # player n: desenhar poligno com n+1 lados (ex.: player 2 -> triângulo)   
        points = []
        a = (2*pi)/(player+1)
        raio = int((dist/2)-10)
        points.append((xc,yc-raio))
        for i in range (player):
            y = int(yc - (raio * sin(a+(pi/2)+a*i)))
            x = int(xc + (raio * cos(a+(pi/2)+a*i)))
            points.append((x,y))
        pygame.draw.polygon(screen,WHITE,points,5)
        
    
def Play(w,player, c,l):
    """ Handles a player play """

    # tried to play on not empty spot
    if Board[c][l] != -1:
        return False

    else:
        Board[c][l] = player
        # adicionar codigo para desenhar cruz/bola 
        shapes(w, player,c,l)
        return True

def main():
    player = 0
    w = makescreen() #cria a janela de jogo

    # game loop
    sair = False
    while not sair:
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = True
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                c,l = convert(pos)
                
                if Play(w,player, c,l):
                    # if played on valid spot increment player
                    player += 1
        
                    if player >= NPLAYERS:
                        player = 0              
                

if __name__ == "__main__":
    main()