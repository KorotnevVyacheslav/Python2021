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
        self.y = randint(30,300)

        self.vx = randint(-100,100)
        self.vy = randint(-10,10)/2

        self.r = randint(10,20)
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
        self.y = randint(30,300)

        self.vx = randint(-10,10)
        self.vy = randint(-10,10) / 4

        self.r = randint(10,20)
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



class Defender:
    ''' Class of defenders '''

    def __init__(self, x0 , y0):
        ''' Initialization
        x,y - position
        vx,vy - velocity
        r - radius
        coulour - colour of ball
        points - cost of ball
        '''

        self.x = 600
        self.y = 900

        self.vx = 100 * (x0 - self.x) / math.sqrt((x0 - self.x)**2 + (y0 - self.y)**2)
        self.vy = 100 * (y0 - self.y) / math.sqrt((x0 - self.x)**2 + (y0 - self.y)**2)

        self.r = 10
        self.colour = WHITE

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




def checking(pool, pool2):
    ''' Check ticking the ball
    pool - pool of targets
    pool2 - pool of defenders
    '''
    k = True
    sum = 0
    for defender in pool2:
        for ball in pool:
            if k:
                x = defender.x
                y = defender.y
                if ball.x - ball.r <= x and ball.x + ball.r >= x and ball.y - ball.r <= y and ball.y + ball.r >= y:
                    sum += ball.points
                    k = False
                    pool.remove(ball)
                    pool2.remove(defender)
        k = True
    for defender in pool2:
        y = defender.y
        if y < 20: pool2.remove(defender)
    return sum


def checking2(pool):
    ''' Check ticking the ball
    x,y - mouse position
    '''
    k = False
    for ball in pool:
        if ball.y + ball.r >= 900:
            k = True
            #pool.remove(ball)
    return k

def updating_pool(n1 , n2):
    pool = [Ball()] * (n1 + n2)
    for i in range(n1):
        pool[i] = Ball()
    for i in range(n1, n2 + n1, 1):
        pool[i] = Ball_updated()
    return pool

pool = updating_pool(NUMBER_OF_BALLS , NUMBER_OF_BALLS_UPDATED)

pool2 = []


pygame.display.update()
clock = pygame.time.Clock()
finished = False
TIME = 0

rounds = 1
p = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pool2.append(Defender(event.pos[0] , event.pos[1]))

    for ball in pool:
        ball.draw(screen)
        ball.move( deltat )
        ball.collision(0 , 1200 , 0 , 900)

    for ball in pool2:
        ball.draw(screen)
        ball.move( deltat )
        ball.collision(0 , 1200 , 0 , 900)

    pygame.display.update()
    screen.fill(BLACK)
    rect(screen, WHITE ,( 0, 900, 1200 , 100))

    SUM += checking(pool, pool2)

    text_points = font.render(str(SUM), True, (0, 100, 0))
    screen.blit(text_points,(100,920))

    text_time = font.render(str(TIME), True, (0, 100, 0))
    screen.blit(text_time,(300,920))

    TIME+=1/FPS
    TIME = float('{:.2f}'.format(TIME))
    SUM -=1/FPS*1000
    SUM = float('{:.0f}'.format(SUM))

    if checking2(pool):
        text = font.render("GAME OVER! CONGRATULATIONS!", True, (0, 100, 0))
        screen.blit(text,(200,500))
        f = open('winners2.txt','a')
        f.write(NAME + " " + str(SUM) + '\n')
        f.close()
        finished = True

    if len(pool) == 0:
        pool = [Ball()] * (NUMBER_OF_BALLS_UPDATED + NUMBER_OF_BALLS)

        for i in range(NUMBER_OF_BALLS):
            pool[i] = Ball()
            for j in range(rounds):
                pool[i].vy *= 1.5
                if abs(pool[i].vy) > 50: pool[i].vy = 50
            rounds +=  1

        for i in range(NUMBER_OF_BALLS, NUMBER_OF_BALLS_UPDATED + NUMBER_OF_BALLS, 1):
            pool[i] = Ball_updated()

pygame.quit()
