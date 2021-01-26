import time
from cmath import sin, cos
from guis import colors
from gobjects.cube import Cube
from abc import ABC

smoves = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class SConfig:
    name = str()
    color = tuple()
    block_size = int()
    status = str()
    ismoving = True
    score = int()
    head_direction = (0, 0)
    head_position = tuple()
    a_dir = int()
    blocks = list()

    def cprint(self):
        config_JSON = {
            "NAME": self.name,
            "HEAD_POSITION": self.head_position,
            "HEAD_DIRECTION": self.head_direction,
            "BLOCKS": self.blocks,
            "BLOCK_SIZE": self.block_size,
            "COLOR": self.color,
            "A_DIR": self.a_dir,
            "SCORE": self.score,
            "STATUS": self.status
        }
        print(config_JSON)
        return  config_JSON



class Snake(ABC):
    name = 'snake'
    block_type = 'snake'
    score = 1

    def __init__(self, position, name=str(time.time()), color=colors.DARK_GREEN, block_size=10, dir=(0, 0)):
        self.place_of_birth = position
        self.config = SConfig()
        self.config.name = name
        self.config.color = color
        self.config.block_size = block_size
        self.setOriginPosition(position)
        self.setHeadDirection(dir)
        self.direction = dir
        self.blocks = self.__createSnake()
        self.config.blocks = self.blocks
        self.addBlock()
        self.addBlock()
        self.addBlock()
        self.a_dir = 90

    def __checkDir(self, dir):
        if dir == (0, 0):
            dir = (1, 0)
        return dir

    def addBlock(self):
        color = self.config.color
        block_size = self.config.block_size
        last_block_pos = self.getEndPosition()
        last_block_dir = self.getEndDirection()
        last_block_dir = self.__checkDir(last_block_dir)
        new_block_pos = (last_block_pos[0] - int(last_block_dir[0]),
                         last_block_pos[1] - int(last_block_dir[1]))
        new_block_dir = last_block_dir
        tail = Cube(new_block_pos, new_block_dir, color, size=block_size, type=self.block_type, status='moving')
        self.blocks.append(tail)


    def setOriginPosition(self, o_pos):
        self.config.head_position = o_pos

    def plusScore(self):
        self.score += 1

    def __createSnake(self):
        blocks = list()
        head_pos = self.config.head_position
        head_dir = self.config.head_direction
        snake_color = self.config.color
        block_size = self.config.block_size
        head = Cube(head_pos, head_dir, snake_color, size=block_size, status='moving', type=self.block_type)
        blocks.append(head)
        return blocks

    def __setAngle(self, new_angle):
        self.a_dir = new_angle
        self.config.a_dir = new_angle

    def __checkCol(self):
        head_dir = self.config.head_direction
        poss = self.getAllPos()
        head_pos = self.getHeadPosition()
        # fut_head_pos = (head_pos[0] + head_dir[0],
        #                 head_pos[1] + head_dir[1])
        if head_pos in poss[1:]:
            # print('samocol')
            # self.freeze()
            self.coll()
        else:
            return False

    def __checkMoving(self):
        if self.direction == (0, 0):
            self.freeze()
        else:
            self.unfreeze()

    def getLen(self):
        self.snake_size = len(self.blocks)
        self.config.snake_size = self.snake_size
        return self.snake_size

    def setHeadPosition(self, pos):
        self.config.head_position = pos

    def getHeadPosition(self):
        return self.config.head_position

    def getHeadLastPosition(self):
        return self.blocks[0].getLastPos()

    def setHeadDirection(self, new_dir):
        self.config.head_direction = new_dir

    def getHeadDirection(self):
        return self.config.head_direction

    def getStatus(self):
        return self.config.status

    def getEndPosition(self):
        end = self.blocks[-1]
        return end.getPosition()

    def getEndDirection(self):
        end = self.blocks[-1]
        return end.getDir()

    def changeColor(self, new_color):
        for block in self.blocks:
            block.changeColor(new_color)

    def pop(self):
        if len(self.blocks) > 3:
            self.blocks.pop()

    def pops(self, times):
        for time in range(times):
            self.pop()

    def respawn(self, location=(5, 5), dir=(1, 0), status='alive'):
        self.blocks.clear()
        self.score = 0
        self.__init__(self.place_of_birth,
                      name=self.config.name,
                      dir=self.config.head_direction,
                      color=self.config.color,
                      block_size=self.config.block_size)

    def move(self, direction):
        self.direction = direction

    def getAngle(self):
        angle = self.a_dir
        return angle

    def rotate(self, new_angle):
        self.__setAngle(new_angle)
        new_dx = cos(new_angle)
        new_dy = sin(new_angle) * (-1)
        self.direction = (round(new_dx.real), round(new_dy.real))

    def getAllPos(self):
        all_pos = list()
        for element in self.blocks:
            all_pos.append(element.getPosition())
        return all_pos

    def freeze(self):
        self.config.ismoving = False
        for block in self.blocks:
            block.stop()
            # print(block.getDir())

    def unfreeze(self):
        self.config.ismoving = True
        for block in self.blocks:
            block.go()

    def asRing(self):
        last_poss = [self.getHeadLastPosition()]
        for i, block in enumerate(self.blocks[1:]):
            lp = last_poss[-1]
            block_pos = block.getPosition()
            block_dir = block.getDir()
            if block_pos != lp:
                block.changePos(lp)
                last_block_x = lp[0] - block_dir[0]
                last_block_y = lp[1] - block_dir[1]
                block_last_pos = (last_block_x, last_block_y)
                block.addLastPos(block_last_pos)
                last_poss.append(block_last_pos)
                print(i+1, block_pos, lp)

    def coll(self):
        self.config.ismoving = False
        for i, block in enumerate(self.blocks):
            block.stop()
            block.back_in_time()
            if i == 0:
                self.config.head_position = block.getPosition()


    def update(self):
        last_dirs = list()
        last_poss = list()
        self.getLen()
        # self.__checkMoving()
        self.__checkCol()
        # self.asRing()
        if self.config.ismoving == True:
            for i, segment in enumerate(self.blocks):
                if i == 0:
                    # segment.changeDir(self.direction)
                    # segment.update()
                    last_dir = segment.getDir()
                    last_pos = segment.getPosition()
                    segment.changeDir(self.direction)
                    segment.update()
                    self.setHeadPosition(segment.getPosition())
                    self.setHeadDirection(segment.getDir())
                    last_dirs.append(last_dir)
                    last_poss.append(last_pos)

                else:
                    new_dir = last_dirs[-1]
                    new_pos = last_poss[-1]
                    last_dir = segment.getDir()
                    last_pos = segment.getPosition()
                    segment.changeDir(new_dir)
                    segment.update()
                    test_pos = segment.getPosition()
                    if test_pos != new_pos:
                        segment.changePos(new_pos)
                    last_dirs.append(last_dir)
                    last_poss.append(last_pos)

    def draw(self):
        blocks = list()
        for segment in self.blocks:
            blocks.append(segment.draw())
        return blocks
