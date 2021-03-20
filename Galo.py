# -*- coding: utf-8 -*-
import pygame
import random
from math import *
pygame.init()

NPLAYERS = 2             # definir o nº de jogadores
BOARDSIZE = 3           # definir o tamanho do board (BOARDSIZE*BOARDSIZE)

LIGHT_BLACK = (20, 20, 20)
WHITE = (207, 207, 207)
LIGHT_GREEN = (109, 215, 143)

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
    """Converte as coordenadas do "rato" para uma posição (coluna,linha) no jogo"""
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
    """Desenha o poligono do jogador na sua jogada"""
    
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


def Wins(screen):
    """Verifica se alguém ganhou"""
    
    check_e = True
    for l in range (BOARDSIZE):
        check_h = True # True quando todos os elementos de uma linha são iguais (e não vazios)
        for c in range (BOARDSIZE):
            if (Board[c][l] != Board[0][l]) or (Board[c][l] == -1):
                if Board[c][l] == -1: 
                    check_e = False
                check_h = False
                break
        if check_h == True: 
            pygame.draw.line(screen,WHITE,(xo-dist,int(yo-(dist/2)+dist*l)), (xo+(dist*(BOARDSIZE-1)),int((yo-dist/2)+dist*l)),10)
            check_e = False
            r = "w"
            return r

        
    for c in range (BOARDSIZE):
        check_v = True # True quando todos os elementos de uma coluna são iguais (e não vazios)
        for l in range (BOARDSIZE):
            if (Board[c][l] != Board[c][0]) or (Board[c][l] == -1):
                if Board[c][l] == -1: 
                    check_e = False
                check_v = False
                break
        if check_v == True: 
            pygame.draw.line(screen,WHITE,(int(xo-(dist/2)+dist*c), yo-dist),(int(xo-(dist/2)+dist*c),yo+(dist*(BOARDSIZE-1))),10) 
            check_e = False  
            r = "w"
            return r         
    
    
    
    check_d1 = True 
    for c in range(BOARDSIZE):
        if ((Board[c][c] != Board[0][0]) or (Board[c][c] == -1)):
            if Board[c][c] == -1: 
                check_e = False
            check_d1 = False
            break
    if check_d1 == True:
        pygame.draw.line(screen,WHITE,(xo-dist,yo-dist), (xo+(dist*(BOARDSIZE-1)),yo+(dist*(BOARDSIZE-1))),10)
        check_e = False
        r = "w"
        return r
    
    
    
    check_d2 = True 
    for c in range(BOARDSIZE):
        if (Board[BOARDSIZE-1-c][c] != Board[BOARDSIZE-1][0]) or (Board[BOARDSIZE-1-c][c] == -1):
            if Board[BOARDSIZE-1-c][c] == -1: 
                check_e = False
            check_d2 = False
            break
    if check_d2 == True:
        pygame.draw.line(screen,WHITE,(xo+(dist*(BOARDSIZE-1)),yo-dist), (xo-dist,yo+(dist*(BOARDSIZE-1))),10)
        check_e = False
        r = "w"
        return r
            
        
        
    """ if win == False:
        check_e = True
        for c in range (BOARDSIZE):
            for l in range (BOARDSIZE):
                if Board[l][c] == -1:
                    check_e = False
                    break """ #como ja vamos percorrer por todos os pontos fui verificando la no meio se havia empate ou nao ent ja n e preciso este ciclo
            
        
    if check_e == True: 
        r = "e"
    
    else: r = 0
    
    return r


def freePosFunc():
    freePos = []
    for i in range(BOARDSIZE):
        for j in range(BOARDSIZE):
            if Board[i][j] == -1:
                freePos.append([i,j])
    return freePos


