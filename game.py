import pygame as pg
import sys
import random
import time
from os import path
from globals import *
from ai_blue import *
from ai_red import *

pg.init()
map_data = []
clock = pg.time.Clock()
turn = 1
my_font = pg.font.SysFont('latobold', 30, True, False)
my_font_2 = pg.font.SysFont('latobold', 25, True, False)
my_font_3 = pg.font.SysFont('latobold', 20, True, False)

back_group = pg.sprite.Group()
red_ships = pg.sprite.Group()
blue_ships = pg.sprite.Group()
missile_group = pg.sprite.Group()
effect_group = pg.sprite.Group()

# title of game
message_title = my_font.render(TITLE, True, WHITE)
title_rect = message_title.get_rect()
title_rect.centerx = round(WIDTH / 2)
title_rect.y = 520
# game current turn
message_turn = my_font_2.render(TURN + f'{turn}', True, WHITE)
turn_rect = message_turn.get_rect()
turn_rect.centerx = round(WIDTH / 2)
turn_rect.y = 550
# turn progress guide
message_next_turn = my_font_3.render(NEXT_TURN, True, WHITE)
next_turn_rect = message_next_turn.get_rect()
next_turn_rect.centerx = round(WIDTH / 2)
next_turn_rect.y = 590
# new game guide
message_new_game = my_font_3.render(NEWGAME, True, WHITE)
new_game_rect = message_new_game.get_rect()
new_game_rect.centerx = round(WIDTH / 2)
new_game_rect.y = 615
# exit game guide
message_exit_game = my_font_3.render(ENDGAME, True, WHITE)
exit_game_rect = message_exit_game.get_rect()
exit_game_rect.centerx = round(WIDTH / 2)
exit_game_rect.y = 640
# BLUE
message_blue = my_font.render(BLUE_TEAM, True, BLUE)
blue_rect = message_blue.get_rect()
blue_rect.centerx = 250
blue_rect.y = 520
# BLUE_NAME
blue_name = 'Taesu Kim'
message_blue_name = my_font_3.render(PLAYER_NAME + blue_name, True, WHITE)
blue_name_rect = message_blue_name.get_rect()
blue_name_rect.centerx = 250
blue_name_rect.y = 560
# BLUE_SHIPS
message_blue_ships = my_font_3.render(LEFT_SHIPS + str(len(blue_ships.sprites())), True, WHITE)
blue_ships_rect = message_blue_ships.get_rect()
blue_ships_rect.centerx = 250
blue_ships_rect.y = 590
# RED
message_red = my_font.render(RED_TEAM, True, RED)
red_rect = message_red.get_rect()
red_rect.centerx = 950
red_rect.y = 520
# RED_NAME
red_name = 'Taesu Park'
message_red_name = my_font_3.render(PLAYER_NAME + red_name, True, WHITE)
red_name_rect = message_red_name.get_rect()
red_name_rect.centerx = 950
red_name_rect.y = 560
# RED_SHIPS
message_red_ships = my_font_3.render(LEFT_SHIPS + str(len(red_ships.sprites())), True, WHITE)
red_ships_rect = message_red_ships.get_rect()
red_ships_rect.centerx = 950
red_ships_rect.y = 590
# SCREEN
screen = pg.display.set_mode((WIDTH, HEIGHT))
background = pg.image.load('images/background.jpeg')
pg.display.set_caption('BATTLE-SHIP')

def draw_text():
    screen.blit(message_title, title_rect)
    screen.blit(message_new_game, new_game_rect)
    message_turn = my_font_2.render(TURN + f'{turn}', True, WHITE)
    screen.blit(message_turn, turn_rect)
    screen.blit(message_next_turn, next_turn_rect)
    screen.blit(message_exit_game, exit_game_rect)

    pg.draw.line(screen, WHITE, [500, 520], [500, 670], 4)
    pg.draw.line(screen, WHITE, [700, 520], [700, 670], 4)

    screen.blit(message_blue, blue_rect)
    screen.blit(message_blue_name, blue_name_rect)
    message_blue_ships = my_font_3.render(LEFT_SHIPS + str(len(blue_ships.sprites())), True, WHITE)
    screen.blit(message_blue_ships, blue_ships_rect)
    screen.blit(message_red, red_rect)
    screen.blit(message_red_name, red_name_rect)
    message_red_ships = my_font_3.render(LEFT_SHIPS + str(len(red_ships.sprites())), True, WHITE)
    screen.blit(message_red_ships, red_ships_rect)

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
        self.child = None

    def set_child(self, target_ship):
        if target_ship:
            fire = Fire(self.rect.x, self.rect.y, self)
            self.child = fire
            effect_group.add(fire)
            print(f'({self.rect.x}, {self.rect.y}) has been attacked.')

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

