import pygame
from pygame.draw import *
from random import *
print()
pygame.init()

FPS = 30

IMAGE_WIDTH=1000
IMAGE_HEIGHT=1000
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(200, 0, 0)
SKY_COLOR=(255, 255, 0)
SUN_COLOR=(0, 255, 255)

screen = pygame.display.set_mode((IMAGE_WIDTH,IMAGE_HEIGHT))
screen.fill(WHITE)

surf=pygame.Surface((IMAGE_WIDTH,IMAGE_HEIGHT))
surf.fill(WHITE)

def pictureofbear(x,y,k,screen):
    '''
    risuet medvedya
    x,y - position
    k - coefficient uvelicheniya
    screen - poverhnost' dlya risovaniya
    '''
    circle(screen, WHITE, (x+k*100-k*10, y-k*10),3)
    circle(screen, WHITE, (x+k*100+k*40, y),3)
    circle(screen, WHITE, (x+k*100-k*40, y-k*10), 7)
    ellipse(screen, WHITE, [x, y, k*100, k*200])
    ellipse(screen, WHITE, [x+k*60, y-k*20, k*80, k*40])
    ellipse(screen, WHITE, [x+k*100-k*10, y+k*60, k*60, k*20])
    ellipse(screen, WHITE, [x+k*100-k*60, y+k*200-k*30, k*80, k*60])
    ellipse(screen, WHITE, [x+k*100, y+k*200, k*100, k*40])

    circle(screen, BLACK, (x+k*100-k*10, y-k*10), 3)
    circle(screen, BLACK, (x+k*100+k*40, y), 3)
    circle(screen, BLACK, (x+k*100-k*40, y-k*10), 7,2)
    lines(screen, BLACK, False, [[x+k*100, y+k*10], [x+k*120, y+k*10]], 5)
    ellipse(screen, BLACK, [x, y, k*100, k*200], 2)
    ellipse(screen,BLACK, [x+k*60, y-k*20, k*80, k*40], 2)
    ellipse(screen, BLACK, [x+k*100-k*10, y+k*60, k*60, k*20], 2)
    ellipse(screen, BLACK, [x+k*100-k*60, y+k*200-k*30, k*80, k*60], 2)
    ellipse(screen, BLACK, [x+k*100, y+k*200, k*100, k*40], 2)
    ellipse(screen, BLACK, [x+k*320-k*50, y+k*100-k*20-k*100+k*200-k*20, k*120, k*60])
    ellipse(screen, (randint(0,255), randint(0,255), randint(0,255)), [x+k*320-k*50+k*10, y+k*100-k*20-k*100+k*200-k*20+k*10, k*100, k*40])
    lines(screen, BLACK, False, [[x+k*100, y+k*100], [x+k*120, y+k*100-k*20],[x+k*320, y+k*100-k*20-k*100],[x+k*320, y+k*100-k*20-k*100+k*200]], 5)

def pictureoffish(x,y,k,screen):
    '''
    risuet ribu
    x,y - position
    k - coefficient uvelicheniya
    screen - poverhnost' dlya risovaniya
    '''
    ellipse(screen, WHITE, [x, y+k*50, k*400, k*100])
    ellipse(screen, BLACK, [x, y+k*50, k*400, k*100], 2)
    polygon(screen, BLACK, [(x,y+k*100),(x-k*100,y+k*100-k*100),(x-k*100,y+k*100+k*100),(x,y+k*100)])
    circle(screen, BLACK, (x+k*300, y+k*100), k*20)
    circle(screen, RED, (x+k*300, y+k*100), k*10)

rect(surf, SUN_COLOR, (0, 0, 1000, 300))
rect(surf, BLACK, (0, 300, 1000, 10))
circle(surf, SKY_COLOR, (700, 200), 100)
circle(surf, SUN_COLOR, (700, 200), 80)
rect(surf, SKY_COLOR, (600, 200, 200+5, 10))
rect(surf,SKY_COLOR , (600+100, 200-100, 10, 200))


for i in range(100):
    x=randint(0,1)
    if x==1: xbool=True
    if x==0: xbool=False
    surf=pygame.transform.flip(surf ,xbool,False)
    pictureofbear(randint(0,800),randint(200,800),randint(1,20)/20,surf)
    pictureoffish(randint(200,800),randint(400,800),randint(1,20)/30,surf)
    surf=pygame.transform.flip(surf ,xbool,False)

screen.blit(surf, (0, 0))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
