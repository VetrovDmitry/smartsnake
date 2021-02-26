import numpy as np
import time
import pickle
import random
from mathmethods.mathfuctions import local_mean_squared_error, sig_der, sig, stabilitron
from mathmethods.matrix import multiplyByRow


DTYPE = 'float64'


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



class Layer:
    def __init__(self, size):
        self.i1 = size[0]
        self.i2 = size[1]
        self.size = size
        self.weights = self.__createWeights(self.size)

    def __createWeights(self, size):
        new_weights = np.random.normal(0.0, 1, size)
        new_weights = np.array(new_weights, dtype=DTYPE)
        return new_weights

    def getWeights(self):
        return self.weights

    def setWeights(self, new_weights):
        if self.weights.shape == new_weights.shape:
            self.weights = np.array(new_weights, dtype=DTYPE)

    def setErrors(self, errors):
        self.errors = errors

    def getErrors(self):
        return self.errors



class SnakeBrain:
    def __init__(self, name='test'):
        self.name = name
        self.layers = list()

    def saveBrain(self, dir):
        weights = self.getWeights()
        save_path = '{0}/{1}_{2}.pickle'.format(dir, self.name, int(time.time()))
        with open(save_path, 'wb') as f:
            pickle.dump(weights, f)
            print('saved {}'.format(save_path))

    def loadBrain(self, dir, brain_name):
        brain_path = '{}/{}'.format(dir, brain_name)
        with open(brain_path, 'rb') as f:
            weights = pickle.load(f)

        for layer in weights:
            l_shape = layer.shape
            self.addLayer(l_shape)

        self.setWeights(weights)


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

    def justToThink(self, x, all_activatios=False):
        x = np.array(x, dtype=DTYPE)
        activations = [x]
        for layer in self.layers:
            input_data = activations[-1]
            current_weights = layer.weights
            activation = np.dot(current_weights.T, input_data)
            activation = sig(activation)
            activations.append(activation)

        if all_activatios:
            return activations
        else:
            return activations[-1]

    def errorSearch(self, error):
        errors = [error]
        for layer in reversed(self.layers):
            last_error = errors[-1]
            current_weights = layer.weights
            currnet_errors = np.dot(current_weights, last_error)
            currnet_errors = np.array(currnet_errors, dtype=DTYPE)
            current_mse = local_mean_squared_error(currnet_errors)
            layer.setErrors(current_mse)
            errors.append(current_mse)

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
            d_weights = np.array(d_weights)
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