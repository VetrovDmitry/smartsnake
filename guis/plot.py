import pygame, sys
from pygame.locals import *
import numpy
import matplotlib
from guis import colors

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
from cmath import sin


def datagen(x_range, p=1):
    X = list()
    Y = list()
    x_start = x_range[0]
    x_end = x_range[1]
    while x_start != x_end:
        X.append(float(x_start))
        y = 10*sin(x_start).real
        Y.append(y)
        x_start += p
    return numpy.column_stack([X, Y])


fig = plt.figure(figsize=[3, 3])
ax = fig.add_subplot(111)
canvas = agg.FigureCanvasAgg(fig)

def plot(data):
   ax.plot(data)
   canvas.draw()
   renderer = canvas.get_renderer()

   raw_data = renderer.tostring_rgb()
   size = canvas.get_width_height()

   return pygame.image.fromstring(raw_data, size, "RGB")

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 400))

pygame.display.set_caption('Animating Objects')
# img = pygame.image.load('head.jpg')

steps = numpy.linspace(20, 360, 40).astype(int)
right = numpy.zeros((2, len(steps)))
down = numpy.zeros((2, len(steps)))
left = numpy.zeros((2, len(steps)))
up = numpy.zeros((2, len(steps)))

right[0] = steps
right[1] = 20

down[0] = 360
down[1] = steps

left[0] = steps[::-1]
left[1] = 360

up[0] = 20
up[1] = steps[::-1]

pos = datagen((0, 1000), p=1)
print(pos)
i = 0
history = numpy.array([])
surf = plot(history)
rect_color = colors.RED
rect = pygame.Surface((10, 10))
print(pos)
while True:
   # Erase screen
    screen.fill((255, 255, 255))

    if i >= len(pos):
        i = 0
        surf = plot(history)



    # rect.fill(rect_color)
    # screen.blit(rect, pos[i])
    history = numpy.append(history, pos[i])
    screen.blit(surf, (0, 0))

    i += 1

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(10)

#
# if __name__ == "__main__":
#