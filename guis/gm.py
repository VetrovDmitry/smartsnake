import pygame as pg
from abc import ABC


class GraphicManager(ABC):
    """PRIMITIVE GRAPHIC OPERATIONS"""
    location = tuple()
    font_size = 30
    cursor_thickness = 4

    def setLocation(self, location):
        self.location = location

    def find_center(self, first_layer_size, second_layer_size):
        """returns center for two layers"""
        x = int(first_layer_size[0] / 2 - second_layer_size[0] / 2)
        y = int(first_layer_size[1] / 2 - second_layer_size[1] / 2)
        return (x, y)

    def createRect(self, ab):
        """creates rect by a an b"""
        rect = pg.Surface(ab)
        return rect

    def createBackground(self, size):
        self.background = pg.Surface(size)

    def fillBackground(self, color):
        self.background.fill(color)

    def cursor_size(self, t_size):
        cursor_x = t_size[0] + self.cursor_thickness * 2
        cursor_y = t_size[1]
        return (cursor_x, cursor_y)

    def createRotateText(self, label, color, size):
        font = pg.font.Font(None, size)
        text = font.render(label, 4, color)
        text = pg.transform.rotate(text, 90)
        return text

    def createText(self, label, color, size=4):
        font = pg.font.Font(None, size)
        text = font.render(str(label), 4, color)
        return text

    def draw(self, surface):
        surface.blit(self.background, self.location)