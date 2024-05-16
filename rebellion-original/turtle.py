"""
turtle-class
contain a super class called Turtle
two subclasses called Cop and Agent

@author: Josh Feng   - 1266669
@Date: 24 April 2024
"""

import random
from math import exp, floor
from dynamicParams import *
from initialParams import *


class Turtle:
    """
    simulates a turtle object, which the behaviours are shared by both cop and turtle.
    """
    def __init__(self, x, y):
        """initial location"""
        self.x = x
        self.y = y

    def canMove(self) -> bool:
        """return move value"""
        return True

    def move(self, patches) -> (int, int):
        """
        move logic
        1. if not allowed move then return self locations
        2. get neighbour patches and random select one free location
        3. if there is not more free location then return self locations
        """

        if not self.canMove():
            return self.x, self.y

        # get neighbour patches and random select one free location
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
        """return active value"""
        pass


class Cop(Turtle):
    """
    cop class which contain Turtle surer class
    simulates cop behaviour
    """
    def __init__(self, x, y):
        """initial the cop"""
        super().__init__(x, y)
        self.movement = True  # Cop movement always true

    def enforce(self, turtle: list[Turtle]) -> (int, int):
        """
        find and arrest the agent that is active in the neighbours
        """

        # get all the active agent in the neighbours
        agentActive = []
        for i in turtle:
            if isinstance(i, Agent):
                if i.get_active():
                    agentActive.append(i)

        # not move if not contain active agent
        if len(agentActive) == 0:
            return self.x, self.y

        # random select and move to the active agent
        tempAgent = random.choice(agentActive)
        self.x = tempAgent.x
        self.y = tempAgent.y
        tempAgent.active = False
        tempAgent.jail_term = random.randint(0, MAX_JAIL_TERM)

        return self.x, self.y


class Agent(Turtle):
    """
    simulate agent behaviour
    """
    def __init__(self, x, y, movement):
        """initial the agent"""
        super().__init__(x, y)
        self.jail_term = 0
        self.risk_aversion = random.uniform(0, 1)
        self.perceived_hardship = random.uniform(0, 1)
        self.active: bool = False
        self.movement = movement  # get movement bool from dynamicParams

    def canMove(self) -> bool:
        """return self move value"""
        if self.movement and self.jail_term == 0:
            return True
        else:
            return False

    def decrease_jail_term(self):
        """decrease the jail term by 1 for each tick"""
        if self.jail_term > 0:
            self.jail_term -= 1

    def get_active(self):
        """return active value"""
        return self.active

    def is_active(self, c, a):
        """
        check if agent is active
        """

        if self.jail_term > 0:
            return False

        grievance = self.perceived_hardship * (1 - GOVERNMENT_LEGITIMACY)
        estimatedArrestProbability = 1 - exp(-K * floor(c / a))
        self.active = (grievance - self.risk_aversion * estimatedArrestProbability) > THRESHOLD
