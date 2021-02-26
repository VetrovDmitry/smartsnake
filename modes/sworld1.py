import pygame as pg
from gobjects.food import FoodPacker
from utils.snake_mind import SmartSnake, SmartMama
from guis.tablo import Tabloes
from guis.utils import DrawGrid
from utils.mathmethods import Matrix
from utils.gamesatisfaction import WorldRules, Map
from guis import colors
from utils.handmade import AllSprites, getParams


pg.init()


"""PRESTART SETTINGS"""

DISPLAY_SETTINGS = getParams('DISPLAY_SETTINGS')
GAME_SETTINGS = getParams('GAME_SETTINGS')
CONTROLS = getParams('CONTROLS')

TABLO_SIZE = tuple(DISPLAY_SETTINGS['TABLO_SIZE_LAB2'])
WIN_SIZE = tuple(DISPLAY_SETTINGS['WIN_SIZE_LAB2'])
GAMEFIELD_SIZE = tuple(DISPLAY_SETTINGS['GAMEFIELD_SIZE_LAB2'])
GF_PIXELS = tuple(DISPLAY_SETTINGS['GF_PIXELS_LAB2'])
SNAKE_VIEWFIELD_SIZE = DISPLAY_SETTINGS['SNAKE_VIEWFIELD_SIZE']
BLOCK_SIZE = DISPLAY_SETTINGS['BLOCK_SIZE_LAB2']
GRID_SIZE = 2
GRID_COLOR = colors.BLACK


"""IN-GAME PRESETTINGS"""

STANDART_TICK = 12

gf_pixel_count_x = GAMEFIELD_SIZE[0] // BLOCK_SIZE
gf_pixel_count_y = GAMEFIELD_SIZE[1] // BLOCK_SIZE
gamefield_matrix_size = (gf_pixel_count_x, gf_pixel_count_y)
gf_color = colors.WHITE
win_fill = colors.NICE_NORMAL

D = 20
gf_1_loc = (D, D)
tb_1_loc = (D, GAMEFIELD_SIZE[1]+2*D)

ENERGY_COUNT = 2
FOOD_COUNT = 500
farea_1 = [[3, gamefield_matrix_size[0]-3], [3, gamefield_matrix_size[1]-3]]
fcolor_1 = colors.YELLOW

snake_color = colors.DARK_GREEN
first_snakes_names = ['Mishanya', 'Tosha', 'Tolya', 'Tanya', 'Rita', 'Vikus', 'Robin', 'Sanchez']
first_snake_positions = [(7, 16), (30, 22), (22, 21), (22, 28), (22, 35), (28, 12), (9, 11), (31, 10)]
CONTROLP = 10

CURSOR = 0


"""UTILS"""

def Restart():
    global GAME
    GAME = False
    game_start()

def Controls():
    global FOOD_COUNT, ENERGY_COUNT, CURSOR, GAME, CONTROLP

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                GAME = False
                pg.quit()
            elif event.key == pg.K_r:
                Restart()
            elif event.key == pg.K_KP9:
                CONTROLP += 1
            elif event.key == pg.K_KP6:
                CONTROLP -= 1
            elif event.key == pg.K_KP7:
                FOOD_COUNT += 50
            elif event.key == pg.K_KP4:
                FOOD_COUNT -= 50
            elif event.key == pg.K_KP8:
                ENERGY_COUNT += 1
            elif event.key == pg.K_KP5:
                ENERGY_COUNT -= 1
            elif event.key == pg.K_RIGHT:
                CURSOR += 1
            elif event.key == pg.K_LEFT:
                CURSOR -= 1




def game_start():
    """GAME VARIABLES"""
    global FOOD_COUNT, ENERGY_COUNT, CURSOR, GAME, CONTROLP
    GAME = True
    ITERS = 0
    t_labels = ['ITER', 'CHILDS', 'MUTS', 'FOOD', 'ENRGY', 'CNTRLC']
    tables_group_size_1 = (GAMEFIELD_SIZE[0], TABLO_SIZE[1])
    gf_size_normal = (GAMEFIELD_SIZE[0] + GRID_SIZE,
                      GAMEFIELD_SIZE[1] + GRID_SIZE)

    """TABLOES SETTINGS"""
    tabloes_1 = Tabloes(t_labels, tables_group_size_1, 10)

    """MATRIX SETTINGS"""
    gf_matrix = Matrix(gamefield_matrix_size, 0)

    """STATIC OBJECTS SETTINGS"""
    around_wall = Map(gamefield_matrix_size, BLOCK_SIZE, circuit=True)
    wall_sprites = around_wall.getSprites()

    """FOOD OBJECTS"""
    # Valya = SmartSnake('Valya', first_snake_position_1, (1, 0), gf_matrix, block_size=BLOCK_SIZE)

    food_sprites = AllSprites()
    first_f_c = FOOD_COUNT
    food_1 = FoodPacker(farea_1, first_f_c, fcolor_1, BLOCK_SIZE)
    food_sprites.append(food_1)

    """CHILDS OBJECTS"""
    mother_nature = SmartMama(gf_matrix, CONTROLP)
    for i, s_name in enumerate(first_snakes_names):
        pos = first_snake_positions[i]
        mother_nature.append(SmartSnake(s_name, pos, (1, 0), gf_matrix, block_size=BLOCK_SIZE, c=ENERGY_COUNT, color=snake_color))


    """WINDOW AND SURFACES CREATING"""

    win = pg.display.set_mode(WIN_SIZE, pg.FULLSCREEN)
    gamefield_1 = pg.Surface(gf_size_normal)
    clock = pg.time.Clock()
    while GAME:
        pg.time.delay(10)
        clock.tick(STANDART_TICK)

        """KEY SCANNING"""
        Controls()
        # Pause()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    # FOOD_COUNT += 1
                    print(FOOD_COUNT)
                elif event.key == pg.K_DOWN:
                    # FOOD_COUNT -= 1
                    print(FOOD_COUNT)

        """WORLD RULES"""
        WorldRules(mother_nature, food_sprites, wall_sprites)

        """MATRIX UPDATING"""

        """FORAMTING MATRIX"""

        gf_matrix.refresh()
        gf_matrix = wall_sprites.print_to_matrix(gf_matrix)
        gf_matrix = food_sprites.print_to_matrix(gf_matrix)
        gf_matrix = mother_nature.getMovingSprites().print_to_matrix(gf_matrix)

        mother_nature.evolution(gf_matrix)
        childs = mother_nature.getChildCount()
        muts = mother_nature.getMuts()
        # m_score = mother_nature.getMscore()

        # detector = mother_nature.getSnakeVisionByI(CURSOR)
        # print(detector.matrix)

        """UPDATING"""
        tabloes_1.update((ITERS, childs, muts, FOOD_COUNT, ENERGY_COUNT, CONTROLP))
        food_1.setCount(FOOD_COUNT)
        wall_sprites.update()
        food_sprites.update()
        mother_nature.update()
        # tablo_1.update(ITERS, False)

        """RENDERING"""

        win.fill(win_fill)
        tabloes_1.draw(win, tb_1_loc)
        gamefield_1.fill(gf_color)
        food_sprites.draw(gamefield_1)
        mother_nature.getMovingSprites().draw(gamefield_1)
        wall_sprites.draw(gamefield_1)
        DrawGrid(gamefield_1, BLOCK_SIZE, GRID_COLOR, grid_size=GRID_SIZE)
        win.blit(gamefield_1, gf_1_loc)


        pg.display.update()
        ITERS += 1


game_start()

