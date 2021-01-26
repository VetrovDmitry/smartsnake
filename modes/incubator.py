import pygame as pg
from objects import FoodPacker
from guiparts import GraphicManager, DrawGrid, RandomColors
from utils.handmade import AllSprites, getParams, smart_pos_for_area, AllAies
from utils.mathmethods import Matrix
from utils.snake_mind import SmartSnake
from utils.gamesatisfaction import Map
from guis import colors

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
    snake_first_count = 2
    food_count = 66
    standart_tick = 2
    GAME = True
    gf_color = colors.WHITE
    grid_size_1 = 1
    gf_size_normal = (GAMEFIELD_SIZE[0] + grid_size_1 // 2,
                      GAMEFIELD_SIZE[1] + grid_size_1 // 2)
    gf_pixel_count_x = GAMEFIELD_SIZE[0] // BLOCK_SIZE
    gf_pixel_count_y = GAMEFIELD_SIZE[1] // BLOCK_SIZE
    gamefield_matrix_size = (gf_pixel_count_x, gf_pixel_count_y)
    gf_matrix = Matrix(gamefield_matrix_size, 0)

    wall_color_1 = colors.DARK_BLUE
    wall_color_2 = colors.DARK_BROWN
    food_color_1 = colors.RED
    snake_colors = RandomColors(snake_first_count)
    grid_color_1 = colors.BLACK
    snake_spawn_area = [[3, 15], [3, 15]]
    farea_1 = [[3, 57], [3, 33]]

    win = pg.display.set_mode(WIN_SIZE)
    gamefield = pg.Surface(gf_size_normal)

    around_wall = Map(gamefield_matrix_size, BLOCK_SIZE, circuit=True)
    wall_sprites = around_wall.getSprites()

    food_sprites = AllSprites()
    food_sprites.append(FoodPacker(farea_1, food_count, food_color_1, BLOCK_SIZE))
    # Ghora = SmartSnake((7, 3), (1, 0), 0,
    #                    color=colors.NICE_GREEN,
    #                    size=BLOCK_SIZE,
    #                    matrix_environment=gf_matrix,
    #                    detections=(1, 2, 3),
    #                    a_0=90)
    #
    # Grisha = SmartSnake((7, 17), (1, 0), 0,
    #                    color=colors.DARK_RED,
    #                    size=BLOCK_SIZE,
    #                    matrix_environment=gf_matrix,
    #                    detections=(1, 2, 3),
    #                    a_0=90)
    #
    # just_sprites = AllSprites()
    # just_sprites.append(Ghora.snake)
    # just_sprites.append(Grisha.snake)


    moving_sprites = AllAies()

    for i, snake in enumerate(range(snake_first_count)):
        new_coors = smart_pos_for_area(snake_spawn_area, moving_sprites.getAllPositions())
        new_color = snake_colors[i]
        new_snake = SmartSnake(new_coors, (1, 0), 0,
                               color=new_color,
                               size=BLOCK_SIZE,
                               matrix_environment=gf_matrix,
                               relations=moving_sprites,
                               detections=(1, 2, 3),
                               a_0=90)

        new_snake.setName('Ghora_{}'.format(i))
        moving_sprites.append(new_snake)

    clock = pg.time.Clock()
    while GAME:
        pg.time.delay(35)
        clock.tick(standart_tick)

        """FORMATING MATRIX OF A GLOBAL GAMEPROCESS EVENTS"""

        gf_matrix.refresh()
        gf_matrix = wall_sprites.print_to_matrix(gf_matrix)
        gf_matrix = food_sprites.print_to_matrix(gf_matrix)
        # gf_matrix = just_sprites.print_to_matrix(gf_matrix)
        gf_matrix = moving_sprites.print_to_matrix(gf_matrix)

        moving_sprites.play(gf_matrix, learn=True)

        # moving_sprites.play(gf_matrix, learn=True, lr=0.01)

        # just_sprites.update()
        """WORLD RULES"""

        # WorldRules(just_sprites, food_sprites, wall_sprites)

        """UPDATE PART"""


        moving_sprites.update()

        """SCREEN DRAWING"""

        gamefield.fill(gf_color)
        wall_sprites.draw(gamefield)
        food_sprites.draw(gamefield)
        moving_sprites.draw(gamefield)
        # just_sprites.draw(gamefield)

        DrawGrid(gamefield, BLOCK_SIZE, color=grid_color_1, grid_size=grid_size_1)
        w_center = GraphicManager().find_center(WIN_SIZE, GAMEFIELD_SIZE)
        win.blit(gamefield, (w_center[0], w_center[0]))
        pg.display.update()

main()



