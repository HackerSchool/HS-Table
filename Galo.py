# -*- coding: utf-8 -*-
import pygame
import random
from math import *
pygame.init()

NPLAYERS = 3             # definir o nº de jogadores
BOARDSIZE = 6         # definir o tamanho do board (BOARDSIZE*BOARDSIZE)

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


def freePosFunc(): #creates a list of possible valid plays
    freePos = []
    for i in range(BOARDSIZE):
        for j in range(BOARDSIZE):
            if Board[i][j] == -1:
                freePos.append([i,j])
    return freePos


def randomBot(w, player, freePos): #choses a random move from the free spaces
    aux = random.random()
    rand = int ((aux * len(freePos)) // 1)
    Play(w, player, freePos[rand][0], freePos[rand][1])
    return


def auxWin(c, l): #helps the minimax function knowing if a given move wins on the spot
    flag = True
    for i in range(BOARDSIZE):
        if (Board[c][i] != Board[c][l]) or (Board[c][i] == -1):
            flag = False
            break
    if flag:
        
        return True
    flag = True

    for i in range(BOARDSIZE):
        if (Board[i][l] != Board[c][l]) or (Board[i][l] == -1):
            flag = False
            break
    if flag:
        
        return True
    flag = True

    if c == l:
        for i in range(BOARDSIZE):
            if (Board[i][i] != Board[c][l]) or (Board[i][i] == -1):
                flag = False
                break
        if flag:
            
            return True
        flag = True

    if l == BOARDSIZE - 1 - c:
        for i in range(BOARDSIZE):
            if (Board[i][BOARDSIZE - 1 - i] != Board[c][l]) or (Board[i][BOARDSIZE - 1 - i] == -1):
                flag = False
                break
        if flag:
            
            return True

            
    
    return False


def GodBot(player, freePos, freePosNum, depth=1, flag=1): #minimax algorithm kinda
    if flag == 0 and depth == NPLAYERS + 1:
        return [None, 0]
    if depth > 50/(BOARDSIZE * log2(BOARDSIZE)) and depth > 3: #max depth para impedir que fique 1000 anos a calcular a segunda jogada com tabuleiros grandes

        return [None, 0]

    if freePosNum == BOARDSIZE ** 2 and flag: #it takes a lot of time for the first move..
        return [[0,0],0]


    best = [None, 0]
    for i in range(freePosNum):
        aux = False
        Board[freePos[i][0]][freePos[i][1]] = (player + depth - 1) % NPLAYERS
        w = auxWin(freePos[i][0],freePos[i][1])
        p = player == (depth - 1 + player) % NPLAYERS
        if w:
            score = 100*(1+freePosNum) if p else -100*(1+freePosNum)
            best = [freePos[i], score]
            Board[freePos[i][0]][freePos[i][1]] = -1
            return best #não vale a pena continuar ou avançar no depth
        else:
            temp = freePos[i]
            del freePos[i]
            pos, score = GodBot(player, freePos, freePosNum - 1, depth + 1, flag)
            freePos.insert(i, temp)
            if score == best[1]: #just to add some randomness or else it gets pretty repetitive
                c = random.random()
                if c < 0.5:
                    aux = True
            if (score > best[1] and p) or (score < best[1] and not p) or aux or best[0] is None:
                best = [freePos[i], score]
        Board[freePos[i][0]][freePos[i][1]] = -1
    return best

        
def winsAnalise(w, win, player): #just so we dont have to repeat code
    sair = False
    if win == "w":#ajust for the play before
        if player == 0:
            player = NPLAYERS - 1
        else:
            player -= 1
        sair = True
        print ("player",player + 1, "wins!")
    elif win == "e": 
        print ("jogo empatado")
        sair = True
    return sair



def humanPlay(w, player): #just so we dont have to repeat code
    while True:
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                c,l = convert(pos)
                
                if Play(w,player, c,l):
                    # if played on valid spot increment player
                    player += 1

                    if player >= NPLAYERS:
                        player = 0    
                    return player  
            if event.type == pygame.QUIT: #dá mensagens de erro se sairmos na nossa jogada :(
                sair = True
                pygame.quit()
                
    

    
def galo():
    bot = [False, False, True] #chose the difficulty
    first = False #if true human starts
    aux = 0
    player = 0
    w = makescreen() #cria a janela de jogo

    # game loop
    sair = False
    while not sair:
        pygame.display.update()
        
        for event in pygame.event.get():
            if (bot[0] or bot[1] or bot[2]) and not sair:
                if (player > 0 and first) or (player < NPLAYERS - 1 and not first):
                    if bot[0]: #easy just random
                        freePos = freePosFunc()
                        randomBot(w, player, freePos)
                    elif bot[1]: # only knows if he can win on the spot or if someone else can in their next move (and stops them)
                        freePos = freePosFunc()
                        temp = len(freePos)
                        best = GodBot(player, freePos, temp, 1, 0)
                        Play(w,player,best[0][0],best[0][1])
                    else: #hard
                        freePos = freePosFunc()
                        temp = len(freePos)
                        best = GodBot(player, freePos, temp)
                        Play(w,player,best[0][0],best[0][1])
                    win = Wins(w)
                    sair = winsAnalise(w, win, player)
                    if sair:
                        pygame.display.update()
                        pygame.time.delay(100)
                        w.fill(LIGHT_BLACK)

                    player += 1
                    if player == NPLAYERS:
                        player = 0

                elif not sair:
                    player = humanPlay(w, player)
                    win = Wins(w)
                    sair = winsAnalise(w, win, player)
                    if sair:
                        pygame.display.update()
                        pygame.time.delay(100)
                        w.fill(LIGHT_BLACK)

            elif not sair:
                player = humanPlay(w, player)
                win = Wins(w)
                sair = winsAnalise(w, win, player)
                if sair:
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