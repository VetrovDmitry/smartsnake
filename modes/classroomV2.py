import pygame as pg
from gobjects.food import FoodPacker
from guis import colors
from guis.utils import render, DrawGrid
from utils.handmade import load_params, find_center, AllSprites
from utils.gamesatisfaction import Pause, Map, WorldRulesPVE
from utils.mathmethods import Matrix
from snakemind.visitor import Visitor
from cmath import pi


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
gamefield_pos = find_center(win_size, gamefield_size)
gamefield_color = colors.LIGHT_GREY

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

"""CREATING VISUALISATION"""

pg.init()
win = pg.display.set_mode(win_size)
pg.display.set_caption('classroom')
gamefield = pg.Surface(gamefield_size)

"""IN-GAME FUNCTIONS"""

def Controls():
    key = pg.key.get_pressed()
    if key[pg.K_ESCAPE]:
        Pause()
    if key[pg.K_w]:
        teacher.moveByRot('UP')
        teacher.update()
    if key[pg.K_a]:
        teacher.moveByRot('LEFT')
        teacher.update()
    if key[pg.K_d]:
        teacher.moveByRot('RIGHT')
        teacher.update()
    if key[pg.K_r]:
        teacher.respawn((10, 10), (1, 0))
    if key[pg.K_u]:
        teacher_screen = teacher.getVisionScreen()
        teacher_screen.prettyPrint()


def start():
    global gf_matrix

    GAME = True
    clock = pg.time.Clock()
    while GAME:
        pg.time.delay(10)
        clock.tick(7)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                GAME = False

        """SCANNING"""

        Controls()

        """LOGIC"""

        WorldRulesPVE(moving_sprites, food_sprites, wall_sprites)

        """FORMATING MATRIX"""

        gf_matrix.refresh()
        gf_matrix = wall_sprites.print_to_matrix(gf_matrix)
        gf_matrix = food_sprites.print_to_matrix(gf_matrix)
        gf_matrix = moving_sprites.print_to_matrix(gf_matrix)
        teacher.updateVision(gf_matrix)

        """RENDERING"""

        moment_color = colors.RAINBOW_1()
        win.fill(moment_color)
        gamefield.fill(colors.GREY)
        wall_sprites.draw(gamefield)
        food_sprites.draw(gamefield)
        moving_sprites.draw(gamefield)
        DrawGrid(gamefield, block_size, moment_color, grid_size)
        win.blit(gamefield, gamefield_pos)
        pg.display.update()


start()

pg.quit()