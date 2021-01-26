import numpy as np
from utils.mathmethods import SnakeBrain, newGen
from utils.handmade import getParams, AllSprites
from gobjects.snake import Snake
from utils.mathmethods import Matrix, localExtractor, radToDegrees, brainFromWeights
from cmath import pi
import time
from guis import colors

DISPLAY_SETTINGS = getParams('DISPLAY_SETTINGS')
SNAKE_VIEWFIELD_SIZE = DISPLAY_SETTINGS['SNAKE_VIEWFIELD_SIZE']

class PhotoSnake:
    pass

class SmartConfig:
    snake_name = str()
    score = 0
    color = tuple()
    vision = list()
    activations = list()
    head_pos = tuple()
    head_dir = tuple()
    tail_end_pos = tuple()
    tail_end_dir = tuple()
    block_size = 10
    weights = list()


class SmartSnake:
    own_name = 'snake_v3'
    viewfield_size = SNAKE_VIEWFIELD_SIZE
    local_moves = {
        'UP': 0,
        'LEFT': pi/2,
        'RIGHT': -pi/2
    }
    detectors = {
        1: Matrix(viewfield_size),
        2: Matrix(viewfield_size),
        3: Matrix(viewfield_size)
    }

    def __init__(self, name, pos, dir, matrix_environment, color, a_0=180, in_config=False, exist_brain=False, block_size=10, c=5):
        self.config = SmartConfig()
        self.color = color
        self.energy = 100
        self.c = c
        self.config.snake_name = name
        start_head_pos = pos
        start_head_dir = dir
        self.snake = Snake(start_head_pos, name, color=color, block_size=block_size, dir=dir)
        self.blocks = self.snake.blocks
        self.config.block_size = block_size
        self.config.head_pos = self.snake.getHeadPosition()
        self.config.head_dir = self.snake.getHeadDirection()
        self.config.tail_end_pos = self.snake.getEndPosition()
        self.config.tail_end_dir = self.snake.getEndDirection()
        self.a_0 = a_0
        self.setVisionAngle(a_0)
        self.vision_screen = Matrix(self.viewfield_size)
        self.matrix_environment = matrix_environment
        self.status = 'alive'
        if exist_brain:
            self.brain = exist_brain
        else:
            self.brain = self.__createBrain()
        self.config.weights = self.brain.getWeights()

    def __createBrain(self):
        core_1 = SnakeBrain()
        core_1.addLayer((121, 30))
        core_1.addLayer((30, 15))
        core_1.addLayer((15, 3))

        # core_2 = SnakeBrain()
        # core_2.addLayer((121, 25))
        # core_2.addLayer((25, 10))
        # core_2.addLayer((10, 3))
        #
        # core_3 = SnakeBrain()
        # core_3.addLayer((121, 25))
        # core_3.addLayer((25, 10))
        # core_3.addLayer((10, 3))
        return core_1

    def getColor(self):
        return self.color

    def getHeadPosition(self):
        self.config.head_pos = self.snake.getHeadPosition()
        return self.config.head_pos

    def getBrain(self):
        return self.brain

    def getWeights(self):
        return self.config.weights

    def getChildBrain(self):
        return self.brain.newBrain()

    def getLen(self):
        len = self.snake.getLen()
        self.config.score = len - 2
        return len

    def getDir(self):
        return self.snake.direction

    def getScore(self):
        score = self.snake.score
        self.config.score = score
        return score

    def getAllPos(self):
        return self.snake.getAllPos()

    def getAllBlocks(self):
        return self.snake.blocks

    def getEnergy(self):
        return self.energy

    def getStatus(self):
        return self.status

    def getDetections(self):
        self.refreshDetectors()
        for m, row in enumerate(self.vision_screen.matrix):
            for n, signal in enumerate(row):
                if self.detectors.get(signal, False):
                    self.detectors.get(signal).matrix[m][n] = 1
                else:
                    pass

        return self.detectors

    def getSnakeAngle(self):
        snake_angle = self.snake.getAngle()
        self.vision_angle = snake_angle
        return snake_angle

    def getVisionAngle(self):
        angle = self.vision_angle
        return angle

    def setVisionAngle(self, new_angle):
        self.vision_angle = new_angle

    def updateC(self, new_c):
        self.c = new_c

    def __plusEnergy(self):
        self.energy += 14*self.c

    def __minusEnergy(self):
        self.energy -= self.c

    def __energyLogic(self):
        energy = self.getEnergy()
        if energy < 0:
            if self.snake.getLen() > 2:
                self.pop()
            else:
                self.coll()

    def addBlock(self):
        self.snake.addBlock()
        self.__plusEnergy()

    def pops(self, count):
        self.snake.pops(count)

    def pop(self):
        self.snake.pop()
        self.__plusEnergy()

    def play(self, vision_screen, learn=False, lr=0.01):
        vision_screen.reshape((self.viewfield_size[0] * self.viewfield_size[1], 1))
        # vision_screen.appendX(self.getScore())
        # vision_screen.appendX(self.energy)
        predict = self.brain.play(vision_screen.matrix, learn, lr)
        moves = ['LEFT', 'UP', 'RIGHT']
        predict = np.argmax(predict)
        move = moves[predict]
        rot = self.local_moves.get(move)
        self.moveByRot(rot)

    def checkSnakeStatus(self):
        if self.snake.getStatus() == 'alive':
            return True
        else:
            return False

    def respawn(self):
        self.snake.respawn()

    def refreshDetectors(self):
        for detector in self.detectors.values():
            detector.refresh()

    def coll(self):
        self.snake.changeColor(colors.DARK_GREY)
        self.snake.coll()
        self.snake.freeze()
        self.die()

    def updateVision(self, m_env):
        vision = self.vision_screen
        vision.refresh()
        pos = self.snake.getHeadPosition()
        self.matrix_environment = m_env
        vision_screen = localExtractor(m_env, vision, pos)
        vision_screen.setCenter(3)
        vision_angle = self.getVisionAngle()
        vision_degrees = -radToDegrees(vision_angle) + self.a_0
        self.vision_screen = vision_screen
        self.vision_screen.rotate(vision_degrees)
        return self.vision_screen

    def checkAngle(self,angle):
        new_angle = angle
        if new_angle >= 2*pi:
            while new_angle >= 2 * pi:
                new_angle -= 2*pi
        elif new_angle < 0:
            while new_angle < 0:
                new_angle += 2*pi
        return new_angle

    def moveByRot(self, local_dir):
        last_angle = self.snake.getAngle()
        rotation = local_dir
        new_angle = last_angle + rotation
        new_angle = self.checkAngle(new_angle)
        self.setVisionAngle(new_angle)
        self.snake.rotate(new_angle)

    def study(self, vision_screen, lr=0.01):
        vision_screen.reshape((self.viewfield_size[0] * self.viewfield_size[1], 1))
        predict = self.brain.studing(vision_screen.matrix)
        moves = ['LEFT', 'UP', 'RIGHT']
        predict = np.argmax(predict)
        move = moves[predict]
        rot = self.local_moves.get(move)
        self.moveByRot(rot)

    def evolution(self, gf):
        vision_screen = self.updateVision(gf)
        self.play(vision_screen, learn=False)

    def die(self):
        self.status = 'dead'

    def update(self):
        self.__energyLogic()
        self.__minusEnergy()
        self.snake.update()
        self.blocks = self.snake.blocks

    def draw(self):
        blocks = self.snake.draw()
        return  blocks


