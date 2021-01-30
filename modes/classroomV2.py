import pygame as pg
from gobjects.food import FoodPacker
from guis import colors
from guis.visiontablo import VisionTablo
from guis.utils import DrawGrid, renderPixels
from utils.handmade import load_params, find_center, AllSprites
from utils.gamesatisfaction import Pause, Map, WorldRulesPVE
from utils.mathmethods import Matrix, SnakeBrain
from snakemind.visitor import Visitor
from cmath import pi
import numpy as np


"""ACTIONS"""

actions = ['LEFT', 'UP', 'RIGHT']

"""PRESTART SETTINGS"""

PARAMS_PATH = 'PARAMS.json'
MODE_NAME = 'CLASSROOM_V2'
params = load_params(PARAMS_PATH)
display_settings = params.get('DISPLAY_SETTINGS')[MODE_NAME]
game_settings = params.get('GAME_SETTINGS')
CONTROLS = params.get('CONTROLS')

"""VISUALISATION SETTINGS"""

tablo = tuple(display_settings['TABLO_SIZE'])
win_size = tuple(display_settings['WIN_SIZE'])
gamefield_size = tuple(display_settings['GAMEFIELD_SIZE'])
block_size = display_settings['BLOCK_SIZE']
grid_size = display_settings['GRID_SIZE']

"""MATH-PART SETTINGS"""

gf_x_count =  gamefield_size[0] // block_size
gf_y_count =  gamefield_size[1] // block_size
gamefield_matrix_size = (gf_x_count, gf_y_count)
gf_matrix = Matrix(gamefield_matrix_size, 0)

"""VISUALISATION TEMPLATE"""


grid_color = colors.BLACK
gamefield_pos = (15, 15)
gamefield_color = colors.LIGHT_GREY
panarama_color = colors.BLACK
panarama_pos = (15+gamefield_size[0], 0)
panarama_size = (300, 300)

"""GAME OBJECTS"""
# Params

first_food_count = 5
first_food_position = (5, 5)
food_area = ((5, gamefield_matrix_size[0] - 5),
             (5, gamefield_matrix_size[1] - 5))
food_color = colors.DARK_LOSOS

visitor_first_position = (10, 10)
visitor_first_direction = (1, 0)
visitor_color = colors.GREEN
visitor_vision_angle = - pi / 2


#  Static objects

around_wall = Map(gamefield_matrix_size, block_size, circuit=True)
wall_sprites = around_wall.getSprites()


#  Food objects

food_sprites = AllSprites()
food = FoodPacker(food_area, first_food_count, food_color, block_size)
food_sprites.append(food)

#  Moving objects

moving_sprites = AllSprites()
teacher = Visitor(visitor_first_position, dir=visitor_first_direction, color=visitor_color, block_size=block_size)
teacher.setLocalAngle(visitor_vision_angle)
moving_sprites.append(teacher)

#  Smart object

x, y = teacher.viewfield_size
layer_size_1 = (x * y, 9)
layer_size_2 = (9, 5)
layer_size_3 = (5, 3)
learning_rate = 0.01

brain = SnakeBrain()
brain.addLayer(layer_size_1)
brain.addLayer(layer_size_2)
brain.addLayer(layer_size_3)


"""CREATING VISUALISATION"""

pg.init()
win = pg.display.set_mode(win_size)
pg.display.set_caption('classroom')
gamefield = pg.Surface(gamefield_size)
panarama = VisionTablo(panarama_pos, panarama_size, 15)

"""IN-GAME FUNCTIONS"""

def Controls():
    key = pg.key.get_pressed()
    if key[pg.K_ESCAPE]:
        Pause()
    if key[pg.K_KP8]:
        teacher.moveByRot('UP')
        right_answer = np.array([0, 1, 0])
        food_detector = teacher.getDetectors().get(2)
        brain.learning(food_detector.flatten(), right_answer, learning_rate)
        teacher.update()
    if key[pg.K_KP4]:
        teacher.moveByRot('LEFT')
        right_answer = np.array([1, 0, 0])
        food_detector = teacher.getDetectors().get(2)
        brain.learning(food_detector.flatten(), right_answer, learning_rate)
        teacher.update()

    if key[pg.K_KP6]:
        teacher.moveByRot('RIGHT')
        right_answer = np.array([0, 0, 1])
        food_detector = teacher.getDetectors().get(2)
        brain.learning(food_detector.flatten(), right_answer, learning_rate)
        teacher.update()
    if key[pg.K_p]:
        food.plusBlock()
    if key[pg.K_o]:
        food.minusBlock()
    if key[pg.K_r]:
        teacher.respawn((10, 10), (1, 0))

    if key[pg.K_u]:
        food_detector = teacher.getDetectors().get(2)
        answer = brain.justToThink(food_detector.flatten())
        print(answer)



def start():
    global gf_matrix

    GAME = True
    clock = pg.time.Clock()
    while GAME:
        pg.time.delay(10)
        clock.tick(10)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                GAME = False

        """SCANNING"""

        Controls()

        """LOGIC"""
        moment_color = colors.RAINBOW_1()

        WorldRulesPVE(moving_sprites, food_sprites, wall_sprites)
        panarama.update(moment_color)
        """FORMATING MATRIX"""

        gf_matrix.refresh()
        gf_matrix = wall_sprites.print_to_matrix(gf_matrix)
        gf_matrix = food_sprites.print_to_matrix(gf_matrix)
        gf_matrix = moving_sprites.print_to_matrix(gf_matrix)

        #  Teacher updating

        teacher.updateVision(gf_matrix)
        viewfield_matrix = teacher.getVisionScreen()
        detectors_matrix = teacher.getDetectors()
        panarama.drawFromMatrix(viewfield_matrix, 0)
        panarama.drawFromMatrix(detectors_matrix[1], 1)
        panarama.drawFromMatrix(detectors_matrix[2], 2)
        panarama.drawFromMatrix(detectors_matrix[3], 3)

        #  Brain teaching

        food_detector = teacher.getDetectors().get(2)
        brain_answer = brain.justToThink(food_detector.flatten())

        """RENDERING"""


        win.fill(moment_color)
        gamefield.fill(colors.GREY)
        wall_sprites.draw(gamefield)
        food_sprites.draw(gamefield)
        moving_sprites.draw(gamefield)
        DrawGrid(gamefield, block_size, moment_color, grid_size)
        win.blit(gamefield, gamefield_pos)
        panarama.draw(win)
        pg.display.update()


start()

pg.quit()