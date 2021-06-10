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
        self.last_attack_result = self.last_attack_result

    def ai_action(self, turn, map):
        x = random.randint(0, 9) * 50
        y = random.randint(0, 9) * 50
        return self.attacking_order(x, y)
