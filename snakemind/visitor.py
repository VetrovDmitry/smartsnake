from gobjects.snake import Snake
from utils.mathmethods import Matrix, localExtractor, radToDegrees, angleToDirection
from utils.handmade import load_params
from cmath import pi


PARAMS_PATH = 'PARAMS.json'
params = load_params(PARAMS_PATH)

snake_viewfield_size = params.get('BRAIN_SETTINGS')['SNAKE_VIEWFIELD_SIZE']

local_moves = {
        'UP': 0,
        'LEFT': -pi/2,
        'RIGHT': pi/2
    }


class Visitor(Snake):
    """using to create training data"""
    viewfield_size = snake_viewfield_size
    __angle = 0
    __local_angle = 0
    __vision_screen = Matrix(viewfield_size)
    __detectors = {
        1: Matrix(snake_viewfield_size),
        2: Matrix(snake_viewfield_size),
        3: Matrix(snake_viewfield_size)
    }

    def __checkAngle(self):
        if self.getAngle() == 2 * pi:
            self.setAngle(0)
        if self.getAngle() == - 2 * pi:
            self.setAngle(0)

    def setAngle(self, new_angle):
        self.__angle = new_angle

    def getAngle(self):
        return self.__angle

    def setLocalAngle(self, angle):
        self.__local_angle = angle

    def getLocalAngle(self):
        return self.__local_angle

    def moveByRot(self, angle_direction):
        self.__checkAngle()
        d_a = local_moves.get(angle_direction)
        moment_angle = self.getAngle()
        moment_angle += d_a
        self.setAngle(moment_angle)
        direction = angleToDirection(moment_angle)
        self.move(direction)

    def updateVision(self, matrix_environment):
        moment_head_pos = self.getHeadPosition()
        vision_angle = self.getLocalAngle() - self.getAngle()
        vision_degrees = radToDegrees(vision_angle)
        self.__vision_screen.refresh()
        self.__vision_screen = localExtractor(matrix_environment, self.__vision_screen, moment_head_pos)
        vision_angle = -self.getLocalAngle() + self.getAngle()
        vision_degrees = radToDegrees(vision_angle)
        self.__vision_screen.rotate(vision_degrees)
        self.__fillDetectors()
        return self.__vision_screen

    def getVisionScreen(self):
        return self.__vision_screen

    def __fillDetectors(self):
        self.__refreshDetectors()
        for m, row in enumerate(self.getVisionScreen().matrix):
            for n, signal in enumerate(row):
                if self.__detectors.get(signal):
                    self.__detectors.get(signal).matrix[m][n] = 1
                else:
                    pass

    def getDetectors(self):
        return self.__detectors


    def __refreshDetectors(self):
        for detector in self.__detectors.values():
            detector.refresh()
