"""
Class to manage the evolution of Story during the experiment
"""
from sea.engine.model.Dice import Dice
from sea.engine.model.Enemy import Enemy
from sea.engine.model.Item import Item
from sea.engine.story import Story
import math
import time

from googletrans import Translator


class SEAengine:
    def __init__(self):
        # Model
        self.story = None
        self.dungeon = None

        # Init Macros to set enemies and items
        self.init_macros = []

        # Current State
        self.environment = {}

        # Room the participant is facing
        self.current_room = None

        # Last crossroad for the backtracking
        self.previous_cross = None

        # Current passage
        self.current_passage = None

        # Previous passage, if the backtrack is not available
        self.previous_passage = None

        # Game started
        self.is_running = False

        # Game Dice for cycled and random rolls
        self.dice = None

        # Language specs
        self.lang = "ita"

    def start_game(self):
        self.is_running = True
        self.next_room()

    def end_game(self):
        self.is_running = False

    def load_dungeon(self, filename, room_order):
        self.story = Story.parse_raw_twine_file(filename, store_json=True)
        if not self.story.set_order(room_order):
            print("Unable to set room order")
            return False

        self.dungeon = self.story.get_dungeon()
        self.init_macros = self.story.get_init_macros()
        return True

    def init_environment(self, eq_initial=50, eq_low=5, eq_medium=10, eq_high=20, random_seed=False, seed=42, lang="ita"):
        self.environment['hp'] = eq_initial
        self.environment['low'] = eq_low
        self.environment['medium'] = eq_medium
        self.environment['high'] = eq_high

        self.environment['eq_sub_1'] = self.environment['hp'] - 1
        self.environment['eq_sub_1_half'] = math.floor(self.environment['eq_sub_1'] / 2)

        self.environment['power'] = 0
        self.environment['money'] = 0

        self.environment['checkResult'] = False
        self.environment['rollResult'] = False
        self.environment['failRoll'] = False
        self.environment['rollCD'] = 0
        self.environment['enemyDmg'] = 0
        self.environment['enemyDef'] = 0

        self.dice = Dice(20, cycle=True, fixed_seed=seed, random_seed=random_seed)
        self.environment['roll_tmp'] = 0
        self.environment['power_tmp'] = 0
        self.environment['inventory'] = {}
        self.environment['equipment'] = {}
        self.environment['sounds'] = {}
        self.environment['image'] = ""
        self.environment['sound'] = False
        self.environment['playSound'] = False

        self.lang = lang
        self.environment['lang'] = lang
        self.environment['translator'] = Translator()

        # Init items and enemies
        for macro in self.init_macros:
            self.environment = macro.exec(self.environment)

    def get_stats(self):
        return self.get_hp(), self.get_power(), self.get_inventory()

    def get_current_passage_name(self):
        return self.current_passage.name

    def get_current_room_name(self):
        return self.current_room.name

    def go_back(self):
        # If I can go back
        if self.previous_cross is not None:
            self.current_room = self.previous_cross
            self.current_passage = self.current_room.get_backtrack_passage()
            self.previous_cross = None
            return True
        else:
            self.current_passage = self.previous_passage
            return False

    def next_room(self):

        if self.dungeon is None or len(self.dungeon) == 0:
            self.is_running = False
            return False

        self.current_room = self.dungeon.popitem()[1]
        if self.previous_cross is None and self.current_room.is_crossroad():
            self.previous_cross = self.current_room

        self.current_passage = self.current_room.get_start_passage()
        self.current_passage.render(self.environment)

        return True

    def next_passage(self, to_passage):
        self.previous_passage = self.current_passage
        self.current_passage = self.current_room.get_passage(to_passage)
        self.current_passage.render(self.environment)

    def is_alive(self):
        if 'hp' in self.environment.keys():
            return self.environment['hp'] > 0
        return False

    def get_inventory(self):
        return self.environment['inventory']

    def get_hp(self):
        return self.environment['hp']

    def set_hp(self, hp):
        self.environment['hp'] = hp

    def get_power(self):
        return self.environment['power']

    def get_image(self):
        return self.environment['image']

    def get_sound(self):
        if self.environment['playSound']:
            self.environment['playSound'] = False
            return True, self.environment['soundToPlay'], self.environment['playSoundMode']

        return False, None, None

    def set_sound_to_play(self, event):
        if event in self.environment['sounds']:
            self.environment['soundToPlay'] = self.environment['sounds'][event]
            self.environment['playSound'] = True
            self.environment['playSoundMode'] = "once"

    def get_countdown(self):
        return self.environment['countdown_seconds'], self.environment['timeout_passage']

    def get_command(self):
        return self.environment['command']

    def check_have_item(self):
        return self.environment['checkResult']

    def parse_item_effect(self, effect, temporary=True):
        """
        win -> win a fight
        rollback -> rollback the time and go back to the previous decision
        extra_life -> if dead, return to the previous crossroad
        roll +X -> add X to the roll until the end of the fight
        power +X -> add X to the power permanently
        heal X -> restore X EQ
        """

        root = effect.split()
        if root[0] == "roll":
            if temporary:
                self.environment['roll_tmp'] = 0
                self.environment['roll_tmp'] = int(root[1].replace("+", ""))
            else:
                self.environment['roll'] += int(root[1].replace("+", ""))

        elif root[0] == "heal":
            self.environment['hp'] += int(root[1])
        elif root[0] == "power":
            if temporary:
                self.environment['power_tmp'] = 0
                self.environment['power_tmp'] = int(root[1].replace("+", ""))
            else:
                self.environment['power'] += int(root[1].replace("+", ""))
        else:
            self.environment[root[0]] = True

    def check_and_use_special_effects(self, effect):
        if effect in self.environment and self.environment[effect]:
            self.environment[effect] = False

            # drop the coin if used
            if effect == "extra_life":
                self.environment['inventory'].pop('EXTRA LIFE', None)

            # drop the coin if used
            if effect == "win":
                self.environment['inventory'].pop('Guanto del non-infinito', None)

            return True

        return False

    def check_extra_life(self):
        if "EXTRA LIFE" in self.environment['inventory']:
            self.environment["extra_life"] = True

    def use_item_callback(self, item_name):
        item = self.get_item(item_name)
        effect = item.effect
        print(effect)
        if self.environment['inventory'][item_name].is_consumable:

            self.parse_item_effect(effect, temporary=True)
            qta_check = self.environment['inventory'][item_name].use()
            if not qta_check:
                del self.environment['inventory'][item_name]

            return True

        # equip the item
        if item.name not in self.environment['equipment'].keys():
            self.parse_item_effect(effect, temporary=False)
            self.environment['equipment'][item.name] = item

        return False

    def roll_attack_and_check(self):

        if self.environment['failRoll']:
            self.environment['failRoll'] = False
            fail = True
        else:
            fail = False

        dice_roll = self.dice.roll(cd=self.environment['enemyDef'], fail=fail)
        attack = dice_roll
        if not fail:
            attack += self.environment['power']
            attack += self.environment['power_tmp']
            self.environment['power_tmp'] = 0
        return attack >= self.environment['enemyDef'], dice_roll, attack

    def roll_dice_and_check(self):

        if self.environment['failRoll']:
            self.environment['failRoll'] = False
            fail = True
        else:
            fail = False

        print(self.environment['rollCD'])

        dice_roll = self.dice.roll(cd=self.environment['rollCD'], fail=fail)
        res = dice_roll
        res += self.environment['roll_tmp']
        self.environment['roll_tmp'] = 0
        return res >= self.environment['rollCD'], dice_roll, res

    def roll_random(self):
        return self.dice.roll_random()

    def get_item(self, name):
        return self.environment['items'][name]

    def get_passage(self, passage_name, render=False):

        passage = self.story.get_passage(passage_name)
        if render:
            passage.render(self.environment)
            return passage

        return passage
