import random
from guis import colors
from guis.utils import render
from abc import ABC
import json


MODES = {
    'nothing': 0,
    'barrier':1,
    'food': 2,
    'snake': 3
}

DETECTIONS_COLORS = {
        0: colors.DARK_GREEN,
        1: colors.VERY_LIGHT_GREEN,
        2: colors.LIGHT_BLUE,
        3: colors.LIGHT_PINK
    }

def find_center(size_1, size_2):
    x_1 = size_1[0]
    x_2 = size_2[0]
    y_1 = size_1[1]
    y_2 = size_2[1]
    dx = (x_1 - x_2) // 2
    dy = (y_1 - y_2) // 2
    return (dx, dy)

def load_params(param_path):
    with open(param_path) as file:
        text = file.read()
    params = json.loads(text)
    return params


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
        random_x = random.randrange(0, dx+1, 1)
        random_y = random.randrange(0, dy+1, 1)
        random_x += area_x_1
        random_y += area_y_1
        if (random_x, random_y) not in all_positions:
            new_pos = (random_x, random_y)
            search = False
            return new_pos
        else:
            pass

    return positions


class AllSprites(ABC):
    def __init__(self):
        self.sprites = list()

    def getAllPos(self):
        poss = list()
        for sprite in self.sprites:
            poss += sprite.getAllPos()
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
                block_color = block.getColor()
                block_type = block.getType()
                block_int = MODES.get(block_type)
                block_ppos = block.getPosition()
                b_pp_n = block_ppos[1]
                b_pp_m = block_ppos[0]

                if (b_pp_m, b_pp_n) not in pixels_positions:
                    pixels_positions.append((b_pp_m, b_pp_n))
                    M.matrix[b_pp_n][b_pp_m] = block_int
                else:
                    pass

        return M

    def getExceptHead(self, head_pos):
        copied_sprites = self.sprites
        current_sprite, current_index = self.getSpriteByPos(head_pos)
        copied_sprites.pop(current_index)
        poss = list()
        for sprite in copied_sprites:
            for pos in sprite.getAllPos():
                poss.append(pos)
        return poss


    def getSpriteByPos(self, pos):
        for i, sprite in enumerate(self.sprites):
            if pos in sprite.getAllPos():
                return sprite

    def getBlockByPos(self, pos):
        sprites = self.sprites
        for sprite in sprites:
            for block in sprite.blocks:
                block_pos = block.getPosition()
                if pos == block_pos:
                    return block


class AllAies(AllSprites):

    def printDirs(self):
        for player in self.sprites:
            current_dir = player.getDir()
            current_name = player.getName()
            print(current_name, ": ", current_dir)

    def printPoss(self):
        for player in self.sprites:
            current_poss = player.getAllPos()
            current_name = player.getName()
            print(current_name, ": ", current_poss)

    def play(self, input_environment, learn=False, lr=0.1):
        for player in self.sprites:
            player.updateVision(input_environment)
            # player.play(learn=learn, lr=lr)
            # player_detections = player.getDetections()
            # print(player_detections)
            # print('++++++++++++++++++++++')


    def print_to_matrix(self, M):
        pixels_positions = list()
        sprites = self.sprites
        for obj in sprites:
            for block in obj.getAllBlocks():
                block_color = block.getColor()
                block_type = block.getType()
                block_int = MODES.get(block_type)
                block_ppos = block.getPosition()
                b_pp_n = block_ppos[1]
                b_pp_m = block_ppos[0]

                if (b_pp_m, b_pp_n) not in pixels_positions:
                    pixels_positions.append((b_pp_m, b_pp_n))
                    M.matrix[b_pp_n][b_pp_m] = block_int
                else:
                    pass

        return M