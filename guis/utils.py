from guis import colors
import pygame as pg
from random import randrange as rrange
from utils.mathmethods import posToLoc


detections_colors = {
        0: colors.BLACK,
        1: colors.LIGHT_BLUE,
        2: colors.LIGHT_PINK,
        3: colors.LIGHT_GREEN
    }


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



def render(surface, object):
    """BLITING OBJECT SPRITES INTO CURRENT SURFACE"""
    for pixel in object.draw():
        pg.draw.rect(surface, pixel[0], pixel[1])


def renderPixels(surface, pixels_poss, pixel_types, pixel_size):
    for i, pixel_pos in enumerate(pixels_poss):
        current_type = pixel_types[i]
        pixel_color = detections_colors.get(current_type)
        pixel_loc = posToLoc(pixel_pos, pixel_size)
        pixel = (pixel_loc[0], pixel_loc[1], pixel_size, pixel_size)
        pg.draw.rect(surface, pixel_color, pixel)
