import pygame as pg
import sys
from os import path
from globals import *

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
sprite_group = pg.sprite.Group()
missile_group = pg.sprite.Group()

class Missile(pg.sprite.Sprite):
    def __init__(self, col, row):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path.join('images', 'missile.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = col
        self.rect.y = row
        self._layer = 2
    def moveto_target(self):
        print('')

class Ship(pg.sprite.Sprite):
    def __init__(self, col, row, direction):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path.join('images', 'destroyer.png')).convert_alpha()
        if direction == 'right': self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = col
        self.rect.y = row
        self._layer = 1
    def attack(self):
        x = self.rect.x
        y = self.rect.y
        missile = Missile(x, y)
        sprite_group.add(missile)


ship = Ship(150, 150, 'left')
sprite_group.add(ship)
ship2 = Ship(900, 250, 'right')
sprite_group.add(ship2)

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
            sprite_group.add(sea)
        if map_data[col][0][row] == 'x':
            blank = Blank(col, row)
            sprite_group.add(blank)

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, (0, 0, 0, 50), (x, 0), (x, 500))
    for y in range(0, 500, TILESIZE):
        pg.draw.line(screen, (0, 0, 0, 50), (0, y), (WIDTH, y))

done = False
while not done:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                ship.attack()
    screen.fill(BLACK)
    
    screen.blit(background, (0, -176))
    screen.blit(message_title, title_rect)
    sprite_group.draw(screen)
    missile_group.draw(screen)
    draw_grid()
    pg.display.update()
pg.quit()
sys.exit()
