import random
from guis import colors
from gobjects.cube import Cube
from gobjects.object_daddy import GameObject

class Food(GameObject):
    name = 'food'
    block_type = 'food'
    status = 'existing'
    blocks = list()

    def __init__(self, position, color=colors.RED, size=50):
        self.color = color
        self.size = size
        self.position = position
        self.blocks.append(Cube(self.position, color=self.color, size=self.size, type=self.block_type))

    def changeLoc(self, new_location):
        self.position = new_location
        self.blocks[0].changePos(self.position)

    def changeColor(self, new_color):
        self.color = new_color
        for block in self.blocks:
            block.changeColor(self.color)

    def update(self):
        status = self.status



class FoodPacker(GameObject):
    block_type = 'food'

    def __init__(self, area, count, color, size):
        self.color = color
        self.size = size
        self.area = area
        self.count = count
        self.blocks = list()
        self.positions = self.__genPositions(area, count)
        self.genFood()
        # for pos in first_positions:
        #     self.blocks.append(Cube(pos, color=color, size=size, type=self.block_type))

    def getArea(self):
        return self.area

    def __genPositions(self, area, count):
        positions = list()
        area_x_1 = area[0][0]
        area_x_2 = area[0][1]
        area_y_1 = area[1][0]
        area_y_2 = area[1][1]
        dx = area_x_2 - area_x_1
        dy = area_y_2 - area_y_1
        for position in range(count):
            random_x = random.randrange(0, dx+1, 1)
            random_y = random.randrange(0, dy+1, 1)
            random_x += area_x_1
            random_y += area_y_1
            positions.append((random_x, random_y))

        return positions

    def __genPosition(self):
        searching = True
        area = self.area
        area_x_1 = area[0][0]
        area_x_2 = area[0][1]
        area_y_1 = area[1][0]
        area_y_2 = area[1][1]
        dx = area_x_2 - area_x_1
        dy = area_y_2 - area_y_1
        random_x = 0
        random_y = 0
        while searching:
            random_x = random.randrange(0, dx)
            random_y = random.randrange(0, dy)
            random_x += area_x_1
            random_y += area_y_1
            if (random_x, random_y) not in self.getAllPos():
                searching = False

        return (random_x, random_y)

    def genFood(self):
        size = self.size
        color = self.color
        positions = self.positions
        blocks = self.blocks
        for pos in positions:
            blocks.append(Cube(pos, color=color, size=size, type=self.block_type))

        self.blocks = blocks

    def getCount(self):
        return self.count

    def setCount(self, count):
        self.count = count

    def minusBlock(self):
        if len(self.blocks) > 1:
            self.blocks.pop()

    def plusBlock(self):
        new_pos = self.__genPosition()
        self.addBlock(new_pos)

    def addBlock(self, new_pos):
        self.blocks.append(Cube(new_pos, color=self.color, size=self.size, type=self.block_type))

    def checkCount(self):
        if len(self.blocks) > self.count:
            while len(self.blocks) > self.count:
                self.minusBlock()
        elif len(self.blocks) < self.count:
            while len(self.blocks) < self.count:
                self.plusBlock()

    def update(self):
        self.checkCount()