def randomBot(w, player, freePos): 
    aux = random.random()
    rand = int ((aux * len(freePos)) // 1)
    Play(w, player, freePos[rand][0], freePos[rand][1])
    return


def auxWin(c,l):
    flag = True
    for i in range(BOARDSIZE):
        if (Board[c][i] != Board[c][l]) or (Board[c][i] == -1):
            flag = False
            break
    if flag:
        Board[c][l] = -1
        return True
    flag = True

    for i in range(BOARDSIZE):
        if (Board[i][l] != Board[c][l]) or (Board[i][l] == -1):
            flag = False
            break
    if flag:
        Board[c][l] = -1
        return True
    flag = True

    if c == l:
        for i in range(BOARDSIZE):
            if (Board[i][i] != Board[c][l]) or (Board[i][i] == -1):
                flag = False
                break
        if flag:
            Board[c][l] = -1
            return True
        flag = True

    if l == BOARDSIZE - 1 - c:
        for i in range(BOARDSIZE):
            if (Board[i][BOARDSIZE - 1 - i] != Board[c][l]) or (Board[i][BOARDSIZE - 1 - i] == -1):
                flag = False
                break
        if flag:
            Board[c][l] = -1
            return True

            
    Board[c][l] = -1
    return False


def minimax(w,player, count):
    freePos = freePosFunc()
    
    if len(freePos) == BOARDSIZE ** 2:
        Play(w,player,0,0)
        return
    for i in range(len(freePos)):
        Board[freePos[i][0]][freePos[i][1]] = player
        if auxWin(freePos[i][0],freePos[i][1]):
            Play(w,player,freePos[i][0],freePos[i][1])
            return
        Board[freePos[i][0]][freePos[i][1]] = -1
    randomBot(w,player, freePos)

    return


def GodBot(w, player):

    return
                    
    
def galo():
    bot = True
    player = 0
    w = makescreen() #cria a janela de jogo

    # game loop
    sair = False
    while not sair:
        pygame.display.update()
        
        for event in pygame.event.get():
            """ if event.type == pygame.QUIT:
                sair = False
                pygame.quit() """
            if bot:
                if player < NPLAYERS - 1:
                    minimax(w, player, 0)
                    win = Wins(w)
                    if win == "w":
                        sair = True
                        print ("player",player + 1, "wins!")
                        pygame.display.update()
                        pygame.time.delay(100)
                        w.fill(LIGHT_BLACK)
                    
                    
                    elif win == "e": 
                        print ("jogo empatado")
                        sair = True
                        print ("player",player + 1, "wins!")
                        pygame.display.update()
                        pygame.time.delay(100)
                        w.fill(LIGHT_BLACK)

                    player += 1
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        c,l = convert(pos)
                        
                        if Play(w,player, c,l):
                            # if played on valid spot increment player
                            player += 1
                
                            if player >= NPLAYERS:
                                player = 0       
                    
                        win = Wins(w)
                        if win == "w":
                            player += 1
                            sair = True
                            print ("player",player + 1, "wins!")
                            pygame.display.update()
                            pygame.time.delay(100)
                            w.fill(LIGHT_BLACK)
                        
                        
                        elif win == "e": 
                            print ("jogo empatado")
                            sair = True
                            print ("player",player + 1, "wins!")
                            pygame.display.update()
                            pygame.time.delay(100)
                            w.fill(LIGHT_BLACK)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    c,l = convert(pos)
                    
                    if Play(w,player, c,l):
                        # if played on valid spot increment player
                        player += 1
            
                        if player >= NPLAYERS:
                            player = 0       
                
                    win = Wins(w)
                    if win == "w":
                        sair = True
                        print ("player",player + 1, "wins!")
                        pygame.display.update()
                        pygame.time.delay(100)
                        w.fill(LIGHT_BLACK)
                        
                        
                    elif win == "e": 
                        print ("jogo empatado")
                        sair = True
                        print ("player",player + 1, "wins!")
                        pygame.display.update()
                        pygame.time.delay(100)
                        w.fill(LIGHT_BLACK)
                    
        
            if event.type == pygame.QUIT:
                sair = True
                pygame.quit()
    
    while sair:
        pygame.display.update()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = False
                pygame.quit()
            
if __name__ == "__main__": #safety reasons (so entra se for chamado aqui)
    galo()