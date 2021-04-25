import pygame
from assets.Color import *
from assets.Dimensions import *
from math import sqrt, sin, cos, pi, atan, acos
from random import randint

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
                near_x, near_y = self.GetNearestPoint(ball)

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
           

    def erase(self, holes, balls, walls):
        screen.fill(DARK_GREEN)
    
        for hole in holes:
            hole.Render()

        for b in balls:
            b.Render()

        for wall in walls:
            wall.Render()


    def render(self, pos, holes, balls, walls, anglePrev):
        self.angle =  AngleVector(-self.vel_x, self.vel_y) * 180 / pi + 33 


        self.image = pygame.transform.rotate(self.original, self.angle)
        screen.blit(self.image, (pos[0] - self.image.get_width() // 2, pos[1] - self.image.get_height() // 2))
        pygame.display.flip() 
        pygame.time.delay(15)
        self.erase(holes, balls, walls)


        while True:
            for event in pygame.event.get(): #just when taco moves again it gets erased
                pygame.display.flip()
                if not pygame.mouse.get_pressed()[0]:
                    return 0, [], self.angle
                else:
                    return 1, event.pos, self.angle #it moved but button is still pressed..
        

    
    def move(self, balls, holes, walls, first = True):
        a = 0
        pos = []
        anglePrev = 0
        vel_xPrev = []
        vel_yPrev = []
        stickPrev = [0,0]
        while True:  
            while not a: #waits for the first position
                for event in pygame.event.get():                              
                    if pygame.mouse.get_pressed()[0]:
                        pos = event.pos
                        a = 1
                        break 
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        running = False
            a, pos, anglePrev = self.render(pos, balls, holes, walls, anglePrev)
            if not a:
                first = True
                vel_xPrev = []
                vel_yPrev = []
            while not a: 
                for event in pygame.event.get():                               
                    if pygame.mouse.get_pressed()[0]:
                        pos = event.pos
                        a = 1
                        break 
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        running = False        
            self.x = pos[0]
            self.y = pos[1]
            if first:
                self.vel_x = 0
                self.vel_y = 0
                vel_x = 0
                vel_y = 0
                first = False #still doesnt work.. its supposed to not allow huge velocities when you stop pressing and then press again very far away
            else:
                vel_x = (self.x - stickPrev[0]) / 2
                vel_y = (self.y - stickPrev[1]) / 2

            stickPrev = pos
            vel_xPrev.append(vel_x) 
            vel_yPrev.append(vel_y)
            if (len(vel_xPrev) > 10):
                vel_xPrev.pop(0)
                vel_yPrev.pop(0)
            self.vel_x = sum(vel_xPrev) / len(vel_xPrev)
            self.vel_y = sum(vel_yPrev) / len(vel_yPrev)

            if stick.CheckCollision(balls[0]):
                break
                
    
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
            vel_ball = 0

            # calculate incidence angles of balls
            angle_self = AngleVector(self.vel_x, self.vel_y)

            # calculate the angle of collision
            angle_ab = AngleVector(dist_x, dist_y)

            ball.vel_x = vel_self * cos(angle_self - angle_ab) * cos(angle_ab) + vel_ball * sin(- angle_ab) * cos(angle_ab + pi / 2)
            ball.vel_y = vel_self * cos(angle_self - angle_ab) * sin(angle_ab) + vel_ball * sin(- angle_ab) * sin(angle_ab + pi / 2)
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

    def Move(self):
        """ Moves the ball """

        self.x += self.vel_x
        self.y += self.vel_y

        # atrito
        self.ChangeVelMagnitude(self.Velocity*0.997)

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

            # makes balls (and all my problems) go away
            while sqrt((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2) <= self.radius + ball.radius:
                self.Move()
                ball.Move()

class Hole():
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    
    def Render(self):
        """ Renders the hole """

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

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

def stoped(balls):
    for b in balls:
        if b.vel_x != 0 or b.vel_y != 0:
            return 0
    return 1

def bolaBranca(balls):
    a = 0
    b = 1
    if len(balls) == 16:
        return 0
    if balls[0].color != WHITE: #white fell in hole
        while not a: #waits for the first position
            for event in pygame.event.get():                              
                if pygame.mouse.get_pressed()[0]:
                    pos = event.pos
                    balls.insert(0, Ball(pos[0], pos[1], BALL_RADIUS, WHITE)) #maybe mudamos isto para ser balls.append() e depois balls[0] troca com balls[len(balls)] pq deve ser mais eficiente e em principio n faz diferenca
                    a = 1
                    break 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
            
            if a: #choosing final position
                while b:
                    for event in pygame.event.get():                              
                        if pygame.mouse.get_pressed()[0]:
                            pos = event.pos
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
                        else:
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
                                pygame.display.flip()

        balls[0].Render()
        pygame.display.flip()
        return 1
    return 0


def gotIn(balls, players, player, prev):
    flag1, flag2 = 0, 0
    if players[player].prevBalls < players[player].balls: #meteu uma(s) bola(s) sua
        players[player].prevBalls = players[player].balls 
        flag1 = 1
    if players[(player + 1) % 2].prevBalls < players[(player + 1) % 2].balls: #meteu uma(s) bola(s) do seu adversario
        players[(player + 1) % 2].prevBalls = players[(player + 1) % 2].balls
        flag2 = 1

    if not flag1 and not flag2:
        if len(balls) < prev: #quando ainda n têm equipa ainda n conseguem atribuir bolas msm que estas entrem
            prev = len(balls)
            return 1, prev
        else:
            return 0, prev
    elif flag1:
        prev = len(balls)
        return 1, prev
    else:
        prev = len(balls)
        return 0, prev
    

def defColor(players, player, balls):
    countB = 0
    countR = 0
    for b in balls:
        if b.color == BLUE:
            countB += 1
        if b.color == RED:
            countR += 1
    
    #BLUE ------------> 1!
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
        players[(player + 1) % 2].prevBalls = 7 - countR

def aux(players, player, balls): #bug ainda pode correr mal se estiver a linha toda quase toda ocupada..
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
                print("here")
                while True:
                    print("1")
                    balls[len(balls) - 1].y += 10 
                    dist_y = b.y - balls[len(balls) - 1].y

                    # see if collided WHYYYYY
                    dist = sqrt(dist_x ** 2 + dist_y ** 2)

                    if dist > 2 * b.radius:
                        break
                print("hereee")
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
            print(balls[len(balls) - 1].y)
            aux(players, player, balls)
            print(balls[len(balls) - 1].y)
        elif players[player].color == 0:
            balls.append(Ball(TABLE_WIDTH // 5, TABLE_HEIGHT // 4, BALL_RADIUS, RED))
            aux(players, player, balls)
        else: #já havia bolas dentro de buracos mas ainda n havia cores definidas
            balls.append(Ball(TABLE_WIDTH // 5, TABLE_HEIGHT // 4, BALL_RADIUS, BLUE))
            aux(players, player, balls)
            players[player].color = 1
            players[(player + 1) % 2].color = 0
        players[player].balls -= 1
        balls[len(balls) - 1].Render()
        pygame.display.flip()
    return

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
    Ball(TABLE_WIDTH // 5, TABLE_HEIGHT // 2, BALL_RADIUS, WHITE, 15),
    Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2, BALL_RADIUS, BLUE),
    Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2 + 2 * (BALL_RADIUS + 1), BALL_RADIUS, RED),
    #Ball(TABLE_WIDTH // 5, TABLE_HEIGHT // 4, BALL_RADIUS, BLUE),
    Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2 + 4 * (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
    #Ball(TABLE_WIDTH // 5, TABLE_HEIGHT // 4 + 65, BALL_RADIUS, RED),
    Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2 - 2 * (BALL_RADIUS + 1), BALL_RADIUS, RED),
    Ball(10 *TABLE_WIDTH // 11, TABLE_HEIGHT // 2 - 4 * (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
    Ball(10 *TABLE_WIDTH // 11 - 2 * BALL_RADIUS, TABLE_HEIGHT // 2 + (BALL_RADIUS + 1), BALL_RADIUS, RED),
    Ball(10 *TABLE_WIDTH // 11 - 2 * BALL_RADIUS, TABLE_HEIGHT // 2 + 3 * (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
    Ball(10 *TABLE_WIDTH // 11 - 2 * BALL_RADIUS, TABLE_HEIGHT // 2 - (BALL_RADIUS + 1), BALL_RADIUS, RED),
    Ball(10 *TABLE_WIDTH // 11 - 2 * BALL_RADIUS, TABLE_HEIGHT // 2 - 3 * (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
    Ball(10 *TABLE_WIDTH // 11 - 4 * BALL_RADIUS, TABLE_HEIGHT // 2, BALL_RADIUS, LIGHT_BLACK),
    Ball(10 *TABLE_WIDTH // 11 - 4 * BALL_RADIUS, TABLE_HEIGHT // 2 + 2 * (BALL_RADIUS + 1), BALL_RADIUS, RED),
    Ball(10 *TABLE_WIDTH // 11 - 4 * BALL_RADIUS, TABLE_HEIGHT // 2 - 2 * (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
    Ball(10 *TABLE_WIDTH // 11 - 6 * BALL_RADIUS, TABLE_HEIGHT // 2 + (BALL_RADIUS + 1), BALL_RADIUS, RED),
    Ball(10 *TABLE_WIDTH // 11 - 6 * BALL_RADIUS, TABLE_HEIGHT // 2 - (BALL_RADIUS + 1), BALL_RADIUS, BLUE),
    Ball(10 *TABLE_WIDTH // 11 - 8 * BALL_RADIUS, TABLE_HEIGHT // 2, BALL_RADIUS, RED),
]

balls_in_hole = []

pygame.display.flip()

running = True

stick = taco(0,0,10)
flag = 0

players = [Player(), Player()]
player = 0
prev = 16

blackin = 0

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

    pygame.display.flip()

    balls_to_remove = []

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
            elif balls[i].color == RED and players[player].color == 1:
                players[(player + 1) % 2].balls += 1
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

        #if in the first move a player puts all the balls from his color and the black one (pretty much impossible) he will lose :/

        if blackin and (players[player].balls < 7): #black gone before its time..
            print("Player ", (player + 1) % 2 + 1, "Wins!")
            break

        if blackin and (players[player].balls == 7):
            if balls[0].color != White: #meteu a preta e a branca...
                print("Player ", (player + 1) % 2 + 1, "Wins!")
                break
            else: #meteu a preta e ganhou!
                print("Player ", player + 1, "Wins!")
                break 

        if bolaBranca(balls): #remove a ball from current player
            removeBall(players, player, balls)           
            
        idk, prev = gotIn(balls, players, player, prev) 
        if idk and (players[0].color == -1): #determine each players color     
            defColor(players, player, balls)
        if not idk: #no ball got in (changes players)
            player += 1
            if player == 2:
                player = 0
        #print(player + 1) #currently this player is moving
        print("player: ",player + 1,"|\tcolor (1 -> blue, 0 -> red): ",  players[player].color,"|\tnumber of balls in holes: ", players[player].balls)
        stick.move(balls, holes, walls)
        
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
