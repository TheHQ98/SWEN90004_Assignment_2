# initial params
# @Author Josh Feng
# @Date 22 April 2024

# changeable params
INITIAL_COP_DENSITY = float(0.04)
INITIAL_AGENT_DENSITY = float(0.7)
VISION_PATCHES = 7

# fixed params
TILE_HEIGHT = 40
TILE_WIDTH = 40

K = 2.3
THRESHOLD = 0.1

def board():
    return TILE_HEIGHT * TILE_WIDTH

