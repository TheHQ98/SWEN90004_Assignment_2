"""
main class

@author: Josh Feng   - 1266669
        Justin Zhang - 1153289
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
