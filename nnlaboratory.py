from objects import FoodPacker, Wall
from guiparts import GraphicManager, DrawGrid, Tablo
from handmade import AllSprites, getParams, renderPixels
from mathmethods import Matrix
from snake_mind import SmartSnake
from gamesatisfaction import WorldRules, Map
import colors
import pygame as pg
from sys import stdout


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
i = 0

"""UTILS"""

def Pause():
    pause = True
    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                pause = False


def printToDisplay():
    global gf_matrix, vf_matrix, i

    lines = list()
    for line in gf_matrix.matrix:
        l = str()
        for element in line:
            l += str(element)
        l += '\n'
        lines.append(l)

    with open('C:/Users/79999/pproject/SMARTSNAKE/screens/screen_matrix{}.txt'.format(i), 'w') as logger:
        logger.writelines(lines)
    vf_matrix.prettyPrint()
    i += 1


class Controls:
    status = 'flex'

    def __init__(self, game_object, ctype='KEYS_1', ):
        self.go = game_object
        self.ctype = ctype

    def scanEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse(event)
            elif event.type == pg.KEYDOWN:
                self.keyboard(event)

    def mouse(self, event):
        if event.button == 1 and self.status == 'flex':
            pos = pg.mouse.get_pos()
            pixel_mouse = (pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE)
            if pixel_mouse in self.go.snake.getAllPos():
                self.status = 'get da touch'
            else:
                self.status = 'flex'
        elif event.button == 1 and self.status == 'get da touch':
            pos = pg.mouse.get_pos()
            pixel_mouse = (pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE)
            if pixel_mouse not in self.go.snake.getAllPos():
                moment_mouse = pg.mouse.get_pos()
                pixel_mouse = (moment_mouse[0] // BLOCK_SIZE - 1, moment_mouse[1] // BLOCK_SIZE - 1)
                ghoras_dir = self.go.snake.direction
                gos_len = self.go.snake.getLen()
                gos_delta = gos_len - 3
                self.go.snake.respawn(pixel_mouse, dir=ghoras_dir, status='alive')
                for i in range(gos_delta):
                    self.go.snake.addBlock()
                self.status = 'flex'
        elif event.button == 3:
            printToDisplay()

    def keyboard(self, event):
        key = str(event.key)
        move_choice = CONTROLS[self.ctype].get(key, False)
        if move_choice and self.go.local_moves.get(move_choice, False):
            direction = self.go.local_moves.get(move_choice, False)
            self.go.moveByRot(direction)
        elif int(key) == pg.K_r:
            self.go.snake.respawn()
        elif int(key) == pg.K_ESCAPE:
            Pause()
        else:
            pass


"""LABORATORY ACTIVATION"""


def main():
    global gf_matrix, vf_matrix, train_data
    train_data = list()
    standart_tick = 10
    GAME = True
    gf_color = colors.WHITE
    grid_size_1 = 1
    grid_size_2 = 1
    S_VIEWFIELD_SIZE = (SNAKE_VIEWFIELD_SIZE[0]*BLOCK_SIZE + grid_size_2//2,
                        SNAKE_VIEWFIELD_SIZE[1]*BLOCK_SIZE + grid_size_2//2)
    gf_size_normal = (GAMEFIELD_SIZE[0] + grid_size_2//2,
                      GAMEFIELD_SIZE[1] + grid_size_2//2)
    grid_color_1 = colors.BLACK
    grid_color_2 = colors.LIGHT_GREEN
    snake_color_1 = colors.NICE_DARK
    snake_color_2 = colors.LIGHT_BLUE
    wall_color = colors.BROWN

    farea_1 = [[3, 57], [3, 33]]
    fcount_1 = 66
    fcolor_1 = colors.RED

    farea_2 = [[35, 46], [3, 11]]
    fcount_2 = 15
    fcolor_2 = colors.GREEN

    farea_3 = [[3, 57], [3, 33]]
    fcount_3 = 20
    fcolor_3 = colors.YELLOW

    first_snake_position_1 = (40, 5)
    first_snake_position_2 = (10, 10)

    gf_pixel_count_x = GAMEFIELD_SIZE[0] // BLOCK_SIZE
    gf_pixel_count_y = GAMEFIELD_SIZE[1] // BLOCK_SIZE
    gamefield_matrix_size = (gf_pixel_count_x, gf_pixel_count_y)
    gf_matrix = Matrix(gamefield_matrix_size, 0)

    vf_pixel_count_x = SNAKE_VIEWFIELD_SIZE[0]
    vf_pixel_count_y = SNAKE_VIEWFIELD_SIZE[1]
    vf_matrix_size = (vf_pixel_count_x, vf_pixel_count_y)
    vf_matrix = Matrix(vf_matrix_size, 0)

    win = pg.display.set_mode(WIN_SIZE)
    gamefield = pg.Surface(gf_size_normal)
    snake_viewfield = pg.Surface(S_VIEWFIELD_SIZE)
    detectors_collection = {
        1: pg.Surface(S_VIEWFIELD_SIZE),
        2: pg.Surface(S_VIEWFIELD_SIZE),
        3: pg.Surface(S_VIEWFIELD_SIZE),
    }

    around_wall = Map(gamefield_matrix_size, BLOCK_SIZE, circuit=True)
    wall_sprites = around_wall.getSprites()

    food_sprites = AllSprites()
    food_sprites.append(FoodPacker(farea_1, fcount_1, fcolor_1, BLOCK_SIZE))
    food_sprites.append(FoodPacker(farea_2, fcount_2, fcolor_2, BLOCK_SIZE))
    food_sprites.append(FoodPacker(farea_3, fcount_3, fcolor_3, BLOCK_SIZE))

    moving_sprites = AllSprites()
    Ghora = SmartSnake(first_snake_position_1,
                       (1, 0),
                       0,
                       snake_color_1,
                       size=BLOCK_SIZE,
                       matrix_environment=gf_matrix,
                       relations=moving_sprites,
                       detections=(1, 2, 3),
                       a_0=90)

    Ghora.setName('Ghora')

    moving_sprites.append(Ghora.snake)
    ghoras_control = Controls(Ghora, ctype='KEYS_1')
    # Pappa = SmartSnake(first_snake_position_2,
    #                    (1, 0),
    #                    0,
    #                    snake_color_1,
    #                    size=BLOCK_SIZE,
    #                    matrix_environment=gf_matrix,
    #                    relations=moving_sprites,
    #                    detections=(1, 2, 3),
    #                    a_0=90)
    #
    # Pappa.setName('Pappa')
    #
    # moving_sprites.append(Pappa.snake)
    clock = pg.time.Clock()
    while GAME:
        pg.time.delay(10)
        clock.tick(standart_tick)

        """key scanning"""

        ghoras_control.scanEvents()

        """GAME STRUCTURE"""


        """WORLD RULES"""

        WorldRules(moving_sprites, food_sprites, wall_sprites)

        """"""

        """UPDATE PART"""

        moving_sprites.update()
        # Ghora.printScore()



        """FORMATING MATRIX"""
        gf_matrix.refresh()
        gf_matrix = wall_sprites.print_to_matrix(gf_matrix)
        gf_matrix = food_sprites.print_to_matrix(gf_matrix)
        gf_matrix = moving_sprites.print_to_matrix(gf_matrix)

        vf_matrix = Ghora.updateVision(gf_matrix)
        detections = Ghora.getDetections()

        Ghora.play(learn=True, lr=0.007)
        # Pappa.play(learn=True, lr=0.01)

        """SCREEN DRAWING"""

        snake_viewfield.fill(gf_color)
        pix_poss, pix_typ = vf_matrix.Pdraw()
        renderPixels(snake_viewfield, pix_poss, pix_typ, BLOCK_SIZE)
        DrawGrid(snake_viewfield, BLOCK_SIZE, color=grid_color_2, grid_size=grid_size_2)

        for i, detection_screen in enumerate(detectors_collection.values()):
            detection_screen.fill(colors.BLACK)
            if detections.get(i+1):
                det_pos, det_typ = detections.get(i+1).Pdraw()
                renderPixels(detection_screen, det_pos, det_typ, BLOCK_SIZE)
                DrawGrid(detection_screen, BLOCK_SIZE, color=colors.LIGHT_GREEN, grid_size=grid_size_2)

        gamefield.fill(gf_color)
        wall_sprites.draw(gamefield)
        food_sprites.draw(gamefield)
        moving_sprites.draw(gamefield)

        DrawGrid(gamefield, BLOCK_SIZE, color=grid_color_1, grid_size=grid_size_1)

        w_center = GraphicManager().find_center(WIN_SIZE, GAMEFIELD_SIZE)
        win.blit(gamefield, (w_center[0], w_center[0]))
        det_x = w_center[0] - 1
        det_y = 600
        for detector_screen in detectors_collection.values():
            det_x += detector_screen.get_size()[0] + 10
            win.blit(detector_screen, (det_x, det_y))

        win.blit(snake_viewfield, (w_center[0]-1, 600))
        pg.display.update()
main()
