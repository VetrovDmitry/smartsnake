from objects import Snake, Food, Wall
from guiparts import GraphicManager, Tablo, DrawGrid, Scale
from handmade import AllSprites, getParams, render
import colors
import numpy as np
import pygame as pg


pg.init()

"""PRESETTINGS"""

DISPLAY_SETTINGS = getParams('DISPLAY_SETTINGS')
GAME_SETTINGS = getParams('GAME_SETTINGS')
CONTROLS = getParams('CONTROLS')

TABLO_SIZE = tuple(DISPLAY_SETTINGS['TABLO_SIZE'])
WIN_SIZE = tuple(DISPLAY_SETTINGS['WIN_SIZE'])
GAMEFIELD_SIZE = tuple(DISPLAY_SETTINGS['GAMEFIELD_SIZE_LAB'])
SNAKE_VIEWFIELD_SIZE = tuple(DISPLAY_SETTINGS['SNAKE_VIEWFIELD_SIZE'])
BLOCK_SIZE = DISPLAY_SETTINGS['BLOCK_SIZE']
S_VIEWFIELD_SIZE = (SNAKE_VIEWFIELD_SIZE[0] * BLOCK_SIZE + 2, SNAKE_VIEWFIELD_SIZE[1] * BLOCK_SIZE + 2)
"""UTILS"""

def get_all_positions():
    return 0


class Controls:
    command_container = list()

    def scanEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse(event)
            elif event.type == pg.KEYDOWN:
                self.keyboard(event)

    def mouse(self, event):
        global blocks_scale, I
        x1 = int()
        x2 = int()
        is_selected = False
        if event.button == 1:
            pos = pg.mouse.get_pos()
            # pixel_mouse = (pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE)
            # print(pos)
            cursor_pos = blocks_scale.getCursorPos()
            cursor_size = blocks_scale.getCursorSize()
            if cursor_pos[0] <= pos[0] and pos[0] <= cursor_pos[0] + cursor_size[0]:
                print('Yes')
                if cursor_pos[1] <= pos[1] and pos[1] <= cursor_pos[1] + cursor_size[1]:
                    print('True')
                    mouse = pg.mouse
                    blocks_scale.selected()
                    if is_selected == True:
                        x2 = mouse.get_pos()[0]
                        dx = blocks_scale.dx

                    elif is_selected == False:
                        x1 = pos[0]
                        is_selected = True




    def keyboard(self, event):
        pass



"""LABORATORY ACTIVATION"""


def main():
    global blocks_scale, I
    GAME = True
    grid_size = 2
    standart_tick = GAME_SETTINGS['STANDART_TICK']
    grid_color = colors.BLACK
    win_color = colors.NICE_GREEN
    bf_color = colors.WHITE
    vf_color = colors.WHITE
    controls = Controls()
    win = pg.display.set_mode(WIN_SIZE)
    build_field = pg.Surface(GAMEFIELD_SIZE)
    view_field = pg.Surface(S_VIEWFIELD_SIZE)
    scales_field = pg.Surface(TABLO_SIZE)
    blocks_scale = Scale((0, 0), TABLO_SIZE, 10, 'BLOCKS')

    center_w_b = GraphicManager().find_center(WIN_SIZE, GAMEFIELD_SIZE)
    center_w_b = (center_w_b[0], center_w_b[0])


    clock = pg.time.Clock()
    I = 8
    while GAME:
        pg.time.delay(10)
        clock.tick(standart_tick)
        """KEY AND MOUSE SCANNING"""
        controls.scanEvents()

        """LOGIC"""

        """UPDATE"""
        blocks_scale.update(I)


        """RENDER"""
        win.fill(win_color)
        build_field.fill(bf_color)
        DrawGrid(build_field, BLOCK_SIZE, color=grid_color, grid_size=grid_size)
        view_field.fill(vf_color)
        scales_field.fill(colors.BLACK)
        blocks_scale.draw(scales_field)

        win.blit(scales_field, center_w_b)
        pg.display.update()


main()