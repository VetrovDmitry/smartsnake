import pygame as pg
from mathmethods.matrix import Matrix
from utils.handmade import load_params, find_center, randomXY
from guis import colors
from guis.visiontablo import VisionTablo
from guis.tablo import Tablo
from snakemind.visitor import Visitor


"""PRESTART SETTINGS"""

PARAMS_PATH = 'PARAMS.json'

MODE_NAME = 'PHOTOSTUDIO'
PARAMS = load_params(PARAMS_PATH)
display_settings = PARAMS.get('DISPLAY_SETTINGS')[MODE_NAME]
game_settings = PARAMS.get('GAME_SETTINGS')

"""VISUALUSATION SETTINGS"""
tablo_size = tuple(display_settings['TABLO_SIZE'])
win_size = tuple(display_settings['WIN_SIZE'])
grid_size = display_settings['GRID_SIZE']
viewfield_size = display_settings['VIEWFIELD_SIZE']
viewfield_pos = find_center(win_size, viewfield_size)
collections_status = '{}/{}'


"""MATRIX SETTINGS"""
K = 1
matrix_size = display_settings['MATRIX_SIZE']
viewfield_matrix = Matrix(matrix_size)
matrix_center = (matrix_size[0] // 2, matrix_size[1] // 2)
ready_positions = [matrix_center]

"""CREATING VISUALISATION"""

pg.init()

win = pg.display.set_mode(win_size)
pg.display.set_caption('photostudio')
panarama = VisionTablo(viewfield_pos, viewfield_size, 15)
count_tablo = Tablo('EXAMPLES', tablo_size, (1, 1))
"""OBJECTS"""
shot_count = matrix_size[0] * matrix_size[1] - 1
photographer = Visitor((0, 0), dir=(0, -1), color=colors.BROWN)

def movePixel():
    success = False
    while success is not True:
        new_pos = randomXY(matrix_size)
        if new_pos not in ready_positions:
            y, x = new_pos
            viewfield_matrix.refresh()
            viewfield_matrix.fillByPos(x, y, K)
            ready_positions.append(new_pos)
            success = True

def shot(choice):
    viewfield_matrix.prettyPrint()
    print(choice)
    movePixel()

def Conrols():
    key = pg.key.get_pressed()
    if key[pg.K_c]:
        movePixel()

    if key[pg.K_KP8]:
        choice = [0, 1, 0]
        shot(choice)
    elif key[pg.K_KP4]:
        choice = [1, 0, 0]
        shot(choice)
    elif key[pg.K_KP6]:
        choice = [0, 0, 1]
        shot(choice)


def start():
    GAME = True
    # viewfield_matrix.fillByPos(2, 1, 1)
    clock = pg.time.Clock()
    while GAME:
        pg.time.delay(15)
        clock.tick(5)
        moment_color = colors.RAINBOW_1()

        """SCANNING"""

        for event in pg.event.get():
            if event.type == pg.QUIT:
                GAME = False

        Conrols()

        """UPDATING"""
        panarama.update(moment_color)
        photographer.updateViewfield(viewfield_matrix)
        detectors_matrix = photographer.getDetectors()
        panarama.drawFromMatrix(viewfield_matrix, 0)
        panarama.drawFromMatrix(detectors_matrix[1], 1)
        panarama.drawFromMatrix(detectors_matrix[2], 2)
        panarama.drawFromMatrix(detectors_matrix[3], 3)

        count_tablo.update(collections_status.format(len(ready_positions) - 1, shot_count), False, moment_color)
        win.fill(moment_color)
        panarama.draw(win)
        count_tablo.draw(win)
        #
        pg.display.update()



start()

pg.quit()
# pg.init()

