from guis.gm import GraphicManager
import pygame as pg
from guis import colors
from guis.utils import detections_colors, renderPixels, DrawGrid


class VisionTablo(GraphicManager):
    def __init__(self, location, size, line_size):
        self.setLocation(location)
        self.size = size
        self.createBackground(size)
        # self.fillBackground(colors.WHITE)
        self.__setFat(line_size)
        self.__setTemplate()

    def __setFat(self, line_size):
        self.line_size = line_size
        self.display_size = (self.size[0] - 3 * line_size)/2

    def __setTemplate(self):
        pos_1_1 = (self.line_size, self.line_size)
        pos_1_2 = (2 * self.line_size + self.display_size, self.line_size)
        pos_2_1 = (self.line_size, 2 * self.line_size + self.display_size)
        pos_2_2 = (2 * self.line_size + self.display_size,
                   2 * self.line_size + self.display_size)
        self.template = [pos_1_1, pos_1_2, pos_2_1, pos_2_2]

    def __setPixelSize(self):
        pass

    def drawFromMatrix(self, matrix, num):
        matrix_dsize = matrix.matrix.shape[0]
        pixel_size = int(self.display_size // matrix_dsize)
        pixels_poss, pixel_types = matrix.Pdraw()
        display_pos = self.template[num]
        self.display_size = pixel_size * matrix_dsize
        display = self.createRect((self.display_size, self.display_size))
        renderPixels(display, pixels_poss, pixel_types, pixel_size)
        DrawGrid(display, pixel_size, self.moment_color, grid_size=1)
        self.background.blit(display, display_pos)


    def update(self, moment_color):
        self.moment_color = moment_color
        self.fillBackground(moment_color)


