import random
from math import exp, floor
from .constant import *



class Turtle:
    def __init__(self, x, y, role=CIVI):
        self.x = x
        self.y = y
        self.risk_aversion = random.random()
        self.percieved_hardship = random.random()
        self.active = False
        self.jailterm = 0
        self.role = role

    def moveRandom(self, movement):
        """
        randomly pick an available move
        :return:
        """
        if self.jailterm > 0 or (not movement and self.role==CIVI):
            return

        pass

    def checkRevolt(self, neighbour_cop: int, neighbour_civi: int) -> None:
        """
        Pass in number of cops, number of civilian from the surrounding, then check if agent should
        revolve the civilian
        :param neibour_cop: number of cop in neighbourhood
        :param neighbour_civi: number of active civilian from neighbourhood
        :return:
        """
        if self.role == COP or self.jailterm > 0:
            return
        # TODO: global variables not linked(government_legitimacy, k, threshold)
        grievance = self.percieved_hardship * (1 - government_legitimacy)
        estimated_arrest_prob = 1 - exp(-k * floor(neighbour_cop / neighbour_civi + 1))
        self.active = (grievance - self.risk_aversion * estimated_arrest_prob) > threshold