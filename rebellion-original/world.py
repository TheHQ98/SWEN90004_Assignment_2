from turtle import Turtle
import random
class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.patches = []
        self.cops = []
        self.civies = []
        self.tick = 0
        for x in range(width):
            row = []
            for y in range(height):
                row.append(Patch(x, y))
            self.patches.append(row)

    def update(self):
        # move all non-jailed agents
        for i in (random.shuffle(self.cops + self.civies)):
            # i.move()
        # check all civies to revolt
        for i in self.civies:
            i.checkRevolt()
        # make cops hunt
        for i in self.cops:
            # i.hunt()

        # reduce all jail terms
        for c in self.civies:
            if c.jailterm > 0:
                c.jailterm -= 1
        # renew tick
        self.tick += 1
        pass

class Patch:
    def __init__(self, x, y):
        self.members = []
        self.neighbourTiles = []

    def add_member(self, agent:Turtle):
        self.members.append(agent)



