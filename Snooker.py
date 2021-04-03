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

        self.vel_x -= 0.001*self.vel_x #atrito
        self.vel_y -= 0.001*self.vel_y #atrito

        if sqrt(self.vel_x ** 2 + self.vel_y ** 2) < 0.1: 
            self.vel_x = 0
            self.vel_y = 0


    def CheckCollision(self, ball):
        """ Checks if a ball has collided with self """

        # vector that links the balls
        dist_x = ball.x - self.x
        dist_y = ball.y - self.y

        # see if collided
        dist = sqrt(dist_x ** 2 + dist_y ** 2)

        if dist <= self.radius + ball.radius:

            # calculate modulus of velocitys
            vel_self = sqrt(self.vel_x ** 2 + self.vel_y ** 2)
            vel_ball = sqrt(ball.vel_x ** 2 + ball.vel_y ** 2)

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
            return True
        
        return False

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snooker')

walls = [Border(0, 0, width, 10, BLACK), Border(0, 0, 10, height, BLACK), Border(width - 10, 0, 10, height, BLACK), Border(0, height -10, width, 10, BLACK)]
holes = [Hole(0, 0, 100, BLACK)]
balls = []

for i in range(0, int(input("Numero de bolas: "))):
    balls.append(Ball(randint(50, width-50), randint(50, height-50), 50, (randint(0,255), randint(0,255), randint(0,255))))

    balls[i].vel_x = randint(-10, 10)
    balls[i].vel_y = randint(-10, 10)

pygame.display.flip()

running = True

while running:
    pygame.time.delay(10)
    screen.fill(DARK_GREEN)
    
    for hole in holes:
        hole.Render()

    for b in balls:
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

    for i in balls_to_remove:
        balls.pop(i)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
