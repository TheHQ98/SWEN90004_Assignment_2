import random
import dynamicParams, initialParams
from math import exp, floor
from .world import Patch
from .constant import *


class Turtle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def canMove(self) -> bool:
        return True

    def move(self, patches: list[Patch]) -> (int, int):
        if not self.canMove():
            return self.x, self.y

        tempPatches = []
        for patch in patches:
            if patch.is_free():
                tempPatches.append(patch)

        nextMove = random.choice(tempPatches)

        return nextMove.x, nextMove.y

    def get_active(self):
        pass


class Cop(Turtle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.movement = True  # Cop movement always true

    def enforce(self, turtle: list[Turtle]) -> (int, int):
        agentActive = []
        for i in turtle:
            if type(i) is Agent:
                if i.get_active():
                    agentActive.append(i)

        if agentActive:
            tempAgent = random.choice(agentActive)
            self.x = tempAgent.x
            self.y = tempAgent.y
            tempAgent.jail_term = dynamicParams.MAX_JAIL_TERM

        return self.x, self.y


class Agent(Turtle):
    active: bool

    def __init__(self, x, y, movement):
        super().__init__(x, y)
        self.jail_term = 0
        self.risk_aversion = random.random()
        self.perceived_hardship = random.random()
        self.active = False
        self.movement = movement  # get movement bool from dynamicParams

    def canMove(self) -> bool:
        if self.movement and self.jail_term == 0:
            return True
        else:
            return False

    def decrease_jail_term(self):
        if self.jail_term > 0:
            self.jail_term -= 1

    # def estimated_arrest_probability(self, cop_cnt, active_cnt):
    #     c = cop_cnt
    #     a = 1 + active_cnt
    #
    #     return 1 - exp(-initialParams.K * floor(c / a))

    def get_active(self):
        return self.active

    def is_active(self, c, a):
        grievance = self.perceived_hardship * (1 - dynamicParams.GOVERNMENT_LEGITIMACY)
        self.active = \
            (grievance - self.risk_aversion * 1 - exp(-initialParams.K * floor(c / a + 1))) > initialParams.THRESHOLD
