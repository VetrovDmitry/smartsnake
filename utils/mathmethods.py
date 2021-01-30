import numpy as np
from cmath import sin, cos, acos, asin, pi
import random
import time



def angleToDirection(angle):
    dir_x = int(cos(angle).real)
    dir_y = int(sin(angle).real)
    return (dir_x, dir_y)

def posToLoc(pos, pixel_size):
    x = pos[0] * pixel_size
    y = pos[1] * pixel_size
    return (x, y)

def sig(x):
    sig_x = 1 / (1 + np.exp(-x))
    return sig_x

def sig_der(x):
    return x * (1 - x)


def stabilitron(x):
    if x >= 0.85:
        y = 1
    else:
        y = 0
    return y


def multiplyByRow(matrix_1, matrix_2):
    if len(matrix_1) == len(matrix_2):
        new_matrix = list()
        for i, row_1 in enumerate(matrix_1):
            row_2 = matrix_2[i]
            row = row_1 * row_2
            new_matrix.append(row)

        response = np.array(new_matrix)
    else:
        response = False

    return response


class Matrix:
    edge_pos = (0, 0)

    def __init__(self, m_size, substrate=0):
        self.size = m_size
        self.substrate = substrate
        self.matrix = self.createMatrix(m_size, substrate)

    def reshape(self, new_shape):
        self.matrix = self.matrix.reshape(new_shape)

    def T(self):
        return self.matrix.T

    def refresh(self):
        self.matrix = self.createMatrix(self.size, self.substrate)

    def createMatrix(self, size, substrate):
        n = size[1]
        m = size[0]
        matrix = list()
        for row in range(n):
            r = list()
            for column in range(m):
                r.append(substrate)
            matrix.append(r)

        matrix = np.array(matrix)
        return matrix

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

