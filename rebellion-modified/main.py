"""
the modified rebellion model
the agent have two different attribute, left or right
different attribute will affect risk_aversion and perceived_hardship values

simplify run the program by using main class
the program will run for 200 ticks, and will produce an output csv file in the same directory
csv file values contains:
    tick, quiet, jailed, active

Changeable parameters are in initialParams.py and dynamicParams.y
initialParams.py is for static parameters include:
    INITIAL_COP_DENSITY
    INITIAL_AGENT_DENSITY
    VISION_PATCHES
    LEFT_RIGHT_RATIO
dynamicParams.py is for dynamic parameters include:
    GOVERNMENT_LEGITIMACY
    MAX_JAIL_TERM
    MOVEMENT

@author: Josh Feng   - 1266669
        Justin Zhang - 1153289
        Yixing Bai - 1506220
@Date: 24 April 2024
"""

from world import World
from initialParams import *


def main():
    print("program Started")

    # get initial params
    world = World(agent_density=INITIAL_AGENT_DENSITY, cop_density=INITIAL_COP_DENSITY, vision=VISION_PATCHES)
    tick = 0

    with open(FILE_ADDRESS, 'w+') as fp:
        fp.write('tick,quiet,jailed,active\n')
        for i in range(MAX_TICK):
            print("Tick " + str(tick))
            s = world.update()
            fp.write(f"{s}\n")
            tick += 1

    print("program Ended")


if __name__ == '__main__':
    main()
