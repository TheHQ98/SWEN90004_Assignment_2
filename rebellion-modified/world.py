"""
world-class
Contains the World class for controlling simulation flow & Patches as grid representations

@author: Justin Zhang - 1153289
@Date: 24 April 2024
"""

# from turtle import Cop, Agent, Turtle
import random
from dynamicParams import *
from initialParams import *
from turtles import Turtle, Cop, Agent


class World:
    def __init__(self, cop_density, agent_density, vision):
        self.verify_parameters(cop_density, agent_density, vision)
        self.width: int = TILE_WIDTH
        self.height: int = TILE_HEIGHT
        self.patches: list[list[Patch]] = []
        self.cops: list[Cop] = []
        self.agents: list[Agent] = []
        self.tick: int = -1
        self.movement: bool = True
        self.vision = vision
        self.initialize_patches()
        self.initialise_turtles(cop_density, agent_density)

    def verify_parameters(self, cop_density, agent_density, vision):
        """
        Verifies that the parameters are valid
        """
        if cop_density + agent_density > 100:
            raise Exception("Invalid parameters: cop + agents exceeds capacity of world")
        if vision > MAX_VISION or vision < 0:
            raise Exception("Invalid parameters: Vision exceeds the world")

    def initialize_patches(self):
        """
        create patch as container & store its neighbour reference, top left as (0, 0)
        """
        for x in range(self.width):
            row = []
            for y in range(self.height):
                row.append(Patch(x, y))
            self.patches.append(row)
        for y in range(self.height):
            for x in range(self.width):
                neighbour_coord = self.patches[x][y].get_neighbour_coords(self.vision, mode="rect")
                tmp_neighbours = [self.patches[a][b] for a, b in neighbour_coord]
                self.patches[x][y].neighbour_patches = tmp_neighbours

    def initialise_turtles(self, cop_density, agent_density):
        """
        instantiate turtle objects
        """
        patch_cnt = self.height * self.width
        cop_cnt = round(cop_density * 0.01 * patch_cnt)
        agent_cnt = round(agent_density * 0.01 * patch_cnt)
        left_cnt = agent_cnt * LEFT_RIGHT_RATIO
        loc_map = [(x, y) for x in range(self.width) for y in range(self.height)]
        random.shuffle(loc_map)
        for i in range(cop_cnt):
            x, y = loc_map.pop()
            cop = Cop(x, y)
            self.patches[x][y].add_member(cop)
            self.cops.append(cop)
        for i in range(agent_cnt):
            x, y = loc_map.pop()
            if (i < left_cnt):
                agent = Agent(x, y, MOVEMENT, LEFT)
                self.patches[x][y].add_member(agent)
                self.agents.append(agent)
            else:
                agent = Agent(x, y, MOVEMENT, RIGHT)
                self.patches[x][y].add_member(agent)
                self.agents.append(agent)
            # agent = Agent(x, y, MOVEMENT, )


    def update(self):
        """
        run update cycle of a tick
        """
        # move all non-jailed turtles
        turt = self.cops + self.agents

        self.rule_M(turt)
        self.rule_A()
        self.rule_C()

        # reduce all jail terms
        for c in self.agents:
            c.decrease_jail_term()
        # renew tick
        self.tick += 1

        jail_cnt, active_cnt, quiet_cnt = self.get_stats()
        return f"{self.tick},{quiet_cnt},{jail_cnt},{active_cnt}"

    def rule_M(self, turt):
        """
        rule M(ove), move each turtle randomly
        """
        for i in turt:
            self.patches[i.x][i.y].remove_member(i)
            neighbours = self.patches[i.x][i.y].neighbour_patches
            next_x, next_y = i.move(neighbours)
            self.patches[next_x][next_y].add_member(i)

    def rule_A(self):
        """
        rule A(gent), determine if agent should be active or not
        """
        for agent in self.agents:
            neighbour_turtles = self.patches[agent.x][agent.y].get_neighbour_turtles()
            cop_cnt, active_cnt = 0, 0
            for i in neighbour_turtles:
                if isinstance(i, Cop):
                    cop_cnt += 1
                if isinstance(i, Agent):
                    if i.active:
                        active_cnt += 1

            agent.is_active(cop_cnt, active_cnt+1)

    def rule_C(self):
        """
        role C(op), cops out arresting people
        """
        for cop in self.cops:
            neighbour_turtles = self.patches[cop.x][cop.y].get_neighbour_turtles()
            self.patches[cop.x][cop.y].remove_member(cop)
            next_x, next_y = cop.enforce(neighbour_turtles)
            self.patches[next_x][next_y].add_member(cop)

    def get_stats(self):
        """
        extract stats from patches: Jail, Active, Quiet
        """
        jail_cnt, active_cnt, quiet_cnt = 0, 0, 0
        for i in self.agents:
            if i.jail_term > 0:
                jail_cnt += 1
            elif i.active:
                active_cnt += 1
            else:
                quiet_cnt += 1
        return jail_cnt, active_cnt, quiet_cnt

    def print_patches(self):
        """
        Debug method for printing patches
        """
        for x in range(self.width):
            for y in range(self.height):
                print(f"({x:02},{y:02}) | {self.patches[x][y].get_string()}")
        print(f"{self.tick}-----------------------------------------------")



class Patch:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.members: list[Turtle] = []
        self.neighbour_patches: list[Patch] = []
        # TODO: Optionally optimise by caching neighbour cop & agent/active count, updated on local change

    def add_member(self, agent: Turtle):
        """
        adds a new turtle to this patch
        """
        self.members.append(agent)

    def remove_member(self, agent: Turtle):
        """
        removes a turtle from this patch
        """
        self.members.remove(agent)

    def get_neighbour_turtles(self):
        """
        return all the neighbour turtles
        """
        ans = []
        for p in self.neighbour_patches:
            ans.extend(p.members)
        return ans

    def get_neighbour_coords(self, r: float, mode="Manhattan") -> list[(int, int)]:
        """
        Given vision range r, return all the coords that count as neighbour
        """
        radius = round(r)
        ans = []
        if mode == "Manhattan":
            for dx in range(-radius, radius + 1):  # Range from -r to r
                for dy in range(-radius, radius + 1):  # Range from -r to r
                    if abs(dx) + abs(dy) <= radius:  # Manhattan distance check
                        x = (self.x + dx) % TILE_WIDTH
                        y = (self.y + dy) % TILE_HEIGHT
                        if (x, y) != (self.x, self.y):  # Optionally exclude the center point
                            ans.append((x, y))
        else:
            x_range, y_range = range(self.x - radius, self.x + radius), range(self.y - radius, self.y + radius)
            ans = [(x % TILE_WIDTH, y % TILE_HEIGHT) for y in y_range for x in x_range]
        # ans.remove((t.x, t.y)) # activate to remove self
        return ans

    def is_free(self) -> bool:
        """
        return true if no agent on current tile, v.v.
        """
        if not self.members:
            return True
        for i in self.members:
            if type(i) is Cop or (type(i) is Agent and i.jail_term == 0):
                return False
        return True

    def get_string(self):
        """
        return string representation of patch
        """
        output = ""
        for i in self.members:
            if type(i) is Cop:
                output += NUM_COP
            elif i.jail_term > 0:
                output += NUM_JAILED
            elif i.active:
                output += NUM_ACTIVE
            else:
                output += NUM_QUIET
        return output
