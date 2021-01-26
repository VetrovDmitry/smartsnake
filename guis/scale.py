from guis.gm import GraphicManager
from guis import colors
import pygame as pg

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