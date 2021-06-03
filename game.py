import pygame as pg
import sys
import random
from math import cos, e, sin, floor
from os import path
from globals import *
from ai_blue import *
from ai_red import *

pg.init()
map_data = []
clock = pg.time.Clock()
turn = 0
_last_position = (0, 0)
_last_result = 'no'
# def set_last_position(pos: tuple):
#     _last_position = pos
# def set_last_result(result: str):
#     _last_result = result
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
map_data = list(map(lambda x: x[0], map_data))
for col in range(0, len(map_data)):
    for row in range(0, len(map_data[col])):    
        if map_data[col][row] == 'o':
            sea = Sea(col, row)
            back_group.add(sea)
        if map_data[col][row] == 'x':
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
        self.speed = 25

    def update(self):
        print('update!')
        x = self.target['x']
        y = self.target['y']
        #####################################################3
        if self.rect.x != x:
            if self.rect.x > x:
                self.rect.x -= self.speed
            elif self.rect.x < x:
                self.rect.x += self.speed
        if self.rect.y != y:
            if self.rect.y > y:
                self.rect.y -= self.speed
            elif self.rect.y < y:
                self.rect.y += self.speed
        #####################################################
        if self.rect.y == y and self.rect.x == x:
            explode = Explode(x, y)
            effect_group.add(explode)
            missile_group.remove(self)
        fx = MissileFx(self)
        missile_group.add(fx)

