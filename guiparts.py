import pygame as pg
from enum import Enum
import colors
from abc import ABC
from random import randrange as rrange


FONT_SIZE = 40


class GraphicManager(ABC):
    """PRIMITIVE GRAPHIC OPERATIONS"""
    font_size = 30
    cursor_thickness = 4

    def find_center(self, first_layer_size, second_layer_size):
        """returns center for two layers"""
        x = int(first_layer_size[0] / 2 - second_layer_size[0] / 2)
        y = int(first_layer_size[1] / 2 - second_layer_size[1] / 2)
        return (x, y)

    def createRect(self, ab):
        """creates rect by a an b"""
        rect = pg.Surface(ab)
        return rect


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



class Button(GraphicManager):
    background_color = colors.GREY
    text_color = colors.BLACK

    def __init__(self, i, label, size, loc):
        self.i = i
        self.label = label
        self.sizeXY = size
        self.location = loc

    def get_highs(self):
        return 0

    def update(self, I):
        layer = self.createRect(self.sizeXY)

        if I == self.i:
            text_color = colors.WHITE
            self.background_color = colors.DARK_GREY
        else:
            text_color = colors.BLACK.value
            self.background_color = colors.GREY

        layer.fill(self.background_color)
        text = self.createText(self.label, text_color)

        text_size = text.get_size()
        center = self.find_center(self.sizeXY, text_size)
        layer.blit(text, center)
        self.layer = layer

    def draw(self, surface):
        surface.blit(self.layer, self.location)


class Cursor(GraphicManager):
    position = tuple()
    color = colors.WHITE
    cursor_thickness = 4

    def __init__(self, i, size):
        self.i = i
        self.sizeXY = self.cursor_size(size)


    def update(self, I):
        self.i = I
        layer = self.createRect(self.sizeXY)
        layer.fill(self.color)
        self.layer = layer

    def draw(self, surface):
        surface_size = surface.get_size()
        surface_center = self.find_center(surface_size, self.sizeXY)
        surface.blit(self.layer, surface_center)


class Tablo(GraphicManager):
    """TABLO SHOWS MOMENT PARAMS"""
    text_color = colors.BLACK
    name_size = 35
    count_size = 50

    def __init__(self, label, size, loc, background_color=colors.GREY, plus_color=colors.WHITE):
        self.label = label
        self.size = size
        self.location = loc
        self.background_color = background_color
        self.plus_color = plus_color

    def get_highs(self):
        return 0

    def changeBGColor(self, new_color):
        self.background_color = new_color

    def update(self, count, status):
        layer = self.createRect(self.size)

        layer.fill(self.background_color)

        if status:
            self.text_color = self.plus_color
        else:
            self.text_color = colors.BLACK

        table_name = self.createRotateText(self.label, self.text_color, self.name_size)
        text_size = table_name.get_size()
        center_1 = self.find_center(self.size, text_size)
        layer.blit(table_name, (1, center_1[1]))

        count_text = self.createText(count, self.text_color, self.count_size)
        count_text_size = count_text.get_size()
        center_2 = self.find_center(self.size, count_text_size)
        layer.blit(count_text, center_2)
        self.layer = layer

    def draw(self, surface):
        surface.blit(self.layer, self.location)


class Scale(GraphicManager):
    dl = 4
    dy = 20
    cursor_size = (7, 24)
    line_color = colors.WHITE
    basis_color = colors.GREY
    cursor_color = colors.GREEN
    name_color = colors.WHITE
    SELECTED = False

    def __init__(self, location, size, positions, scale_name=''):
        self.location = location
        self.size = size
        self.scale = self.createScale(size, positions, scale_name)
        self.cursor = self.createCursor(self.cursor_size)

    def getCursorPos(self):
        pos = self.cursor_position
        return pos

    def getCursorSize(self):
        size = self.cursor_size
        return size


    def createScale(self, s_size, count, s_name):
        layer = pg.Surface(s_size)
        miniline_size = 2
        sx = 3
        x1 = 0 + self.dl
        x2 = layer.get_size()[0] - self.dl
        dx = (x2 - x1) // count
        self.dx = dx
        y1 = layer.get_size()[1] // 2 - self.dy
        y2 = y1
        self.y = y2
        self.poss = list()
        layer.fill(self.basis_color)
        x = x1
        while x < x2:

            self.poss.append(x)
            pg.draw.line(layer, self.line_color, (x+miniline_size//2, y1-sx), (x+miniline_size//2, y2+sx), 3)
            x += dx

        pg.draw.line(layer, self.line_color, (x1, y1), (x2, y2), 2)
        text = self.createText(s_name, self.name_color, 45)
        center_of_basis_and_text  = self.find_center(layer.get_size(), text.get_size())
        layer.blit(text, (center_of_basis_and_text[0], center_of_basis_and_text[1] + self.dy))
        self.scale = layer
        return self.scale

    def createCursor(self, c_size):
        cursor = pg.Surface(c_size)
        cursor.fill(self.cursor_color)
        self.cursor = cursor
        return self.cursor

    def changeCursorPos(self):
        pass


    def selected(self):
        self.SELECTED = True

    def unselected(self):
        self.SELECTED = False

    def follow(self, mous):
        self.mouse_pos = mous.get_pos()

    def update(self, i):
        poss = self.poss
        scale = self.scale
        cursor = self.cursor
        if self.SELECTED is True:
            mouse_pos = self.mouse_pos
            cursor_position = (mouse_pos[0] // 2, self.y - self.cursor_size[1] // 2)


        else:
            cursor_position = (poss[i] - self.cursor_size[0]//2, self.y - self.cursor_size[1]//2)

        self.cursor_position = cursor_position
        full_scale = scale.blit(cursor, cursor_position)
        self.full_scale = scale
        return (self.full_scale, i)


    def draw(self, surface):
        scale = pg.Surface(self.size)

        scale.blit(self.full_scale, self.location)
        surface.blit(scale, (0, 0))


class Pixel(GraphicManager):
    followed_objects = list()

    def __init__(self, objects, size):
        self.followed_objects = objects
        self.size = size


def DrawGrid(surface, block_size, color=colors.WHITE, grid_size=4):
    """DRAW GRID!"""
    grid_color = color
    x = -block_size
    y = -block_size
    surface_size = surface.get_size()

    for x_row in range(surface_size[0] // block_size + 1):
        x += block_size
        pg.draw.line(surface, grid_color, (x, 0), (x, surface_size[1]), grid_size)
    for y_row in range(surface_size[1] // block_size + 2):
        y += block_size
        pg.draw.line(surface, grid_color, (0, y), (surface_size[0], y), grid_size)


def RandomColors(count):
    colors = list()
    for c in range(count):
        R = rrange(0, 255)
        G = rrange(0, 255)
        B = rrange(0, 255)
        color = (R, G, B)
        colors.append(color)
    return colors
