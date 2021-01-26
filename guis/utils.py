from guis import colors
import pygame as pg
from random import randrange as rrange

def DrawGrid(surface, block_size, color=colors.WHITE, grid_size=4):
    """DRAW GRID!"""
    grid_color = color
    x = -block_size
    y = -block_size
    surface_size = surface.get_size()

    for x_row in range(surface_size[0] // block_size + 1):
        x += block_size
        pg.draw.line(surface, grid_color, (x, 0), (x, surface_size[1]), grid_size)
    for y_row in range(surface_size[1] // block_size + 2):
        y += block_size
        pg.draw.line(surface, grid_color, (0, y), (surface_size[0], y), grid_size)


def RandomColors(count):
    colors = list()
    for c in range(count):
        R = rrange(0, 255)
        G = rrange(0, 255)
        B = rrange(0, 255)
        color = (R, G, B)
        colors.append(color)
    return colors


def render(surface, object):
    """BLITING ALL SPRITES TO CURRENT SURFACE"""
    for pixel in object.draw():
        pg.draw.rect(surface, pixel[0], pixel[1])
