# -*- coding: utf-8 -*-
import pygame
import random
from math import *
from Color import *
pygame.init()


SCREEN_WIDTH = int(pygame.display.Info().current_w)
SCREEN_HEIGHT = int(pygame.display.Info().current_h)
LARGURA, ALTURA = int(0.75 * SCREEN_WIDTH), int(0.75 * SCREEN_HEIGHT)

FONT_ORIGAMI = 'fonts/Origami.ttf'
FONT_RAJDHANI = 'fonts/Rajdhani-Medium.ttf'
FONT_RAJDHANI_BOLD = 'fonts/Rajdhani-Bold.ttf'
MAIN_FONT = pygame.font.Font(FONT_ORIGAMI, int(ALTURA/7))
SMALL_FONT = pygame.font.Font (FONT_RAJDHANI,int(ALTURA/20))
  

def makescreen(BOARDSIZE,dist,xo,yo,RONDAS,r):
    """ Inicializa o screen com a grade de jogo e as rondas"""
    
    screen = pygame.display.set_mode((LARGURA,ALTURA))
    pygame.display.set_caption ("Jogo do Galo")
    screen.fill(LIGHT_BLACK)
    
    for i in range (BOARDSIZE-1):
            pygame.draw.line (screen, LIGHT_GREEN, ((xo + (dist*i)), 50) ,((xo + (dist*i)),(ALTURA-50)),10) # linhas horizontais 
            pygame.draw.line (screen, LIGHT_GREEN, ((xo - dist), (yo + (dist*i))), ((xo + (BOARDSIZE-1)*dist),(yo + (dist*i))), 10) #linhas verticais
    
    if RONDAS > 1:
        string = "ROUND " + str(r+1) + " OF " + str(RONDAS)
        text_r = SMALL_FONT.render(str(string),True, WHITE)
        textrRect = text_r.get_rect()
        textrRect.center = ((LARGURA-(LARGURA//10)),(ALTURA//20))
        screen.blit(text_r,textrRect)
    
    return screen

def convert(BOARDSIZE,dist,pos,xo,yo):
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

def shapes(dist,xo,yo,screen,player,c,l):
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
        
def Play(Board,dist,xo,yo,w,player, c,l):
    """ Handles a player play """
    
    # tried to play on not empty spot
    if Board[c][l] != -1:
        return False

    else:
        Board[c][l] = player
        # adicionar codigo para desenhar cruz/bola 
        shapes(dist,xo,yo,w, player,c,l)
        return True
       
def Wins(BOARDSIZE,screen,Board,dist,xo,yo):
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
            
    if check_e == True: 
        r = "e"
    
    else: r = 0
    
    return r


def freePosFunc(Board, BOARDSIZE): #creates a list of possible valid plays
    freePos = []
    for i in range(BOARDSIZE):
        for j in range(BOARDSIZE):
            if Board[i][j] == -1:
                freePos.append([i,j])
    return freePos


def randomBot(Board, dist, xo, yo, w, player, freePos): #choses a random move from the free spaces
    aux = random.random()
    rand = int ((aux * len(freePos)) // 1)
    Play(Board, dist, xo, yo, w, player, freePos[rand][0], freePos[rand][1])
    return


def auxWin(Board, BOARDSIZE, c, l): #helps the minimax function knowing if a given move wins on the spot
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


def GodBot(NPLAYERS, Board, BOARDSIZE, player, freePos, freePosNum, depth=1, flag=1): #minimax algorithm kinda
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
        w = auxWin(Board, BOARDSIZE, freePos[i][0],freePos[i][1])
        p = player == (depth - 1 + player) % NPLAYERS
        if w:
            score = 100*(1+freePosNum) if p else -100*(1+freePosNum)
            best = [freePos[i], score]
            Board[freePos[i][0]][freePos[i][1]] = -1
            return best #não vale a pena continuar ou avançar no depth
        else:
            temp = freePos[i]
            del freePos[i]
            pos, score = GodBot(NPLAYERS, Board, BOARDSIZE, player, freePos, freePosNum - 1, depth + 1, flag)
            freePos.insert(i, temp)
            if score == best[1]: #just to add some randomness or else it gets pretty repetitive
                c = random.random()
                if c < 0.5:
                    aux = True
            if (score > best[1] and p) or (score < best[1] and not p) or aux or best[0] is None:
                best = [freePos[i], score]
        Board[freePos[i][0]][freePos[i][1]] = -1
    return best


def winsAnalise(LARGURA, ALTURA, w, win, player): #just so we dont have to repeat code
    if win == "w":

        s = pygame.Surface((LARGURA,ALTURA)) 
        s.set_alpha(200)              
        s.fill((20,20,20))

        pygame.display.update()
        pygame.time.delay(300)
        w.blit(s, (0,0))
        
        string = "player " + str(player) + " wins!"
        
        text_w = MAIN_FONT.render(str(string), True,LIGHT_GREEN)
        textwRect = text_w.get_rect()
        textwRect.center = (LARGURA // 2, ALTURA // 2)
        
        text_t = SMALL_FONT.render("TAP TO CONTINUE",True, WHITE)
        texttRect = text_t.get_rect()
        texttRect.center = (LARGURA//2,(ALTURA//2)+(ALTURA//7))
        
        w.blit(text_w,textwRect)
        w.blit(text_t,texttRect)
        
        pygame.display.update()

        while True:
            pygame.display.update()            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return 1
                            
        
    elif win == "e": 

        s = pygame.Surface((LARGURA,ALTURA)) 
        s.set_alpha(200)              
        s.fill((20,20,20))
        
        pygame.display.update()
        pygame.time.delay(300)
        
        w.blit(s,(0,0))
        
        text_d = MAIN_FONT.render ("it's a draw!",True,LIGHT_GREEN)
        textdRect = text_d.get_rect()
        textdRect.center = (LARGURA//2,ALTURA//2)
        
        text_t = SMALL_FONT.render("TAP TO CONTINUE",True, WHITE)
        texttRect = text_t.get_rect()
        texttRect.center = (LARGURA//2,(ALTURA//2)+(ALTURA//7))
        
        w.blit(text_d,textdRect)
        w.blit(text_t,texttRect)
        
        pygame.display.update()
        
        while True:
            pygame.display.update()            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return 1
                    
    else:
        return 0


def humanPlay(NPLAYERS, BOARDSIZE, Board, dist, xo, yo, w, player): #just so we dont have to repeat code
    while True:
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("hello")
                pos = pygame.mouse.get_pos()
                c,l = convert(BOARDSIZE,dist,pos,xo,yo)
                
                if Play(Board,dist,xo,yo,w,player, c,l):
                    # if played on valid spot increment player
                    player += 1

                    if player >= NPLAYERS:
                        player = 0    
                    return player  
            if event.type == pygame.QUIT: #dá mensagens de erro se sairmos na nossa jogada :(
                sair = True
                pygame.quit()

    
def galo(NPLAYERS,BOARDSIZE,RONDAS):

    dist = int ((ALTURA-100)/BOARDSIZE)          # distância entre duas linhas consecutivas (lado do quadrado)
    
    if BOARDSIZE//2 != 0:
        xo = int ((LARGURA/2)-(dist/2)-((dist*(BOARDSIZE-3)/2))) # x da primeira linha vertical quando BOARDSIZE é ímpar
        yo = int ((ALTURA/2)-(dist/2)-((dist*(BOARDSIZE-3)/2))) # y da primeira linha vertical quando BOARDSIZE é ímpar
    else:
        xo = int ((LARGURA/2) - (dist*(BOARDSIZE-2)/2)) # x da primeira linha vertical quando BOARDSIZE é par
        yo = int ((ALTURA/2) - (dist*(BOARDSIZE-2)/2)) # y da primeira linha vertical quando BOARDSIZE é par

    # game loop
    sair = False
    
    for r in range(RONDAS):
        
        # create the board (matriz BOARDSIZE x BOARDSIZE)
        Board=[]
        for i in range (BOARDSIZE):
            Board.append([-1 for i in range(BOARDSIZE)])
            
        player = 0
        w = makescreen(BOARDSIZE,dist,xo,yo,RONDAS,r) #cria a janela de jogo
        t = 0
        
        while not sair:
            pygame.display.update()
            for event in pygame.event.get():
                #if event.type == pygame.MOUSEBUTTONDOWN:
                player = humanPlay(NPLAYERS, BOARDSIZE, Board, dist, xo, yo, w, player)    
                win = Wins(BOARDSIZE,w,Board,dist,xo,yo)
                print ("t",t)
                
                #if t == 0:
                t = winsAnalise(LARGURA, ALTURA, w, win, player)
                        
                if t != 0: 
                    t = 2
                    break 
            
            #adicionei isto para se carregarem no 'x' a meio de um jogo
            if event.type == pygame.QUIT:
                sair = True
                pygame.quit()

            if t == 2:
                break


        #acho q isto não é preciso mas i'm scared de apagar lol
        """for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                sair = True
                break
            if event.type == pygame.QUIT:
                sair = True
                pygame.quit()"""
    
    while sair:
        pygame.display.update()
        if t != 0:
            break
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = False
                pygame.quit()


def galo_BOT(NPLAYERS,BOARDSIZE,RONDAS, dificulty):
    bot = [False, False, False]
    bot[dificulty] = True

    dist = int ((ALTURA-100)/BOARDSIZE)          # distância entre duas linhas consecutivas (lado do quadrado)
    
    if BOARDSIZE//2 != 0:
        xo = int ((LARGURA/2)-(dist/2)-((dist*(BOARDSIZE-3)/2))) # x da primeira linha vertical quando BOARDSIZE é ímpar
        yo = int ((ALTURA/2)-(dist/2)-((dist*(BOARDSIZE-3)/2))) # y da primeira linha vertical quando BOARDSIZE é ímpar
    else:
        xo = int ((LARGURA/2) - (dist*(BOARDSIZE-2)/2)) # x da primeira linha vertical quando BOARDSIZE é par
        yo = int ((ALTURA/2) - (dist*(BOARDSIZE-2)/2)) # y da primeira linha vertical quando BOARDSIZE é par

    # game loop
    sair = False
    
    for r in range(RONDAS):
        
        # create the board (matriz BOARDSIZE x BOARDSIZE)
        Board=[]
        for i in range (BOARDSIZE):
            Board.append([-1 for i in range(BOARDSIZE)])
            
        player = 0
        w = makescreen(BOARDSIZE,dist,xo,yo,RONDAS,r) #cria a janela de jogo
        t = 0
        first = False if (r%2 == 0) else True
        
        while not sair:
            pygame.display.update()
            for event in pygame.event.get():
                if (player > 0 and first) or (player < NPLAYERS - 1 and not first):
                    if bot[0]: #easy just random
                        freePos = freePosFunc(Board, BOARDSIZE)
                        randomBot(Board, dist, xo, yo, w, player, freePos)
                    elif bot[1]: # only knows if he can win on the spot or if someone else can in their next move (and stops them)
                        freePos = freePosFunc(Board, BOARDSIZE)
                        temp = len(freePos)
                        best = GodBot(Board, BOARDSIZE, player, freePos, temp, 1, 0)
                        Play(Board, dist, xo, yo, w,player,best[0][0],best[0][1])
                    else: #hard
                        freePos = freePosFunc(Board, BOARDSIZE)
                        temp = len(freePos)
                        best = GodBot(NPLAYERS, Board, BOARDSIZE, player, freePos, temp)
                        Play(Board, dist, xo, yo, w,player,best[0][0],best[0][1])
                    win = Wins(BOARDSIZE, w, Board, dist, xo, yo)
                    t = winsAnalise(LARGURA, ALTURA, w, win, player)
                    if t != 0:
                        t = 2
                        break 

                    player += 1
                    if player == NPLAYERS:
                        player = 0

                elif t == 0:
                    player = humanPlay(NPLAYERS, BOARDSIZE, Board, dist, xo, yo, w, player)    
                    win = Wins(BOARDSIZE,w,Board,dist,xo,yo)
                    print ("t",t)
                    t = winsAnalise(LARGURA, ALTURA, w, win, player)                            
                    if t != 0:
                        t = 2
                        break 
            
            #adicionei isto para se carregarem no 'x' a meio de um jogo
            if event.type == pygame.QUIT:
                sair = True
                pygame.quit()

            if t == 2: 
                break


        #acho q isto não é preciso mas i'm scared de apagar lol
        """for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                sair = True
                break
            if event.type == pygame.QUIT:
                sair = True
                pygame.quit()"""
    
    while sair:
        pygame.display.update()
        if t != 0:
            break
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = False
                pygame.quit()
            
#galo()
