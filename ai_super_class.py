from constants import *
import random

class SuperAi:
    def __init__(self, team, Ship):
        # global FILL_YOUR_NAME
        self.team = team
        # self.name = FILL_YOUR_NAME
        self.ships = []
        self.current_ship = None
        self.last_attack_result = []
        self.initial_ships_pos = []
        self.Ship = Ship
    def create_ships(self):
        from game import map_data, blue_ships, red_ships
        def is_valied_hori(x, y):
            if x != 0:
               x = int(x / TILESIZE)
            if y != 0:
               y = int(y / TILESIZE)
            try:
                print(x, y)
                if map_data[y][x] == 'o' and map_data[y][x+1] == 'o' and map_data[y][x+2] == 'o' and map_data[y][x+3] == 'o' and map_data[y][x+4] == 'o':
                    return True
                else: 
                    print(f'{(x * TILESIZE, y * TILESIZE)} hori 씹혔어요')
                    return False
            except IndexError:
                print(f'{(x * TILESIZE, y * TILESIZE)} hori 씹혔어요')
                return False

        def is_valied_verti(x, y):
            if x != 0:
               x = int(x / TILESIZE)
            if y != 0:
               y = int(y / TILESIZE)
            try:
                if map_data[y][x] == 'o' and map_data[y+1][x] == 'o' and map_data[y+2][x] == 'o' and map_data[y+3][x] == 'o' and map_data[y+4][x] == 'o':
                    return True
                else:
                    print(f'{(x * TILESIZE, y * TILESIZE)} vertical 씹혔어요')
                    return False
            except IndexError:
                print(f'{(x * TILESIZE, y * TILESIZE)} vertical 씹혔어요')
                return False

        if self.team == 'blue':
            for i in self.initial_ships_pos:
                if is_valied_hori(i[0], i[1]) == True:
                    new_ship = self.Ship(i[0], i[1], self.team, 'horizontal')
                    self.ships.append(new_ship)
                    blue_ships.add(new_ship)
                    x = i[0]
                    y = i[1]
                    if x != 0:
                        x = int(x / TILESIZE)
                    if y != 0:
                        y = int(y / TILESIZE)
                    for j in range(0, 5):
                        map_data[y] = map_data[y][0:x+j] + '1' + map_data[y][x+j+1:]
                else:
                    if is_valied_verti(i[0], i[1]) == True:
                        new_ship = self.Ship(i[0], i[1], self.team, 'vertical')
                        self.ships.append(new_ship)
                        blue_ships.add(new_ship)
                        x = i[0]
                        y = i[1]
                        if x != 0:
                            x = int(x / TILESIZE)
                        if y != 0:
                            y = int(y / TILESIZE)
                        for j in range(0, 5):
                            map_data[y+j] = map_data[y+j][0:x] + '1' + map_data[y+j][x+1:]
        elif self.team == 'red':
            self.initial_ships_pos = list(map(lambda i : [i[0] + 700, i[1]], self.initial_ships_pos))
            for i in self.initial_ships_pos:
                if is_valied_hori(i[0], i[1]) == True:
                    new_ship = self.Ship(i[0], i[1], self.team, 'horizontal')
                    self.ships.append(new_ship)
                    red_ships.add(new_ship)
                    x = i[0]
                    y = i[1]
                    if x != 0:
                        x = int(x / TILESIZE)
                    if y != 0:
                        y = int(y / TILESIZE)
                    for j in range(0, 5):
                        map_data[y] = map_data[y][0:x+j] + '2' + map_data[y][x+j+1:]
                else:
                    if is_valied_verti(i[0], i[1]) == True:
                        new_ship = self.Ship(i[0], i[1], self.team, 'vertical')
                        self.ships.append(new_ship)
                        red_ships.add(new_ship)
                        x = i[0]
                        y = i[1]
                        if x != 0:
                            x = int(x / TILESIZE)
                        if y != 0:
                            y = int(y / TILESIZE)
                        for j in range(0, 5):
                            map_data[y+j] = map_data[y+j][0:x] + '2' + map_data[y+j][x+1:]

    def attacking_order(self, x: int, y: int):
        from game import blue_ships, red_ships
        #! 입력 좌표가 최대값(450)을 넘어가면 450으로 보정
        #! 0이나 50의 배수가 아니라면, 입력값과 가장 가까운 50의 배수로 보정(내림)
        new_x = x
        new_y = y
        if new_x > 450:
            new_x = 450
        elif new_x != 0 and new_x % TILESIZE != 0:
            if new_x < TILESIZE:
                new_x = 0
            else:
                new_x -= (new_x % TILESIZE)
        if new_y > 450:
            new_y = 450
        elif new_y != 0 and new_y % TILESIZE != 0:
            if new_y < TILESIZE:
                new_y = 0
            else:
                new_y -= (new_y % TILESIZE)
        blue_ships_num = len(blue_ships.sprites())
        red_ships_num = len(red_ships.sprites())
        print(f'{self.team} => {x} {y}')
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

    def ai_action(self, turn, map):
        print('''inherit class method''')

    def ai_init(self):
        self.create_ships()

    def set_attack_result(self, result, position):
        self.last_attack_result.append({'result': result, 'position': position})
        print(f'{self.team} attacked {position} position => {result}')
