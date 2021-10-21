import pygame
import math
import json
from pygame.draw import *
from random import randint, choice
pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 1000))
font = pygame.font.Font(None, 72)

deltat = 0.1 #normalization of time

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE=(255,255,255)
COLOURS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

NUMBER_OF_TARGETS = 10
NUMBER_OF_UPDATED_TARGETS = 10
SUM = 0
NAME = "Vyacheslav"

if input("Is your name Vyacheslav? Y/N  ") == "N": NAME = input("Enter your name: ") #requesting name



class Target:
    ''' Class of balls that is need to be defended '''

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
        ''' Drawing ball
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
        there is no collision with lower wall - the end of the game
        '''

        if self.x - self.r<= width_left: self.vx *= -1
        if self.x + self.r >= width_right: self.vx *= -1
        if self.y - self.r <= height_left: self.vy *= -1


class Target_updated:
    ''' Class of updated targets that is need to be defended '''

    def __init__(self):
        ''' Initialization
        x,y - position
        vx,vy - velocity
        r - lenght of the square edge
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
        coulour - colour of square
        '''

        rect(surface, self.colour, (self.x - self.r, self.y - self.r, 2 * self.r , 2 * self.r))

    def move(self, dt):
        ''' Move square
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
        there is no collision with lower wall - the end of the game
        '''

        if self.x - self.r<= width_left: self.vx *= -1
        if self.x + self.r >= width_right: self.vx *= -1
        if self.y - self.r <= height_left: self.vy *= -1



class Defender:
    ''' Class of defenders '''

    def __init__(self, x0 , y0):
        ''' Initialization
        x0, y0 - coordinates of mouse to determine the direction
        x,y - position
        vx,vy - velocity
        r - radius
        coulour - colour of ball
        '''

        self.x = 600
        self.y = 900

        self.vx = 100 * (x0 - self.x) / math.sqrt((x0 - self.x)**2 + (y0 - self.y)**2)
        self.vy = 100 * (y0 - self.y) / math.sqrt((x0 - self.x)**2 + (y0 - self.y)**2)

        self.r = 10
        self.colour = WHITE

    def draw(self, surface):
        ''' Draw defender
        surface - surface the defender draws on
        x,y - position
        r - radius
        coulour - colour of ball
        '''

        circle(surface, self.colour, (self.x, self.y) , self.r)

    def move(self, dt):
        ''' Move defender
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
        there is no collision with lower wall - for fun
        '''

        if self.x - self.r<= width_left: self.vx *= -1
        if self.x + self.r >= width_right: self.vx *= -1
        if self.y - self.r <= height_left: self.vy *= -1




def checking(pool, pool2):
    ''' Check ticking the ball with defender
    pool - pool of targets
    pool2 - pool of defenders
    '''
    k = True
    sum = 0
    for defender in pool2:
        for target in pool:
            if k:
                x = defender.x
                y = defender.y
                if target.x - target.r <= x and target.x + target.r >= x and target.y - target.r <= y and target.y + target.r >= y:
                    sum += target.points
                    k = False
                    pool.remove(target)
                    pool2.remove(defender)
        k = True
    for defender in pool2:
        y = defender.y
        if y < 20: pool2.remove(defender)
    return sum


def checking2(pool):
    ''' Check ticking the ball with lower edge
    pool - pool of targets
    '''
    k = False
    for target in pool:
        if target.y + target.r >= 900:
            k = True
    return k

def updating_pool(n1 , n2):
    ''' refilling the pool with targets
    n1 - number of simple targets
    n2 - number of updated targets
    '''
    pool = [Target()] * (n1 + n2)
    for i in range(n1):
        pool[i] = Target()
    for i in range(n1, n2 + n1, 1):
        pool[i] = Target_updated()
    return pool

pool = updating_pool(NUMBER_OF_TARGETS , NUMBER_OF_UPDATED_TARGETS)
pool2 = []

pygame.display.update()
clock = pygame.time.Clock()
finished = False
TIME = 0

rounds = 1
p = False
m = False
while not finished:
    clock.tick(FPS)
    pygame.display.update()
    screen.fill(BLACK)
    rect(screen, WHITE ,( 0, 900, 1200 , 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pool2.append(Defender(event.pos[0] , event.pos[1]))

    #writing summary of points
    text_points = font.render(str(SUM), True, (0, 100, 0))
    screen.blit(text_points,(100,920))

    #writing time
    text_time = font.render(str(TIME), True, (0, 100, 0))
    screen.blit(text_time,(500,920))

    #m = false - game is not over
    if not m:
        for ball in pool:
            #moving and drawing simple targets
            ball.draw(screen)
            ball.move( deltat )
            ball.collision(0 , 1200 , 0 , 900)

        for ball in pool2:
            #moving and drawing updated targets
            ball.draw(screen)
            ball.move( deltat )
            ball.collision(0 , 1200 , 0 , 900)


        SUM += checking(pool, pool2)
        #updating time
        TIME += 1 / FPS
        TIME = float('{:.2f}'.format(TIME))
        #updating points
        SUM -= 1 / FPS * 1000
        SUM = float('{:.0f}'.format(SUM))

        if checking2(pool):
            #adding player results to txt
            f = open('winners2.txt','a')
            f.write(NAME + " " + str(SUM) + '\n')
            f.close()

            #loading all results
            with open("winners_data.json", "r") as write_file:
                loaded = json.load(write_file)
            #adding player results
            loaded.append( {'name': NAME, 'points': SUM } )

            #sorting all results
            for i in range(len(loaded) - 1 ):
                k = i
                for j in ( i + 1 , len(loaded) - 1):
                    dict1 = loaded[k]
                    dict2 = loaded[j]
                    if dict1.get('points', 0) < dict2.get('points', 0): k = j
                c = loaded[k]
                loaded[k] = loaded[i]
                loaded[i] = c
            #writing results to file
            with open("winners_data.json", "w") as write_file:
                json.dump(loaded,  write_file)

            m = True

        if len(pool) == 0:
            #updating pool
            NUMBER_OF_UPDATED_TARGETS *= 2
            pool = [Target()] * (NUMBER_OF_UPDATED_TARGETS + NUMBER_OF_TARGETS)

            for i in range(NUMBER_OF_TARGETS):
                pool[i] = Target()
                #for j in range(rounds):
                    #pool[i].vx *= 1.5
                    #if abs(pool[i].vy) > 50: pool[i].vy = 50
                rounds +=  1


            for i in range(NUMBER_OF_TARGETS, NUMBER_OF_UPDATED_TARGETS + NUMBER_OF_TARGETS, 1):
                pool[i] = Target_updated()
    if m:
            #writing results of 5 best players on the screen
            text = font.render("YOU WON! CONGRATULATIONS!", True, (0, 100, 0))
            screen.blit(text,(200,800))
            with open("winners_data.json", "r") as write_file:
                loaded = json.load(write_file)
            for i in range(min(len(loaded) , 5)):
                text = font.render( loaded[i].get('name', 0) + "   " + str(loaded[i].get('points', 0)), True, (0, 100, 0))
                screen.blit(text,(200 , 100 + i * 100))


pygame.quit()
