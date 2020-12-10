import pygame as pg
from objects import FoodPacker, Wall
from guiparts import GraphicManager, DrawGrid, Tablo, RandomColors
from handmade import AllSprites, getParams, renderPixels, smart_pos_for_area
from mathmethods import Matrix
from snake_mind import SmartSnake
from gamesatisfaction import WorldRules, Map
import colors


pg.init()


"""PRESETTINGS"""

DISPLAY_SETTINGS = getParams('DISPLAY_SETTINGS')
GAME_SETTINGS = getParams('GAME_SETTINGS')
CONTROLS = getParams('CONTROLS')

TABLO_SIZE = tuple(DISPLAY_SETTINGS['TABLO_SIZE'])
WIN_SIZE = tuple(DISPLAY_SETTINGS['WIN_SIZE'])
GAMEFIELD_SIZE = tuple(DISPLAY_SETTINGS['GAMEFIELD_SIZE_LAB'])
GF_PIXELS = tuple(DISPLAY_SETTINGS['GF_PIXELS'])
SNAKE_VIEWFIELD_SIZE = DISPLAY_SETTINGS['SNAKE_VIEWFIELD_SIZE']
BLOCK_SIZE = DISPLAY_SETTINGS['BLOCK_SIZE']
iteration = 0

"""UTILS"""

def Pause():
    pause = True
    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                pause = False


class Controls:
    def scanEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse(event)
            elif event.type == pg.KEYDOWN:
                self.keyboard(event)

    def mouse(self, event):
        if event.button == 1:
            pos = pg.mouse.get_pos()
            pixel_mouse = (pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE)

    def keyboard(self, event):
        key = str(event.key)


def main():
    snake_first_count = 10
    food_count = 66
    standart_tick = 10
    GAME = True
    gf_color = colors.WHITE
    grid_size_1 = 1
    gf_size_normal = (GAMEFIELD_SIZE[0] + grid_size_1 // 2,
                      GAMEFIELD_SIZE[1] + grid_size_1 // 2)
    gf_pixel_count_x = GAMEFIELD_SIZE[0] // BLOCK_SIZE
    gf_pixel_count_y = GAMEFIELD_SIZE[1] // BLOCK_SIZE
    gamefield_matrix_size = (gf_pixel_count_x, gf_pixel_count_y)

    wall_color_1 = colors.DARK_BLUE
    wall_color_2 = colors.DARK_BROWN
    food_color_1 = colors.RED
    snake_colors = RandomColors(snake_first_count)
    grid_color_1 = colors.BLACK

    farea_1 = [[3, 57], [3, 33]]

    win = pg.display.set_mode(WIN_SIZE)
    gamefield = pg.Surface(gf_size_normal)

    around_wall = Map(gamefield_matrix_size, BLOCK_SIZE, circuit=True)
    wall_sprites = around_wall.getSprites()

    food_sprites = AllSprites()
    food_sprites.append(FoodPacker(farea_1, food_count, food_color_1, BLOCK_SIZE))

    moving_sprites = AllSprites()


    for snake in range(snake_first_count):
        new_coors = smart_pos_for_area()
        new_snake = SmartSnake()