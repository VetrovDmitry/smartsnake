from math import pi, sin, cos
import numpy as np


def angleToDirection(angle):
    dir_x = int(cos(angle).real)
    dir_y = int(sin(angle).real)
    return (dir_x, dir_y)


def posToLoc(pos, pixel_size):
    x = pos[0] * pixel_size
    y = pos[1] * pixel_size
    return (x, y)


def radToDegrees(rads):
    degrees = 180 * rads / pi
    return degrees


def sig(x):
    sig_x = 1 / (1 + np.exp(-x))
    return sig_x


def sig_der(x):
    return x * (1 - x)


def local_mean_squared_error(error):
    return error ** 2


def stabilitron(x):
    if x >= 0.85:
        y = 1
    else:
        y = 0
    return y