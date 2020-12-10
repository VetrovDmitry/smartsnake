import random
import numpy as np
import json
import pygame as pg
import colors


CONFIG_PATH = 'C:/Users/79999/pproject/SMARTSNAKE/PARAMS.json'
MODES = {
    'nothing': 0,
    'barrier': 1,
    'food': 2,
    'snake': 3
}

DETECTIONS_COLORS = {
        0: colors.DARK_GREEN,
        1: colors.VERY_LIGHT_GREEN,
        2: colors.LIGHT_BLUE,
        3: colors.LIGHT_PINK
    }

def posToLoc(pos, pixel_size):
    x = pos[0] * pixel_size
    y = pos[1] * pixel_size
    return (x, y)

def getParams(module_name):
    with open(CONFIG_PATH, 'r') as file:
        txt = file.read()
        text = json.loads(txt)
        params = text.get(module_name)
    return params

def render(surface, object):
    """BLITING ALL SPRITES TO CURRENT SURFACE"""
    for pixel in object.draw():
        pg.draw.rect(surface, pixel[0], pixel[1])

def renderPixels(surface, pixels_poss, pixel_types, pixel_size):
    for i, pixel_pos in enumerate(pixels_poss):
        current_type = pixel_types[i]
        pixel_color = DETECTIONS_COLORS.get(current_type)
        pixel_loc = posToLoc(pixel_pos, pixel_size)
        pixel = (pixel_loc[0], pixel_loc[1], pixel_size, pixel_size)


        pg.draw.rect(surface, pixel_color, pixel)

def randomXY(range, step=1):
    """GENERATOR FOR RANDOM PAIR"""
    x = random.randrange(0, range[0], step)
    y = random.randrange(0, range[1], step)
    return(x, y)

def smart_coors(range, step, all_positions):
    """GENERATOR FOR RANDOM PAIR(x, y) FOR VACANT RANGE"""
    gen = True
    coors = tuple()
    while gen:
        xy = randomXY(range, step)
        if xy not in all_positions:
            coors = xy
            gen = False
    return coors

def smart_pos_for_area(area_border, all_positions):
    search = True
    positions = list()
    area_x_1 = area_border[0][0]
    area_x_2 = area_border[0][1]
    area_y_1 = area_border[1][0]
    area_y_2 = area_border[1][1]
    dx = area_x_2 - area_x_1
    dy = area_y_2 - area_y_1
    while search:
        random_x = random.randrange(0, dx)
        random_y = random.randrange(0, dy)
        random_x += area_x_1
        random_y += area_y_1
        if (random_x, random_y) not in all_positions:
            new_pos = (random_x, random_y)
            search = False
            return new_pos
        else:
            pass

    return positions


class AllSprites:
    def __init__(self):
        self.sprites = list()

    def getAllPositions(self):
        poss = list()
        sprites = self.sprites
        for sprite in sprites:
            for pos in sprite.getAllPos():
                poss.append(pos)

        return poss

    def append(self, new_sprite):
        self.sprites.append(new_sprite)

    def getSprites(self):
        return self.sprites

    def freezeAll(self):
        for sprite in self.sprites:
            sprite.freeze()


    def unfreezeAll(self):
        for sprite in self.sprites:
            sprite.unfreeze()


    def update(self):
        for sprite in self.sprites:
            sprite.update()

    def draw(self, surface):
        for sprite in self.sprites:
            render(surface, sprite)

    def getLen(self):
        lengh = len(self.sprites)
        return lengh

    def showTypes(self):
        sprites = self.sprites
        for sprite in sprites:
            for block in sprite.blocks:

                print(block.type)

        print('---------')

    def print_to_matrix(self, M):
        pixels_positions = list()
        sprites = self.sprites
        for sprite in sprites:
            for block in sprite.blocks:
                block_color = block.color
                block_type = block.type
                block_int = MODES.get(block_type)
                block_ppos = block.position
                b_pp_n = block_ppos[1]
                b_pp_m = block_ppos[0]

                if (b_pp_m, b_pp_n) not in pixels_positions:
                    pixels_positions.append((b_pp_m, b_pp_n))
                    M.matrix[b_pp_n][b_pp_m] = block_int
                else:
                    pass

        return M

    def getSpriteByPos(self, pos):
        sprites = self.sprites
        for sprite in sprites:
            if pos in sprite.getAllPos():
                return sprite

    def getBlockByPos(self, pos):
        sprites = self.sprites
        for sprite in sprites:
            for block in sprite.blocks:
                block_pos = block.position
                if pos == block_pos:
                    return block


class MatrixView:
    MV = list()
    def __init__(self, size):
        self.columns = size[0]
        self.rows = size[1]
        matrix = list()
        for i in range(self.rows):
            column = list()
            for j in range(self.columns):
                column.append(0)
            matrix.append(column)
        self.MV = np.array(matrix)
        print(self.MV)



