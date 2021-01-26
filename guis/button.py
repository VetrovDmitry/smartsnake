from guis.gm import GraphicManager
from guis import colors


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