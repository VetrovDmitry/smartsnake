from guis.gm import GraphicManager
from guis import colors
import pygame as pg

class Tablo(GraphicManager):
    """TABLO SHOWS MOMENT PARAMS"""
    text_color = colors.BLACK
    name_size = 25
    count_size = 50

    def __init__(self, label, size, loc, background_color=colors.GREY, plus_color=colors.WHITE):
        self.label = label
        self.size = size
        self.setLocation(loc)
        self.background_color = background_color
        self.plus_color = plus_color

    def get_highs(self):
        return 0

    def changeBGColor(self, new_color):
        self.background_color = new_color

    def update(self, count, status):
        pass
        # layer.fill(self.background_color)
        #
        # if status:
        #     self.text_color = self.plus_color
        # else:
        #     self.text_color = colors.BLACK
        #
        # table_name = self.createRotateText(self.label, self.text_color, self.name_size)
        # text_size = table_name.get_size()
        # center_1 = self.find_center(self.size, text_size)
        # layer.blit(table_name, (1, center_1[1]))
        #
        # count_text = self.createText(count, self.text_color, self.count_size)
        # count_text_size = count_text.get_size()
        # center_2 = self.find_center(self.size, count_text_size)
        # layer.blit(count_text, center_2)
        # self.layer = layer

    def draw(self, surface):
        surface.blit(self.layer, self.location)


class Tabloes:
    def __init__(self, labels, l_size, d, orientation='horizontal'):
        self.labels = labels
        self.size = l_size
        self.d = d
        self.base = self.__createLayer(l_size)
        self.markup, self.table_size = self.__createMarkup(l_size, len(labels), orientation)
        self.tables = self.__createTables(labels, self.markup, self.table_size)


    def __createLayer(self, size):
        base = pg.Surface(size)
        return base

    def __createMarkup(self, size, count, orientation):
        markup = list()
        if orientation == 'horizontal':
            table_size_x = size[0] // count - self.d
            table_size_y = self.size[1]
            for i, table in enumerate(range(count)):
                table_pos = (i * (table_size_x + self.d), 0)
                markup.append(table_pos)

        elif orientation == 'vertical':
            table_size_x = self.size[0]
            table_size_y = size[1] // count - self.d
            for i, table in enumerate(range(count)):
                table_pos = (0, i * (table_size_x + self.d))
                markup.append(table_pos)
        else:
            table_size_x = 150
            table_size_y = 100

        table_size = (table_size_x, table_size_y)
        return (markup, table_size)

    def __createTables(self, names, markup, table_size):
        tables = list()
        for i, name in enumerate(names):
            table_pos = markup[i]
            tables.append(Tablo(name, table_size, table_pos))

        return tables

    def getMarkup(self):
        return self.markup

    def update(self, infos):
        for i, table in enumerate(self.tables):
            table.update(infos[i], False)

    def draw(self, surface, loc):
        self.base.fill(colors.YELLOW)
        for table in self.tables:
            table.draw(self.base)

        surface.blit(self.base, loc)



