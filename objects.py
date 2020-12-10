import random
import colors
from cmath import cos, sin


def RandomXY(rows):
    x = random.randrange(0, rows)
    y = random.randrange(0, rows)
    return (x, y)



class Cube:
    def __init__(self, position, dir=(0, 0), color=colors.WHITE, size=20, type='food', status='moving', head=False):
        self.position = position
        self.dir = dir
        self.color = color
        self.size = size
        self.type = type
        self.status = status
        self.next_pos = (0, 0)
        self.head = head

    def __del__(self):
        # print('расщипление')
        self.color = colors.WHITE

    def getDir(self):
        return self.dir

    def delete(self):
        self.__del__()

    def stop(self):
        self.status = 'stop'

    def go(self):
        self.status = 'moving'

    def __rect(self, xy):
        self.x = xy[0] * self.size
        self.y = xy[1] * self.size
        return (self.x, self.y, self.size, self.size)

    def changeColor(self, new_color):
        self.color = new_color

    def changeDir(self, new_dir):
        # self.status = 'moving'
        self.dir = new_dir

    def changeLoc(self, new_loc):
        self.position = new_loc

    def getPastLoc(self):
        pos = self.position
        dir = self.dir
        last_position = (pos[0] - dir[0],
                         pos[1] - dir[1])
        return last_position

    def back_in_time(self):
        self.changeLoc(self.getPastLoc())

    def update(self):
        if self.status == 'moving':
            self.position = (self.position[0] + self.dir[0],
                             self.position[1] + self.dir[1])
            self.next_pos = (self.position[0] + self.dir[0],
                             self.position[1] + self.dir[1])
        elif self.status == 'stop':
            self.position = (self.position[0],
                             self.position[1])

    def draw(self):
        full_location = self.__rect(self.position)
        return (self.color, full_location)


class Snake:
    score = 0
    lives = 1
    name = 'snake'
    block_type = 'snake'
    blocks = list()
    snake_size = len(blocks)

    def __init__(self, location, color, dir=(1, 0), a_dir=0, size=50, status="alive", freeze='False'):
        self.a_dir = a_dir
        self.color = color
        self.main_color = color
        self.direction = dir
        self.size = size
        self.location = location
        self.status = status
        self.head = Cube(location, self.direction, self.color, self.size, type=self.block_type, head=True)
        self.blocks.append(self.head)
        self.addBlock()
        self.addBlock()
        if freeze is True:
            self.freeze()

    def snakeFromBody(self, body):
        snake_len = len(body)

    def cutEnd(self, lengh):
        end = list()
        for time in range(lengh):
            self.blocks[-1].stop()
            end.append(self.blocks[-1])
            # self.pop()
        return end

    def getLen(self):
        self.snake_size = len(self.blocks)
        return self.snake_size

    def getHeadPosition(self):
        head = self.blocks[0]
        return head.position

    def getEndPosition(self):
        end = self.blocks[-1]
        return end.position

    def getEndDirection(self):
        end = self.blocks[-1]
        return  end.dir

    def ricochet(self):
        if self.direction == (0, 1):
            self.direction = (0, -1)
        elif self.direction == (0, -1):
            self.direction = (0, 1)
        elif self.direction == (-1, 0):
            self.direction = (1, 0)
        elif self.direction == (1, 0):
            self.direction = (-1, 0)

    def changeColor(self, new_color):
        for block in self.blocks:
            block.changeColor(new_color)

    def pop(self):
        if len(self.blocks) > 1:
            del self.blocks[-1]

    def pops(self, times):
        for time in range(times):
            self.pop()

    def respawn(self, location=(5, 5), dir=(1, 0), status='alive'):
        location = self.location
        self.blocks.clear()
        self.score = 0
        self.__init__(location=location, dir=self.direction, a_dir=self.a_dir, color=self.color, size=self.size, status=status)

    def coll(self):
        self.status = 'dead'
        blocks = self.blocks
        stopped_blocks = list()
        for block in blocks:
            block.stop()
            block.back_in_time()
            stopped_blocks.append(block)
        self.blocks = blocks

    def freeze(self):
        blocks = self.blocks
        stopped_blocks = list()
        for block in blocks:
            block.stop()
            stopped_blocks.append(block)
        self.blocks = blocks

    def unfreeze(self):
        blocks = self.blocks
        stopped_blocks = list()
        for block in blocks:
            block.go()
            stopped_blocks.append(block)
        self.blocks = blocks

    def check(self):
        blocks = self.blocks
        for block in blocks:
            print(block.dir)

    def die(self):
        self.status = 'dead'
        if len(self.blocks) > 10:
            self.lives += 1

        while len(self.blocks) > self.lives:
            self.pop()

        for block in self.blocks:
            block.changeColor(colors.DARK_RED)

    def move(self, direction):
        self.direction = direction

    def getAngle(self):
        angle = self.a_dir
        return angle

    def setAngle(self, new_angle):
        self.a_dir = new_angle

    def rotate(self, new_angle):
        self.a_dir = new_angle
        new_dx = cos(new_angle)
        new_dy = sin(new_angle) * (-1)
        self.direction = (round(new_dx.real), round(new_dy.real))

    def getAllPos(self):
        all_pos = list()
        blocks = self.blocks
        for element in blocks:
            all_pos.append(element.position)
        return all_pos

    def addBlock(self):
        last_block = self.blocks[-1]
        last_block_pos = last_block.position
        last_block_dir = last_block.getDir()
        new_block_pos = (last_block_pos[0] - last_block_dir[0],
                         last_block_pos[1] - last_block_dir[1])
        new_block_dir = last_block_dir
        tail = Cube(new_block_pos, new_block_dir, self.color, self.size, type=self.block_type)
        self.blocks.append(tail)

    def checkCol(self):
        poss = self.getAllPos()
        head_pos = self.blocks[0].position
        fut_head_pos = (head_pos[0] + self.direction[0],
                        head_pos[1] + self.direction[1] )
        if fut_head_pos in poss:
            self.coll()
        else:
            return False

    def update(self):
        self.getLen()
        self.checkCol()
        last_dir = tuple()
        for i, segment in enumerate(self.blocks):
            if i == 0:
                last_dir = segment.dir
                segment.dir = self.direction
                segment.update()
            else:
                l = segment.dir
                moment_dir = last_dir
                segment.changeDir(moment_dir)
                segment.update()
                last_dir = l

    def draw(self):
        blocks = list()
        for segment in self.blocks:
            blocks.append(segment.draw())
        return blocks


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
            all_pos.append(element.position)
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