class MissileFx(pg.sprite.Sprite):
    def __init__(self, parent):
        pg.sprite.Sprite.__init__(self)
        self.parent = parent
        self.x = self.parent.rect.x
        self.y = self.parent.rect.y
        self.image = pg.Surface((self.x, self.y))
        self.image.fill(GRAY)
        pg.draw.circle(self.image, GRAY, (self.x // 2, self.y // 2), 5)
        self.image = pg.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(centerx = self.x, centery = self.y)
        self.size = 20
        self.animation_time = round(100 / 100, 2)
        self.current_time = 0
    
    def update(self):
        if self.size == 0:
            missile_group.remove(self)
        else:
            self.size -= 5
            self.image = pg.transform.scale(self.image, (self.size, self.size))

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
    def __init__(self, col, row, team, direction):
        pg.sprite.Sprite.__init__(self)
        self.team = team
        self.image = pg.image.load(path.join('images', 'destroyer.png')).convert_alpha()
        if self.team == 'red': self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = col
        self.rect.y = row
        self.direction = direction
        if self.direction == 'vertical': self.image = pg.transform.rotate(self.image, 90)
        self.enemy_group = None
        if self.team == 'blue': self.enemy_group = red_ships
        elif self.team == 'red': self.enemy_group = blue_ships

    def attack(self, target):
        global _last_result
        global _last_position
        x = self.rect.centerx
        y = self.rect.centery
        missile = Missile(x, y, self.team, target)
        missile_group.add(missile)
        for i in back_group:
            if i.rect.x + 25 == target['x'] and i.rect.y + 25 == target['y']:
                for j in self.enemy_group:
                    if target['x'] == j.rect.x and target['y'] == j.rect.y:
                        i.set_child(target)
                        _last_result = 'hit'
                        _last_position = (target['x'], target['y'])
                    else:
                        _last_result = 'nohit'
                        _last_position = (target['x'], target['y'])

class MyAi:
    def __init__(self, team, name):
        self.team = team
        self.name = name or 'unnamed'
        self.ships = []
        self.current_ship = None
        self.last_attack_result = []

    def create_ships(self):
        global map_data

        def is_valied_hori(x, y):
            if x != 0:
               x = int(x / 50)
            if y != 0:
               y = int(y / 50)
            try:
                print(x, y)
                # if map_data[x][y] == 'o' and map_data[x][y+1] == 'o' and map_data[x][y+2] == 'o' and map_data[x][y+3] == 'o' and map_data[x][y+4] == 'o':
                if map_data[y][x] == 'o' and map_data[y][x+1] == 'o' and map_data[y][x+2] == 'o' and map_data[y][x+3] == 'o' and map_data[y][x+4] == 'o':
                    return True
                else: 
                    print(f'{(x*50, y*50)} hori 씹혔어요')
                    return False
            except IndexError:
                print(f'{(x*50, y*50)} hori 씹혔어요')
                return False

        def is_valied_verti(x, y):
            if x != 0:
               x = int(x / 50)
            if y != 0:
               y = int(y / 50)
            try:
                # if map_data[x][y] == 'o' and map_data[x+1][y] == 'o' and map_data[x+2][y] == 'o' and map_data[x+3][y] == 'o' and map_data[x+4][y] == 'o':
                if map_data[y][x] == 'o' and map_data[y+1][x] == 'o' and map_data[y+2][x] == 'o' and map_data[y+3][x] == 'o' and map_data[y+4][x] == 'o':
                    return True
                else:
                    print(f'{(x*50, y*50)} vertical 씹혔어요')
                    return False
            except IndexError:
                print(f'{(x*50, y*50)} vertical 씹혔어요')
                return False

        if self.team == 'blue':
            SHIPS_POS = [[150, 100], [50, 100], [200, 300], [0, 450]]
            for i in SHIPS_POS:
                if is_valied_hori(i[0], i[1]) == True:
                    new_ship = Ship(i[0], i[1], self.team, 'horizontal')
                    self.ships.append(new_ship)
                    blue_ships.add(new_ship)
                    x = i[0]
                    y = i[1]
                    if x != 0:
                        x = int(x / 50)
                    if y != 0:
                        y = int(y / 50)
                    for j in range(0, 5):
                        map_data[y] = map_data[y][0:x+j] + '1' + map_data[y][x+j+1:]
                else:
                    if is_valied_verti(i[0], i[1]) == True:
                        new_ship = Ship(i[0], i[1], self.team, 'vertical')
                        self.ships.append(new_ship)
                        blue_ships.add(new_ship)
                        x = i[0]
                        y = i[1]
                        if x != 0:
                            x = int(x / 50)
                        if y != 0:
                            y = int(y / 50)
                        for j in range(0, 5):
                            map_data[y+j] = map_data[y+j][0:x] + '1' + map_data[y+j][x+1:]
        elif self.team == 'red':
            SHIPS_POS = [[150, 100], [250, 50], [200, 300], [0, 450]]
            SHIPS_POS = list(map(lambda i : [i[0] + 700, i[1]], SHIPS_POS))
            for i in SHIPS_POS:
                if is_valied_hori(i[0], i[1]) == True:
                    new_ship = Ship(i[0], i[1], self.team, 'horizontal')
                    self.ships.append(new_ship)
                    red_ships.add(new_ship)
                    x = i[0]
                    y = i[1]
                    if x != 0:
                        x = int(x / 50)
                    if y != 0:
                        y = int(y / 50)
                    for j in range(0, 5):
                        map_data[y] = map_data[y][0:x+j] + '2' + map_data[y][x+j+1:]
                else:
                    if is_valied_verti(i[0], i[1]) == True:
                        new_ship = Ship(i[0], i[1], self.team, 'vertical')
                        self.ships.append(new_ship)
                        red_ships.add(new_ship)
                        x = i[0]
                        y = i[1]
                        if x != 0:
                            x = int(x / 50)
                        if y != 0:
                            y = int(y / 50)
                        for j in range(0, 5):
                            map_data[y+j] = map_data[y+j][0:x] + '2' + map_data[y+j][x+1:]
        print(map_data)
        # print(blue_ships.sprites()[0].rect, blue_ships.sprites()[1].rect, blue_ships.sprites()[2].rect, blue_ships.sprites()[3].rect)

    def attacking_order(self, x: int, y: int):
        #! 입력 좌표가 최대값(450)을 넘어가면 450으로 보정
        #! 0이나 50의 배수가 아니라면, 입력값과 가장 가까운 50의 배수로 보정(내림)
        new_x = x
        new_y = y
        if new_x > 450:
            new_x = 450
        elif new_x != 0 and new_x % 50 != 0:
            if new_x < 50:
                new_x = 0
            else:
                new_x -= (new_x % 50)
        if new_y > 450:
            new_y = 450
        elif new_y != 0 and new_y % 50 != 0:
            if new_y < 50:
                new_y = 0
            else:
                new_y -= (new_y % 50)
        blue_ships_num = len(blue_ships.sprites())
        red_ships_num = len(red_ships.sprites())
        if self.team == 'blue':
            new_x += 725
            new_y += 25
            self.current_ship = blue_ships.sprites()[random.randrange(0, blue_ships_num)]
        elif self.team == 'red':
            new_x += 25
            new_y += 25
            self.current_ship = red_ships.sprites()[random.randrange(0, red_ships_num)]
        target = {'x': new_x, 'y': new_y}
        self.current_ship.attack(target)

    def ai_action(self, turn):
    #############################* USER CODE HERE * ###################################### 
        x = random.randint(0, 450)
        y = random.randint(0, 450)
        result = self.last_attack_result
        if turn == 1:
            self.attacking_order(x, y)
        else:
            if len(result) == 0:
                self.attacking_order(x, y)
            else:
                if result[-1]['result'] == 'nohit':
                    for i in list(reversed(result)):
                        if i['result'] == 'hit':
                            x = i['position'][0] + 50
                            y = i['position'][1]
                            self.attacking_order(x, y)
                        else:
                            self.attacking_order(x, y)
                elif result[-1]['result'] == 'hit':
                            x = x + 50
                            self.attacking_order(x, y)

    #! Don't edit global variable / constant or Fn
    # Attack Function is self.attacking_order(x: int, y: int) -> void
    # 'x' or 'y' position must be 0 ~ 450 and also multiple of fifty
    # Position value will auto adjustment, if position value over 450 or not multiple of fifty
    # Your attacking order's result will be in self.last_attack_result list ([{position: tuple, result: str} ... {position: tuple, result: str}])     
    #############################* USER CODE HERE * ###################################### 

    def ai_init(self):
        self.create_ships()
        print('')

    def set_attack_result(self, result, position):
        self.last_attack_result.append({'result': result, 'position': position})
        print(f'{self.team} attacked {position} position => {result}')
    
def generate_user_action_result(attack_position: tuple, team: str):
    if team == 'blue':
        for i in blue_ships:
            if i.rect.x == attack_position[0] and i.rect.y == attack_position[1]:
                return 'hit'
            else:
                return 'nohit'

blue_man = MyAi('blue', 'Taesu Kim')
blue_man.ai_init()
red_man = MyAi('red', 'Taesu Park')
red_man.ai_init()

done = False
while not done:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                turn += 1
                print(f'**********************{turn} turn!**********************')
                blue_man.ai_action(turn)
                blue_man.set_attack_result(_last_result, _last_position)
                print(_last_position, _last_result)
                red_man.ai_action(turn)
                red_man.set_attack_result(_last_result, _last_position)
                print(_last_position, _last_result)
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
