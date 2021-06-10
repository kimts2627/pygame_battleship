import pygame as pg
import sys
import copy
import pprint
import math
import random
from os import path
from constants import *
from ai_blue import BlueAi
from ai_red import RedAi
pp = pprint.PrettyPrinter(width=41, compact=True)

##########################################################
######################## INIT ############################
##########################################################

pg.init()
map_data = []
clock = pg.time.Clock()
turn = 0
_last_position = (0, 0)
_last_result = 'no'
win_status = ''
screen_status = 'main'

screen = pg.display.set_mode((WIDTH, HEIGHT))
background = pg.image.load('images/background.jpeg')
pg.display.set_caption('BATTLE-SHIP')

back_group = pg.sprite.Group()
red_ships = pg.sprite.Group()
blue_ships = pg.sprite.Group()
missile_group = pg.sprite.Group()
effect_group = pg.sprite.Group()
wreck_group = pg.sprite.Group()

##########################################################
################### CLASS & FUNCTIONS ####################
##########################################################

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

with open('map.txt', 'r') as file:
    for line in file:
        map_data.append(line.strip('\n').split(' '))
map_data = list(map(lambda x: x[0], map_data))
for i in range(0, len(map_data)):
    for j in range(0 , len(map_data[i])):
        if map_data[i][j] == 'x':
            tile = Blank(i, j)
            back_group.add(tile)
        elif map_data[i][j] == 'o':
            tile = Sea(i, j)
            back_group.add(tile)

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, BLACK, (x, 0), (x, 500))
    for y in range(0, 500, TILESIZE):
        pg.draw.line(screen, BLACK, (0, y), (WIDTH, y))

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
        self.pos_list = [(self.rect.x, self.rect.y), (target['x'], target['y'])]
        self.pos = self.pos_list[0]
        self.speed = 25
        self.next_pos_index = 1
        self.angle = math.degrees(math.atan2(self.rect.centery - target['y'], target['x'] - self.rect.centerx))
        self.image = pg.transform.rotate(self.image, self.angle)

    def update(self):
        x = self.target['x']
        y = self.target['y']
        missile_dir = pg.math.Vector2(self.pos_list[self.next_pos_index]) - self.pos
        if missile_dir.length() < self.speed:
            self.pos = self.pos_list[self.next_pos_index]
            self.next_pos_index = (self.next_pos_index + 1) % len(self.pos_list)
        else:
            missile_dir.scale_to_length(self.speed)
            new_pos = pg.math.Vector2(self.pos) + missile_dir
            self.pos = (new_pos.x, new_pos.y)
        self.rect.x = round(self.pos[0])
        self.rect.y = round(self.pos[1])

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
        self.x = parent.rect.x
        self.y = parent.rect.y
        if parent.team == 'red': self.x = self.x + 70
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
            self.size -= 4
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
    def __init__(self, col, row):
        pg.sprite.Sprite.__init__(self)
        self.grid_x = row * TILESIZE
        self.grid_y = col * TILESIZE
        self.current_img = 1
        self.image = pg.image.load(path.join('images', 'fire', f'fire{self.current_img}.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.grid_x
        self.rect.y = self.grid_y
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

def generate_user_action_result(attack_position: tuple, team: str):
    global map_data
    map_y = int(attack_position[0] / TILESIZE)
    map_x = int(attack_position[1] / TILESIZE)

    def find_hitted_ship(attack_position, ship_group):
        x = attack_position[0]
        y = attack_position[1]
        print(x, y)
        for i in ship_group.sprites():
            print(i.rect, i.direction)
            for j in range(0, 5):
                if i.direction == 'horizontal':
                    print(i.rect.x + (TILESIZE * j), x)
                    print(i.rect.y, y)
                    if i.rect.x + (TILESIZE * j) == x and i.rect.y == y:
                        return i
                elif i.direction == 'vertical':
                    if i.rect.x == x and i.rect.y + (TILESIZE * j) == y:
                        return i

    if team == 'blue':
        if map_data[map_x][map_y] == '2':
            map_data[map_x] = map_data[map_x][0:map_y] + '3' + map_data[map_x][map_y+1:]
            attacked_ship = find_hitted_ship(attack_position, red_ships)
            attacked_ship.hit_count += 1
            return 'hit'
        elif map_data[map_x][map_y] == 'o':
            map_data[map_x] = map_data[map_x][0:map_y] + 'x' + map_data[map_x][map_y+1:]
            return 'nohit'
        else:
            return 'nohit'
    elif team == 'red':
        if map_data[map_x][map_y] == '1':
            map_data[map_x] = map_data[map_x][0:map_y] + '3' + map_data[map_x][map_y+1:]
            attacked_ship = find_hitted_ship(attack_position, blue_ships)
            attacked_ship.hit_count += 1
            return 'hit'
        elif map_data[map_x][map_y] == 'o':
            map_data[map_x] = map_data[map_x][0:map_y] + 'x' + map_data[map_x][map_y+1:]
            return 'nohit'
        else:
            return 'nohit'

class Ship(pg.sprite.Sprite):
    def __init__(self, col, row, team, direction):
        pg.sprite.Sprite.__init__(self)
        self.team = team
        self.image = pg.image.load(path.join('images', 'ships', 'destroyer.png')).convert_alpha()
        if self.team == 'red': self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = col
        self.rect.y = row
        self.direction = direction
        if self.direction == 'vertical': self.image = pg.transform.rotate(self.image, 90)
        self.hit_count = 0

    def attack(self, target):
        global _last_result
        global _last_position
        x = self.rect.centerx
        y = self.rect.centery
        missile = Missile(x, y, self.team, target)
        missile_group.add(missile)
        _last_position = (target['x'] - 25, target['y'] - 25)
        _last_result = generate_user_action_result(_last_position, self.team)
    
    def update(self):
        hitted = self.hit_count
        team = self.team
        dir = self.direction
        if hitted != 0:
            self.image = pg.image.load(path.join('images', 'ships', f'destroyer{hitted}.png')).convert_alpha()
            if team == 'red': self.image = pg.transform.flip(self.image, True, False)
            if dir == 'vertical': self.image = pg.transform.rotate(self.image, 90)

class DestoryedShip(pg.sprite.Sprite):
    def __init__(self, col, row, team, direction):
        pg.sprite.Sprite.__init__(self)
        self.team = team
        self.direction = direction
        self.image = pg.image.load(path.join('images', 'ships', f'destroyer{random.randint(5, 6)}.png')).convert_alpha()
        if self.team == 'red': self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = col
        self.rect.y = row
        if self.direction == 'vertical': self.image = pg.transform.rotate(self.image, 90)
        
def ship_hit_checker(blue_group, red_group):
    global mini_map
    blues = blue_group.sprites()
    reds = red_group.sprites()
    for i in blues:
        if i.hit_count == 5:
            wreck = DestoryedShip(i.rect.x, i.rect.y, i.team, i.direction)
            wreck_group.add(wreck)
            blue_group.remove(i)
            print('blue team ship is sink down!')
    for i in reds:
        if i.hit_count == 5:
            wreck = DestoryedShip(i.rect.x, i.rect.y, i.team, i.direction)
            wreck_group.add(wreck)
            red_group.remove(i)
            print('red team ship is sink down!')

def map_status_draw(map):
    global back_group
    back_group.empty()
    for i in range(0, len(map)):
        for j in range(0, len(map[i])):
            if map[i][j] == 'x':
                new_tile = Blank(i, j)
                back_group.add(new_tile)
            elif map[i][j] == '3':
                new_tile = Fire(i, j)
                back_group.add(new_tile)
            elif map[i][j] == 'o':
                new_tile = Sea(i, j)
                back_group.add(new_tile)

class BlackOut(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.level = 1
        self.image = pg.Surface((1200, 700), pg.SRCALPHA)
        self.image.set_colorkey(BLACK)
        self.image = self.image.convert_alpha()
        self.image.fill((0, 0, 0, 90))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
    
    def update(self, mt):
        global screen_status
        if self.level == 255:
            screen_status = 'result'
        else:
            self.level += 1
            self.image.fill((0, 0, 0, self.level))

black = BlackOut()

def winner_checker():
    global win_status
    global blue_ships
    global red_ships
    global message_result
    if len(blue_ships.sprites()) == 0:
        win_status = 'RED'
        black_out = BlackOut()
        effect_group.add(black_out)
    elif len(red_ships.sprites()) == 0:
        win_status = 'BLUE'
        black_out = BlackOut()
        effect_group.add(black_out)

##########################################################
###################### AI INIT ###########################
##########################################################

blue_man = BlueAi('blue', Ship)
blue_man.ai_init()
red_man = RedAi('red', Ship)
red_man.ai_init()

##########################################################
######################## TEXT ############################
##########################################################

my_big_font = pg.font.SysFont('arial', 50, True, False)
my_font = pg.font.SysFont('arial', 30, True, False)
my_font_2 = pg.font.SysFont('arial', 25, True, False)
my_font_3 = pg.font.SysFont('arial', 20, True, False)
my_small_font = pg.font.SysFont('arial', 10, True, False)

##* GAME SCREEN *##
# GAME TITLE
message_title = my_font.render(TITLE, True, WHITE)
title_rect = message_title.get_rect()
title_rect.centerx = round(WIDTH / 2)
title_rect.y = 520
# TURN
message_turn = my_font_2.render(TURN + f'{turn}', True, WHITE)
turn_rect = message_turn.get_rect()
turn_rect.centerx = round(WIDTH / 2)
turn_rect.y = 550
# NEXT TURN
message_next_turn = my_font_3.render(NEXT_TURN, True, WHITE)
next_turn_rect = message_next_turn.get_rect()
next_turn_rect.centerx = round(WIDTH / 2)
next_turn_rect.y = 590
# NEW GAME
# message_new_game = my_font_3.render(NEWGAME, True, WHITE)
# new_game_rect = message_new_game.get_rect()
# new_game_rect.centerx = round(WIDTH / 2)
# new_game_rect.y = 615
# QUIT GAME
message_exit_game = my_font_3.render(ENDGAME, True, WHITE)
exit_game_rect = message_exit_game.get_rect()
exit_game_rect.centerx = round(WIDTH / 2)
exit_game_rect.y = 640
# BLUE
message_blue = my_font.render(BLUE_TEAM, True, BLUE)
blue_rect = message_blue.get_rect()
blue_rect.centerx = 250
blue_rect.y = 520
# BLUE NAME
blue_name = blue_man.name
message_blue_name = my_font_3.render(PLAYER_NAME + blue_name, True, WHITE)
blue_name_rect = message_blue_name.get_rect()
blue_name_rect.centerx = 250
blue_name_rect.y = 560
# BLUE SHIPS
message_blue_ships = my_font_3.render(LEFT_SHIPS + str(len(blue_ships.sprites())), True, WHITE)
blue_ships_rect = message_blue_ships.get_rect()
blue_ships_rect.centerx = 250
blue_ships_rect.y = 590
# RED
message_red = my_font.render(RED_TEAM, True, RED)
red_rect = message_red.get_rect()
red_rect.centerx = 950
red_rect.y = 520
# RED NAME
red_name = red_man.name
message_red_name = my_font_3.render(PLAYER_NAME + red_name, True, WHITE)
red_name_rect = message_red_name.get_rect()
red_name_rect.centerx = 950
red_name_rect.y = 560
# RED SHIPS
message_red_ships = my_font_3.render(LEFT_SHIPS + str(len(red_ships.sprites())), True, WHITE)
red_ships_rect = message_red_ships.get_rect()
red_ships_rect.centerx = 950
red_ships_rect.y = 590

##* MAIN SCREEN *##
# MAIN TITLE
message_main_title = my_big_font.render(TITLE, True, WHITE)
main_title_rect = message_main_title.get_rect()
main_title_rect.centerx = round(WIDTH / 2)
main_title_rect.centery = round(HEIGHT / 2 - 100)
# START GAME
message_start_game = my_font_2.render(START_GAME, True, WHITE)
start_game_rect = message_start_game.get_rect()
start_game_rect.centerx = round(WIDTH / 2)
start_game_rect.centery = round(HEIGHT / 2 - 30)
# VERSION
message_version = my_small_font.render(VERSION, True, WHITE)
version_rect = message_version.get_rect()
version_rect.centerx = round(WIDTH / 2)
version_rect.centery = round(HEIGHT - 50)

##* RRESULT SCREEN *##
# RESULT
# message_result = my_big_font.render(f'{win_status} {RESULT}', True, WHITE)
# result_rect = message_result.get_rect()
# result_rect.centerx = round(WIDTH / 2)
# result_rect.centery = round(HEIGHT / 2)

def draw_text():
    screen.blit(message_title, title_rect)
    # screen.blit(message_new_game, new_game_rect)
    message_turn = my_font_3.render(TURN + f'{turn}', True, WHITE)
    screen.blit(message_turn, turn_rect)
    screen.blit(message_next_turn, next_turn_rect)
    screen.blit(message_exit_game, exit_game_rect)

    pg.draw.line(screen, WHITE, [460, 520], [460, 670], 4)
    pg.draw.line(screen, WHITE, [740, 520], [740, 670], 4)

    screen.blit(message_blue, blue_rect)
    screen.blit(message_blue_name, blue_name_rect)
    message_blue_ships = my_font_3.render(LEFT_SHIPS + str(len(blue_ships.sprites())), True, WHITE)
    screen.blit(message_blue_ships, blue_ships_rect)
    screen.blit(message_red, red_rect)
    screen.blit(message_red_name, red_name_rect)
    message_red_ships = my_font_3.render(LEFT_SHIPS + str(len(red_ships.sprites())), True, WHITE)
    screen.blit(message_red_ships, red_ships_rect)

def draw_main_text():
    screen.blit(message_main_title, main_title_rect)
    pg.draw.line(screen, WHITE, [160, 290], [1060, 290], 2)
    screen.blit(message_start_game, start_game_rect)
    screen.blit(message_version, version_rect)

def draw_result_text():
    message_result = my_big_font.render(f'{win_status} {RESULT}', True, WHITE)
    result_rect = message_result.get_rect()
    result_rect.centerx = round(WIDTH / 2)
    result_rect.centery = round(HEIGHT / 2)
    screen.blit(message_result, result_rect)


##########################################################
###################### GAME LOOP #########################
##########################################################

done = False
while not done: 
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if screen_status == 'main':
                    screen_status = 'game'
                elif screen_status == 'game' and len(blue_ships.sprites()) != 0 and len(red_ships.sprites()) != 0:
                    turn += 1
                    print(f'********************************************************')
                    print(f'************************{turn} turn!*************************')
                    print(f'********************************************************')
                    hidden_map = copy.deepcopy(map_data)
                    for i in range(len(hidden_map)):
                        for j in range(len(hidden_map[i])):
                            if hidden_map[i][j] == '2':
                                hidden_map[i] = hidden_map[i][0:j] + 'o' + hidden_map[i][j+1:]
                    blue_man.ai_action(turn, hidden_map)
                    blue_man.set_attack_result(_last_result, _last_position)
                    hidden_map = copy.deepcopy(map_data)
                    for i in range(len(hidden_map)):
                        for j in range(len(hidden_map[i])):
                            if hidden_map[i][j] == '1':
                                hidden_map[i] = hidden_map[i][0:j] + 'o' + hidden_map[i][j+1:]
                    red_man.ai_action(turn, hidden_map)
                    red_man.set_attack_result(_last_result, _last_position)
                    ship_hit_checker(blue_ships, red_ships)
                    winner_checker()
                    map_status_draw(map_data)
                    pp.pprint(map_data)
                elif screen_status == 'result':
                    done = True
            elif event.key == pg.K_q:
                done = True

    screen.fill(BLACK)
    
    if screen_status == 'main':
        screen.blit(background, (0, -176))
        draw_main_text()
        pg.display.update()
    elif screen_status == 'game':
        screen.blit(background, (0, -176))
        mt = 0.06
        draw_text()
        draw_grid()
        red_ships.draw(screen)
        blue_ships.draw(screen)
        red_ships.update()
        blue_ships.update()
        missile_group.draw(screen)
        missile_group.update()
        back_group.draw(screen)
        back_group.update(mt)
        wreck_group.draw(screen)
        wreck_group.update()
        effect_group.draw(screen)
        effect_group.update(mt)
        pg.display.update()
    elif screen_status == 'result':
        screen = pg.display.set_mode((WIDTH, HEIGHT))
        screen.fill(BLACK)
        draw_result_text()
        pg.display.update()


pg.quit()
sys.exit()
