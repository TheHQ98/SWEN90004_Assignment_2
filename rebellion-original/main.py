from world import World
from initialParams import *


def main():
    print("program Started")
    world = World(agent_density=INITIAL_AGENT_DENSITY, cop_density=INITIAL_COP_DENSITY, vision=VISION_PATCHES)
    tick = 0

    with open('output.csv', 'w+') as fp:
        fp.write('tick,quiet,jailed,active\n')
        for i in range(1000):
            print("Tick " + str(tick))
            s = world.update()
            fp.write(f"{s}\n")
            tick += 1

    print("program Ended")


if __name__ == '__main__':
    main()
