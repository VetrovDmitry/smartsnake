import time
from cmath import sin


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREY = (180, 180, 180)
GREY = (90, 90, 90)
DARK_GREY = (40, 40, 40)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
GREEN = (50, 205, 50)
YELLOW = (255, 215, 0)
LIGHT_BLUE = (64, 224, 208)
LIGHT_PINK = (238, 130, 238)
DARK_LOSOS = (233, 150, 122)
DARK_BLUE = (72, 61, 99)
BROWN = (192, 113, 11)
NICE_GREEN = (176, 255, 200)
NICE_LIGHT = (241, 226, 252)
NICE_NORMAL = (211, 116, 246)
NICE_DARK = (190, 64, 236)
JUICY_GREEN = (39, 236, 85)
DARK_BROWN = (67, 39, 32)
DARK_GREEN = (9, 127, 68)
LIGHT_GREEN = (0, 242, 121)
VERY_LIGHT_GREEN = (189, 255, 223)
VERY_LIGHT_GREEN_1 = (170, 240, 190)
VERY_LIGHT_GREEN_2 = (166, 225, 174)

def RAINBOW_1():
    fi_r = 2
    k_r = 0.2
    r_channel = abs(sin(time.time() * k_r + fi_r).real) * 255
    fi_g = 0
    k_g = 0.2
    g_channel = abs(sin(time.time() * k_g + fi_g).real) * 180
    fi_b = 8
    k_b = 0.2
    b_channel = abs(sin(time.time() * k_b + fi_b).real) * 255
    return (r_channel, g_channel, b_channel)


