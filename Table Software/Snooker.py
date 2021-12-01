import pygame
import random
pygame.init()

from assets.Color import *
from assets.Dimensions import *
from assets.buttons_and_text import *
from math import e, sqrt, sin, cos, pi, atan, acos
from random import randint
from assets.fade import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snooker')

# image = pygame.image.load("assets/images/taco.png").convert()
""" screen.blit(image, (0,0))
pygame.display.flip()
pygame.time.delay(1500) """

BALL_RADIUS = int(20)
HOLE_RADIUS = int((2 * BALL_RADIUS * 1.6)/2)
TABLE_WIDTH = int(SCREEN_WIDTH)
TABLE_HEIGHT = int(TABLE_WIDTH // 2)
BORDER_SIZE = HOLE_RADIUS

#print(2 * HOLE_RADIUS, TABLE_HEIGHT - BORDER_SIZE, TABLE_WIDTH / 2 - 3 * HOLE_RADIUS, BORDER_SIZE, WHITE)

def AngleVector(x, y):
    """ Returns the angle of a vector with the x axis """

    try:
        angle = atan(y/x)
    except ZeroDivisionError:
        if y < 0:
            return -pi/2
        else:
            return pi/2

    if x < 0:
        angle += pi

    return angle 

def MagnitudeVector(x, y):
    """ Returns the magnitude of a vector """
    return sqrt(x**2 + y**2)

def Check(ball, pos):
    dist_x = ball.x - pos[0]
    dist_y = ball.y - pos[1]

    # see if collided WHYYYYY
    dist = sqrt(dist_x ** 2 + dist_y ** 2)

    if dist <= ball.radius: 
        return 1
    return 0

class Border():
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def Render(self):
        """ Renders the border """

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))

    def CheckCollision(self, ball):
        """ Checks if a ball has collided with self """

        near_x, near_y = self.GetNearestPoint(ball)

        # get normal vector and get distance
        normal_x = ball.x - near_x
        normal_y = ball.y - near_y
        dist = MagnitudeVector(normal_x, normal_y)
        normal_x /= dist
        normal_y /= dist

        if dist <= ball.radius:
            #print("here")

            # rotate axis
            vel_x = normal_y * ball.vel_x - normal_x * ball.vel_y
            vel_y = normal_x * ball.vel_x + normal_y * ball.vel_y

            # invert y
            vel_y *= -.95

            # de-rotate axis
            ball.vel_x = normal_y * vel_x + normal_x * vel_y
            ball.vel_y = -normal_x * vel_x + normal_y * vel_y

            # makes balls (and all my problems) go away
            while MagnitudeVector(ball.x - near_x, ball.y - near_y) <= ball.radius:
                ball.Move()
                # near_x, near_y = self.GetNearestPoint(ball)

    def GetNearestPoint(self, ball):
        """ Calculates the nearest point of self to the border """

        # aligned vertically
        if ball.x >= self.x and ball.x <= self.x + self.w:
            if ball.y > self.y:
                y = self.y + self.h
            else:
                y = self.y

            x = ball.x

        # aligned horizontally
        elif ball.y >= self.y and ball.y <= self.y + self.h:
            if ball.x > self.x:
                x = self.x + self.w
            else:
                x = self.x

            y = ball.y

        # coming from a diagonal
        else:
            # discover wich corner the ball is aproaching
            if ball.x < self.x:
                x = self.x
            else: 
                x = self.x + self.w

            if ball.y < self.y:
                y = self.y
            else:
                y = self.y + self.h

        return x, y

