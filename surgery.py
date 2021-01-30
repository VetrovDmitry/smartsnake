from utils.mathmethods import SnakeBrain, Matrix
import numpy as np


def main():
    brain_mini = SnakeBrain()

    brain_mini.addLayer((81, 5))
    brain_mini.addLayer((5, 4))
    brain_mini.addLayer((4, 3))

    # x_mini = np.array([0.5, 0.77, 0.15, 1.05, 0, 0.98, -2.0, 1, 0])
    y_mini = np.array([1, 0, 0])
    y_mini_2 = np.array([0, 0, 1])
    # print(x_mini.shape)
    # brain_mini.learning(x_mini, y_mini, 0.1)
    # brain_1 = SnakeBrain()
    # #
    x_2 = Matrix((9, 9), 0.11)
    # r_x_2 = x_2.matrix
    # r_x_2 = r_x_2.reshape(1, 81)[0]
    r_x_2 = x_2.flatten()
    print(r_x_2)
    # pred_mini = brain_mini.justToThink(r_x_2)
    brain_mini.learning(r_x_2, y_mini_2, 0.12)
    # pred_mini_2 = brain_mini.justToThink(r_x_2)
    # print(pred_mini, pred_mini_2)
    # print(pred_mini)
    # print(r_x_2)
    # print(x_mini)
    # # #
    # y = np.array([0, 1, 0])
    # # #
    # brain_1.addLayer((9, 5))
    # brain_1.addLayer((5, 4))
    # brain_1.addLayer((4, 3))
    # # print(x_2.flatten().shape)
    # pred_y_1_1 = brain_1.justToThink(x_2.flatten())
    # sigma_y = y - pred_y_1_1
    # errors_1 = brain_1.errorSearch(sigma_y)
    # for err in errors_1:
    #     print(err.shape)
    # brain_1.learning(x_2.flatten(), y, 0.5)
    #
    # # for weight in weights:
    # #     print(weight, '\n')
    #
    # pred_y = brain_1.justToThink(x_2.flatten())
    # print(pred_y)
    #
    # brain_1.learning(x_2.flatten(), y, 0.1)
    #
    # pred_y = brain_1.justToThink(x_2.flatten())
    # print(pred_y)
    # sigma_1 = y - pred_y
    # print(pred_y, y)
    # print(sigma_1)

    # errors = brain_1.errorSearch(sigma_1)
    # # for error in errors:
    # #     print(error)
    #
    # weights = brain_1.remember(x, errors, 0.15)
    # # print(weights)
    # brain_1.setWeights(weights)
    # pred_y_after_trainning = brain_1.justToThink(x)
    # print('----')
    # print('\n', pred_y_after_trainning)


main()