from guis import colors
from gobjects.cube import Cube


class Wall:
    blocks = list()
    name = 'wall'
    block_type = 'barrier'

    def __init__(self, edges, color=colors.BLACK, size=50):
        self.edges = edges
        self.color = color
        self.size = size
        self.blocks = self.createWall()

    def changeColor(self, new_color):
        self.color = new_color
        for block in self.blocks:
            block.changeColor(self.color)

    def getAllPos(self):
        all_pos = list()
        blocks = self.blocks
        for element in blocks:
            all_pos.append(element.getPosition())
        return all_pos

    def checkPoints(self, points):
        response = int()
        if len(points) == 1:
            response = 1
        elif len(points) == 2:
            response = 2
        elif len(points) == 4:
            response = 4

        return response

    def createPile(self, loc):
        pile = Cube(loc, color=self.color, size=self.size, type=self.block_type)

        pile = [pile.draw(),]
        return pile

    def createWall(self):
        wall = list()
        origin = self.edges[0]
        end = self.edges[1]
        horizontal_block_count = end[0] - origin[0] + 1
        vertical_block_count = end[1] - origin[1] + 1

        for i in range(horizontal_block_count):
            block_x_coord = (i + origin[0])
            for j in range(vertical_block_count):
                block_y_coord = (j + origin[1])
                block_position = (block_x_coord, block_y_coord)
                block = Cube(block_position, color=self.color, size=self.size, status='stop', type=self.block_type)
                wall.append(block)

        self.blocks = wall
        return self.blocks

    def update(self):
        pass

    def draw(self):
        blocks = list()
        for element in self.blocks:
            blocks.append((element.draw()))

        return blocks
