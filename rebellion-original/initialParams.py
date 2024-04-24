# initial params
# @Author Josh Feng
# @Date 22 April 2024

# changeable params
INITIAL_COP_DENSITY = 4
INITIAL_AGENT_DENSITY = 70
VISION_PATCHES = 3

# fixed params
TILE_HEIGHT = 10
TILE_WIDTH = 10

K = 2.3
THRESHOLD = 0.1

def board():
    return TILE_HEIGHT * TILE_WIDTH

MAX_VISION = 10