import pygame
import math
from pygame.draw import *
from random import randint, choice
pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 1000))
font = pygame.font.Font(None, 72)

deltat = 0.1

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE=(255,255,255)
COLOURS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

NUMBER_OF_BALLS = 10
NUMBER_OF_BALLS_UPDATED = 10
SUM = 0
NAME = "Vyacheslav"

if input("Is your name Vyacheslav? Y/N") == "N": NAME=input("enter your name: ")


class Ball:
    ''' Class of balls '''

    def __init__(self):
        ''' Initialization
        x,y - position
        vx,vy - velocity
        r - radius
        coulour - colour of ball
        points - cost of ball
        '''

        self.x = randint(100,1100)
        self.y = randint(100,800)

        self.vx = randint(-100,100)
        self.vy = randint(-100,100)

        self.r = randint(30,50)
        self.colour = choice(COLOURS)
        self.points = int( 100000 / self.r )

    def draw(self, surface):
        ''' Draw ball
        x,y - position
        r - radius
        coulour - colour of ball
        '''

        circle(surface, self.colour, (self.x, self.y) , self.r)

    def move(self, dt):
        ''' Move ball
        x,y - position
        vx,vy - velocity
        dt - changing of time
        '''

        self.x = self.vx * dt + self.x
        self.y = self.vy * dt + self.y

    def collision(self, width_left, width_right, height_left, height_right):
        ''' Check collision with walls
        width_left, width_right - coordinates of vertical walls
        height_left, height_right - coordinates of gorizontal(sorry) walls
        '''

        if self.x - self.r<= width_left: self.vx *= -1
        if self.x + self.r >= width_right: self.vx *= -1
        if self.y - self.r <= height_left: self.vy *= -1
        if self.y + self.r >= height_right: self.vy *= -1

class Ball_updated:
    ''' Class of updated balls '''

    def __init__(self):
        ''' Initialization
        x,y - position
        vx,vy - velocity
        r - radius
        t - parameter for geometry
        coulour - colour of ball
        points - cost of ball
        '''
        self.t = 0
        self.x = randint(100,1100)
        self.y = randint(100,800)

        self.vx = randint(-10,10)
        self.vy = randint(-10,10)

        self.r = randint(30,50)
        self.colour = choice(COLOURS)
        self.points = int( 100000 / self.r )

    def draw(self, surface):
        ''' Draw ball
        x,y - position
        r - radius
        coulour - colour of ball
        '''

        rect(surface, self.colour, (self.x - self.r, self.y - self.r, 2 * self.r , 2 * self.r))

    def move(self, dt):
        ''' Move ball
        x,y - position
        vx,vy - velocity
        dt - changing of time
        '''

        self.t += dt
        self.x += self.vx * abs(math.sin(self.t))
        self.y += self.vy * abs(math.sin(self.t))

    def collision(self, width_left, width_right, height_left, height_right):
        ''' Check collision with walls
        width_left, width_right - coordinates of vertical walls
        height_left, height_right - coordinates of gorizontal(sorry) walls
        '''

        if self.x - self.r<= width_left: self.vx *= -1
        if self.x + self.r >= width_right: self.vx *= -1
        if self.y - self.r <= height_left: self.vy *= -1
        if self.y + self.r >= height_right: self.vy *= -1


def checking(x,y, pool):
    ''' Check ticking the ball
    x,y - mouse position
    '''

    sum=0
    k=False
    for ball in pool:
        if ball.x - ball.r <= x and ball.x + ball.r >= x and ball.y - ball.r <= y and ball.y + ball.r >= y:
             sum += ball.points
             k=True
             pool.remove(ball)

    if not k: sum = -250
    if k:
        for ball in pool:
            ball.vx *= 1.1
            ball.vy *= 1.1
    return sum




pool = [Ball()] * (NUMBER_OF_BALLS_UPDATED + NUMBER_OF_BALLS)

for i in range(NUMBER_OF_BALLS):
    pool[i] = Ball()

for i in range(NUMBER_OF_BALLS, NUMBER_OF_BALLS_UPDATED + NUMBER_OF_BALLS, 1):
    pool[i] = Ball_updated()





pygame.display.update()
clock = pygame.time.Clock()
finished = False
TIME=0


p=True
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            SUM += checking(event.pos[0], event.pos[1], pool)
            print(SUM)

    for ball in pool:
        ball.draw(screen)
        ball.move( deltat )
        ball.collision(0 , 1200 , 0 , 900)

    pygame.display.update()
    screen.fill(BLACK)
    rect(screen, WHITE ,( 0, 900, 1200 , 100))
    text_points = font.render(str(SUM), True, (0, 100, 0))
    screen.blit(text_points,(100,920))

    text_time = font.render(str(TIME), True, (0, 100, 0))
    screen.blit(text_time,(300,920))

    TIME+=1/FPS
    TIME = float('{:.2f}'.format(TIME))

    if len(pool) == 0 and p:
        text = font.render("YOU WON! CONGRATULATIONS!", True, (0, 100, 0))
        screen.blit(text,(200,500))
        f = open('winners.txt','a')
        f.write(NAME + " " + str(SUM) + '\n')
        f.close()
        p=False

    if len(pool) == 0:
        text = font.render("YOU WON! CONGRATULATIONS!", True, (0, 100, 0))
        screen.blit(text,(200,500))

pygame.quit()
