from ai_super_class import SuperAi
import random

FILL_YOUR_NAME = 'I AM A ROBOT'
FOUR_SHIPS_POSITION = [[150, 100], [50, 100], [200, 300], [0, 450]]

class RedAi(SuperAi):
    def __init__(self, team, Ship):
        global FILL_YOUR_NAME
        global FOUR_SHIPS_POSITION
        super().__init__(team, Ship)
        self.name = FILL_YOUR_NAME
        self.initial_ships_pos = FOUR_SHIPS_POSITION

    def ai_action(self, turn, map):
        x = random.randint(0, 9) * 50
        y = random.randint(0, 9) * 50
        result = self.last_attack_result
                
        def invalid_position_checker(map, x, y):
            for i in range(len(map)):
                for j in range(len(map[i])):
                    if i == int(y / 50) and j == int(x / 50):
                        if map[i][j] != 'x' and map[i][j] != '3':
                            return True
            return False
        
        if turn == 1:
            return self.attacking_order(x, y)
        elif result[-1]['result'] == 'nohit':
            if invalid_position_checker(map, x, y) == True:
                return self.attacking_order(x, y)
            else:
                return self.ai_action(turn, map)
        elif result[-1]['result'] == 'hit':
            if result[-1]['position'][0] < 450 and result[-1]['position'][1] >= 0:
                x = result[-1]['position'][0] + 50
                y = result[-1]['position'][1]
                return self.attacking_order(x, y)
            elif result[-1]['position'][1] == 450:
                x = result[-1]['position'][0] - 50
                y = result[-1]['position'][1]
                return self.attacking_order(x, y)
        
#! Don't edit global variable / constant or Fn
# Attack Function is self.attacking_order(x: int, y: int) -> void
# 'x' or 'y' position must be 0 ~ 450 and also multiple of fifty
# Position value will auto adjustment, if position value over 450 or not multiple of fifty
# Your attacking order's result will be in self.last_attack_result list ([{position: tuple, result: str} ... {position: tuple, result: str}])     
