import sqlite3
import os
from mathmethods.matrix import Matrix
import json
import time


class ImageBase:
    def __init__(self):
        pass

    def setPath(self, new_path):
        self.__absolute_path = new_path

    def createBase(self, name):
        self.setPath(name+'.db')
        self.connect()
        cursorObj = self.connection.cursor()
        cursorObj.execute('CREATE TABLE images(id integer, image text, meta text)')
        self.connection.commit()

    def connectTo(self, db_name):
        self.setPath(db_name+'.db')
        self.connect()

    def connect(self):
        self.connection = sqlite3.connect(self.__absolute_path)

    def insertImage(self, image, meta):
        image = json.dump({'image': image})
        meta = json.dump({'meta': meta})
        entity = (0, image, meta)
        cursorObj = self.connection.cursor()
        cursorObj.execute('INSERT INTO images(id, image, meta) VALUES(?, ?, ?)', entity)
        self.connection.commit()




if __name__ == '__main__':
    db_name = 'image22s'
    matrix = Matrix((11, 11))
    flatten_matrix = matrix.flatten()
    IB = ImageBase()
    IB.createBase(db_name)
    IB.insertImage(flatten_matrix, [0, 1, 0])








