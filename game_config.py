SPRITE_SIZE = 16
SPRITE_SCALE = 4
IMAGE_SIZE = SPRITE_SIZE * SPRITE_SCALE

SCREEN_WIDTH = 16 * IMAGE_SIZE
SCREEN_HEIGHT = 14 * IMAGE_SIZE

FPS = 60

IN_GAME_LEVEL_SCREEN = (IMAGE_SIZE, IMAGE_SIZE // 2, IMAGE_SIZE * 13, IMAGE_SIZE * 13)
IN_GAME_INFO_PANEL_X = SCREEN_WIDTH - IMAGE_SIZE * 2
IN_GAME_INFO_PANEL_Y = IMAGE_SIZE // 2

IN_GAME_LEVEL_SCREEN_BORDER_LEFT = IN_GAME_LEVEL_SCREEN[0]
IN_GAME_LEVEL_SCREEN_BORDER_TOP = IN_GAME_LEVEL_SCREEN[1]
IN_GAME_LEVEL_SCREEN_BORDER_RIGHT = IN_GAME_LEVEL_SCREEN[2] + IN_GAME_LEVEL_SCREEN_BORDER_LEFT
IN_GAME_LEVEL_SCREEN_BORDER_BOTTOM = IN_GAME_LEVEL_SCREEN[3] + IN_GAME_LEVEL_SCREEN_BORDER_TOP

INFO_PANEL_X, INFO_PANEL_Y = SCREEN_WIDTH - (IMAGE_SIZE * 2), IMAGE_SIZE // 2

TANK_SPEED = (IMAGE_SIZE // SPRITE_SIZE) * 0.75
TANK_HEALTH = 1
BULLET_SPEED = TANK_SPEED * 3.5
BULLET_DAMAGE = 1
BULLET_LIMIT = 1
DEFAULT_NUMBER_OF_ENEMIES = 20
MAX_ENEMIES_AT_TIME = 4
DEFAULT_EXTRA_LIVES = 2

NUM_OF_DEFAULT_STAGES = 35
DEFAULT_STAGES_DIR = 'default_stages'
NUM_OF_CUSTOM_STAGES = 4
CUSTOM_STAGES_DIR = 'custom_stages'

SPAWN_STAR = {'star_0': [SPRITE_SIZE * 16, SPRITE_SIZE * 6, SPRITE_SIZE, SPRITE_SIZE],
              'star_1': [SPRITE_SIZE * 17, SPRITE_SIZE * 6, SPRITE_SIZE, SPRITE_SIZE],
              'star_2': [SPRITE_SIZE * 18, SPRITE_SIZE * 6, SPRITE_SIZE, SPRITE_SIZE],
              'star_3': [SPRITE_SIZE * 19, SPRITE_SIZE * 6, SPRITE_SIZE, SPRITE_SIZE]}

SHIELD = {'shield_0': [SPRITE_SIZE * 16, SPRITE_SIZE * 9, SPRITE_SIZE, SPRITE_SIZE],
          'shield_1': [SPRITE_SIZE * 17, SPRITE_SIZE * 9, SPRITE_SIZE, SPRITE_SIZE]}

TANK_CRITERIA = [{'health': 1, 'speed': 1,   'bullet_speed': 1,   'bullet_power': 1, 'bullet_limit': 1, 'score': 0},
                 {'health': 1, 'speed': 1,   'bullet_speed': 1.5, 'bullet_power': 1, 'bullet_limit': 1, 'score': 0},
                 {'health': 1, 'speed': 1,   'bullet_speed': 1.5, 'bullet_power': 1, 'bullet_limit': 2, 'score': 0},
                 {'health': 1, 'speed': 1,   'bullet_speed': 1.5, 'bullet_power': 2, 'bullet_limit': 2, 'score': 0},
                 {'health': 1, 'speed': 0.5, 'bullet_speed': 1,   'bullet_power': 1, 'bullet_limit': 1, 'score': 100},
                 {'health': 1, 'speed': 1.5, 'bullet_speed': 1,   'bullet_power': 1, 'bullet_limit': 1, 'score': 200},
                 {'health': 1, 'speed': 1,   'bullet_speed': 1.5, 'bullet_power': 1, 'bullet_limit': 1, 'score': 300},
                 {'health': 4, 'speed': 1,   'bullet_speed': 1,   'bullet_power': 1, 'bullet_limit': 1, 'score': 400}]

MAP_TILES = {
    #  Bricks
    0: {'small':       [SPRITE_SIZE * 16,       SPRITE_SIZE * 4, 8, 8],
        'small_right': [(SPRITE_SIZE * 16) + 8, SPRITE_SIZE * 4, 8, 8],
        'small_bot':   [SPRITE_SIZE * 17,       SPRITE_SIZE * 4, 8, 8],
        'small_left':  [(SPRITE_SIZE * 17) + 8, SPRITE_SIZE * 4, 8, 8],
        'small_top':   [(SPRITE_SIZE * 18),     SPRITE_SIZE * 4, 8, 8]},
    #  Steel
    1: {'small': [SPRITE_SIZE * 16, (SPRITE_SIZE * 4) + 8, 8, 8]},
    #  Forest
    2: {'small': [(SPRITE_SIZE * 16) + 8, (SPRITE_SIZE * 4) + 8, 8, 8]},
    #  Ice
    3: {'small': [(SPRITE_SIZE * 17), (SPRITE_SIZE * 4) + 8, 8, 8]},
    #  Water
    4: {'small_0': [(SPRITE_SIZE * 16) + 8, (SPRITE_SIZE * 5), 8, 8],
        'small_1': [(SPRITE_SIZE * 17),     (SPRITE_SIZE * 5), 8, 8]}
}

POWER_UPS = {'shield':       [(16 * 16), (16 * 7), 16, 16],
             'freeze':       [(16 * 17), (16 * 7), 16, 16],
             'fortify':      [(16 * 18), (16 * 7), 16, 16],
             'power':        [(16 * 19), (16 * 7), 16, 16],
             'explosion':    [(16 * 20), (16 * 7), 16, 16],
             'extra_life':   [(16 * 21), (16 * 7), 16, 16],
             'special':      [(16 * 22), (16 * 7), 16, 16]}

BULLETS = {'Up':    [(SPRITE_SIZE * 20),     (SPRITE_SIZE * 6) + 4, 8, 8],
           'Left':  [(SPRITE_SIZE * 20) + 8, (SPRITE_SIZE * 6) + 4, 8, 8],
           'Down':  [(SPRITE_SIZE * 21),     (SPRITE_SIZE * 6) + 4, 8, 8],
           'Right': [(SPRITE_SIZE * 21) + 8, (SPRITE_SIZE * 6) + 4, 8, 8]}

EXPLOSIONS = {'explode_0': [(SPRITE_SIZE * 16), (SPRITE_SIZE * 8), 16, 16],
              'explode_1': [(SPRITE_SIZE * 17), (SPRITE_SIZE * 8), 16, 16],
              'explode_2': [(SPRITE_SIZE * 18), (SPRITE_SIZE * 8), 16, 16],
              'explode_3': [(SPRITE_SIZE * 19), (SPRITE_SIZE * 8), 32, 32],
              'explode_4': [(SPRITE_SIZE * 21), (SPRITE_SIZE * 8), 32, 32]}

HUD_INFO = {'stage':       [(16 * 20) + 8, (16 * 11), 40, 8],
            'enemy_life':  [(16 * 20), (16 * 12), 8, 8],
            'player_life': [376, 144, 8, 8],
            'info_panel':  [(16 * 23), (16 * 0), 32, (16 * 15)],
            'grey_square': [(16 * 23), (16 * 0), 8, 8]}

CONTEXT = {'pause':     [(16 * 18), (16 * 11), 40, 8],
           'game_over': [(16 * 18), (16 * 11) + 8, 32, 16]}

EAGLE = {'intact':    [(16 * 19), (16 * 2), 16, 16],
         'destroyed': [(16 * 20), (16 * 2), 16, 16]}

# Colors
GRAY = 'grey39'
DARK_GRAY = 'grey20'

# Pause
PAUSE_POS = (IN_GAME_LEVEL_SCREEN_BORDER_LEFT + IN_GAME_LEVEL_SCREEN[2] // 2,
             IN_GAME_LEVEL_SCREEN_BORDER_TOP + IN_GAME_LEVEL_SCREEN[3] // 2)

# HUD
HUD_FONT_SIZE = 32
LEVEL_IMAGE_POS = (14.5 * IMAGE_SIZE, 13 * IMAGE_SIZE)
PLAYER_EXTRA_LIVES_POS = (14.5 * IMAGE_SIZE, 9.5 * IMAGE_SIZE)
REMAINING_TANKS_POS = (14.5 * IMAGE_SIZE, 2 * IMAGE_SIZE)

# Stage Score Screen
SCORE_SCREEN_FONT_SIZE = 32
DEFAULT_HIGH_SCORE = 20000

# Start Screen
SS_OPTION_FONT_SIZE = 32
SS_TITLE_FONT_SIZE = 80
SS_SCROLL_SPEED = 10

OPTION_POSITIONS = [(5 * IMAGE_SIZE, 8 * IMAGE_SIZE),
                    (5 * IMAGE_SIZE, 9 * IMAGE_SIZE),
                    (5 * IMAGE_SIZE, 10 * IMAGE_SIZE)]

TOKEN_POSITIONS = [(4 * IMAGE_SIZE, 7.875 * IMAGE_SIZE),
                   (4 * IMAGE_SIZE, 8.875 * IMAGE_SIZE),
                   (4 * IMAGE_SIZE, 9.875 * IMAGE_SIZE)]

TITLE_POSITIONS = [(8 * IMAGE_SIZE, 4 * IMAGE_SIZE),
                   (8 * IMAGE_SIZE, 5.75 * IMAGE_SIZE)]

# Game Over / Game Completed Screens
GO_FONT_SIZE = 96
GO_LINE_1_POS = (SCREEN_WIDTH // 2, IMAGE_SIZE * 6)
GO_LINE_2_POS = (SCREEN_WIDTH // 2, IMAGE_SIZE * 8)

# Stage Editor
SE_FONT_SIZE = 32
SE_SMALL_FONT_SIZE = 12

# Map Editor
STAGE_MAP_ROWS = 26
STAGE_MAP_COLS = 26

SE_LEVEL_SCREEN = (0, 0, IMAGE_SIZE * 13, IMAGE_SIZE * 13)

SMALL_TILE_SIZE = 32

SE_LEVEL_SCREEN_BORDER_LEFT = SE_LEVEL_SCREEN[0]
SE_LEVEL_SCREEN_BORDER_TOP = SE_LEVEL_SCREEN[1]
SE_LEVEL_SCREEN_BORDER_RIGHT = SE_LEVEL_SCREEN[2] + SE_LEVEL_SCREEN_BORDER_LEFT
SE_LEVEL_SCREEN_BORDER_BOTTOM = SE_LEVEL_SCREEN[3] + SE_LEVEL_SCREEN_BORDER_TOP

TILE_OPTIONS_POS = [(IMAGE_SIZE * 13 + 16, 16),  (IMAGE_SIZE * 13 + 112, 16),
                    (IMAGE_SIZE * 13 + 16, 112), (IMAGE_SIZE * 13 + 112, 112),
                    (IMAGE_SIZE * 13 + 16, 208), (IMAGE_SIZE * 13 + 112, 208),
                    (IMAGE_SIZE * 13 + 16, 304), (IMAGE_SIZE * 13 + 112, 304),
                    (IMAGE_SIZE * 13 + 16, 400), (IMAGE_SIZE * 13 + 112, 400)]

CONFIG_BUTTON_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - IMAGE_SIZE // 2)
ME_STAGE_NUM_POS = (IMAGE_SIZE * 14.5, IMAGE_SIZE * 10)

# Config Editor
SE_TANK_GRID = (IMAGE_SIZE * 2, IMAGE_SIZE * 2, IMAGE_SIZE * 10, IMAGE_SIZE * 2)
SE_TANK_GRID_ROWS = 2
SE_TANK_GRID_COLS = 10

MAP_BUTTON_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - IMAGE_SIZE // 2)
SAVE_BUTTON_POS = (IMAGE_SIZE // 2, SCREEN_HEIGHT - IMAGE_SIZE // 2)
RELOAD_BUTTON_POS = (SCREEN_WIDTH - IMAGE_SIZE // 2, SCREEN_HEIGHT - IMAGE_SIZE // 2)
SAVE_MESSAGE_POS = (SCREEN_WIDTH // 2, IMAGE_SIZE * 10)

SE_TANKS_POS = [(4.5 * IMAGE_SIZE, 6 * IMAGE_SIZE),
                (6.5 * IMAGE_SIZE, 6 * IMAGE_SIZE),
                (8.5 * IMAGE_SIZE, 6 * IMAGE_SIZE),
                (10.5 * IMAGE_SIZE, 6 * IMAGE_SIZE)]

SE_PLUSES_POS = [(4.5 * IMAGE_SIZE, 7 * IMAGE_SIZE),
                 (6.5 * IMAGE_SIZE, 7 * IMAGE_SIZE),
                 (8.5 * IMAGE_SIZE, 7 * IMAGE_SIZE),
                 (10.5 * IMAGE_SIZE, 7 * IMAGE_SIZE)]

SE_MINUS_POS = (IMAGE_SIZE * 13, IMAGE_SIZE * 2.5)
CE_STAGE_NUM_POS = (SCREEN_WIDTH // 2, IMAGE_SIZE)

DEFAULT_ENEMIES_SPAWN_POS = [[(0, 0), (0, 1), (1, 0), (1, 1)],
                             [(12, 0), (12, 1), (13, 0), (13, 1)],
                             [(24, 0), (24, 1), (25, 0), (25, 1)]]
DEFAULT_PLAYER_SPAWN_POS = [(8, 24), (8, 25), (9, 24), (9, 25)]
DEFAULT_BASE_POS = [(12, 24), (12, 25), (13, 24), (13, 25)]
DEFAULT_FORT_POS = [(11, 25), (11, 24), (11, 23), (12, 23), (13, 23), (14, 23), (14, 24), (14, 25)]
