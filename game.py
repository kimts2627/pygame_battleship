import pygame as pg
import sys
from os import path
from globals import *

pg.init()
clock = pg.time.Clock()
big_font = pg.font.SysFont(None, 80)
small_font = pg.font.SysFont(None, 40)
MESSAGE_TITLE = big_font.render("BATTLESHIP", True, (255, 255, 255))
screen = pg.display.set_mode((WIDTH, HEIGHT))
background = pg.image.load('images/background.jpeg')
pg.display.set_caption('pg~!')
sprite_group = pg.sprite.Group()

class Ship(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path.join('images', 'destroyer.png')).convert_alpha()
        self.rect = self.image.get_rect()

ship = Ship()
sprite_group.add(ship)
ship.rect.x = 150
ship.rect.y = 150

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
print(map_data)
for col in range(0, len(map_data)):
    print(map_data[col])
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
    screen.blit(background, (0, -176))
    screen.blit(MESSAGE_TITLE, (0, 500))
    sprite_group.draw(screen)
    draw_grid()
    pg.display.update()
pg.quit()
sys.exit()