class Food:
    name = 'food'
    block_type = 'food'
    status = 'existing'
    blocks = list()

    def __init__(self, position, color=colors.RED, size=50):
        self.color = color
        self.size = size
        self.location = posToLoc(position, self.size)
        self.blocks.append(Cube(self.location, color=self.color, size=self.size, type=self.block_type))

    def changeLoc(self, new_location):
        self.location = new_location
        self.blocks[0].changeLoc(self.location)

    def changeColor(self, new_color):
        self.color = new_color
        for block in self.blocks:
            block.changeColor(self.color)

    def update(self):
        status = self.status

    def draw(self):
        self.update()
        response = self.blocks[0].draw()
        return response


class FoodPacker:
    block_type = 'food'

    def __init__(self, area, count, color, size):
        self.color = color
        self.size = size
        self.area = area
        self.blocks = list()
        self.positions = self.genPositions(area, count)
        self.genFood()
        # for pos in first_positions:
        #     self.blocks.append(Cube(pos, color=color, size=size, type=self.block_type))

    def getArea(self):
        return self.area

    def genPositions(self, area, count):
        positions = list()
        area_x_1 = area[0][0]
        area_x_2 = area[0][1]
        area_y_1 = area[1][0]
        area_y_2 = area[1][1]
        dx = area_x_2 - area_x_1
        dy = area_y_2 - area_y_1
        for position in range(count):
            random_x = random.randrange(0, dx)
            random_y = random.randrange(0, dy)
            random_x += area_x_1
            random_y += area_y_1
            positions.append((random_x, random_y))

        return positions

    def genFood(self):
        size = self.size
        color = self.color
        positions = self.positions
        blocks = self.blocks
        for pos in positions:
            blocks.append(Cube(pos, color=color, size=size, type=self.block_type))

        self.blocks = blocks

    def addBlock(self, new_pos):
        self.blocks.append(Cube(new_pos, color=self.color, size=self.size, type=self.block_type))

    def getAllPos(self):
        all_pos = list()
        blocks = self.blocks
        for element in blocks:
            all_pos.append(element.position)

        return all_pos

    def update(self):
        pass

    def draw(self):
        blocks = list()
        for segment in self.blocks:
            blocks.append(segment.draw())

        return blocks


class Solid:
    def __init__(self, size, ro):
        pass