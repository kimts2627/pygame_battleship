import pygame as pg
import sys
from os import path
from globals import *
import random

pg.init()
clock = pg.time.Clock()
my_font = pg.font.SysFont('latobold', 40, True, False)
message_title = my_font.render(TITLE, True, WHITE)
title_rect = message_title.get_rect()
title_rect.centerx = round(WIDTH / 2)
title_rect.y = 510
screen = pg.display.set_mode((WIDTH, HEIGHT))
background = pg.image.load('images/background.jpeg')
pg.display.set_caption('BATTLE-SHIP')

back_group = pg.sprite.Group()
red_ships = pg.sprite.Group()
blue_ships = pg.sprite.Group()
missile_group = pg.sprite.Group()
effect_group = pg.sprite.Group()

class Missile(pg.sprite.Sprite):
    def __init__(self, col, row, team, target):
        pg.sprite.Sprite.__init__(self)
        self.team = team
        self.target = target
        self.image = pg.image.load(path.join('images', 'missile.png')).convert_alpha()
        if team == 'red': self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = col
        self.rect.y = row
        self.speed = 10

    def update(self):
        print('update!')
        x = self.target.x
        y = self.target.y
        if self.rect.x != x:
            print(f'x는 {self.rect.x}')
            if self.rect.x > x:
                self.rect.x = self.rect.x - self.speed
            elif self.rect.x < x:
                self.rect.x = self.rect.x + self.speed
        if self.rect.y != y:
            print(f'y는 {self.rect.y}')
            if self.rect.y > x:
                self.rect.y = self.rect.y - self.speed
            elif self.rect.y < x:
                self.rect.y = self.rect.y + self.speed
        if self.rect.y == y and self.rect.x == x:
            print('hit!!!!!!!!!')
            explode = Explode(x, y)
            effect_group.add(explode)
            missile_group.remove(self)

class Explode(pg.sprite.Sprite):
    def __init__(self, col, row):
        pg.sprite.Sprite.__init__(self)
        self.current_img = 1
        self.image = pg.image.load(path.join('images', 'effects', f'explode{self.current_img}.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = col
        self.rect.centery = row
    def update(self):
        if self.current_img < 8:
            self.current_img += 1
        elif self.current_img == 8:
            effect_group.empty()
        self.image = pg.image.load(path.join('images', 'effects', f'explode{self.current_img}.png')).convert_alpha()

class Ship(pg.sprite.Sprite):
    def __init__(self, col, row, team):
        pg.sprite.Sprite.__init__(self)
        self.team = team
        self.image = pg.image.load(path.join('images', 'destroyer.png')).convert_alpha()
        if self.team == 'red': self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = col
        self.rect.y = row
        self._layer = 1
    def attack(self, target):
        x = self.rect.x
        y = self.rect.y
        missile = Missile(x, y, self.team, target)
        missile_group.add(missile)

ship = Ship(150, 150, 'blue')
blue_ships.add(ship)
ship2 = Ship(900, 250, 'red')
red_ships.add(ship2)

class Blank(pg.sprite.Sprite):
  def __init__(self, col, row):
    pg.sprite.Sprite.__init__(self)
    self.grid_x = row * TILESIZE
    self.grid_y = col * TILESIZE
    self.image = pg.image.load(path.join('images', 'black.png')).convert_alpha()
    self.rect = self.image.get_rect()

    self.rect.x = self.grid_x
    self.rect.y = self.grid_y

class Sea(pg.sprite.Sprite):
  def __init__(self, col, row):
    pg.sprite.Sprite.__init__(self)
    self.grid_x = row * TILESIZE
    self.grid_y = col * TILESIZE
    self.image = pg.image.load(path.join('images', 'none.png')).convert_alpha()
    self.rect = self.image.get_rect()

    self.rect.x = self.grid_x
    self.rect.y = self.grid_y

map_data = []
with open('map.txt', 'r') as file:
    for line in file:
        map_data.append(line.strip('\n').split(' '))
for col in range(0, len(map_data)):
    for row in range(0, len(map_data[col][0])):    
        if map_data[col][0][row] == 'o':
            sea = Sea(col, row)
            back_group.add(sea)
        if map_data[col][0][row] == 'x':
            blank = Blank(col, row)
            back_group.add(blank)

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, (0, 0, 0, 50), (x, 0), (x, 500))
    for y in range(0, 500, TILESIZE):
        pg.draw.line(screen, (0, 0, 0, 50), (0, y), (WIDTH, y))
    back_group.draw(screen)

done = False
while not done:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                ships_num = len(red_ships.sprites())
                ship = blue_ships.sprites()[random.randrange(0, ships_num)]
                ship.attack(red_ships.sprites()[0].rect)
    screen.fill(BLACK)
    
    screen.blit(background, (0, -176))
    screen.blit(message_title, title_rect)
    draw_grid()
    red_ships.draw(screen)
    blue_ships.draw(screen)
    missile_group.draw(screen)
    missile_group.update()
    effect_group.draw(screen)
    effect_group.update()
    pg.display.update()
pg.quit()
sys.exit()
