from guis.gm import GraphicManager


class Pixel(GraphicManager):
    followed_objects = list()

    def __init__(self, objects, size):
        self.followed_objects = objects
        self.size = size