def centerToEdge(m_size, pos):
    if m_size[0] % 2 != 0 and m_size[0] == m_size[1]:
        dx = int(m_size[0] // 2)
        dy = int(m_size[1] // 2)
        edge_x = pos[0] - dx
        edge_y = pos[1] - dy
        return (edge_x, edge_y)
    else:
        pass


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


def radToDegrees(rads):
    degrees = 180 * rads / pi
    return degrees


class Layer:
    def __init__(self, size):
        self.i1 = size[0]
        self.i2 = size[1]
        self.size = size
        self.weights = self.__createWeights(self.size)

    def __createWeights(self, size):
        new_weights = np.random.normal(0.0, 1, size)
        return new_weights

    def getWeights(self):
        return self.weights

    def setWeights(self, new_weights):
        if self.weights.shape == new_weights.shape:
            self.weights = new_weights

    def setErrors(self, errors):
        self.errors = errors

    def getErrors(self):
        return self.errors



class SnakeBrain:
    def __init__(self):
        self.layers = list()

    def getLen(self):
        return len(self.layers)

    def addLayerWithWeights(self, weights):
        layer = Layer(weights.shape)
        layer.setWeights(weights)
        self.layers.append(layer)

    def addLayer(self, layer_size):
        self.layers.append(Layer(layer_size))

    def newBrain(self):
        new_brain_wights = self.getWeights()
        return new_brain_wights

    def predict(self, X):
        pass

    def reshapeInput(self, x):
        m, n = x.shape
        new_x = x
        new_x.reshape((m * n, 1))
        return new_x

    def justToThink(self, x):
        activations = [x]
        for layer in self.layers:
            input_data = activations[-1]
            current_weights = layer.weights
            activation = np.dot(current_weights.T, input_data)
            activation = sig(activation)
            activations.append(activation)
        return activations[-1]

    def errorSearch(self, error):
        errors = [error]
        for layer in reversed(self.layers):
            last_error = errors[-1]
            current_weights = layer.weights
            currnet_errors = np.dot(current_weights, last_error)
            layer.setErrors(currnet_errors)
            errors.append(currnet_errors)

        return errors[:-1]


    def __stabilize(self, matrix):
        if matrix.shape == (matrix.shape[0], ):
            matrix = matrix.reshape((matrix.shape[0], 1))
        return matrix

    def stb(self, matrix):
        return self.__stabilize(matrix)


    def remember(self, x, rev_errors, lr):
        x = self.__stabilize(x)
        true_activations = [x]
        true_weights = list()
        for i, err in enumerate(reversed(rev_errors)):

            activation = true_activations[-1]
            x_der_x = multiplyByRow(activation, sig_der(activation))
            err = self.__stabilize(err)
            d_weights = np.dot(x_der_x, err.T)
            d_weights = np.dot(d_weights, lr)
            current_weights = self.getWeights()[i]
            new_weights = current_weights + d_weights

            new_activation = np.dot(new_weights.T, activation)
            true_activations.append(new_activation)
            true_weights.append(new_weights)
            # break
            # self.setWeights(true_weights)

        self.setWeights(true_weights)

        return true_weights

    def setWeights(self, new_weights):
        # print(len(new_weights))
        # print(len(self.layers))
        for i, layer in enumerate(self.layers):
            current_new_weights = new_weights[i]
            layer.setWeights(current_new_weights)

    def printErrors(self):
        for layer in self.layers:
            print(layer.getErrors())
            print('_________')

    def getWeights(self):
        weights = list()
        for layer in self.layers:
            weights.append(layer.getWeights())

        return weights


    def studing(self, x, learning_rate=0.1):
        pred_y = self.justToThink(x)
        pred_y = np.array(pred_y)
        stab_y = np.array(list(map(stabilitron, pred_y)))

        sigma_1 = stab_y - pred_y.T
        reversed_errors = self.errorSearch(sigma_1.T)[:-1]
        self.remember(x, reversed_errors, learning_rate)
        stabile_output = self.justToThink(x)
        stab_y_2 = np.array(list(map(stabilitron, pred_y)))
        sigma_2 = stab_y_2 - stabile_output.T
        print(sigma_1, sigma_2)
        return stabile_output

    def learning(self, x, y, learning_rate=0.1):
        pred_y = self.justToThink(x)
        sigma_1 = y - pred_y
        reversed_error = self.errorSearch(sigma_1)
        true_weights = self.remember(x, reversed_error, learning_rate)
        pred_y_2 = self.justToThink(x)
        print('true: {0}, pred_1: {1}, pred_2: {2}'.format(y, pred_y, pred_y_2))
        return true_weights
        # answer_check = self.justToThink(x)

    def train(self, X, Y, epochs):
        for epoch in range(epochs):
            pass

    def play(self, x, learn=False, lr=0.1):
        if learn:
            move = self.studing(x, lr)
        else:
            move = self.justToThink(x)

        return move

    def evolution(self):
        pass


JASA = {
    (1, 5) : 1,
    (6, 12) : 2,
    (13, 20): 3,
    (21, 30): 4,
    (31, 45): 6,
    (46, 60): 7,
    (61, 76): 8,
    (77, 95): 10,
    (96, 122): 11
}


def checkCount(size):
    for event in JASA.keys():
        if size >= event[0] and size <= event[1]:
            return JASA.get(event)
        else:
            return 12


def newGen(brain):
    i = 0
    if int(time.time()) % 7 == 0:
        size = len(brain)
        rand_i = random.randrange(0, size-1)
        layer = brain[rand_i]
        m, n = layer.shape
        size = m * n
        count = checkCount(size)
        for mutation in range(count):
            rand_m = random.randrange(0, m-1)
            rand_n = random.randrange(0, n-1)
            layer[rand_m, rand_n] += random.randrange(-1, 1) // 100
        brain[rand_i] = layer
        i = 1
    return (brain, i)


def brainFromWeights(weights_pack):
    brain = SnakeBrain()
    for weights in weights_pack:
        brain.addLayerWithWeights(weights)
    return brain




if __name__ == '__main__':
    viewfield = Matrix((11, 11), 0)
    viewfield.matrix[1][2] = 1
    viewfield.matrix[7][6] = 1
    viewfield.matrix[1][10] = 1

    viewfield.prettyPrint()
    viewfield.reshape((121, 1))
    viewfield.prettyPrint()
    brain_1 = SnakeBrain()
    brain_1.addLayer((121, 66))
    brain_1.addLayer((66, 30))
    brain_1.addLayer((30, 3))

    ans = brain_1.justToThink(viewfield.matrix)
    print(ans)
    # r = brain_1.studing(viewfield.matrix)
    # print(sys.getsizeof(brain_1))

    # brain_2 = brainFromWeights(brain_1.newBrain())
    #
    # print(brain_2.getWeights())

