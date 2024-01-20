import pygame
import game_config as gc


class GameAssets:
    def __init__(self):
        self.sprite_sheet = load_ind_img('BattleCity')

        self.start_screen_option_font = pygame.font.Font('assets/nintendo-nes-font.ttf', gc.SS_OPTION_FONT_SIZE)
        self.start_screen_title_font = pygame.font.Font('assets/nintendo-nes-font.ttf', gc.SS_TITLE_FONT_SIZE)
        self.hud_overlay_font = pygame.font.Font('assets/nintendo-nes-font.ttf', gc.HUD_FONT_SIZE)
        self.score_screen_font = pygame.font.Font('assets/nintendo-nes-font.ttf', gc.SCORE_SCREEN_FONT_SIZE)
        self.stage_editor_font = pygame.font.Font('assets/nintendo-nes-font.ttf', gc.SE_FONT_SIZE)
        self.stage_editor_small_font = pygame.font.Font('assets/nintendo-nes-font.ttf', gc.SE_SMALL_FONT_SIZE)
        self.gave_over_screen_font = pygame.font.Font('assets/nintendo-nes-font.ttf', gc.GO_FONT_SIZE)

        self.score_screen_images = self._load_score_screen_images()
        self.tank_images = self._load_all_tank_images()
        self.shield_images = self._get_img_dict(gc.SHIELD)
        self.spawn_star_images = self._get_img_dict(gc.SPAWN_STAR)
        self.bullet_images = self._get_img_dict(gc.BULLETS)
        self.explosions = self._get_img_dict(gc.EXPLOSIONS)
        self.hud_images = self._get_img_dict(gc.HUD_INFO, 'black', False)
        self.context = self._get_img_dict(gc.CONTEXT)
        self.powerups = self._get_img_dict(gc.POWER_UPS)
        self.eagle = self._get_img_dict(gc.EAGLE)

        self.brick_tiles = self._get_img_dict(gc.MAP_TILES[0], 'black', False)
        self.steel_tiles = self._get_img_dict(gc.MAP_TILES[1])
        self.forest_tiles = self._get_img_dict(gc.MAP_TILES[2])
        self.ice_tiles = self._get_img_dict(gc.MAP_TILES[3])
        self.water_tiles = self._get_img_dict(gc.MAP_TILES[4])

        self.token_image = pygame.transform.scale_by(self.tank_images['Tank_0']['Gold']['Right'][0], 0.75)
        self.plus_image = load_ind_img('plus', True, 4)
        self.plus_image.set_colorkey('black')
        self.minus_image = load_ind_img('minus', True, 4)
        self.minus_image.set_colorkey('black')

        #  Game Sounds
        self.game_start_sound = pygame.mixer.Sound("sounds/gamestart.ogg")

        self.movement_sound = pygame.mixer.Sound("sounds/background player.ogg")
        self.movement_sound.set_volume(0.3)
        self.channel_player_movement_sound = pygame.mixer.Channel(0)

        self.enemy_movement_sound = pygame.mixer.Sound("sounds/background.mp3")
        self.enemy_movement_sound.set_volume(0.4)
        self.channel_enemy_movement_sound = pygame.mixer.Channel(1)

        self.fire_sound = pygame.mixer.Sound("sounds/fire.mp3")
        self.fire_sound.set_volume(1)
        self.channel_fire_sound = pygame.mixer.Channel(2)

        self.brick_sound = pygame.mixer.Sound("sounds/brick.mp3")
        self.channel_brick_sound = pygame.mixer.Channel(3)

        self.steel_sound = pygame.mixer.Sound("sounds/steel.mp3")
        self.channel_steel_sound = pygame.mixer.Channel(4)

        self.explosion_sound = pygame.mixer.Sound("sounds/explosion.mp3")
        self.channel_explosion_sound = pygame.mixer.Channel(5)

        self.bonus_sound = pygame.mixer.Sound("sounds/bonus.mp3")
        self.channel_bonus_sound = pygame.mixer.Channel(6)

        self.game_over_sound = pygame.mixer.Sound("sounds/gameover.mp3")
        self.channel_game_over_sound = pygame.mixer.Channel(7)

        self.score_sound = pygame.mixer.Sound("sounds/score.mp3")

    def _load_all_tank_images(self):
        tank_image_dict = {}
        for tank in range(8):
            tank_image_dict[f'Tank_{tank}'] = {}
            for group in ['Gold', 'Silver', 'Green', 'Red']:
                tank_image_dict[f'Tank_{tank}'][group] = {}
                for direction in ['Up', 'Down', 'Left', 'Right']:
                    tank_image_dict[f'Tank_{tank}'][group][direction] = []

        for row in range(16):
            for col in range(16):
                surface = pygame.Surface((gc.SPRITE_SIZE, gc.SPRITE_SIZE))
                surface.fill('black')
                surface.blit(self.sprite_sheet, (0, 0), (col * gc.SPRITE_SIZE, row * gc.SPRITE_SIZE,
                                                         gc.SPRITE_SIZE, gc.SPRITE_SIZE))
                surface.set_colorkey('black')
                surface = pygame.transform.scale_by(surface, gc.SPRITE_SCALE)
                tank_level = self._sort_tanks_into_levels(row)
                tank_group = self._sort_tanks_into_groups(row, col)
                tank_direction = self._sort_tanks_by_direction(col)
                tank_image_dict[tank_level][tank_group][tank_direction].append(surface)
        return tank_image_dict

    @staticmethod
    def _load_score_screen_images():
        score_screen_images = {}
        for image in ['hiScore', 'arrow', 'player1', 'pts', 'stage', 'total']:
            score_screen_images[image] = load_ind_img(image)

        return score_screen_images

    @staticmethod
    def _sort_tanks_into_levels(row):
        tank_levels = {0: 'Tank_0', 1: 'Tank_1', 2: 'Tank_2', 3: 'Tank_3',
                       4: 'Tank_4', 5: 'Tank_5', 6: 'Tank_6', 7: 'Tank_7'}
        return tank_levels[row % 8]

    @staticmethod
    def _sort_tanks_into_groups(row, col):
        if 0 <= row <= 7 and 0 <= col <= 7:
            return 'Gold'
        elif 8 <= row <= 16 and 0 <= col <= 7:
            return 'Green'
        elif 0 <= row <= 7 and 8 <= col <= 16:
            return 'Silver'
        else:
            return 'Red'

    @staticmethod
    def _sort_tanks_by_direction(col):
        if col % 8 <= 1:
            return 'Up'
        elif col % 8 <= 3:
            return 'Left'
        elif col % 8 <= 5:
            return 'Down'
        else:
            return 'Right'

    def _get_img_dict(self, img_coord_dict, background_color='black', is_transparent_background=True):
        img_dict = {}
        for key, rect in img_coord_dict.items():
            image = self._get_img(rect[0], rect[1], rect[2], rect[3], background_color, is_transparent_background)
            img_dict[key] = image

        return img_dict

    def _get_img(self, pos_x, pos_y, width, height, background_color='black', is_transparent_background=True):
        surface = pygame.Surface((width, height))
        surface.fill(background_color)
        surface.blit(self.sprite_sheet, (0, 0), (pos_x, pos_y, width, height))
        if is_transparent_background:
            surface.set_colorkey(background_color)
        surface = pygame.transform.scale_by(surface, gc.SPRITE_SCALE)
        return surface


def load_ind_img(path, scale=False, factor=1):
    image = pygame.image.load(f"assets/{path}.png").convert_alpha()
    if scale:
        image = pygame.transform.scale_by(image, factor)
    return image
