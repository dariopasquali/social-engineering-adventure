import random
from random import seed
import time


class Dice:
    def __init__(self, size, cycle=False, fixed_seed=42, random_seed=False):
        self.size = size
        self.cycle = cycle
        self.cycle_counter = 0

        if random_seed:
            seed(time.time())
        else:
            seed(fixed_seed)

    def roll(self, cd=0, fail=False):
        if not self.cycle:
            return random.randint(1, self.size)

        chance = random.randint(0, 99)
        roll_result = random.randint(1, self.size)

        if fail:
            roll_result = random.randint(1, cd)
        else:
            if self.cycle_counter == 0:     # random probability to win
                roll_result = random.randint(1, self.size)
            elif self.cycle_counter == 1:   # 50% probability to win
                if chance < 50:
                    roll_result = random.randint(cd, self.size)
                else:
                    roll_result = random.randint(1, cd)
            else:                           # 100% probability to win
                roll_result = random.randint(cd, self.size)

        self.cycle_counter += 1
        if self.cycle_counter > 3:
            self.cycle_counter = 0

        return roll_result

    def roll_random(self):
        return random.randint(1, self.size)

