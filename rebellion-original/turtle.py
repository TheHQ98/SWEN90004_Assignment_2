import random
import dynamicParams, initialParams
from math import exp, floor
from .constant import *


class Turtle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def canMove(self) -> bool:
        return True

    def move(self) -> None:
        if not self.canMove():
            return

    # def checkRevolt(self, neighbour_cop: int, neighbour_civi: int) -> None:
    #     """
    #     Pass in number of cops, number of civilian from the surrounding, then check if agent should
    #     revolve the civilian
    #     :param neibour_cop: number of cop in neighbourhood
    #     :param neighbour_civi: number of active civilian from neighbourhood
    #     :return:
    #     """
    #     if self.role == COP or self.jailterm > 0:
    #         return
    #     # TODO: global variables not linked(government_legitimacy, k, threshold)
    #     grievance = self.percieved_hardship * (1 - government_legitimacy)
    #     estimated_arrest_prob = 1 - exp(-k * floor(neighbour_cop / neighbour_civi + 1))
    #     self.active = (grievance - self.risk_aversion * estimated_arrest_prob) > threshold


class Cop(Turtle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.movement = True # Cop movement always true

    def run(self):
        self.move()
        self.enforce()

    def enforce(self):
        agentActive = []
        for i in neighbour:
            if i.active:
                agentActive.append(i)

        tempAgent = random.choice(agentActive)
        self.x = tempAgent.x
        self.y = tempAgent.y
        tempAgent.jail_term = dynamicParams.MAX_JAIL_TERM

        pass


class Agent(Turtle):
    active: bool

    def __init__(self, x, y, movement):
        super().__init__(x, y)
        self.jail_term = 0
        self.risk_aversion = random.random()
        self.perceived_hardship = random.random()
        self.active = False
        self.movement = movement  # get movement bool from dynamicParams

    def run(self):
        self.move()
        self.is_active()

    def canMove(self) -> bool:
        if self.movement and self.jail_term == 0:
            return True
        else:
            return False

    def decrease_jail_term(self):
        if self.jail_term > 0:
            self.jail_term -= 1

    def estimated_arrest_probability(self):
        c = len(neighbour_cop)  #TODO
        a = 1 + len(neighbour_agent.active is true)  #TODO

        return 1 - exp(-initialParams.K * floor(c / a + 1))

    def is_active(self):
        grievance = self.perceived_hardship * (1 - dynamicParams.GOVERNMENT_LEGITIMACY)
        self.active = (grievance - self.risk_aversion * self.estimated_arrest_probability()) > initialParams.THRESHOLD
