# -*- coding: utf-8 -*-
import pygame
import random
from math import *
from Color import *
from buttons_and_text import *

pygame.init()


SCREEN_WIDTH = int(pygame.display.Info().current_w)
SCREEN_HEIGHT = int(pygame.display.Info().current_h)
LARGURA, ALTURA = int(0.75 * SCREEN_WIDTH), int(0.75 * SCREEN_HEIGHT)

    
s = pygame.Surface((LARGURA,ALTURA)) 
s.set_alpha(200)              
s.fill((20,20,20))



def makescreen(BOARDSIZE,dist,xo,yo,RONDAS,r):
    """ Inicializa o screen com a grade de jogo e as rondas"""
    
    screen = pygame.display.set_mode((LARGURA,ALTURA))
    pygame.display.set_caption ("Jogo do Galo")
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
            
    if (pos[0] < ((LARGURA//19)+10)) and (pos[0] > ((LARGURA//30)-10)): #se clicarem na pausa
        if (pos[1] < (ALTURA//10)) and (pos[1] > (ALTURA//25)):
            c = -2
            l = -2
            
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
        # desenhar cruz/bola 
        shapes(dist,xo,yo,w, player,c,l)
        return True
       
def Wins(BOARDSIZE,screen,Board,dist,xo,yo):
    """Verifica se alguém ganhou"""
    
    check_e = True
    for l in range (BOARDSIZE):
        check_h = True # True quando todos os elementos de uma linha são iguais (e não vazios)
        for c in range (BOARDSIZE):
            if (Board[c][l] != Board[0][l]) or (Board[c][l] == -1):
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
            check_d2 = False
            break
        
    if check_d2 == True:
        pygame.draw.line(screen,WHITE,(xo+(dist*(BOARDSIZE-1)),yo-dist), (xo-dist,yo+(dist*(BOARDSIZE-1))),10)
        check_e = False
        r = "w"
        return r
            
    if check_e == True: 
        for l in range (BOARDSIZE):
            for c in range (BOARDSIZE):
                if Board[c][l] == -1:
                    check_e = False
                    return 0
        return "e"
    
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

def winsAnalise(s,LARGURA, ALTURA, w, win, player): #just so we dont have to repeat code
    if win == "w":

        pygame.display.update()
        pygame.time.delay(300)
        w.blit(s, (0,0))
        
        string = "player " + str(player + 1) + " wins!"
        
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
                pos = pygame.mouse.get_pos()
                c,l = convert(BOARDSIZE,dist,pos,xo,yo)
                
                if (c == -2) and (l == -2): #quando clicam na pausa
                    return -2
                
                else:                
                    if Play(Board,dist,xo,yo,w,player, c,l):
                        # if played on valid spot increment player  
                        return player  
            if event.type == pygame.QUIT: 
                sair = True #is this sair needed? não é usado nesta função
                return -1 

def getWinner(LARGURA, ALTURA, NPLAYERS, w, winner):
    champs = []
    aux = -1
    for i in range(len(winner)):
        if winner[i] > aux:
            aux = winner[i]
            champs = [] #dump the vector champs (there's a new champ in town)
            champs.append(i)
        elif winner[i] == aux:
            champs.append(i)



    s = pygame.Surface((LARGURA,ALTURA)) 
    s.set_alpha(1000)              
    s.fill((20,20,20))

    pygame.display.update()
    #pygame.time.delay(300)
    w.blit(s, (0,0))
    
    if (len(champs) == 1): #1 winner
        string1 = "winner:"
        string2 = "player " + str(champs[0] + 1)
    elif len(champs) < NPLAYERS:
        string1 = "winners:"
        string2 = "players"
        for i in range(len(champs)):
            if i != 0:
                string2 += ", " + str(champs[i] + 1)
            else:
               string2 += " " + str(champs[i] + 1) 
    else:
        string1 = ""
        string2 = "it's a draw"
    
    text_w = MAIN_FONT.render(str(string1), True,LIGHT_GREEN)
    textwRect = text_w.get_rect()
    textwRect.center = (LARGURA // 2, ALTURA // 2 - ALTURA // 7 )
    w.blit(text_w,textwRect)

    text_w = MAIN_FONT.render(str(string2), True, LIGHT_GREEN)
    textwRect = text_w.get_rect()
    textwRect.center = (LARGURA // 2, ALTURA // 2)
    w.blit(text_w,textwRect)
    
    text_t = SMALL_FONT.render("TAP TO CONTINUE",True, WHITE)
    texttRect = text_t.get_rect()
    texttRect.center = (LARGURA//2,(ALTURA//2)+(ALTURA//7))

    w.blit(text_t,texttRect)
    
    pygame.display.update()

    while True:
        pygame.display.update()            
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

def thinking(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, player):
    SMALL_TEXT_BOT = pygame.font.Font(FONT_RAJDHANI, int(50 / 1440 * SCREEN_HEIGHT))
    pygame.draw.rect(SCREEN, (20, 20, 20), (int(SCREEN_WIDTH / 1.355), int(SCREEN_HEIGHT * 0.935), int(1 / 4 * SCREEN_WIDTH), int(50 / 1440 * SCREEN_HEIGHT)))
        
    text_surf, text_rectangle = text_objects('Player ' + str(player + 1) + ' is thinking', SMALL_TEXT_BOT, (207, 207, 207))
    text_rectangle.center = (int(SCREEN_WIDTH / 1.16), int(SCREEN_HEIGHT * 0.95))
    SCREEN.blit(text_surf, text_rectangle)
    pygame.display.update()

def notThinking(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT):
    pygame.draw.rect(SCREEN, (20,20,20), (int(SCREEN_WIDTH / 1.355), int(SCREEN_HEIGHT * 0.935), int(1 / 4 * SCREEN_WIDTH), int(50 / 1440 * SCREEN_HEIGHT)))
    pygame.display.update()

def printsPlayer(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, player):         
    text_surf, text_rectangle = text_objects('Player ' + str(player + 1), SMALL_FONT, (207, 207, 207))
    text_rectangle.center = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT * 0.024))
    SCREEN.blit(text_surf, text_rectangle)
    pygame.display.update()

def unprintsPlayer(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT):
    pygame.draw.rect(SCREEN, (20,20,20), (int(SCREEN_WIDTH  * 0.44), int(SCREEN_HEIGHT * 0), int(1 / 8 * SCREEN_WIDTH), int(0.066 * SCREEN_HEIGHT)))
    pygame.display.update()
    
def pause(w,s):
    w.blit(s, (0,0))
    
    text = MAIN_FONT.render("PAUSED", True,WHITE)
    textRect = text.get_rect()
    textRect.center = (LARGURA // 2, ALTURA // 4)
    w.blit(text, textRect)
    
    BUTTON_WIDTH = int(LARGURA * 0.8 // 3)
    BUTTON_HEIGHT = int(ALTURA * 5 // 55)
    
    MAIN_BUTTONS_LAYOUT = [((LARGURA - BUTTON_WIDTH) // 2, ALTURA * 5 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
                       ((LARGURA - BUTTON_WIDTH) // 2, ALTURA * 7 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
                       ((LARGURA - BUTTON_WIDTH) // 2, ALTURA * 9 // 12, BUTTON_WIDTH, BUTTON_HEIGHT)]
    
    sair = False
    click = False
    while not sair:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        if button(w,'R E S U M E', *MAIN_BUTTONS_LAYOUT[0], click):
            sair = True
            return 1
            break
        elif button(w,'R E S T A R T', *MAIN_BUTTONS_LAYOUT[1], click):
            sair = True
            return 2
        elif button(w,'Q U I T', *MAIN_BUTTONS_LAYOUT[2], click):
            sair = True
            return 3
    
def galo(NPLAYERS,BOARDSIZE,RONDAS):

    winner = []
    for i in range(NPLAYERS): #initialize vector with number of wins for each player
        winner.append(0)


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
            
        player = r % NPLAYERS
        w = makescreen(BOARDSIZE,dist,xo,yo,RONDAS,r) #cria a janela de jogo
        
        while not sair:
            pygame.display.update()
            #for event in pygame.event.get():
            printsPlayer(w, LARGURA, ALTURA, player)
            p = player
            player = humanPlay(NPLAYERS, BOARDSIZE, Board, dist, xo, yo, w, player) 
            unprintsPlayer(w, LARGURA, ALTURA)   
            if player == -1:
                return
            elif player == -2:
                option = pause(w,s)
                if option == 1:         #resume
                    pygame.time.delay(100)
                    w = makescreen(BOARDSIZE, dist, xo, yo, RONDAS, r)
                    for l in range (BOARDSIZE):
                        for c in range (BOARDSIZE):
                            if (Board[c][l] != -1):
                                player_d = Board[c][l]
                                shapes(dist, xo, yo, w, player_d, c, l)   
                    player = p - 1
                elif option == 2:       #restart
                    pygame.time.delay(100)
                    return -1         
                elif option == 3:       #quit
                    pygame.time.delay(100)
                    return
                
            win = Wins(BOARDSIZE,w,Board,dist,xo,yo)                
                    
            if winsAnalise(s,LARGURA, ALTURA, w, win, player): #draw or victory
                if win == 'w':
                    winner[player] += 1
                break 
            player += 1
            if player >= NPLAYERS:
                player = 0 
        

    getWinner(LARGURA, ALTURA, NPLAYERS, w, winner)
    return



def galo_BOT(NPLAYERS, BOARDSIZE, RONDAS, dificulty, NBOTS):

    winner = []
    for i in range(NPLAYERS): #initialize vector with number of wins for each player
        winner.append(0)

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
            
        player = r % NPLAYERS
        w = makescreen(BOARDSIZE,dist,xo,yo,RONDAS,r) #cria a janela de jogo
        
        while not sair:
            pygame.display.update()    
            #DESTA MANEIRA OS JOGADORES HUMANOS COMEÇAM PRIMEIRO     
            if (player >= NPLAYERS - NBOTS): # (players > 0) or (player < NPLAYERS - 1 and not first):
                printsPlayer(w, LARGURA, ALTURA, player)
                if bot[0]: #easy just random
                    freePos = freePosFunc(Board, BOARDSIZE)
                    randomBot(Board, dist, xo, yo, w, player, freePos)
                elif bot[1]: # only knows if he can win on the spot or if someone else can in their next move (and stops them)
                    thinking(w, LARGURA, ALTURA, player)
                    freePos = freePosFunc(Board, BOARDSIZE)
                    temp = len(freePos)
                    best = GodBot(NPLAYERS, Board, BOARDSIZE, player, freePos, temp, 1, 0)
                    notThinking(w, LARGURA, ALTURA)
                    Play(Board, dist, xo, yo, w,player,best[0][0],best[0][1])
                else: #hard
                    thinking(w, LARGURA, ALTURA, player)
                    freePos = freePosFunc(Board, BOARDSIZE)
                    temp = len(freePos)
                    best = GodBot(NPLAYERS, Board, BOARDSIZE, player, freePos, temp)
                    notThinking(w, LARGURA, ALTURA)
                    Play(Board, dist, xo, yo, w,player,best[0][0],best[0][1])
                unprintsPlayer(w, LARGURA, ALTURA)
                win = Wins(BOARDSIZE, w, Board, dist, xo, yo)
                if winsAnalise(s,LARGURA, ALTURA, w, win, player):
                    if win == 'w':
                        winner[player] += 1
                    t = 2
                    break 

                player += 1
                if player == NPLAYERS:
                    player = 0

            else:
                printsPlayer(w, LARGURA, ALTURA, player)
                p = player
                player = humanPlay(NPLAYERS, BOARDSIZE, Board, dist, xo, yo, w, player) 
                unprintsPlayer(w, LARGURA, ALTURA)
                if player == -1:
                    return   
                elif player == -2:
                    option = pause(w,s)
                    if option == 1:
                        pygame.time.delay(100)
                        w = makescreen(BOARDSIZE, dist, xo, yo, RONDAS, r)
                        for l in range (BOARDSIZE):
                            for c in range (BOARDSIZE):
                                if (Board[c][l] != -1):
                                    player_d = Board[c][l]
                                    shapes(dist, xo, yo, w, player_d, c, l)   
                        player = p - 1
                    elif option == 2:
                        pygame.time.delay(100)
                        return -1   
                    elif option == 3:
                        sair = True
                        pygame.time.delay(100)
                        return 
                win = Wins(BOARDSIZE,w,Board,dist,xo,yo)                       
                if winsAnalise(s,LARGURA, ALTURA, w, win, player):
                    if win == 'w':
                        winner[player] += 1
                    t = 2
                    break 
                player += 1
                if player >= NPLAYERS:
                    player = 0 

    
    getWinner(LARGURA, ALTURA, NPLAYERS, w, winner)
    return
