import numpy as np
from cmath import sin, cos, acos, asin, pi

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
        self.matrix.T

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

    def rotate(self, angle_of_rotation):

        matrix = self.matrix
        if angle_of_rotation < 0:
            angle_of_rotation += 360

        rotations = int(angle_of_rotation // 90)
        #

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
    def __init__(self, size, input_dim=1):
        self.i1 = size[0]
        self.i2 = size[1]
        self.size = size * input_dim
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


def sig(x):
    return 1 / (1 + np.exp(-x))

def sig_der(x):
    return x * (1 - x)

def stabilitron(x):
    if x >= 0.85:
        y = 1
    else:
        y = 0
    return y

class SnakeBrain:
    def __init__(self):
        self.layers = list()

    def getLen(self):
        return len(self.layers)

    def addLayer(self, layer_size):
        self.layers.append(Layer(layer_size))

    def predict(self, X):
        pass

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
        layers = self.layers

        for layer in reversed(layers):
            last_error = errors[-1]
            current_weights = layer.weights
            currnet_errors = np.dot(current_weights, last_error)
            layer.setErrors(currnet_errors)
            errors.append(currnet_errors)

        return errors

    def remember(self, x, rev_errors, lr):
        true_activations = [x]
        true_weights = list()
        for i, err in enumerate(reversed(rev_errors)):
            input_i = true_activations[-1]
            d_input_i = sig_der(input_i)
            dd_input = multiplyByRow(input_i, d_input_i)
            current_weights = self.layers[i].weights
            current_errors = err
            sigma_d_weights_i = np.dot(dd_input, current_errors.T)
            sigma_d_weights_i = np.dot(lr, sigma_d_weights_i)
            new_weights = current_weights + sigma_d_weights_i
            output_1 = sig(np.dot(new_weights.T, input_i))
            true_activations.append(output_1)
            self.layers[i].setWeights(new_weights)
        return true_weights


    def printErrors(self):
        for layer in self.layers:
            print(layer.getErrors())
            print('_________')


    def studing(self, x, learning_rate=0.01):
        pred_y = self.justToThink(x)
        pred_y = np.array(pred_y)
        stab_y = np.array(list(map(stabilitron, pred_y)))
        sigma = stab_y - pred_y.T
        reversed_errors = self.errorSearch(sigma.T)[:-1]

        self.remember(x, reversed_errors, learning_rate)
        stabile_output = self.justToThink(x)
        return stabile_output


    def train(self, X, Y, epochs):
        for epoch in range(epochs):
            pass

    def play(self, detector, learn=False, lr=0.1):
        m, n = detector.shape
        input = detector.reshape((m * n, 1))
        if learn:
            move = self.studing(input, lr)
        else:
            move = self.justToThink(detector)

        return move




if __name__ == '__main__':
    detector_1 = Matrix((9, 9), 8)
    detector_1.reshape([81, 1])
    detector_2 = Matrix((9, 9), 1)
    detector_2.reshape([81, 1])

    brain_1 = SnakeBrain()
    brain_1.addLayer((81, 30))
    brain_1.addLayer((30, 15))
    brain_1.addLayer((15, 3))

    activations_1 = brain_1.justToThink(detector_1.matrix)

    brain_1.studing(detector_1.matrix)


    # brain_2 = SnakeBrain()
    # brain_2.addLayer((2, 3))
    # brain_2.addLayer((3, 2))
    # brain_2.addLayer((2, 1))
    #
    # activations_2 = brain_2.justToThink([2, 1])

    # print(activations_2)
    # for act in activations_2:
    #     print(act)
    #     print("_______________")


    # brain_2.errorSearch(10)
    # brain_2.printErrors()

    # print(activations)
    # f = brain_1.layers[0]
    # output_1 = np.dot(f.weights.T, detector_1.matrix)
    # print(output_1)
    # output_2 = np.dot(f.weights.T, detector_2.matrix)
    # print(output_2)
    # print(sigmoid(output_2))
    # output_3 = np.dot(f.weights.T, detector_3.matrix)
    # print(output_3)

    # # print(122, np.dot(f.weights.T, 1))



