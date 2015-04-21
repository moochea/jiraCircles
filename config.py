#!/usr/bin/env python
import math


#############################
# Configuration file
######################################

#colours

WHITE = (1.0, 1.0, 1.0), # white
GREEN = (0.5, 0.8, 0.5), # green
CYAN = (0.5, 0.8, 0.8), # cyan
RED = (0.5, 0.2, 0.2), # red
YELLOW = (0.8, 0.8, 0.5), # yellow
BLACK = (0.0, 0.0, 0.0) # black
GREY = (0.5, 0.5, 0.5), # grey
PURPLE = (0.2, 0.2, 0.6) #purple
BLUE = (0.2, 0.2, 0.5)



# Size of the OpenGL portion of the window
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 400

# Starting position of the entire window
WINDOW_X, WINDOW_Y = 300, 300

# Window background colour
#BGCOLOUR = WHITE

# FONT size of displayed text

FONT_SIZE_KEY = 12
FONT_COLOUR_KEY =PURPLE 

FONT_SIZE_TITLE = 15
FONT_COLOUR_TITLE = BLACK

FONT_SIZE_SUMMARY = 12
FONT_COLOUR_SUMMARY = BLUE

FONT_TYPE="Impact"
FONT_WRAP_TITLE=15
FONT_WRAP_SUMMARY=100
FONT_PAD=5
INTER_PAD = 2 # This pads in between wrapped lines

# curve or line?
#DEPENDENCY_LINK = "line"
#DEPENDENCY_LINK = "fancy"
DEPENDENCY_LINK = "curve"

# Story circle scale
SCALE=30
# Mapping story states 

story_states = {
        0: "Open",
        1: "Started",
        2: "Awaiting Verification",
        3: "Complete",
        4: "Blocked",
        5: "At Risk",
        6: "Rejected"
        }


# Colour scheme: What state relates to what colour
colour = {
        0: BLACK,
        1: GREEN,
        2: GREEN,
        3: GREEN,
        4: RED,
        5: YELLOW,
        6: GREY,
        }



# Map state to automatic progress setting

state_progress = {
        "Open": 0,
        "Awaiting Verification": 75,
        "Complete": 100,
        "Rejected": 100,
        }


# Constants
twopi = 2*math.pi

