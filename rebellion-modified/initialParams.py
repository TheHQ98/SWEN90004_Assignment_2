"""
initial params

@author: Josh Feng   - 1266669
        Justin Zhang - 1153289
@Date: 24 April 2024
"""

# changeable params
INITIAL_COP_DENSITY = 4  # percentage
INITIAL_AGENT_DENSITY = 70  # percentage
VISION_PATCHES = 7.0
LEFT_RIGHT_RATIO = 0.5

# fixed params (do not change)
TILE_HEIGHT = 40
TILE_WIDTH = 40
K = 2.3
THRESHOLD = 0.1
MAX_VISION = 10

MAX_TICK = 200

FILE_ADDRESS = "output.csv"
NUM_COP = "C"
NUM_JAILED = "J"
NUM_ACTIVE = "A"
NUM_QUIET = "Q"
LEFT = 0
RIGHT = 1
