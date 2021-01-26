from guis.gm import GraphicManager
from guis import colors


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