def game_init():
    ai_blue = MyAi('blue', '김태수')
    ai_red = MyAi('red', '박태수')
    ai_blue.ai_init()
    ai_red.ai_init()

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
        self.curve = 5

    def update(self):
        print('update!')
        x = self.target.x + 25
        y = self.target.y + 25
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
                self.curve + 5
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
        self.image = pg.image.load(path.join('images', 'explode', f'explode{self.current_img}.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = col
        self.rect.centery = row
        self.animation_time = round(100 / 1600, 2)
        self.current_time = 0

    def update(self, mt):
        self.current_time += mt
        if self.current_time >= self.animation_time:
            if self.current_img < 16:
                self.current_img += 1
            elif self.current_img == 16:
                effect_group.remove(self)
            self.image = pg.image.load(path.join('images', 'explode', f'explode{self.current_img}.png')).convert_alpha()
            self.current_time = 0

class Fire(pg.sprite.Sprite):
    def __init__(self, col, row, mother):
        pg.sprite.Sprite.__init__(self)
        self.mother_block = mother
        self.current_img = 1
        self.image = pg.image.load(path.join('images', 'fire', f'fire{self.current_img}.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = col + 25
        self.rect.centery = row + 25
        self.animation_time = round(100 / 400, 2)
        self.current_time = 0

    def update(self, mt):
        self.current_time += mt
        if self.current_time >= self.animation_time:
            if self.current_img < 4:
                self.current_img += 1
            elif self.current_img == 4:
                self.current_img = 1
            self.image = pg.image.load(path.join('images', 'fire', f'fire{self.current_img}.png')).convert_alpha()
            self.current_time = 0

class Ship(pg.sprite.Sprite):
    def __init__(self, col, row, team):
        pg.sprite.Sprite.__init__(self)
        self.team = team
        self.image = pg.image.load(path.join('images', 'destroyer.png')).convert_alpha()
        if self.team == 'red': self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = col
        self.rect.y = row
        self.status = 'normal'

    def attack(self, target):
        x = self.rect.centerx
        y = self.rect.centery
        missile = Missile(x, y, self.team, target)
        missile_group.add(missile)
        for i in back_group:
            if i.rect.x == target.x and i.rect.y == target.y:
                i.set_child(target)

    def mark_to_attacked(self):
        self.status = 'attacked'

# ship = Ship(150, 150, 'blue')
# blue_ships.add(ship)
ship2 = Ship(900, 250, 'red')
red_ships.add(ship2)

class MyAi:
    def __init__(self, team, name, initail_map):
        self.team = team
        self.name = name or 'unnamed'
        self.ships = []
        self.map = initail_map

    def create_ships(self):
        SHIPS_POS = [[150, 100], [250, 50], [200, 300], [0, 450]]
        for i in SHIPS_POS:
            new_ship = Ship(i[0], i[1], self.team)
            if self.team == 'blue':
                self.ships.append(new_ship)
                blue_ships.add(new_ship)
            elif self.team == 'red':
                self.ships.append(new_ship)
                red_ships.add(new_ship)

    def attack(self):
        print('')

    def ai_action(self, turn):
        print('')

    def ai_init(self):
        self.create_ships()
        print('')

    def update_status(self):
        print('')

blue_man = MyAi('blue', 'Taesu Kim', map)
blue_man.create_ships()

done = False
while not done:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                ships_num = len(blue_ships.sprites())
                ship = blue_ships.sprites()[random.randrange(0, ships_num)]
                ship.attack(red_ships.sprites()[0].rect)
                turn += 1
    screen.fill(BLACK)
    
    screen.blit(background, (0, -176))
    draw_text()
    draw_grid()
    red_ships.draw(screen)
    blue_ships.draw(screen)
    missile_group.draw(screen)
    missile_group.update()
    effect_group.draw(screen)
    mt = 0.06
    effect_group.update(mt)
    pg.display.update()

pg.quit()
sys.exit()
