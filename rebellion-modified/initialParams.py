"""
initial params

@author: Josh Feng   - 1266669
        Justin Zhang - 1153289
@Date: 24 April 2024
"""

# changeable params
INITIAL_COP_DENSITY = 4
INITIAL_AGENT_DENSITY = 70
VISION_PATCHES = 7
LEFT_RIGHT_RATIO = 0.34

# fixed params (do not change)
TILE_HEIGHT = 40
TILE_WIDTH = 40
K = 2.3
THRESHOLD = 0.1
MAX_VISION = 10

MAX_TICK = 1000

FILE_ADDRESS = "../VisualGraph/output.csv"  # TODO REMOVE THIS LINE BEFORE SUBMIT
#FILE_ADDRESS = "output.csv"    TODO uncomment this line BEFORE SUBMIT
NUM_COP = "C"
NUM_JAILED = "J"
NUM_ACTIVE = "A"
NUM_QUIET = "Q"
LEFT = 0
RIGHT = 1
