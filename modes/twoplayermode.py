import pygame as pg
from gobjects.food import FoodPacker
from gobjects.snake import Snake
from guiparts import GraphicManager, DrawGrid
from utils.handmade import AllSprites, getParams, smart_pos_for_area
from utils.mathmethods import Matrix
from utils.gamesatisfaction import WorldRules, Map
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
    status = 'flex'

    def __init__(self, game_objects):
        self.game_object_1 = game_objects[0]
        self.game_object_2 = game_objects[1]
        self.keys_1 = CONTROLS.get('KEYS_1')
        self.keys_2 = CONTROLS.get('KEYS_2')

    def scanEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                pass
                # self.mouse(event)
            elif event.type == pg.KEYDOWN:
                self.keyboard(event)

    # def mouse(self, event):
    #     if event.button == 1 and self.status == 'flex':
    #         pos = pg.mouse.get_pos()
    #         pixel_mouse = (pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE)
    #         if pixel_mouse in self.go.snake.getAllPos():
    #             self.status = 'get da touch'
    #         else:
    #             self.status = 'flex'
    #     elif event.button == 1 and self.status == 'get da touch':
    #         pos = pg.mouse.get_pos()
    #         pixel_mouse = (pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE)
    #         if pixel_mouse not in self.go.snake.getAllPos():
    #             moment_mouse = pg.mouse.get_pos()
    #             pixel_mouse = (moment_mouse[0] // BLOCK_SIZE - 1, moment_mouse[1] // BLOCK_SIZE - 1)
    #             ghoras_dir = self.go.snake.direction
    #             gos_len = self.go.snake.getLen()
    #             gos_delta = gos_len - 3
    #             self.go.snake.respawn(pixel_mouse, dir=ghoras_dir, status='alive')
    #             for i in range(gos_delta):
    #                 self.go.snake.addBlock()
    #             self.status = 'flex'

    def keyboard(self, event):
        key = str(event.key)
        if int(key) == pg.K_g:
            self.game_object_1.addBlock()
        elif int(key) == pg.K_h:
            self.game_object_2.addBlock()
        elif int(key) == pg.K_t:
            self.game_object_1.freeze()
        elif int(key) == pg.K_y:
            self.game_object_2.freeze()
        elif int(key) == pg.K_ESCAPE:
            Pause()

        if key in self.keys_1.keys():
            move = self.keys_1.get(key)
            new_direction = CONTROLS.get(move)
            self.game_object_1.move(new_direction)
        elif key in self.keys_2.keys():
            move = self.keys_2.get(key)
            new_direction = CONTROLS.get(move)
            self.game_object_2.move(new_direction)

def main():
    snake_first_count = 2
    food_count = 66
    standart_tick = 10
    GAME = True
    gf_color = colors.WHITE
    grid_size_1 = 1
    grid_color_1 = colors.BLACK

    """GAMEFIELD PRESETTINGS"""

    gf_size_normal = (GAMEFIELD_SIZE[0] + grid_size_1 // 2,
                      GAMEFIELD_SIZE[1] + grid_size_1 // 2)
    gf_pixel_count_x = GAMEFIELD_SIZE[0] // BLOCK_SIZE
    gf_pixel_count_y = GAMEFIELD_SIZE[1] // BLOCK_SIZE
    gamefield_matrix_size = (gf_pixel_count_x, gf_pixel_count_y)
    gf_matrix = Matrix(gamefield_matrix_size, 0)

    """GAME OBJECT PRESSETTINGS"""

    wall_color_1 = colors.DARK_BLUE
    wall_color_2 = colors.DARK_BROWN
    around_wall = Map(gamefield_matrix_size, BLOCK_SIZE, circuit=True)
    wall_sprites = around_wall.getSprites()

    food_color_1 = colors.RED
    farea_1 = [[3, 57], [3, 33]]
    food_sprites = AllSprites()
    food_sprites.append(FoodPacker(farea_1, food_count, food_color_1, BLOCK_SIZE))

    under_control = list()
    snake_names = ['NATASHA', 'KIRILL', 'VALYA', 'PETYA']
    snake_colors = [colors.JUICY_GREEN, colors.DARK_RED]
    snake_spawn_area = [[3, 15], [3, 15]]

    moving_sprites = AllSprites()

    for i, snake_color in enumerate(snake_colors):
        new_player_pos = smart_pos_for_area(snake_spawn_area, moving_sprites.getAllPositions())
        new_player_name = snake_names[i]
        moving_sprites.append(Snake(new_player_pos,
                                    new_player_name,
                                    snake_color,
                                    BLOCK_SIZE,
                                    dir=(1, 0)))

    cntrls = Controls(moving_sprites.getSprites())
    win = pg.display.set_mode(WIN_SIZE)
    gamefield = pg.Surface(gf_size_normal)

    clock = pg.time.Clock()
    while GAME:
        pg.time.delay(10)
        clock.tick(standart_tick)

        """KEY SCANNING"""


        cntrls.scanEvents()
        # print(player_1.getHeadPosition())

        # for event in pg.event.get():
        #     if event.type == pg.QUIT:
        #         pg.quit()
        #
        #     if event.type == pg.KEYDOWN:
        #         if event.key == pg.K_w:
        #             player_1.changeDir((1, 0))
        #         elif event.key == pg.K_s:
        #             player_1.changeDir((-1, 0))
        #
        #         if event.key == pg.K_o:
        #             player_2.changeDir((1, 0))
        #         elif event.key == pg.K_l:
        #             player_2.changeDir((-1, 0))


        """FORMATING MATRIX OF A GLOBAL GAMEPROCESS EVENTS"""

        gf_matrix.refresh()
        gf_matrix = wall_sprites.print_to_matrix(gf_matrix)
        gf_matrix = food_sprites.print_to_matrix(gf_matrix)
        # gf_matrix = just_sprites.print_to_matrix(gf_matrix)
        gf_matrix = moving_sprites.print_to_matrix(gf_matrix)

        """WORLD RULES"""

        WorldRules(m_obj=moving_sprites, f_obj=food_sprites, w_obj=wall_sprites)

        """UPDATE PART"""

        moving_sprites.update()
        # moving_sprites.update()

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