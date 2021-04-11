import pygame
from tic_tac_toe.Color import *
from math import sqrt, sin, cos, pi, atan, acos
from random import randint

(width, height) = (1080, 720)

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

        # aligned vertically
        if ball.x >= self.x and ball.x <= self.x + self.w:
            if ball.y > self.y:
                dist = ball.y - self.y - self.h
            else:
                dist = self.y - ball.y

            if dist < ball.radius:
                ball.vel_y *= -0.95 #loss of energy

        # aligned horizontally
        if ball.y >= self.y and ball.y <= self.y + self.h:
            if ball.x > self.x:
                dist = ball.x - self.x - self.w
            else:
                dist = self.x - ball.x

            if dist < ball.radius:
                ball.vel_x *= -0.95 #loss of energy

class taco():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.radius = radius 
        self.original = pygame.image.load("taco.png").convert_alpha()
        self.angle = AngleVector(self.vel_x, self.vel_y)
        self.image = pygame.transform.rotate(self.original, self.angle)
           

    def render(self, pos, holes, balls, walls):
        self.angle =  AngleVector(-self.vel_x, self.vel_y) * 180 / pi + 33
        self.image = pygame.transform.rotate(self.original, self.angle)
        #print(self.angle)
        screen.blit(self.image, (pos[0] - 300, pos[1]- 300))
        pygame.display.flip()
        pygame.time.delay(30) 
        screen.fill(DARK_GREEN)
    
        for hole in holes:
            hole.Render()

        for b in balls:
            b.Render()

        for wall in walls:
            wall.Render()

         
        while True:
            for event in pygame.event.get(): #just when taco moves again it gets erased
                pygame.display.flip()
                if not pygame.mouse.get_pressed()[0]:
                    return 0, []
                else:
                    return 1, event.pos #it moved but button is still pressed..

    
    def move(self, balls, holes, walls, first = True):
        a = 0
        pos = []
        while True:  
            while not a: #waits for the first position
                for event in pygame.event.get():                              
                    if pygame.mouse.get_pressed()[0]:
                        pos = event.pos
                        a = 1
                        break 
            a, pos = self.render(pos, balls, holes, walls)
            while not a: #if it got off the function without still pressing the button, it waits for a new press
                for event in pygame.event.get():                               
                    if pygame.mouse.get_pressed()[0]:
                        pos = event.pos
                        a = 1
                        break         
            self.x = pos[0]
            self.y = pos[1]
            if first:
                self.vel_x = 0
                self.vel_y = 0
                first = False #still doesnt work.. its supposed to not allow huge velocities when you stop pressing and then press again very far away
            else:
                self.vel_x = (self.x - stickPrev[0]) / 8 #we can play with this 10
                self.vel_y = (self.y - stickPrev[1]) / 8

            stickPrev = pos

            if stick.CheckCollision(balls[0]):
                break
                
    
    @property
    def Velocity(self):
        return MagnitudeVector(self.vel_x, self.vel_y)

    def CheckCollision(self, ball): 
        """ Checks if a ball has collided with self """
        
        dist_x = ball.x - self.x
        dist_y = ball.y - self.y

        # see if collided
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
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
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
        self.ChangeVelMagnitude(self.Velocity*0.999)

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


def stoped(balls):
    for b in balls:
        if b.vel_x != 0 and b.vel_y != 0:
            return 0
    return 1


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snooker')

image = pygame.image.load("taco.png").convert()
""" screen.blit(image, (0,0))
pygame.display.flip()
pygame.time.delay(1500) """

walls = [Border(0, 0, width, 10, BLACK), Border(0, 0, 10, height, BLACK), Border(width - 10, 0, 10, height, BLACK), Border(0, height -10, width, 10, BLACK)]
holes = [Hole(0, 0, 100, BLACK)]
balls = []
balls_in_hole = []


balls.append(Ball(100, 200, 50, WHITE))
balls[0].vel_x = 0
balls[0].vel_y = 0
# for i in range(0, int(input("Numero de bolas: "))):
for i in range(1, 9):
    balls.append(Ball(100 + 110 * i, 200, 50, (randint(0,255), randint(0,255), randint(0,255))))

    balls[i].vel_x = 0#randint(-10, 10)
    balls[i].vel_y = 0#randint(-10, 10)


# balls = [Ball(500, 500, 50, (255, 255, 255))]
# balls[0].vel_x = 100
# balls[0].vel_y = 0       randint(50, height-50)

pygame.display.flip()

running = True

stick = taco(0,0,10)

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
        ball = balls.pop(i)

        balls_in_hole.append(ball)
    
    balls_to_remove = []

    for i in range(0, len(balls_in_hole)):
        ball.radius -= 1
        if ball.radius <= 0:
            balls_to_remove.append(i)

    balls_to_remove.sort(reverse=True)
    for i in balls_to_remove:
        balls_in_hole.pop(i)

    if (stoped(balls)): #time for a move!
        stick.move(balls, holes, walls)
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
