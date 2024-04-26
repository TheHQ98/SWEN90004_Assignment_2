import random
from math import exp, floor
from dynamicParams import *
from initialParams import *
# from .world import Patch


class Turtle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def canMove(self) -> bool:
        return True

    def move(self, patches) -> (int, int):
        if not self.canMove():
            return self.x, self.y

        tempPatches = []
        for patch in patches:
            if patch.is_free():
                tempPatches.append(patch)
        if tempPatches:
            nextMove = random.choice(tempPatches)
        else:
            return self.x, self.y

        self.x, self.y = nextMove.x, nextMove.y
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
            tempAgent.active = False
            tempAgent.jail_term = random.randint(0, MAX_JAIL_TERM)
            # tempAgent.jail_term = MAX_JAIL_TERM

        return self.x, self.y


class Agent(Turtle):

    def __init__(self, x, y, movement):
        super().__init__(x, y)
        self.jail_term = 0
        self.risk_aversion = random.random()
        self.perceived_hardship = random.random()
        self.active: bool = False
        self.movement = movement  # get movement bool from dynamicParams

    def canMove(self) -> bool:
        if self.movement and self.jail_term == 0:
            return True
        else:
            return False

    def decrease_jail_term(self):
        if self.jail_term > 0:
            self.jail_term -= 1

    def get_active(self):
        return self.active

    def is_active(self, c, a):
        grievance = self.perceived_hardship * (1 - GOVERNMENT_LEGITIMACY)
        self.active = (grievance - self.risk_aversion * (1 - exp(-K * floor(c / (a + 1))))) > THRESHOLD
