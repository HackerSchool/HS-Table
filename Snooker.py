import pygame
from tic_tac_toe.Color import *

(width, height) = (1080, 720)

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
                ball.vel_y *= -1

        # aligned horizontally
        if ball.y >= self.y and ball.y <= self.y + self.h:
            if ball.x > self.x:
                dist = ball.x - self.x - self.w
            else:
                dist = self.x - ball.x

            if dist < ball.radius:
                ball.vel_x *= -1
        
class Ball():
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.vel_x = 1
        self.vel_y = -1.5
        self.radius = radius
        self.color = color
    
    def Render(self):
        """ Renders the ball """

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def Move(self):
        """ Moves the ball """

        self.x += self.vel_x
        self.y += self.vel_y


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Project Kobe')

walls = [Border(0, 0, width, 10, BLACK), Border(0, 0, 10, height, BLACK), Border(width - 10, 0, 10, height, BLACK), Border(0, height -10, width, 10, BLACK)]
b = Ball(500, 500, 100, WHITE)

pygame.display.flip()

running = True

while running:
    pygame.time.delay(10)
    screen.fill(DARK_GREEN)

    b.Move()

    for wall in walls:
        wall.CheckCollision(b)
        wall.Render()

    b.Render()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
