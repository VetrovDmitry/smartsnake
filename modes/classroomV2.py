import pygame as pg
import json
import os
from utils.handmade import load_params, find_center
from guis import colors
from guis.utils import render
from utils.gamesatisfaction import Pause
from gobjects.snake import Snake

"""PRESTART SETTINGS"""

PARAMS_PATH = 'PARAMS.json'
params = load_params(PARAMS_PATH)

display_settings = params.get('DISPLAY_SETTINGS')
game_settings = params.get('GAME_SETTINGS')
CONTROLS = params.get('CONTROLS')

"""VISUALISATION SETTINGS"""

tablo = tuple(display_settings['TABLO_SIZE_LAB2'])
win_size = tuple(display_settings['WIN_SIZE_CLASSROOM'])
gamefield_size = tuple(display_settings['GAMEFIELD_SIZE_LAB2'])
gf_pixels = tuple(display_settings['GF_PIXELS_LAB2'])
snake_viewfield_size = tuple(display_settings['SNAKE_VIEWFIELD_SIZE'])
block_size = display_settings['BLOCK_SIZE_LAB2']




"""IN-GAME FUNCTIONS"""
def Controls():
    key = pg.key.get_pressed()
    if key[pg.K_ESCAPE]:
        Pause()
    if key[pg.K_s]:
        teacher.move((0, 1))



"""VISUALISATION TEMPLATE"""
grid_size = 2
grid_color = colors.BLACK
gamefield_pos = find_center(win_size, gamefield_size)
gamefield_color = colors.DARK_LOSOS

pg.init()

win = pg.display.set_mode(win_size)
pg.display.set_caption('classroom')
gamefield = pg.Surface(gamefield_size)



"""GAME OBJECTS"""

teacher = Snake((10, 10), color=colors.GREEN, block_size=20, dir=(1, 0))



def start():
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

        teacher.update()

        """RENDERING"""

        win.fill(colors.RAINBOW_1())
        gamefield.fill(gamefield_color)
        render(gamefield, teacher)

        win.blit(gamefield, gamefield_pos)
        pg.display.update()


start()

pg.quit()