class taco():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.radius = radius 
        self.original = pygame.image.load("assets/images/taco.png").convert_alpha()
        self.angle = AngleVector(self.vel_x, self.vel_y)
        self.image = pygame.transform.rotate(self.original, self.angle)
           

    def erase(self, holes, balls, walls, players, player):
        screen.fill(DARK_GREEN)
    
        for hole in holes:
            hole.Render()        

        for b in balls:
            b.Render()

        for wall in walls:
            wall.Render()
        drawMove(screen,players,player)


    def render(self, pos, balls):
        self.x = pos[0]
        self.y = pos[1]
        self.angle =  AngleVector(-(balls[0].x - self.x), balls[0].y - self.y) * 180 / pi + 33


        self.image = pygame.transform.rotate(self.original, self.angle)
        screen.blit(self.image, (pos[0] - self.image.get_width() // 2, pos[1] - self.image.get_height() // 2))
        pygame.display.flip() 
        #pygame.time.delay(15)
        #self.erase(holes, balls, walls, players, player)

    
    def render2(self, pos, balls):
        self.x = pos[0]
        self.y = pos[1]

        dist_x = balls[0].x - self.x
        dist_y = balls[0].y - self.y

        
        dist = sqrt(dist_x ** 2 + dist_y ** 2)
        if dist <= BALL_RADIUS:
            return 1, []
        x = cos((self.angle - 33) * pi / 180) * dist + balls[0].x
        y = sin(-(self.angle - 33) * pi / 180) * dist + balls[0].y
        
        screen.blit(self.image, (x - self.image.get_width() // 2, y - self.image.get_height() // 2))
        pygame.display.flip() 
        #pygame.time.delay(15)
        return 0, [x, y]
        #self.erase(holes, balls, walls, players, player)

    
    def move(self, balls, holes, walls, players, player, first = True):
        drawMove(screen,players,player)
        pygame.display.flip()
        a = 1
        first = 1
        flag = 0
        while a:
            for event in pygame.event.get():                              
                if pygame.mouse.get_pressed()[0]:
                    pos = list(event.pos)
                    if (first and pos[0] > (SCREEN_WIDTH//30)-5) and (pos[0] < (SCREEN_WIDTH//19)+5) and (pos[1] > (SCREEN_HEIGHT-(SCREEN_HEIGHT//12))) and (pos[1] < (SCREEN_HEIGHT - (SCREEN_HEIGHT//55))): #se clicarem na pausa                        
                        option = pause(screen)
                        if option == 1: #return
                            pygame.time.delay(100)
                            screen.fill(DARK_GREEN)  
                            for hole in holes:
                                hole.Render()

                            for b in balls:
                                b.Render()

                            for wall in walls:
                                wall.Render()
                            drawMove(screen,players,player) 

                            pygame.display.flip()
                            break
                        elif option == 2: #restart
                            return "restart"
                        elif option == 3: #quit
                            return "quit"
                    
                    elif (first and pos[0] > (9.5*SCREEN_WIDTH//10) - SCREEN_WIDTH//70) and (pos[0] < (9.5*SCREEN_WIDTH//10) + SCREEN_WIDTH // 60) and (pos[1] > (SCREEN_HEIGHT-(SCREEN_HEIGHT//11))) and (pos[1] < (SCREEN_HEIGHT - (SCREEN_HEIGHT//55))): #se clicarem no ?
                        about(screen)
                        pygame.time.delay(100)
                        screen.fill(DARK_GREEN)  
                        for hole in holes:
                            hole.Render()

                        for b in balls:
                            b.Render()

                        for wall in walls:
                            wall.Render()
                        drawMove(screen,players,player) 

                        pygame.display.flip()
                        break

                    elif Check(balls[0], pos):
                            continue
                    else:
                        self.erase(holes, balls, walls, players, player)
                        first = 0
                        self.render(pos, balls)
                        

                elif not first:
                    a = 0
                    flag = 1
                    break
                    
        first = 1
        vel_xPrev = []
        vel_yPrev = []
        while flag:
            for event in pygame.event.get():                              
                if pygame.mouse.get_pressed()[0]:
                    pos = list(event.pos)
                    if (first and pos[0] > (SCREEN_WIDTH//30)-5) and (pos[0] < (SCREEN_WIDTH//19)+5) and (pos[1] > (SCREEN_HEIGHT-(SCREEN_HEIGHT//12))) and (pos[1] < (SCREEN_HEIGHT - (SCREEN_HEIGHT//55))): #se clicarem na pausa                        
                        option = pause(screen)
                        if option == 1: #return
                            pygame.time.delay(100)
                            screen.fill(DARK_GREEN)  
                            for hole in holes:
                                hole.Render()

                            for b in balls:
                                b.Render()

                            for wall in walls:
                                wall.Render()
                            drawMove(screen,players,player) 

                            pygame.display.flip()
                            break
                        elif option == 2: #restart
                            return "restart"
                        elif option == 3: #quit
                            return "quit"

                    elif (first and pos[0] > (9.5*SCREEN_WIDTH//10) - SCREEN_WIDTH//70) and (pos[0] < (9.5*SCREEN_WIDTH//10) + SCREEN_WIDTH // 60) and (pos[1] > (SCREEN_HEIGHT-(SCREEN_HEIGHT//11))) and (pos[1] < (SCREEN_HEIGHT - (SCREEN_HEIGHT//55))): #se clicarem no ?
                        about(screen)
                        pygame.time.delay(100)
                        screen.fill(DARK_GREEN)  
                        for hole in holes:
                            hole.Render()

                        for b in balls:
                            b.Render()

                        for wall in walls:
                            wall.Render()
                        drawMove(screen,players,player) 

                        pygame.display.flip()
                        break

                    else:
                        self.erase(holes, balls, walls, players, player)
                        aux, pos = self.render2(pos, balls)
                        if aux and not first:
                            if self.CheckCollision(balls[0]):
                                flag = 0
                                break
                        if first:
                            self.vel_x = 0
                            self.vel_y = 0
                            vel_x = 0
                            vel_y = 0
                            first = 0
                        else:
                            vel_x = (pos[0] - stickPrev[0]) / 1.5
                            vel_y = (pos[1] - stickPrev[1]) / 1.5

                        stickPrev = pos
                        vel_xPrev.append(vel_x) 
                        vel_yPrev.append(vel_y)
                        if (len(vel_xPrev) > 5):
                            vel_xPrev.pop(0)
                            vel_yPrev.pop(0)
                        self.vel_x = sum(vel_xPrev) / len(vel_xPrev)
                        self.vel_y = sum(vel_yPrev) / len(vel_yPrev)
                        """ print("X: ", vel_xPrev)
                        print("Y: ", vel_yPrev) """
                elif not first:
                    first = 1
                        
                    
                
    
    @property
    def Velocity(self):
        return MagnitudeVector(self.vel_x, self.vel_y)

    def CheckCollision(self, ball): 
        """ Checks if a ball has collided with self """
        
        dist_x = ball.x - self.x
        dist_y = ball.y - self.y

        # see if collided WHYYYYY
        dist = sqrt(dist_x ** 2 + dist_y ** 2)

        if dist <= ball.radius: 
            # calculate modulus of velocitys
            vel_self = self.Velocity

            # calculate incidence angles of balls
            angle_self = AngleVector(self.vel_x, self.vel_y)

            # calculate the angle of collision
            #angle_ab = AngleVector(dist_x, dist_y)

            ball.vel_x = vel_self * cos(angle_self)
            ball.vel_y = vel_self * sin(angle_self)

            #ball.vel_x = vel_self * cos(angle_self - angle_ab) * cos(angle_ab) + vel_ball * sin(- angle_ab) * cos(angle_ab + pi / 2)
            #ball.vel_y = vel_self * cos(angle_self - angle_ab) * sin(angle_ab) + vel_ball * sin(- angle_ab) * sin(angle_ab + pi / 2)
            return 1

        return 0

class Ball():
    def __init__(self, x, y, radius, color, velx = 0, vely = 0):
        self.x = x
        self.y = y
        self.vel_x = velx
        self.vel_y = vely
        self.radius = radius
        self.color = color
    
    def Render(self):
        """ Renders the ball """

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def Move(self, atrito = True):
        """ Moves the ball """

        self.x += self.vel_x
        self.y += self.vel_y

        if atrito:
            # atrito
            self.ChangeVelMagnitude(self.Velocity*0.996)

            #print(self.Velocity, self.x)

            # self.vel_x -= 0.001*self.vel_x #atrito
            # self.vel_y -= 0.001*self.vel_y #atrito

            if self.Velocity < 0.1: 
                self.vel_x = 0
                self.vel_y = 0

    @property
    def Velocity(self):
        return MagnitudeVector(self.vel_x, self.vel_y)

    def ChangeVelMagnitude(self, magnitude):
        """ Changes the magnitude of the velocity, maintaining the direction """

        original_magnitude = self.Velocity

        if original_magnitude == 0: return

        self.vel_x *= magnitude/original_magnitude
        self.vel_y *= magnitude/original_magnitude

    def CheckCollision(self, ball):
        """ Checks if a ball has collided with self """

        # vector that links the balls
        dist_x = ball.x - self.x
        dist_y = ball.y - self.y

        # see if collided
        dist = sqrt(dist_x ** 2 + dist_y ** 2)

        if dist <= self.radius + ball.radius:

            while dist < 2 * self.radius:   #fix bug of balls on top of each other
                if self.vel_x != 0 or self.vel_y != 0:
                    self.x -= self.vel_x / 100
                    self.y -= self.vel_y / 100
                if ball.vel_x != 0 or ball.vel_y != 0:
                    ball.x -= ball.vel_x / 100
                    ball.y -= ball.vel_y / 100
                """ else:   #Error
                    print("ERROR")
                    self.vel_x = 1
                    continue """
                # vector that links the balls
                dist_x = ball.x - self.x
                dist_y = ball.y - self.y

                # see if collided
                dist = sqrt(dist_x ** 2 + dist_y ** 2)

            # calculate modulus of velocitys
            vel_self = self.Velocity
            vel_ball = ball.Velocity

            vel_self *= 0.95 #loss of energy
            vel_ball *= 0.95

            # calculate incidence angles of balls
            angle_self = AngleVector(self.vel_x, self.vel_y)

            angle_ball = AngleVector(ball.vel_x, ball.vel_y)

            # calculate the angle of collision
            angle_ab = AngleVector(dist_x, dist_y)

            # calculate velocities, using this equations: https://williamecraver.wixsite.com/elastic-equations
            self.vel_x = vel_ball * cos(angle_ball - angle_ab) * cos(angle_ab) + vel_self * sin(angle_self - angle_ab) * cos(angle_ab + pi / 2)
            self.vel_y = vel_ball * cos(angle_ball - angle_ab) * sin(angle_ab) + vel_self * sin(angle_self - angle_ab) * sin(angle_ab + pi / 2)

            ball.vel_x = vel_self * cos(angle_self - angle_ab) * cos(angle_ab) + vel_ball * sin(angle_ball - angle_ab) * cos(angle_ab + pi / 2)
            ball.vel_y = vel_self * cos(angle_self - angle_ab) * sin(angle_ab) + vel_ball * sin(angle_ball - angle_ab) * sin(angle_ab + pi / 2)

            vel_self = self.Velocity
            vel_ball = ball.Velocity

            # print(self.vel_x, self.vel_y, ball.vel_x, ball.vel_y)

            # self.ChangeVelMagnitude(2)
            # ball.ChangeVelMagnitude(2)

            #count = 0

            # makes balls (and all my problems) go away
            """ while (sqrt((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2) <= self.radius + ball.radius) and count < 1000:
                self.Move(atrito = False)
                ball.Move(atrito = False)
                
                count +=  """

            # self.ChangeVelMagnitude(vel_self)
            # ball.ChangeVelMagnitude(vel_ball)

class Hole():
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    
    def Render(self):
        """ Renders the hole """

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    
    def getOptimal(self):
        if self.x == HOLE_RADIUS and self.y == HOLE_RADIUS: #top left
            return HOLE_RADIUS + cos(pi/4) * HOLE_RADIUS, HOLE_RADIUS + HOLE_RADIUS * sin(pi/4)
        elif self.x == TABLE_WIDTH - HOLE_RADIUS and self.y == TABLE_HEIGHT - HOLE_RADIUS: #bottom right
            return TABLE_WIDTH - HOLE_RADIUS - cos(pi/4) * HOLE_RADIUS, TABLE_HEIGHT - HOLE_RADIUS - HOLE_RADIUS * sin(pi/4)
        elif self.x == HOLE_RADIUS and self.y == TABLE_HEIGHT - HOLE_RADIUS: #bottom left
            return HOLE_RADIUS + cos(pi/4) * HOLE_RADIUS, TABLE_HEIGHT - HOLE_RADIUS - HOLE_RADIUS * sin(pi/4)
        elif self.x == TABLE_WIDTH - HOLE_RADIUS and self.y == HOLE_RADIUS: #top right
            return TABLE_WIDTH - HOLE_RADIUS - cos(pi/4) * HOLE_RADIUS, HOLE_RADIUS + HOLE_RADIUS * sin(pi/4)
        elif self.x == TABLE_WIDTH/2 and self.y == 0: #top middle
            return TABLE_WIDTH / 2, HOLE_RADIUS
        elif self.x == TABLE_WIDTH/2 and self.y == TABLE_HEIGHT: #bottom middle
            return TABLE_WIDTH / 2, TABLE_HEIGHT - HOLE_RADIUS

        """ [
        Hole(HOLE_RADIUS, HOLE_RADIUS, HOLE_RADIUS, BLACK), 
        Hole(TABLE_WIDTH - HOLE_RADIUS, TABLE_HEIGHT - HOLE_RADIUS, HOLE_RADIUS, BLACK), 
        Hole(HOLE_RADIUS, TABLE_HEIGHT - HOLE_RADIUS, HOLE_RADIUS, BLACK), 
        Hole(TABLE_WIDTH - HOLE_RADIUS, HOLE_RADIUS, HOLE_RADIUS, BLACK), 
        Hole(TABLE_WIDTH/2, 0, HOLE_RADIUS, BLACK), 
        Hole(TABLE_WIDTH/2, TABLE_HEIGHT, HOLE_RADIUS, BLACK)
        ] """


    def CheckCollision(self, ball):
        """ Checks if a ball has collided with self """

        # vector that links the balls
        dist_x = ball.x - self.x
        dist_y = ball.y - self.y

        # see if collided
        dist = sqrt(dist_x ** 2 + dist_y ** 2)

        if dist <= self.radius:
            self.vel_x = dist_x
            self.vel_y = dist_y
            return True
        
        return False

class Player():
    def __init__(self, color = -1, balls = 0):
        self.color = color
        self.balls = balls
        self.prevBalls = 0

class BOT():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.radius = radius 
        self.original = pygame.image.load("assets/images/taco.png").convert_alpha()
        self.angle = AngleVector(self.vel_x, self.vel_y)
        self.image = pygame.transform.rotate(self.original, self.angle)
           

    def erase(self, holes, balls, walls, players, player):
        screen.fill(DARK_GREEN)
    
        for hole in holes:
            hole.Render()        

        for b in balls:
            b.Render()

        for wall in walls:
            wall.Render()
        drawMove(screen,players,player)


    def render(self, pos, balls):
        self.x = pos[0]
        self.y = pos[1]
        self.angle =  AngleVector(-(balls[0].x - self.x), balls[0].y - self.y) * 180 / pi + 33


        self.image = pygame.transform.rotate(self.original, self.angle)
        screen.blit(self.image, (pos[0] - self.image.get_width() // 2, pos[1] - self.image.get_height() // 2))
        pygame.display.flip() 
        #pygame.time.delay(15)
        #self.erase(holes, balls, walls, players, player)


    
    def move(self, balls, holes, walls, players, player):
        random.shuffle(balls)   #Just for a little bit of randomness
        for i in range(len(balls)):
            if balls[i].color == WHITE and i != 0:
                aux = balls[0]
                balls[0] = balls[i]
                balls[i] = aux
                break
        
                

        pos = [0, 0]
        drawMove(screen,players,player)
        pygame.display.flip()

        angle = self.getVel(balls, holes, walls, players, player)

        self.vel_x = 16 * cos(angle)
        self.vel_y = 16 * sin(angle)

        pos[0] = balls[0].x - 20 * self.vel_x
        pos[1] = balls[0].y - 20 * self.vel_y

        self.render(pos, balls)  

        self.x = pos[0]
        self.y = pos[1]  

        while True:
            self.x += 0.25 * self.vel_x
            self.y += 0.25 * self.vel_y 
            if self.CheckCollision(balls[0]):
                break             
            self.erase(holes, balls, walls, players, player)
            screen.blit(self.image, (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2))
            pygame.display.flip()                        
                    


    def checkCollisonBall(self, balls, ball1, ball2, aux_dist):
        for aux in balls:
            dist = sqrt((ball2.x - balls[0].x)**2 + (ball2.y - balls[0].y)**2)
            #print(dist, aux_dist)

            if  dist >= aux_dist:
                return 2

            if aux.color == WHITE:
                continue
            dist_x = aux.x - ball2.x
            dist_y = aux.y - ball2.y

            # see if collided WHYYYYY
            dist = sqrt(dist_x ** 2 + dist_y ** 2)


            if dist <= 2 * ball1.radius: 
                if aux == ball1:
                    return 1
                else:
                    return 2
        return 0


    def checkCollisonHole(self, balls, ball, tryBall, walls, hole):

        aux_x, aux_y = hole.getOptimal()
        dist_x = aux_x - ball.x
        dist_y = aux_y - ball.y

        dist = sqrt(dist_x ** 2 + dist_y ** 2)

        if dist <= BALL_RADIUS:
            return 1

        for aux in balls:
            if aux.color == WHITE or aux == tryBall:
                continue
            dist_x = aux.x - ball.x
            dist_y = aux.y - ball.y

            # see if collided WHYYYYY
            dist = sqrt(dist_x ** 2 + dist_y ** 2)


            if dist <= 2 * BALL_RADIUS:
                return 2

        for wall in walls:
            near_x, near_y = wall.GetNearestPoint(ball)

            # get normal vector and get distance
            normal_x = ball.x - near_x
            normal_y = ball.y - near_y
            dist = MagnitudeVector(normal_x, normal_y)

            if dist <= BALL_RADIUS:
                return 2
        
        return 0
    

    def getVel(self, balls, holes, walls, players, player):
        direction = 0
        aux = Ball(0, 0, BALL_RADIUS, WHITE)
        aux2 = Ball(0, 0, BALL_RADIUS, WHITE)
        aux_x = 0
        aux_y = 0
        temp = 0
        angle_ab = 0
        aux_dist = 0
        flag = 1

        for ball in balls:
            if ((ball.color == RED and (players[player].color == 0 or players[player].color == -1)) or (ball.color == BLUE and (players[player].color == 1 or players[player].color == -1)) or (players[player].balls == 7 and ball.color == LIGHT_BLACK)):
                for hole in holes:
                    aux_x, aux_y = hole.getOptimal()
                    direction = AngleVector(aux_x - ball.x, aux_y - ball.y)
                    #aux_dist = sqrt((hole.x - ball.x)**2 + (hole.y - ball.y)**2)

                    angle_ab = direction
                    aux_x = ball.x - 2 * BALL_RADIUS * cos(angle_ab)
                    aux_y = ball.y - 2 * BALL_RADIUS * sin(angle_ab)
                    direction = AngleVector(aux_x - balls[0].x, aux_y - balls[0].y)

                    """ aux.x = aux_x
                    aux.y = aux_y
                    aux.Render()
                    pygame.display.flip()


                    flag = 0
                    while not flag:
                        pygame.display.update()            
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                flag = 1
                                break """

                    aux_dist = sqrt((ball.x - balls[0].x)**2 + (ball.y - balls[0].y)**2 + 4 * BALL_RADIUS **2)
                    #aux_dist -= aux_dist / 10   #To avoid errors

                    if aux_dist <= sqrt((aux_x - balls[0].x)**2 + (aux_y - balls[0].y)**2):
                        continue

                    else: #check if ther's a free path
                        #return direction
                        aux.x = balls[0].x
                        aux.y = balls[0].y
                        aux.vel_x = 16 * cos(direction)
                        aux.vel_y = 16 * sin(direction)
                        flag = 1

                        while flag:
                            #print(aux.x)
                            aux.x += aux.vel_x
                            aux.y += aux.vel_y
                            """ aux.Render()
                            pygame.display.flip() """
                            temp = self.checkCollisonBall(balls, ball, aux, aux_dist)

                            if temp == 1: #no balls in the way of the white ball
                                aux2.x = ball.x
                                aux2.y = ball.y
                                aux2.vel_x = 2 * cos(angle_ab)
                                aux2.vel_y = 2 * sin(angle_ab)

                                while True:
                                    aux2.x += aux2.vel_x
                                    aux2.y += aux2.vel_y
                                    temp = self.checkCollisonHole(balls, aux2, ball, walls, hole)
                                    """ aux2.color = ball.color
                                    aux2.Render() """
                                    pygame.display.flip()

                                    if temp == 1:
                                        return direction

                                    elif temp == 2:
                                        flag = 0
                                        break

                                    else:
                                        continue

                                
                            elif temp == 2: #ball in the way
                                break

                            else:
                                continue

                    """ flag = 0
                    while not flag:
                        pygame.display.update()            
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                flag = 1
                                break  """



                    """ angleWhite = AngleVector(ball.x - balls[0].x, ball.y - balls[0].y)
                    dist = sqrt((ball.x - balls[0].x)**2 + (ball.y - balls[0].y)**2)
                    angle = angleWhite - (2 * BALL_RADIUS) / dist
                    angleWhite = angleWhite + (2 * BALL_RADIUS) / dist
                    flag = 0
                    while angle <= angleWhite and not flag:
                        aux.x = balls[0].x
                        aux.y = balls[0].y
                        aux.vel_x = 16 * cos(angle)
                        aux.vel_y = 16 * sin(angle)
                        while True:
                            aux.x += aux.vel_x
                            aux.y += aux.vel_y
                            if sqrt((aux.x - balls[0].x)**2 + (aux.y - balls[0].y)**2) > dist:
                                break
                            temp = self.checkCollisonBall(balls, ball, aux)
                            if temp == 1: #calculate angle
                                angle_ab = AngleVector(ball.x - aux.x, ball.y - aux.y)
                                print(angle_ab, direction)
                                if angle_ab >= direction - 1 / aux_dist and angle_ab <= direction + 1 / aux_dist:
                                    return angle
                                else:
                                    break
                            elif temp == 2:
                                flag = 1
                                break
                            else:
                                continue


                        angle += 1/dist """
                #ball.vel_x = vel_self * cos(angle_self - angle_ab) * cos(angle_ab)
                #for hole in holes:
        return direction

            


    @property
    def Velocity(self):
        return MagnitudeVector(self.vel_x, self.vel_y)

    def CheckCollision(self, ball): 
        """ Checks if a ball has collided with self """
        
        dist_x = ball.x - self.x
        dist_y = ball.y - self.y

        # see if collided WHYYYYY
        dist = sqrt(dist_x ** 2 + dist_y ** 2)

        if dist <= ball.radius: 
            # calculate modulus of velocitys
            vel_self = self.Velocity

            # calculate incidence angles of balls
            angle_self = AngleVector(self.vel_x, self.vel_y)

            # calculate the angle of collision
            #angle_ab = AngleVector(dist_x, dist_y)

            ball.vel_x = vel_self * cos(angle_self)
            ball.vel_y = vel_self * sin(angle_self)

            #ball.vel_x = vel_self * cos(angle_self - angle_ab) * cos(angle_ab) + vel_ball * sin(- angle_ab) * cos(angle_ab + pi / 2)
            #ball.vel_y = vel_self * cos(angle_self - angle_ab) * sin(angle_ab) + vel_ball * sin(- angle_ab) * sin(angle_ab + pi / 2)
            return 1

        return 0

def stoped(balls):
    for b in balls:
        if b.vel_x != 0 or b.vel_y != 0:
            return 0
    return 1

def bolaBranca(balls, holes, walls, players, player, bot = 0):
    b = 1
    """ if len(balls) == 16:
        return 0 """
    if balls[0].color != WHITE: #white fell in hole
        if not bot:
            drawWhite(screen,players,player)
            pygame.display.flip()
            first = 1
            while b:
                for event in pygame.event.get():                              
                    if pygame.mouse.get_pressed()[0]:
                        pos = list(event.pos)
                        
                        if (first and pos[0] > (SCREEN_WIDTH//30)-5) and (pos[0] < (SCREEN_WIDTH//19)+5) and (pos[1] > (SCREEN_HEIGHT-(SCREEN_HEIGHT//12))) and (pos[1] < (SCREEN_HEIGHT - (SCREEN_HEIGHT//55))): #se clicarem na pausa
                            option = pause(screen)
                            if option == 1: #return
                                pygame.time.delay(100)
                                screen.fill(DARK_GREEN)  
                                for hole in holes:
                                    hole.Render()

                                for b in balls:
                                    if b == balls[0] and b.color == WHITE:
                                        continue
                                    b.Render()

                                for wall in walls:
                                    wall.Render()
                                drawWhite(screen,players,player) 

                                pygame.display.flip()
                                break
                            elif option == 2: #restart
                                #Snooker()
                                return "restart"
                            elif option == 3: #quit
                                return "quit"
                        
                        elif (first and pos[0] > (9.5*SCREEN_WIDTH//10) - SCREEN_WIDTH//70) and (pos[0] < (9.5*SCREEN_WIDTH//10) + SCREEN_WIDTH // 60) and (pos[1] > (SCREEN_HEIGHT-(SCREEN_HEIGHT//11))) and (pos[1] < (SCREEN_HEIGHT - (SCREEN_HEIGHT//55))): #se clicarem no ?
                            about(screen)
                            pygame.time.delay(100)
                            screen.fill(DARK_GREEN)  
                            for hole in holes:
                                hole.Render()

                            for b in balls:
                                b.Render()

                            for wall in walls:
                                wall.Render()
                            drawMove(screen,players,player) 

                            pygame.display.flip()
                            break
                        
                        else:
                            if pos[0] <= BORDER_SIZE + BALL_RADIUS:
                                pos[0] = BORDER_SIZE + BALL_RADIUS
                            elif pos[0] > TABLE_WIDTH - (BORDER_SIZE + BALL_RADIUS):
                                pos[0] = TABLE_WIDTH - (BORDER_SIZE + BALL_RADIUS)
                            if pos[1] <= BORDER_SIZE + BALL_RADIUS:
                                pos[1] = BORDER_SIZE + BALL_RADIUS
                            elif pos[1] > TABLE_HEIGHT - (BORDER_SIZE + BALL_RADIUS):
                                pos[1] = TABLE_HEIGHT - (BORDER_SIZE + BALL_RADIUS)
                            if first:
                                first = 0
                                balls.insert(0, Ball(pos[0], pos[1], BALL_RADIUS, WHITE))

                            balls[0].x = pos[0]
                            balls[0].y = pos[1]
                            balls[0].Render()
                            pygame.display.flip()
                            pygame.time.delay(15)
                            screen.fill(DARK_GREEN)    
                            for hole in holes:
                                hole.Render()

                            for b in balls:
                                if b == balls[0]:
                                    continue
                                b.Render()

                            for wall in walls:
                                wall.Render()
                            drawWhite(screen,players,player)
                    elif not first:
                        flag = 0
                        for b in balls:
                            if b == balls[0]:
                                continue 
                            dist_x = b.x - balls[0].x
                            dist_y = b.y - balls[0].y

                            # see if collided WHYYYYY
                            dist = sqrt(dist_x ** 2 + dist_y ** 2)

                            if dist <= 2 * b.radius: 
                                flag = 1
                                break
                        if not flag:
                            b = 0
                            break
                        else:
                            first = 1
                            pygame.display.flip()

            balls[0].Render()
            pygame.display.flip()
            return 1
        else:   #Bot is the one to place the ball
            drawWhite(screen,players,player)
            pygame.display.flip()
            pygame.time.delay(300)
            balls.insert(0, Ball(TABLE_WIDTH / 4, TABLE_HEIGHT / 2, BALL_RADIUS, WHITE))
            flag = 1
            while flag:
                for b in balls:
                    if b == balls[0]:
                        continue 
                    dist_x = b.x - balls[0].x
                    dist_y = b.y - balls[0].y

                    # see if collided WHYYYYY
                    dist = sqrt(dist_x ** 2 + dist_y ** 2)

                    if dist <= 2 * b.radius:
                        while True:
                            balls[0].x += 30 
                            dist_x = b.x - balls[0].x

                            # see if collided WHYYYYY
                            dist = sqrt(dist_x ** 2 + dist_y ** 2)

                            if dist > 2 * b.radius:
                                break
                        flag = 0
                        break
                if not flag:
                    flag = 1
                else:
                    flag = 0
            return 1

    return 0

def gotIn(players, player):
    flag1 = 0
    #flag2 = 0
    """ if players[player].prevBalls == 0 and players[(player + 1) % 2].prevBalls == 0:
        flag2 = 1 """
    if players[player].prevBalls < players[player].balls: #meteu uma(s) bola(s) sua
        players[player].prevBalls = players[player].balls 
        flag1 = 1
    if players[(player + 1) % 2].prevBalls < players[(player + 1) % 2].balls: #meteu uma(s) bola(s) do seu adversario
        players[(player + 1) % 2].prevBalls = players[(player + 1) % 2].balls

    """ if flag2:
        if players[player].balls < players[(player + 1) % 2].balls:
            aux = players[player]
            players[player] = players[(player + 1) % 2]
            players[(player + 1) % 2] = aux """

    if flag1:        
        return 1
    else:
        return 0
    
""" def defColor(players, player, balls):
    countB = 0
    countR = 0
    for b in balls:
        if b.color == BLUE:
            countB += 1
        if b.color == RED:
            countR += 1
    
    #BLUE 
    if countB > countR:
        players[player].color = 0
        players[(player + 1) % 2].color = 1
        players[player].balls = 7 - countR
        players[(player + 1) % 2].balls = 7 - countB
        players[player].prevBalls = 7 - countR
        players[(player + 1) % 2].prevBalls = 7 - countB
    elif countR > countB:
        players[player].color = 1
        players[(player + 1) % 2].color = 0
        players[player].balls = 7 - countB
        players[(player + 1) % 2].balls = 7 - countR
        players[player].prevBalls = 7 - countB
        players[(player + 1) % 2].prevBalls = 7 - countR
    else:
        players[player].color = -1
        players[(player + 1) % 2].color = -1
        players[player].balls = 7 - countB
        players[(player + 1) % 2].balls = 7 - countR
        players[player].prevBalls = 7 - countB
        players[(player + 1) % 2].prevBalls = 7 - countR """

def aux(balls): #bug ainda pode correr mal se estiver a linha toda quase toda ocupada..
    flag = 1
    while flag:
        for b in balls:
            if b == balls[len(balls) - 1]:
                continue 
            dist_x = b.x - balls[len(balls) - 1].x
            dist_y = b.y - balls[len(balls) - 1].y

            # see if collided WHYYYYY
            dist = sqrt(dist_x ** 2 + dist_y ** 2)

            if dist <= 2 * b.radius:
                while True:
                    balls[len(balls) - 1].y += 10 
                    dist_y = b.y - balls[len(balls) - 1].y

                    # see if collided WHYYYYY
                    dist = sqrt(dist_x ** 2 + dist_y ** 2)

                    if dist > 2 * b.radius:
                        break
                flag = 0
                break
        if not flag:
            flag = 1
        else:
            flag = 0

def removeBall(players, player, balls):
    if players[player].balls != 0:
        if players[player].color == 1:
            balls.append(Ball(TABLE_WIDTH // 5, TABLE_HEIGHT // 4, BALL_RADIUS, BLUE))
            aux(balls)
        elif players[player].color == 0:
            balls.append(Ball(TABLE_WIDTH // 5, TABLE_HEIGHT // 4, BALL_RADIUS, RED))
            aux(balls)
        else: #já havia bolas dentro de buracos mas ainda n havia cores definidas
            balls.append(Ball(TABLE_WIDTH // 5, TABLE_HEIGHT // 4, BALL_RADIUS, BLUE))
            aux(balls)
            players[player].color = 1
            players[(player + 1) % 2].color = 0
        players[player].balls -= 1
        players[player].prevBalls -= 1
        balls[len(balls) - 1].Render()
        pygame.display.flip()
    return

def pause(w):
    s = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT)) 
    s.set_alpha(200)              
    s.fill((20,20,20))
    
    w.blit(s, (0,0))
    
    text = MAIN_FONT.render("PAUSED", True,WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2,SCREEN_HEIGHT // 4)
    w.blit(text, textRect)
    
    BUTTON_WIDTH = int(SCREEN_WIDTH * 0.8 // 3)
    BUTTON_HEIGHT = int(SCREEN_HEIGHT * 5 // 55)
    
    MAIN_BUTTONS_LAYOUT = [((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 5 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
                       ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 7 // 12, BUTTON_WIDTH, BUTTON_HEIGHT),
                       ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 9 // 12, BUTTON_WIDTH, BUTTON_HEIGHT)]
    
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
        elif button(w,'R E S T A R T', *MAIN_BUTTONS_LAYOUT[1], click):
            sair = True
            return 2
        elif button(w,'Q U I T', *MAIN_BUTTONS_LAYOUT[2], click):
            sair = True
            return 3


def about(w):
    s = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))        
    s.set_alpha(1000)              
    s.fill((20,20,20))

    pygame.display.update()
    w.blit(s, (0,0))
    #LARGE_TEXT
    #ABOUT
    text = LARGE_MIDDLE_TEXT.render("ABOUT", True, DARK_GREEN)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2,SCREEN_HEIGHT // 14)
    w.blit(text, textRect)


    #Gameplay
    text = LARGER_TEXT.render("Gameplay", True, DARK_GREEN)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 15,1.2*SCREEN_HEIGHT // 8)
    w.blit(text, textRect)




    text = WRITTING_FONT.render("Stick:", True, DARK_GREEN)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 26.5, 1.55 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)



    text = WRITTING_FONT.render("While dragging the finger through the screen you can first choose the direction of the stick.", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 3.24, 1.85*SCREEN_HEIGHT // 8)
    w.blit(text, textRect)

    text = WRITTING_FONT.render("After lifting the finger the direction is set and can no longer be changed.", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 4.03, 2.05 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)

    text = WRITTING_FONT.render("Now it's time to hit the ball. For this you need to move the finger in its direction (the finger doesn't need to be on top of the stick).", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2.33, 2.25 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)

    text = WRITTING_FONT.render("The faster the movement the more speed the ball gains after the collision.", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 3.933, 2.45 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)


    text = WRITTING_FONT.render("White ball:", True, DARK_GREEN)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 18.5, 2.75 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)


    text = WRITTING_FONT.render("After one player puts the white ball in the hole the other can now choose the position of the ball.", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 3.07, 3.05 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)

    text = WRITTING_FONT.render("For this you need to move your finger in the screen until you find the most advantageouse position.", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 3, 3.25 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)

    text = WRITTING_FONT.render("The position is set and can no longer be changed after the finger is lifted.", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 4, 3.45 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)

    text = WRITTING_FONT.render(" If the position of the ball when the finger is lifted is not available the player needs to choose a new position with the same process.", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2.32, 3.65 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)

    text = WRITTING_FONT.render("Both buttons (pause and question mark) can be pressed at all times.", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 4.232, 3.95 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)



    text = LARGER_TEXT.render("Rules", True, DARK_GREEN)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 22, 4.45 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)


    text = WRITTING_FONT.render("If the player who put the white ball in the hole had already balls in holes one of them needs to be removed back to the table (specific position).", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2.123, 4.8 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)

    

    text = WRITTING_FONT.render("In the beggining of the game no player has a set color.", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 5.18, 5.1 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)

    text = WRITTING_FONT.render("This color is set automatically when a player puts for the first time a none white and none black ball in a hole.", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2.74, 5.3 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)

    

    text = WRITTING_FONT.render("First player to put all the balls of one color plus the black one wins.", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 4.35, 5.6 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)

    text = WRITTING_FONT.render("If there's only the black ball left for a speciffic and a player puts both the black and the white ball in a hole the other player wins.", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2.352, 5.8 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)

    text = WRITTING_FONT.render("If a player puts the black ball with still balls of his color on the board the other player wins.", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 3.282, 6 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)

    text = WRITTING_FONT.render("Usually if a player with color (A) hits the white ball and the white ball doesn't hit an (A) colored ball first, it counts as a penalty (same as when someone", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2.023, 6.2 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)

    text = WRITTING_FONT.render("puts the white ball in). HOWEVER, because we know you suck, this rule doesn't exist!", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 3.535, 6.4 * SCREEN_HEIGHT // 8)
    w.blit(text, textRect)

    

    while True:
        pygame.display.update()            
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        
#(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2)
def drawMove(screen, players, player):
    pygame.draw.rect(screen, GREY, (0, int(TABLE_HEIGHT), int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))
    pygame.draw.line(screen, BLUE_IST, (0, int(TABLE_HEIGHT + TABLE_HEIGHT/140 - 1)), (int(SCREEN_WIDTH), int(TABLE_HEIGHT + TABLE_HEIGHT/140 - 1)), int(TABLE_HEIGHT / 70))

    pygame.draw.line (screen, WHITE, ((SCREEN_WIDTH//19),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2) - TABLE_HEIGHT // 30), ((SCREEN_WIDTH//19),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2) + TABLE_HEIGHT // 30), TABLE_WIDTH // 120) #pause button
    pygame.draw.line (screen, WHITE, ((SCREEN_WIDTH//30),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2) - TABLE_HEIGHT // 30), ((SCREEN_WIDTH//30),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2) + TABLE_HEIGHT // 30),TABLE_WIDTH // 120)
    if players[player].color == 0:
        text_b = "Player " + str(player + 1) + " (Red), it's time to move!"
    elif players[player].color == 1:
        text_b = "Player " + str(player + 1) + " (Blue), it's time to move!"
    else:
        text_b = "Player " + str(player + 1) + " (No color yet), it's time to move!"

    text_a = "?"

    string_a = LARGE_MIDDLE_TEXT.render(text_a, True, WHITE)

    string_b = SMALL_FONT.render(text_b,True,WHITE)
    string_br = string_b.get_rect()
    string_br.center = ((SCREEN_WIDTH//2),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2))
    screen.blit(string_b,string_br)
    string_br = string_a.get_rect()
    string_br.center = ((9.5*SCREEN_WIDTH//10),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2))

    screen.blit(string_a,string_br)

def drawWhite(screen, players, player):
    pygame.draw.rect(screen, GREY, (0, int(TABLE_HEIGHT), int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))
    pygame.draw.line(screen, BLUE_IST, (0, int(TABLE_HEIGHT + TABLE_HEIGHT/140 - 1)), (int(SCREEN_WIDTH), int(TABLE_HEIGHT + TABLE_HEIGHT/140 - 1)), int(TABLE_HEIGHT / 70))

    pygame.draw.line (screen, WHITE, ((SCREEN_WIDTH//19),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2) - TABLE_HEIGHT // 30), ((SCREEN_WIDTH//19),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2) + TABLE_HEIGHT // 30), TABLE_WIDTH // 120) #pause button
    pygame.draw.line (screen, WHITE, ((SCREEN_WIDTH//30),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2) - TABLE_HEIGHT // 30), ((SCREEN_WIDTH//30),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2) + TABLE_HEIGHT // 30),TABLE_WIDTH // 120)
    if players[player].color == 0:
        text_b = "Choose a place for the white ball: Player " + str((player + 1) % 2 + 1) + " (Blue)"
    elif players[player].color == 1:
        text_b = "Choose a place for the white ball: Player " + str((player + 1) % 2 + 1) + " (Red)"
    else:
        text_b = "Choose a place for the white ball: Player " + str((player + 1) % 2 + 1)

    text_a = "?"

    string_a = LARGE_MIDDLE_TEXT.render(text_a, True, WHITE)
    string_b = SMALL_FONT.render(text_b, True, WHITE)
    string_br = string_b.get_rect()
    string_br.center = ((SCREEN_WIDTH//2),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2))
    screen.blit(string_b,string_br)
    string_br = string_a.get_rect()
    string_br.center = ((9.5*SCREEN_WIDTH//10),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2))

    screen.blit(string_a,string_br)

def draw(screen, players, player):
    pygame.draw.rect(screen, GREY, (0, int(TABLE_HEIGHT), int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))
    pygame.draw.line(screen, BLUE_IST, (0, int(TABLE_HEIGHT + TABLE_HEIGHT/140 - 1)), (int(SCREEN_WIDTH), int(TABLE_HEIGHT + TABLE_HEIGHT/140 - 1)), int(TABLE_HEIGHT / 70))
    pygame.draw.line (screen, WHITE, ((SCREEN_WIDTH//19),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2) - TABLE_HEIGHT // 30), ((SCREEN_WIDTH//19),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2) + TABLE_HEIGHT // 30), TABLE_WIDTH // 120) #pause button
    pygame.draw.line (screen, WHITE, ((SCREEN_WIDTH//30),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2) - TABLE_HEIGHT // 30), ((SCREEN_WIDTH//30),(SCREEN_HEIGHT - (SCREEN_HEIGHT - TABLE_HEIGHT - TABLE_HEIGHT / 70) // 2) + TABLE_HEIGHT // 30),TABLE_WIDTH // 120)
   
    color = players[player].color
    if color == 0: # player 0 is red
        if player == 0:
            text_b = "Player " + str(player + 1) + " (Red): " + str(players[player].balls)
            text_r = "Player " + str((player + 1) % 2 + 1) + " (Blue): " + str(players[(player + 1) % 2].balls)         
        else:
            text_b = "Player " + str(player + 1) + " (Red): " + str(players[player].balls)
            text_r = "Player " + str((player + 1) % 2 + 1) + " (Blue): " + str(players[(player + 1) % 2].balls)         

    elif color == 1:
        if player == 0:
            text_b = "Player " + str(player + 1) + " (Blue): " + str(players[player].balls)
            text_r = "Player " + str((player + 1) % 2 + 1) + " (Red): " + str(players[(player + 1) % 2].balls)
        else:
            text_b = "Player " + str(player + 1) + " (Blue): " + str(players[player].balls)
            text_r = "Player " + str((player + 1) % 2 + 1) + " (Red): " + str(players[(player + 1) % 2].balls)
    else:
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

    
def win(screen,player,players,who):
    
    # who = o -> other player wins ; who = t -> this player wins
    
    s = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT)) 
    s.set_alpha(200)              
    s.fill((20,20,20))
    screen.blit(s, (0,0))
    
    if who == "o": #other player wins
        who = (player + 1) % 2 
    
    else: #this player wins
        who = player 
    
    color = players[who].color
    
    if color == 1: # Blue player wins
        string = "Player " + str(who+1) + " (BLue) Wins!"
    elif color == 0: # Red player wins
        string = "Player " + str(who+1) + " (Red) Wins!"
    else:
        string = "Player " + str( who + 1) + " Wins!"
    
    text_w = MAIN_FONT.render(str(string), True,LIGHT_GREEN)
    textwRect = text_w.get_rect()
    textwRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - (SCREEN_HEIGHT//7))
    
    text_t = SMALL_FONT.render("WOULD YOU LIKE TO PLAY AGAIN?",True, WHITE)
    texttRect = text_t.get_rect()
    texttRect.center = (SCREEN_WIDTH//2,(SCREEN_HEIGHT//2))
    
    screen.blit(text_w,textwRect)
    screen.blit(text_t,texttRect)
    
    pygame.display.update()
    
    sair = False
    click = False
    while not sair:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        if button(screen,'Y E S',(((SCREEN_WIDTH - BUTTON_WIDTH) // 2) - SCREEN_WIDTH//12),(SCREEN_HEIGHT // 2 + (SCREEN_HEIGHT//11)),(BUTTON_WIDTH - SCREEN_WIDTH//11),(BUTTON_HEIGHT), click):
            sair = True
            #Snooker() # Dá bug ao tentar sair do jogo depois ao recomeçar
            return True

        elif button(screen,'N O',(((SCREEN_WIDTH - BUTTON_WIDTH) // 2) + SCREEN_WIDTH//6),(SCREEN_HEIGHT // 2 + (SCREEN_HEIGHT//11)),(BUTTON_WIDTH - SCREEN_WIDTH//11),(BUTTON_HEIGHT) , click):
            sair = True
            return False
        

BOT = BOT(0, 0, 10)
stick = taco(0,0,10)

def Snooker():      

    walls = [
        Border(2.2 * HOLE_RADIUS, 0, TABLE_WIDTH / 2 - 3.2 * HOLE_RADIUS, BORDER_SIZE, WHITE), 
        Border(HOLE_RADIUS + TABLE_WIDTH / 2, 0, TABLE_WIDTH / 2 - 3.2 * HOLE_RADIUS, BORDER_SIZE, WHITE), 
        Border(0, 2.2 * HOLE_RADIUS, BORDER_SIZE, TABLE_HEIGHT - 4.4 * HOLE_RADIUS, WHITE),
        Border(2.2 * HOLE_RADIUS, TABLE_HEIGHT - BORDER_SIZE, TABLE_WIDTH / 2 - 3.2 * HOLE_RADIUS, BORDER_SIZE, WHITE), 
        Border(HOLE_RADIUS + TABLE_WIDTH / 2, TABLE_HEIGHT - BORDER_SIZE, TABLE_WIDTH / 2 - 3.2 * HOLE_RADIUS, BORDER_SIZE, WHITE), 
        Border(TABLE_WIDTH - BORDER_SIZE, 2.2 * HOLE_RADIUS, BORDER_SIZE, TABLE_HEIGHT - 4.4 * HOLE_RADIUS, WHITE),
    ]
    
    holes = [
        Hole(HOLE_RADIUS, HOLE_RADIUS, HOLE_RADIUS, BLACK), 
        Hole(TABLE_WIDTH - HOLE_RADIUS, TABLE_HEIGHT - HOLE_RADIUS, HOLE_RADIUS, BLACK), 
        Hole(HOLE_RADIUS, TABLE_HEIGHT - HOLE_RADIUS, HOLE_RADIUS, BLACK), 
        Hole(TABLE_WIDTH - HOLE_RADIUS, HOLE_RADIUS, HOLE_RADIUS, BLACK), 
        Hole(TABLE_WIDTH/2, 0, HOLE_RADIUS, BLACK), 
        Hole(TABLE_WIDTH/2, TABLE_HEIGHT, HOLE_RADIUS, BLACK)
        ]
    
    balls = [
        #Ball(TABLE_WIDTH // 2,TABLE_HEIGHT // 2, BALL_RADIUS, WHITE, 0, 5),
        # bola branca
        Ball(TABLE_WIDTH // 5, TABLE_HEIGHT // 2, BALL_RADIUS, WHITE),
        # primeira coluna
        Ball(10 *TABLE_WIDTH // 11 - 8 * BALL_RADIUS, TABLE_HEIGHT // 2, BALL_RADIUS, RED),
        # segunda coluna
        Ball(10 *TABLE_WIDTH // 11 - 6 * BALL_RADIUS, TABLE_HEIGHT // 2 + (BALL_RADIUS + 1), BALL_RADIUS, RED),
        Ball(10 *TABLE_WIDTH // 11 - 6 * BALL_RADIUS, TABLE_HEIGHT // 2 - (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
        # terceira coluna
        Ball(10 *TABLE_WIDTH // 11 - 4 * BALL_RADIUS, TABLE_HEIGHT // 2 + 2 * (BALL_RADIUS + 1), BALL_RADIUS, RED),
        Ball(10 *TABLE_WIDTH // 11 - 4 * BALL_RADIUS, TABLE_HEIGHT // 2, BALL_RADIUS, LIGHT_BLACK),
        Ball(10 *TABLE_WIDTH // 11 - 4 * BALL_RADIUS, TABLE_HEIGHT // 2 - 2 * (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
        # quarta coluna
        Ball(10 *TABLE_WIDTH // 11 - 2 * BALL_RADIUS, TABLE_HEIGHT // 2 + 3 * (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
        Ball(10 *TABLE_WIDTH // 11 - 2 * BALL_RADIUS, TABLE_HEIGHT // 2 + (BALL_RADIUS + 1), BALL_RADIUS, RED),
        Ball(10 *TABLE_WIDTH // 11 - 2 * BALL_RADIUS, TABLE_HEIGHT // 2 - (BALL_RADIUS + 1), BALL_RADIUS, RED),
        Ball(10 *TABLE_WIDTH // 11 - 2 * BALL_RADIUS, TABLE_HEIGHT // 2 - 3 * (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
        # quinta coluna
        Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2 + 4 * (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
        Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2 + 2 * (BALL_RADIUS + 1), BALL_RADIUS, RED),
        Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2, BALL_RADIUS, BLUE),
        Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2 - 2 * (BALL_RADIUS + 1), BALL_RADIUS, RED),
        Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2 - 4 * (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
    ]

    # ponham aqui as bolas para testar coisas
    """ balls += [
        #Ball(10 *TABLE_WIDTH // 11 - 10, TABLE_HEIGHT // 2, BALL_RADIUS, WHITE, 0, 0),
        #Ball(TABLE_WIDTH // 2, TABLE_HEIGHT // 2, BALL_RADIUS, WHITE, 50),
        #Ball(TABLE_WIDTH // 2,TABLE_HEIGHT // 2, BALL_RADIUS, WHITE, 5),
        #Ball(TABLE_WIDTH // 2, 3 * TABLE_HEIGHT // 4 + 65, BALL_RADIUS, RED),
        #Ball(TABLE_WIDTH // 2, 3 * TABLE_HEIGHT // 4, BALL_RADIUS, LIGHT_BLACK, 0, 5) #para testar a bola preta entrar
        # Ball(TABLE_WIDTH // 2, TABLE_HEIGHT // 4, BALL_RADIUS, BLUE),
        # Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2 + 2 * (BALL_RADIUS + 1), BALL_RADIUS, RED, 50),
    ] """
    
    balls_in_hole = []
    
    pygame.display.flip()
    
    running = True
    
    flag = 0
    
    players = [Player(), Player()]
    player = 0
    prev = 1
    
    blackin = 0

    first = 1

    fadein_snooker(screen, holes, balls, walls, TABLE_WIDTH, TABLE_HEIGHT)

    pygame.display.flip()
    
    while running:
        pygame.time.delay(10)
        screen.fill(DARK_GREEN)
        
        for hole in holes:
            hole.Render()
    
        for b in balls:
            b.Render()
            b.Move()
    
        for b in balls_in_hole:
            b.Render()
            b.Move()
    
        for wall in walls:
            wall.Render()
        draw(screen,players,player)
    
        pygame.display.flip()
    
        balls_to_remove = []

        if first:
            first = 0
            #print("player: ",player + 1,"|\tcolor (1 -> blue, 0 -> red): ",  players[player].color,"|\tnumber of balls in holes: ", players[player].balls)
            temp = stick.move(balls, holes, walls, players, player)
            if temp == "quit":
                quit_game = True
                return quit_game
            elif temp == "restart":
                return 0
            continue

    
        for i in range(0, len(balls)):
            for j in range(i+1, len(balls)):
                balls[i].CheckCollision(balls[j])
    
            for wall in walls:
                wall.CheckCollision(balls[i])
    
            for hole in holes:
                if hole.CheckCollision(balls[i]):
                    balls_to_remove.append(i)
    
        balls_to_remove.sort(reverse=True)
    
        for i in balls_to_remove:
            if players[player].color != -1:
                if balls[i].color == BLUE and players[player].color == 1:
                    players[player].balls += 1
                elif balls[i].color == RED and players[player].color == 0:
                    players[player].balls += 1
                elif balls[i].color == BLUE and players[player].color == 0:
                    players[(player + 1) % 2].balls += 1
                    if prev:
                        if players[player].balls < players[(player + 1) % 2].balls:
                            aux = players[player]
                            players[player] = players[(player + 1) % 2]
                            players[(player + 1) % 2] = aux
                elif balls[i].color == RED and players[player].color == 1:
                    players[(player + 1) % 2].balls += 1
                    if prev:
                        if players[player].balls < players[(player + 1) % 2].balls:
                            aux = players[player]
                            players[player] = players[(player + 1) % 2]
                            players[(player + 1) % 2] = aux
            else: #atribuir cores
                prev = 1
                if balls[i].color == BLUE:
                    players[player].balls += 1
                    players[player].color = 1
                    players[(player + 1) % 2].color = 0
                elif balls[i].color == RED:
                    players[player].balls += 1
                    players[player].color = 0
                    players[(player + 1) % 2].color = 1 

            if balls[i].color == LIGHT_BLACK:
                blackin = 1
    
            flag = 1
            ball = balls.pop(i)
    
            balls_in_hole.append(ball)
        
        balls_to_remove = []
    
        for i in range(0, len(balls_in_hole)):
            ball.radius -= 1
            if ball.radius < 0:
                flag = 0
                balls_to_remove.append(i)
    
        balls_to_remove.sort(reverse=True)
        for i in balls_to_remove:
            balls_in_hole.pop(i)
    
        if (stoped(balls) and not flag): #time for a move!
            prev = 0
    
            #if in the first move a player puts all the balls from his color and the black one (pretty much impossible) he will lose :/
    
            if blackin and (players[player].balls < 7): #black gone before its time..
                running = win(screen,player,players, "o")
                #print("Player ", (player + 1) % 2 + 1, "Wins!")
                if running == False:
                    quit_game = True
                    return quit_game
                else:
                    pass
                break
    
            if blackin and (players[player].balls == 7):
                if balls[0].color != WHITE: #meteu a preta e a branca...
                    running = win(screen, player,players, "o")
                    #print("Player ", (player + 1) % 2 + 1, "Wins!")
                    if running == False:
                        quit_game = True
                        return quit_game
                    else:
                        pass
                    break
                else: #meteu a preta e ganhou!
                    running = win(screen, player, players, "t") 
                    #print("Player ", player + 1, "Wins!")
                    if running == False:
                        quit_game = True
                        return quit_game
                    else:
                        pass
                    break 
            temp = bolaBranca(balls, holes, walls, players, player)
            if temp == "quit":
                quit_game = True
                return quit_game
            elif temp == "restart":
                return 0
            elif temp: #remove a ball from current player
                removeBall(players, player, balls) 
                
            idk = gotIn(players, player) 
            if not idk or temp: #no ball got in (changes players)
                player += 1
                if player == 2:
                    player = 0
            #print(player + 1) #currently this player is moving
            #print("player: ",player + 1,"|\tcolor (1 -> blue, 0 -> red): ",  players[player].color,"|\tnumber of balls in holes: ", players[player].balls)
            temp = stick.move(balls, holes, walls, players, player)
            if temp == "quit":
                quit_game = True
                return quit_game
            elif temp == "restart":
                return 0
            
            
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (pos[0] > (SCREEN_WIDTH//30)-5) and (pos[0] < (SCREEN_WIDTH//19)+5) and (pos[1] > (SCREEN_HEIGHT-(SCREEN_HEIGHT//12))) and (pos[1] < (SCREEN_HEIGHT - (SCREEN_HEIGHT//55))): #se clicarem na pausa
                    option = pause(screen)
                    if option == 1: #return
                        pygame.time.delay(100)
                    elif option == 2: #restart
                        return 0 # Dá bug ao tentar sair do jogo depois de recomeçar
                        if quit_game == True:
                            return quit_game
                    elif option == 3: #quit
                        quit_game = True
                        return quit_game
                elif (pos[0] > (9.5*SCREEN_WIDTH//10) - SCREEN_WIDTH//70) and (pos[0] < (9.5*SCREEN_WIDTH//10) + SCREEN_WIDTH // 60) and (pos[1] > (SCREEN_HEIGHT-(SCREEN_HEIGHT//11))) and (pos[1] < (SCREEN_HEIGHT - (SCREEN_HEIGHT//55))): #se clicarem no ?
                    about(screen)
                    pygame.time.delay(100)
                    screen.fill(DARK_GREEN)  
                    for hole in holes:
                        hole.Render()

                    for b in balls:
                        b.Render()

                    for wall in walls:
                        wall.Render()
                    drawMove(screen,players,player) 

                    pygame.display.flip()
                    break

def Snooker_BOT(bvb = 0):      

    walls = [
        Border(2.2 * HOLE_RADIUS, 0, TABLE_WIDTH / 2 - 3.2 * HOLE_RADIUS, BORDER_SIZE, WHITE), 
        Border(HOLE_RADIUS + TABLE_WIDTH / 2, 0, TABLE_WIDTH / 2 - 3.2 * HOLE_RADIUS, BORDER_SIZE, WHITE), 
        Border(0, 2.2 * HOLE_RADIUS, BORDER_SIZE, TABLE_HEIGHT - 4.4 * HOLE_RADIUS, WHITE),
        Border(2.2 * HOLE_RADIUS, TABLE_HEIGHT - BORDER_SIZE, TABLE_WIDTH / 2 - 3.2 * HOLE_RADIUS, BORDER_SIZE, WHITE), 
        Border(HOLE_RADIUS + TABLE_WIDTH / 2, TABLE_HEIGHT - BORDER_SIZE, TABLE_WIDTH / 2 - 3.2 * HOLE_RADIUS, BORDER_SIZE, WHITE), 
        Border(TABLE_WIDTH - BORDER_SIZE, 2.2 * HOLE_RADIUS, BORDER_SIZE, TABLE_HEIGHT - 4.4 * HOLE_RADIUS, WHITE),
    ]
    
    holes = [
        Hole(HOLE_RADIUS, HOLE_RADIUS, HOLE_RADIUS, BLACK), 
        Hole(TABLE_WIDTH - HOLE_RADIUS, TABLE_HEIGHT - HOLE_RADIUS, HOLE_RADIUS, BLACK), 
        Hole(HOLE_RADIUS, TABLE_HEIGHT - HOLE_RADIUS, HOLE_RADIUS, BLACK), 
        Hole(TABLE_WIDTH - HOLE_RADIUS, HOLE_RADIUS, HOLE_RADIUS, BLACK), 
        Hole(TABLE_WIDTH/2, 0, HOLE_RADIUS, BLACK), 
        Hole(TABLE_WIDTH/2, TABLE_HEIGHT, HOLE_RADIUS, BLACK)
        ]
    
    balls = [
        #Ball(TABLE_WIDTH // 2,TABLE_HEIGHT // 2, BALL_RADIUS, WHITE, 0, 5),
        # bola branca
        Ball(TABLE_WIDTH // 5, TABLE_HEIGHT // 2, BALL_RADIUS, WHITE),
        # primeira coluna
        Ball(10 *TABLE_WIDTH // 11 - 8 * BALL_RADIUS, TABLE_HEIGHT // 2, BALL_RADIUS, RED),
        # segunda coluna
        Ball(10 *TABLE_WIDTH // 11 - 6 * BALL_RADIUS, TABLE_HEIGHT // 2 + (BALL_RADIUS + 1), BALL_RADIUS, RED),
        Ball(10 *TABLE_WIDTH // 11 - 6 * BALL_RADIUS, TABLE_HEIGHT // 2 - (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
        # terceira coluna
        Ball(10 *TABLE_WIDTH // 11 - 4 * BALL_RADIUS, TABLE_HEIGHT // 2 + 2 * (BALL_RADIUS + 1), BALL_RADIUS, RED),
        Ball(10 *TABLE_WIDTH // 11 - 4 * BALL_RADIUS, TABLE_HEIGHT // 2, BALL_RADIUS, LIGHT_BLACK),
        Ball(10 *TABLE_WIDTH // 11 - 4 * BALL_RADIUS, TABLE_HEIGHT // 2 - 2 * (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
        # quarta coluna
        Ball(10 *TABLE_WIDTH // 11 - 2 * BALL_RADIUS, TABLE_HEIGHT // 2 + 3 * (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
        Ball(10 *TABLE_WIDTH // 11 - 2 * BALL_RADIUS, TABLE_HEIGHT // 2 + (BALL_RADIUS + 1), BALL_RADIUS, RED),
        Ball(10 *TABLE_WIDTH // 11 - 2 * BALL_RADIUS, TABLE_HEIGHT // 2 - (BALL_RADIUS + 1), BALL_RADIUS, RED),
        Ball(10 *TABLE_WIDTH // 11 - 2 * BALL_RADIUS, TABLE_HEIGHT // 2 - 3 * (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
        # quinta coluna
        Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2 + 4 * (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
        Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2 + 2 * (BALL_RADIUS + 1), BALL_RADIUS, RED),
        Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2, BALL_RADIUS, BLUE),
        Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2 - 2 * (BALL_RADIUS + 1), BALL_RADIUS, RED),
        Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2 - 4 * (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
    ]

    # ponham aqui as bolas para testar coisas
    """ balls += [
        #Ball(10 *TABLE_WIDTH // 11 - 10, TABLE_HEIGHT // 2, BALL_RADIUS, WHITE, 0, 0),
        #Ball(TABLE_WIDTH // 2, TABLE_HEIGHT // 2, BALL_RADIUS, WHITE, 50),
        #Ball(TABLE_WIDTH // 2,TABLE_HEIGHT // 2, BALL_RADIUS, WHITE, 5),
        #Ball(TABLE_WIDTH // 4, TABLE_HEIGHT // 2, BALL_RADIUS, RED),
        #Ball(TABLE_WIDTH // 4 + 50, TABLE_HEIGHT // 2, BALL_RADIUS, BLUE),
        #Ball(TABLE_WIDTH // 2, 3 * TABLE_HEIGHT // 4, BALL_RADIUS, LIGHT_BLACK, 0, 5) #para testar a bola preta entrar
        # Ball(TABLE_WIDTH // 2, TABLE_HEIGHT // 4, BALL_RADIUS, BLUE),
        # Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2 + 2 * (BALL_RADIUS + 1), BALL_RADIUS, RED, 50),
    ] """
    
    balls_in_hole = []
    
    pygame.display.flip()
    
    running = True
    
    flag = 0
    
    players = [Player(), Player()]
    player = 0
    prev = 1
    
    blackin = 0

    first = 1

    fadein_snooker(screen, holes, balls, walls, TABLE_WIDTH, TABLE_HEIGHT)
    
    while running:
        pygame.time.delay(10)
        screen.fill(DARK_GREEN)
        
        for hole in holes:
            hole.Render()
    
        for b in balls:
            b.Render()
            b.Move()
    
        for b in balls_in_hole:
            b.Render()
            b.Move()
    
        for wall in walls:
            wall.Render()
        draw(screen,players,player)
    
        pygame.display.flip()
    
        balls_to_remove = []

        if first:
            first = 0
            #print("player: ",player + 1,"|\tcolor (1 -> blue, 0 -> red): ",  players[player].color,"|\tnumber of balls in holes: ", players[player].balls)
            if not bvb:
                temp = stick.move(balls, holes, walls, players, player)
                if temp == "quit":
                    quit_game = True
                    return quit_game
                elif temp == "restart":
                    return 0
            else:
                BOT.move(balls, holes, walls, players, player)
            
            continue

    
        for i in range(0, len(balls)):
            for j in range(i+1, len(balls)):
                balls[i].CheckCollision(balls[j])
    
            for wall in walls:
                wall.CheckCollision(balls[i])
    
            for hole in holes:
                if hole.CheckCollision(balls[i]):
                    balls_to_remove.append(i)
    
        balls_to_remove.sort(reverse=True)
    
        for i in balls_to_remove:
            if players[player].color != -1:
                if balls[i].color == BLUE and players[player].color == 1:
                    players[player].balls += 1
                elif balls[i].color == RED and players[player].color == 0:
                    players[player].balls += 1
                elif balls[i].color == BLUE and players[player].color == 0:
                    players[(player + 1) % 2].balls += 1
                    if prev:
                        if players[player].balls < players[(player + 1) % 2].balls:
                            aux = players[player]
                            players[player] = players[(player + 1) % 2]
                            players[(player + 1) % 2] = aux
                elif balls[i].color == RED and players[player].color == 1:
                    players[(player + 1) % 2].balls += 1
                    if prev:
                        if players[player].balls < players[(player + 1) % 2].balls:
                            aux = players[player]
                            players[player] = players[(player + 1) % 2]
                            players[(player + 1) % 2] = aux
            else: #atribuir cores
                prev = 1
                if balls[i].color == BLUE:
                    players[player].balls += 1
                    players[player].color = 1
                    players[(player + 1) % 2].color = 0
                elif balls[i].color == RED:
                    players[player].balls += 1
                    players[player].color = 0
                    players[(player + 1) % 2].color = 1 

            if balls[i].color == LIGHT_BLACK:
                blackin = 1
    
            flag = 1
            ball = balls.pop(i)
    
            balls_in_hole.append(ball)
        
        balls_to_remove = []
    
        for i in range(0, len(balls_in_hole)):
            ball.radius -= 1
            if ball.radius < 0:
                flag = 0
                balls_to_remove.append(i)
    
        balls_to_remove.sort(reverse=True)
        for i in balls_to_remove:
            balls_in_hole.pop(i)
    
        if (stoped(balls) and not flag): #time for a move!
            prev = 0
    
            #if in the first move a player puts all the balls from his color and the black one (pretty much impossible) he will lose :/
    
            if blackin and (players[player].balls < 7): #black gone before its time..
                running = win(screen,player,players, "o")
                #print("Player ", (player + 1) % 2 + 1, "Wins!")
                if running == False:
                    quit_game = True
                    return quit_game
                else:
                    pass
                break
    
            if blackin and (players[player].balls == 7):
                if balls is None or balls[0].color != WHITE: #meteu a preta e a branca...
                    running = win(screen, player,players, "o")
                    #print("Player ", (player + 1) % 2 + 1, "Wins!")
                    if running == False:
                        quit_game = True
                        return quit_game
                    else:
                        pass
                    break
                else: #meteu a preta e ganhou!
                    running = win(screen, player, players, "t") 
                    #print("Player ", player + 1, "Wins!")
                    if running == False:
                        quit_game = True
                        return quit_game
                    else:
                        pass
                    break 
            if player == 0 or bvb:
                temp = bolaBranca(balls, holes, walls, players, player, 1)
            else:
                temp = bolaBranca(balls, holes, walls, players, player)
            if temp == "quit":
                quit_game = True
                return quit_game
            elif temp == "restart":
                return 0
            elif temp: #remove a ball from current player
                removeBall(players, player, balls) 
                
            idk = gotIn(players, player) 
            if not idk or temp: #no ball got in (changes players)
                player += 1
                if player == 2:
                    player = 0
            #print(player + 1) #currently this player is moving
            #print("player: ",player + 1,"|\tcolor (1 -> blue, 0 -> red): ",  players[player].color,"|\tnumber of balls in holes: ", players[player].balls)
            


            if player == 0 and not bvb:
                temp = stick.move(balls, holes, walls, players, player)
                if temp == "quit":
                    quit_game = True
                    return quit_game
                elif temp == "restart":
                    return 0
            else: #BOT
                BOT.move(balls, holes, walls, players, player)

            
            
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (pos[0] > (SCREEN_WIDTH//30)-5) and (pos[0] < (SCREEN_WIDTH//19)+5) and (pos[1] > (SCREEN_HEIGHT-(SCREEN_HEIGHT//12))) and (pos[1] < (SCREEN_HEIGHT - (SCREEN_HEIGHT//55))): #se clicarem na pausa
                    option = pause(screen)
                    if option == 1: #return
                        pygame.time.delay(100)
                    elif option == 2: #restart
                        return 0
                        quit_game = Snooker() # Dá bug ao tentar sair do jogo depois de recomeçar
                        if quit_game == True:
                            return quit_game
                    elif option == 3: #quit
                        quit_game = True
                        return quit_game
                elif (pos[0] > (9.5*SCREEN_WIDTH//10) - SCREEN_WIDTH//70) and (pos[0] < (9.5*SCREEN_WIDTH//10) + SCREEN_WIDTH // 60) and (pos[1] > (SCREEN_HEIGHT-(SCREEN_HEIGHT//11))) and (pos[1] < (SCREEN_HEIGHT - (SCREEN_HEIGHT//55))): #se clicarem no ?
                    about(screen)
                    pygame.time.delay(100)
                    screen.fill(DARK_GREEN)  
                    for hole in holes:
                        hole.Render()

                    for b in balls:
                        b.Render()

                    for wall in walls:
                        wall.Render()
                    drawMove(screen,players,player) 

                    pygame.display.flip()
                    break
