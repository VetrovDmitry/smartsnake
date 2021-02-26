from utils.handmade import AllSprites, smart_pos_for_area
from gobjects.wall import Wall
from guis import colors
import pygame as pg


def Pause():
    pause = True
    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                pause = False


def WorldRulesPVE(m_sprites, f_sprites, w_sprites):
    sprite = m_sprites.getSprites()[0]
    sprite_head_pos = sprite.getHeadPosition()
    sprite_all_pos = sprite.getAllPos()
    if sprite_head_pos in f_sprites.getAllPos():
        eaten_food = f_sprites.getBlockByPos(sprite_head_pos)
        food_object = f_sprites.getSprites()[0]
        food_area = food_object.getArea()
        new_pos = smart_pos_for_area(food_area, sprite_all_pos)
        eaten_food.changePos(new_pos)
        sprite.addBlock()
    elif sprite_head_pos in w_sprites.getAllPos():
        sprite.coll()



class Map:
    def __init__(self, map_size, block_size, circuit=False):
        self.m_size = map_size
        self.block_size = block_size
        self.sprites = AllSprites()
        if circuit:
            for i, wall in enumerate(self.createCircuit(map_size)):
                if i >= 4:
                    self.sprites.append(Wall(wall, color=colors.DARK_RED, size=self.block_size))
                else:
                    self.sprites.append(Wall(wall, color=colors.DARK_BLUE, size=self.block_size))

    def createCircuit(self, ranges):
        edges = [((0, 0), (0, ranges[1] - 1)),
                 ((0, 0), (ranges[0] - 1, 0)),
                 ((ranges[0] - 1, 0), (ranges[0] - 1, ranges[1] - 1)),
                 ((0, ranges[1] - 1), (ranges[0] - 1, ranges[1] - 1)),
                 ((1, 1), (1, ranges[1] - 2)),
                 ((1, 1), (ranges[0] - 2, 1)),
                 ((1, ranges[1] - 2), (ranges[0] - 2, ranges[1] - 2)),
                 ((ranges[0] - 2, 1), (ranges[0] - 2, ranges[1] - 2))]
        return edges

    def getSprites(self):
        return self.sprites




if __name__ == '__main__':
    laboratory_map = Map((100, 50))

