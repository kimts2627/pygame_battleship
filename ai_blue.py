from ai_super_class import SuperAi
import random

FILL_YOUR_NAME: str = 'Taesu Kim!'
FOUR_SHIPS_POSITION: list[list[int, int]] = [[150, 100], [250, 50], [200, 300], [0, 450]]

class BlueAi(SuperAi):
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
        return self.attacking_order(x, y)

        
#! Don't edit global variable / constant or Fn
# Attack Function is self.attacking_order(x: int, y: int) -> void
# 'x' or 'y' position must be 0 ~ 450 and also multiple of fifty
# Position value will auto adjustment, if position value over 450 or not multiple of fifty
# Your attacking order's result will be in self.last_attack_result list ([{position: tuple, result: str} ... {position: tuple, result: str}])     