class SmartMama:
    def __init__(self, m_env, control_p=10):
        self.progeny = list()
        self.gf_matrix = m_env
        self.control_p = control_p
        self.m_sprites = self.getMovingSprites()
        self.muts = 0

    def getAllPositions(self):
        sprites = self.getMovingSprites()
        poss = sprites.getAllPositions()
        return poss

    def append(self, new_stepchild):
        self.progeny.append(new_stepchild)

    def updateVisions(self, gf_matrix):
        detections = list()
        vf_matrix = list()
        for child in self.progeny:
            vf_matrix.append(child.updateVision(gf_matrix))
            detections.append(child.getDetections())

        self.gf_matrix = gf_matrix
        self.last_detections = detections
        return (detections, vf_matrix)

    def getPoss(self, index):
        poss = list()
        for i, obj in enumerate(self.progeny):
            if i != index:
                for pos in obj.getAllPos():
                    poss.append(pos)
        return poss

    def getChildCount(self):
        return len(self.progeny)

    def getMuts(self):
        return self.muts

    def getMscore(self):
        score_sum = 0
        child_count = self.getChildCount()
        for child in self.progeny:
            score_sum += child.getScore()
        m_score = score_sum // child_count
        return m_score

    def getMovingSprites(self):
        m_sprites = AllSprites()
        for child in self.progeny:
            m_sprites.append(child.snake)
        self.sprites = m_sprites
        return m_sprites

    def getSnakeVisionByI(self, i):
        snake_vision = self.progeny[i].vision_screen
        return snake_vision

    def createChildBrain(self, in_config):
        pass

    def updateC(self, new_c):
        for child in self.progeny:
            child.updateC(new_c)

    def checkStatuses(self):
        for child in self.progeny:
            if child.status == 'dead':
                child_index = self.progeny.index(child)
                self.progeny.pop(child_index)

    def checkChildEnergy(self):
        for child in self.progeny:
            if child.getEnergy() <= 0:
                child.coll()

    def checkLen(self):
        if len(self.progeny) < 1:
            return False
        else:
            return True

    def checkPregnacy(self):
        for child in self.progeny:
            if child.getLen() == self.control_p:
                p_b = child.snake.getEndPosition()
                p_d = child.snake.getEndDirection()
                p_d = (p_d[0] * (-1), p_d[1] * (-1))
                child.snake.pops(3)
                color = child.getColor()
                brain = child.getChildBrain()

                brain, w = newGen(brain)
                brain = brainFromWeights(brain)
                self.muts += w
                new_child = SmartSnake('test{}'.format(time.time()), p_b, p_d,
                                       self.gf_matrix, block_size=child.config.block_size,
                                       exist_brain=brain, color=color)
                self.progeny.append(new_child)
                self.m_sprites.append(new_child.snake)

    def checkColls(self):
        for i, child in enumerate(self.progeny):
            poss_without_child = self.getPoss(i)
            child_head_pos = child.getHeadPosition()
            if child_head_pos in poss_without_child:
                child.coll()

    def __getMeanScore(self):
        score_sum = 0
        score_count = len(self.progeny)
        for child in self.progeny:
            score_sum += child.getScore()
        mean_score = score_sum // score_count
        return mean_score

    def getMetrics(self):
        mean_score = self.__getMeanScore()
        childs = len(self.progeny)
        return (childs, mean_score)

    def getTensorsForImage(self):
        return 0

    def update(self):
        self.checkPregnacy()
        self.checkStatuses()
        self.checkColls()
        self.checkChildEnergy()
        for child in self.progeny:
            child.update()

    def evolution(self, gf_matrix):
        for child in self.progeny:
            child.evolution(gf_matrix)






if __name__ == '__main__':
    detector_size = SNAKE_VIEWFIELD_SIZE
