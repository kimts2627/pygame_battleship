from ai_super_class import SuperAi
import random

FILL_YOUR_NAME: str = """FILL_ME_IN"""
FOUR_SHIPS_POSITION: list[list[int, int]] = """FILL_ME_IN"""

class BlueAi(SuperAi):
    def __init__(self, team, Ship):
        global FILL_YOUR_NAME
        global FOUR_SHIPS_POSITION
        super().__init__(team, Ship)
        self.name = FILL_YOUR_NAME
        self.initial_ships_pos = FOUR_SHIPS_POSITION
        self.last_attack_result = self.last_attack_result

    def ai_action(self, turn: int, map: list[str]):
        print('''DELETE_ME''')

        #* <last_attack_result> is your attack result list
        #* ex) [{'result': 'nohit', 'position': (200, 350)}, {'result': 'hit', 'position': (0, 200)}, ... , {'result': 'nohit', 'position': (100, 0)}]
        #* you can lookup result list to use {self.last_attack_result}

        #* input <turn> is game's current turn.
        #* it will be increase each trun start time

        #* input <map> is game's current turn.
        #* ex)  ['ooooooooooxxxxoooooooooo'
        #*       'ooooooooooxxxxoooooooooo'
        #*       'ooooooooooxxxxoooooooooo'
        #*       'ooooooooooxxxxoooooooooo'
        #*       'ooooooooooxxxxoooooooooo'
        #*       'ooooooooooxxxxoooooooooo'
        #*       'ooooooooooxxxxoooooooooo'
        #*       'ooooooooooxxxxoooooooooo'
        #*       'ooooooooooxxxxoooooooooo'
        #*       'ooooooooooxxxxoooooooooo'] 
        #* each string char is one map tile. 
        #* 'x' -> already attacked tile, 'o' -> unknown tile.

        
#! Don't edit global variable / constant or Fn
# Attack Function is self.attacking_order(x: int, y: int) -> void
# 'x' or 'y' position must be 0 ~ 450 and also multiple of fifty
# Position value will auto adjustment, if position value over 450 or not multiple of fifty
# Your attacking order's result will be in self.last_attack_result list ([{position: tuple, result: str} ... {position: tuple, result: str}])     
