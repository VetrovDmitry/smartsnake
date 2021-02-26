from abc import ABC

class GameObject(ABC):
    blocks = list()

    def getAllPos(self):
        all_pos = list()
        for element in self.blocks:
            all_pos.append(element.getPosition())
        return all_pos

    def changeColor(self, new_color):
        for block in self.blocks:
            block.changeColor(new_color)

    def draw(self):
        blocks = list()
        for segment in self.blocks:
            blocks.append(segment.draw())
        return blocks