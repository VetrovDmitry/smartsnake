class ModeConfig:
    def __init__(self, params):
        self.display_settings = params.get('DISPLAY_SETTINGS')
        self.game_settings = params.get('GAME_SETTINGS')
        self.controls = params.get('CONTROLS')
        self.__import_disp_set(self.display_settings)


    def __import_disp_set(self, d_set):
        self.tablo_size = tuple(d_set['TABLO_SIZE_LAB2'])
        self.win_size = tuple(d_set['WIN_SIZE_LAB2'])
        self.gamefield_size = tuple(d_set['GAMEFIELD_SIZE_LAB2'])
        self.gf_pixels = tuple(d_set['GF_PIXELS_LAB2'])
        self.snake_viewfield_size = tuple(d_set['SNAKE_VIEWFIELD_SIZE'])
        self.block_size = d_set['BLOCK_SIZE_LAB2']
        self.grid_size = 2
