import math
from random import choice, randint
import pygame
pygame.init()


FPS = 30

font = pygame.font.Font(None, 72)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE=(255,255,255)
GREY = (0, 20, 20)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

g = 10
k = 0.03

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = 40
        self.y = 450
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.vy += g / 10 - k * self.vy
        self.vx +=  - k * self.vx
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if math.sqrt( (self.x - obj.x)**2 + (self.y - obj.y)**2 ) < self.r + obj.r: return True
        return False

    def collision(self, width_left, width_right, height_left, height_right):
        ''' Check collision with walls
        width_left, width_right - coordinates of vertical walls
        height_left, height_right - coordinates of gorizontal(sorry) walls
        there is no collision with lower wall - the end of the game
        '''

        if self.x - self.r <= width_left:
            self.vx *= -0.95
            self.vy *= 0.95
        if self.x + self.r >= width_right:
            self.vx *= -0.95
            self.vy *= 0.95
        if self.y - self.r <= height_left:
            self.vy *= -0.95
            self.vx *= 0.95
        if self.y + self.r >= height_right:
            self.vy *= -0.95
            self.vx *= 0.95


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1


    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2(-(event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2(-(event.pos[1]-450) , (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

        coor = (40 + self.f2_power * math.cos(self.an), 450 - self.f2_power * math.sin(self.an))
        pygame.draw.line(screen, self.color, (40 , 450) , coor , 10)

    def targetting2(self):
        """Прицеливание. Не зaвисит от положения мыши."""
        coor = (40 + self.f2_power * math.cos(self.an), 450 - self.f2_power * math.sin(self.an))
        pygame.draw.line(screen, self.color, (40 , 450) , coor , 10)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def __init__(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 50)
        self.points = 0
        self.live = 1
        self.color = RED

    def new_target(self):
        x = self.x = randint(600, 780)
        y = self.y = randint(300, 550)
        r = self.r = randint(2, 50)
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.r
        )


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
finished = False
lenght = 0
round = 1

while not finished:
    rounds = font.render(str(round), True, (0, 100, 0))
    screen.fill(WHITE)
    screen.blit(rounds,(30,30))
    for ball in balls:
        ball.draw()
    target.draw()
    for ball in balls:
        ball.draw()

    gun.targetting2()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
            lenght += 1
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for ball in balls:
        ball.collision(0, 800 , 0 , 600 )
        ball.move()

        if ball.hittest(target):
            for i in range(1000):
                screen.fill(WHITE)
                text = font.render("YOU WON! TRY AGAIN!", True, (0, 100, 0))
                screen.blit(text,(100,200))
                text = font.render(str(lenght) + " BALLS", True, (0, 100, 0))
                screen.blit(text,(100,400))
                pygame.display.update()
            target.live = 0
            target.hit()
            target.new_target()
            balls.remove(ball)
            round += 1
            lenght = 0
        if ball.y > 700: balls.remove(ball)
    gun.power_up()
    pygame.display.update()

pygame.quit()
