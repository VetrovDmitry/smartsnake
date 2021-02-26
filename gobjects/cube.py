from guis import colors


class Config:
    last_position = (0, 0)
    last_direction = (0, 0)
    moment_dir = (0, 0)
    type = None
    status = 'stop'

    def __init__(self, pos, color, size):
        self.position = pos
        self.color = color
        self.size = size


class Cube:
    """Класс куб который позволяет создавать квадраты"""
    def __init__(self, position, dir=(0, 0), color=colors.WHITE, size=20, type='food', status='stop', head=False):
        self.config = Config(position, color, size)
        self.config.moment_dir = dir
        self.config.type = type
        self.config.status = status

    def __del__(self):
        del self.config


    def getDir(self):
        return self.config.moment_dir

    def delete(self):
        self.__del__()

    def go(self):
        self.config.status = 'moving'

    def stop(self):
        self.config.status = 'stop'

    def __rect(self, xy):
        size = self.config.size
        x = xy[0] * size
        y = xy[1] * size
        return (x, y, size, size)

    def changeColor(self, new_color):
        self.config.color = new_color

    def changeDir(self, new_dir):
        last_dir = self.getDir()
        self.config.moment_dir = new_dir
        self.config.last_direction = last_dir

    def changePos(self, new_pos):
        last_pos = self.getPosition()
        self.config.position = new_pos
        self.config.last_position = last_pos

    def getPosition(self):
        return self.config.position

    def getLastPos(self):
        return self.config.last_position

    def addLastPos(self, new_last_pos):
        self.config.last_position = new_last_pos

    def getColor(self):
        return self.config.color

    def getType(self):
        return self.config.type

    def addLastDir(self, last_dir):
        self.config.last_direction = last_dir

    def getLastDir(self):
        return self.config.last_direction

    def getStatus(self):
        return self.config.status

    def back_in_time(self):
        self.changePos(self.getLastPos())
        # moment_pos = self.getPosition()
        # moment_dir = self.getDir()
        # last_pos = (moment_pos[0] - moment_dir[0],
        #             moment_pos[1] - moment_dir[1])
        # last_pos = self.getLastPos()
        # self.changePos(last_pos)
        # self.stop()

    def update(self):
        if self.config.status == 'moving':
            k = 1
        elif self.config.status == 'stop':
            k = 0
        position = self.getPosition()
        direction = self.getDir()
        new_position_x = position[0] + direction[0] * k
        new_position_y = position[1] + direction[1] * k
        new_position = (new_position_x, new_position_y)
        self.changePos(new_position)

    def draw(self):
        position = self.getPosition()
        full_location = self.__rect(position)
        color = self.getColor()
        return (color, full_location)