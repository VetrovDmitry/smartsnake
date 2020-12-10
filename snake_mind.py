import numpy as np
from mathmethods import SnakeBrain
from handmade import getParams
from objects import Snake
from mathmethods import Matrix, localExtractor, centerToEdge, radToDegrees
from cmath import cos, sin, pi
from sys import stdout


DISPLAY_SETTINGS = getParams('DISPLAY_SETTINGS')
SNAKE_VIEWFIELD_SIZE = DISPLAY_SETTINGS['SNAKE_VIEWFIELD_SIZE']


class SmartSnake:
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


    own_name = 'snake_v3'

    def __init__(self, pos, dir, a_dir, color, size, matrix_environment, relations, freeze=False, detections=(1, 2, 3), a_0=90):
        self.color = color
        self.matrix_environment = matrix_environment
        self.size = size
        self.snake = Snake(pos, color, dir, a_dir, size, freeze=freeze)
        self.a_0 = a_0
        self.setVisionAngle(0)
        self.vision_screen = Matrix(self.viewfield_size)
        self.relations = relations
        self.__createBrain()

    def __createBrain(self):
        brain = SnakeBrain()
        brain.addLayer((121, 25))
        brain.addLayer((25, 10))
        brain.addLayer((10, 3))
        self.brain = brain

    def play(self, learn=False, lr=0.01):
        detections = self.vision_screen
        # detections.reshape((self.viewfield_size[0] * self.viewfield_size[1], 1))
        predict = self.brain.play(detections.matrix, learn, lr)
        moves = ['LEFT', 'UP', 'RIGHT']
        predict = np.argmax(predict)

        move = moves[predict]
        # print(move)
        rot = self.local_moves.get(move)
        self.moveByRot(rot)
        if self.snake.status is not 'alive':
            self.snake.respawn()


    def setName(self, name):
        self.own_name = name

    def getName(self):
        return self.own_name

    def getSnakeAngle(self):
        snake_angle = self.snake.getAngle()
        self.vision_angle = snake_angle
        return snake_angle

    def checkSnakeStatus(self):
        if self.snake.status == 'alive':
            return True
        else:
            return False

    def setVisionAngle(self, new_angle):
        self.vision_angle = new_angle

    def getVisionAngle(self):
        angle = self.vision_angle
        return angle

    def getDetections(self):
        vision_screen = self.vision_screen
        self.updateDetectors()
        for m, row in enumerate(vision_screen.matrix):
            for n, signal in enumerate(row):
                if self.detectors.get(signal, False):
                    self.detectors.get(signal).matrix[m][n] = 1
                else:
                    pass

        return self.detectors

    def updateDetectors(self):
        for detector in self.detectors.values():
            detector.refresh()

    def printScore(self):
        print("{}'s score: {}".format(self.own_name, self.snake.score))

        stdout.flush()

    def checkPregnancy(self):
        snake_size = self.snake.getLen()
        if snake_size == 8:
            snake_end_pos = self.snake.getEndPosition()
            snake_end_dir = self.snake.getEndDirection()
            self.snake.pops(3)
            baby = self.__init__(snake_end_pos,
                                 snake_end_dir,

                                 )


    def updateVision(self, m_env):
        # self.checkPregnancy()
        vision = self.vision_screen
        vision.refresh()
        pos = self.snake.getHeadPosition()
        self.matrix_environment = m_env
        vision_screen = localExtractor(m_env, vision, pos)
        vision_angle = self.getVisionAngle()
        vision_degrees = -radToDegrees(vision_angle) + self.a_0
        self.vision_screen = vision_screen
        if self.checkSnakeStatus():
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

    def getVisionScreen(self, matrix_environment):
        self.updateVision(matrix_environment)
        return self.vision_screen

    def update(self):
        self.checkPregnancy()
        self.snake.update()

    def draw(self):
        blocks = self.snake.draw()
        return  blocks






if __name__ == '__main__':
    detector_size = SNAKE_VIEWFIELD_SIZE
