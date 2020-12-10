from handmade import AllSprites, smart_pos_for_area
from objects import Wall
import colors



def WorldRules(m_obj, f_obj, w_obj):
    moving_poss = m_obj.getAllPositions()
    for sprite in m_obj.sprites:
        sprite_head_pos = sprite.getHeadPosition()
        if sprite_head_pos in f_obj.getAllPositions():
            eaten_food = f_obj.getBlockByPos(sprite_head_pos)
            food_object = f_obj.getSpriteByPos(sprite_head_pos)
            food_area = food_object.getArea()
            new_pos = smart_pos_for_area(food_area, moving_poss)
            eaten_food.changeLoc(new_pos)
            sprite.addBlock()
            sprite.score += 1
        elif sprite_head_pos in w_obj.getAllPositions():
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

