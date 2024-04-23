from .turtle import Cop, Agent, Turtle
import random
from .constant import *


class World:
    def __init__(self, width, height, cop_density, agent_density, vision):
        self.verify_parameters(width, height, cop_density, agent_density, vision)
        self.width: int = width
        self.height: int = height
        self.patches: list[list[Patch]] = []
        self.cops: list[Cop] = []
        self.agents: list[Agent] = []
        self.tick: int = 0
        self.movement: bool = True
        self.vision = vision
        self.initialize_patches(vision)
        self.initialise_turtles(cop_density, agent_density)

    def verify_parameters(self, width, height, cop_density, agent_density, vision):
        """
        Verifies that the parameters are valid
        """
        if width > MAX_WIDTH or height > MAX_HEIGHT or width <= 0 or height <= 0:
            raise Exception("Invalid parameters: World dimension invalid")
        if cop_density + agent_density > 100:
            raise Exception("Invalid parameters: cop + agents exceeds capacity of world")
        if vision > MAX_VISION or vision < 0:
            raise Exception("Invalid parameters: Vision exceeds the world")

    def initialize_patches(self, vision):
        """
        create patch as container & store its neighbour reference, top left as (0, 0)
        """
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Patch(x, y))
            self.patches.append(row)
        # TODO: initialize each patch with its neighbouring patch reference

    def initialise_turtles(self, cop_density, agent_density):
        patch_cnt = self.height * self.width
        cop_cnt = round(cop_density * 0.01 * patch_cnt)
        agent_cnt = round(agent_density * 0.01 * patch_cnt)
        loc_map = [(x, y) for x in range(self.width) for y in range(self.height)]
        random.shuffle(loc_map)
        for i in range(cop_cnt):
            x, y = loc_map.pop()
            self.patches[x][y].add_member(Cop(x, y))
        for i in range(agent_cnt):
            x, y = loc_map.pop()
            self.patches[x][y].add_member(Agent(x, y))

    def update(self):
        # move all non-jailed turtles
        for i in (random.shuffle(self.cops + self.agents)):
            self.patches[i.x][i.y].remove_member(i)
            next_x, next_y = i.moveRandom(self.movement) # expects turtles to set its own coordinate within moveRandom
            self.patches[next_x][next_y].add_member(i)

        # check all agents to revolt, O(civ * n_size * avg_turtlePerPatch)
        for agent in self.agents:
            neighbour_turtles = self.patches[agent.x][agent.y].get_neighbour_turtles()
            cop_cnt, active_cnt = 0, 0
            for i in neighbour_turtles:
                if type(i) is Cop:
                    cop_cnt += 1
                elif i.active:
                    active_cnt += 1
                # if i.role == COP:
                #     cop_cnt += 1
                # elif i.active:
                #     active_cnt += 1
            agent.checkRevolt(cop_cnt, active_cnt)
        # make cops hunt
        for cop in self.cops:
            # neighbour_turtles = self.patches[civ.x][civ.y].get_neighbour_turtles()
            self.patches[cop.x][cop.y].remove_member(cop)
            # next_x, next_y = cop.hunt(neighbour_turtles)
            # self.patches[next_x][next_y].add_member(cop)

        # reduce all jail terms
        for c in self.agents:
            if c.jail_term > 0:
                c.jail_term -= 1
        # renew tick
        self.tick += 1


class Patch:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.members = []
        self.neighbourPatches = []
        # TODO: Optionally optimise by caching neighbour cop & agent/active count, updated on local change

    def add_member(self, agent: Turtle):
        self.members.append(agent)

    def remove_member(self, agent: Turtle):
        self.members.remove(agent)

    def get_neighbour_turtles(self):
        """
        return all the neighbour turtles
        """
        ans = []
        for p in self.neighbourPatches:
            ans.extend(p.members)
        return ans
