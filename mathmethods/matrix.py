import numpy as np


DTYPE = 'float64'


def centerToEdge(m_size, pos):
    if m_size[0] % 2 != 0 and m_size[0] == m_size[1]:
        dx = int(m_size[0] // 2)
        dy = int(m_size[1] // 2)
        edge_x = pos[0] - dx
        edge_y = pos[1] - dy
        return (edge_x, edge_y)
    else:
        pass

def createFullMatrixFromTemplate(template):
    t_size = template.getShape()
    full_matrix_size_x = 2 * t_size[1] - 1
    full_matrix_size_y = 2 * t_size[0] - 1
    matrix_size = (full_matrix_size_y, full_matrix_size_x)
    full_matrix = Matrix(matrix_size)
    full_matrix.createParts(t_size)
    first_part = template
    full_matrix.addPart(first_part.matrix, 0)
    template.rotate(90)
    second_part = template
    full_matrix.addPart(second_part.matrix, 1)
    template.rotate(90)
    thrid_part = template
    full_matrix.addPart(thrid_part.matrix, 2)
    template.rotate(90)
    four_part = template
    full_matrix.addPart(four_part.matrix, 3)
    full_matrix.normalizeMatrix()
    return full_matrix


def multiplyByRow(matrix_1, matrix_2):
    if matrix_1.shape == matrix_2.shape:
        new_matrix = list()
        for i, row_1 in enumerate(matrix_1):
            row_2 = matrix_2[i]
            row = row_1 * row_2
            new_matrix.append(row)

        response = np.array(new_matrix, dtype='float32')
    else:
        response = False

    return response


def localExtractor(M1, M2, position):
    M_m = M1.size[1]
    M_n = M1.size[0]

    m_size = M2.size
    edge_pos = centerToEdge(m_size, position)

    edge_x1 = edge_pos[0]
    edge_x2 = edge_x1 + m_size[0]
    edge_y1 = edge_pos[1]
    edge_y2 = edge_y1 + m_size[1]

    M2.refresh()

    for m, row in enumerate(range(edge_y1, edge_y2)):
        for n, column in enumerate(range(edge_x1, edge_x2)):
            if column >= 0 and column < M_n:
                if row >= 0 and row < M_m:
                    try:

                        M2.matrix[m][n] = M1.matrix[row][column]
                    except:
                        print(column, row)
                else:
                    M2.matrix[m][n] = 0
            else:
                M2.matrix[m][n] = 0
    return M2


class Parts:
    def __init__(self, part_size):
        self.locations = self.__createLoc(part_size)

    def __createLoc(self, size):
        locs = dict()
        locs[0] = (0, 0)
        locs[1] = (size[0] - 1, 0)
        locs[2] = (size[0] - 1, size[1] - 1)
        locs[3] = (0, size[1] - 1)
        return locs


class Matrix:
    edge_pos = (0, 0)
    def __init__(self, m_size, substrate=0):
        self.size = m_size
        self.substrate = substrate
        self.matrix = self.createMatrix(m_size, substrate)

    def createMatrixFromArray(self, array):
        self.matrix = array

    def reshape(self, new_shape):
        self.matrix = self.matrix.reshape(new_shape)

    def T(self):
        return self.matrix.T

    def normalizeMatrix(self):
        self.matrix = self.matrix / 100

    def refresh(self):
        self.matrix = self.createMatrix(self.size, self.substrate)

    def createParts(self, size):
        self.parts = Parts(size)

    def addPart(self, part, part_number):
        part_loc = self.parts.locations[part_number]
        for m, row in enumerate(part):
            for n, value in enumerate(row):
                global_m = m + part_loc[0]
                global_n = n + part_loc[1]
                self.fillByPos(global_n, global_m, value)

    def createMatrix(self, size, substrate):
        n = size[1]
        m = size[0]
        matrix = list()
        for row in range(n):
            r = list()
            for column in range(m):
                r.append(substrate)
            matrix.append(r)

        matrix = np.array(matrix, dtype=DTYPE)
        return matrix


    def getShape(self):
        return self.matrix.shape


    def fillByPos(self, x, y, value):
        if x <= self.size[1] - 1 and y <= self.size[0] - 1:
            self.matrix[y][x] = value
        else:
            pass

    def prettyPrint(self):
        print(self.matrix)

    def appendX(self, x):
        self.matrix = np.append(self.matrix, x)

    def rotate(self, angle_of_rotation):

        matrix = self.matrix
        if angle_of_rotation < 0:
            angle_of_rotation += 360

        rotations = int(angle_of_rotation // 90)
        if self.size[0] == self.size[1]:
            for rotation in range(rotations):
                matrix = np.rot90(matrix)

            self.matrix = matrix

    def Pdraw(self):
        matrix = self.matrix
        pixels = list()
        types = list()
        for m, y in enumerate(matrix):
            for n, x in enumerate(y):
                pixels.append(((n, m)))
                types.append(x)

        return (pixels, types)

    def setCenter(self, new_value):
        rows = len(self.matrix)
        columns = len(self.matrix[0])
        center_x = columns // 2
        center_y = rows // 2
        self.matrix[center_y][center_x] = new_value

    def flatten(self):
        m, n = self.matrix.shape
        new_shape = (1, m * n)
        new_matrix = self.matrix.reshape(new_shape)
        return new_matrix[0]