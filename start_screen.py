import pygame
import game_config as gc
from game_assets import GameAssets


class StartScreen:
    def __init__(self, assets: GameAssets):
        self.assets = assets

        self.start_screen = pygame.surface.Surface((gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT))
        self.start_screen.fill('black')
        self.pos_y = gc.SCREEN_HEIGHT
        self.scroll_speed = gc.SS_SCROLL_SPEED
        self.is_scroll_animation_completed = False

        self.is_active = True

        self.is_default_game_active = False
        self.is_custom_game_active = False
        self.is_stage_editor_active = False

        self.option_font = self.assets.start_screen_option_font
        self.option_positions = gc.OPTION_POSITIONS
        self.default_stages_option = self.option_font.render('DEFAULT STAGES', False, 'white')
        self.default_stages_option_rect = self.default_stages_option.get_rect(topleft=self.option_positions[0])
        self.custom_stages_option = self.option_font.render('CUSTOM STAGES', False, 'white')
        self.custom_stages_option_rect = self.custom_stages_option.get_rect(topleft=self.option_positions[1])
        self.stage_editor_option = self.option_font.render('STAGE EDITOR', False, 'white')
        self.stage_editor_option_rect = self.stage_editor_option.get_rect(topleft=self.option_positions[2])

        self.title_font = self.assets.start_screen_title_font
        self.title_positions = gc.TITLE_POSITIONS
        self.title_word_1 = self.title_font.render('BATTLE CITY', False, 'red')
        self.title_word_1_rect = self.title_word_1.get_rect(center=self.title_positions[0])
        self.title_word_2 = self.title_font.render('REWORKED', False, 'red')
        self.title_word_2_rect = self.title_word_2.get_rect(center=self.title_positions[1])

        self.token_positions = gc.TOKEN_POSITIONS
        self.token_image = self.assets.token_image
        self.token_index = 0
        self.token_image_rect = self.token_image.get_rect(topleft=self.token_positions[self.token_index])

        self.start_screen.blit(self.default_stages_option, self.default_stages_option_rect)
        self.start_screen.blit(self.custom_stages_option, self.custom_stages_option_rect)
        self.start_screen.blit(self.stage_editor_option, self.stage_editor_option_rect)
        self.start_screen.blit(self.title_word_1, self.title_word_1_rect)
        self.start_screen.blit(self.title_word_2, self.title_word_2_rect)

    def draw(self, screen):
        screen.blit(self.start_screen, (0, self.pos_y))
        if self.is_scroll_animation_completed:
            screen.blit(self.token_image, self.token_image_rect)

    def input(self, event_list: list):
        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE:
                if not self.is_scroll_animation_completed:
                    self._complete_scroll_animation()
                    return

                if event.key == pygame.K_w:
                    self.token_index -= 1
                    self.token_index = self.token_index % len(self.token_positions)
                    self.token_image_rect.topleft = self.token_positions[self.token_index]

                if event.key == pygame.K_s:
                    self.token_index += 1
                    self.token_index = self.token_index % len(self.token_positions)
                    self.token_image_rect.topleft = self.token_positions[self.token_index]

                if event.key == pygame.K_RETURN:
                    self._select_option()
                    self.is_active = False

    def update(self):
        self._animate_scroll()

    def _animate_scroll(self):
        if self.pos_y == 0:
            self.is_scroll_animation_completed = True

        self.pos_y -= self.scroll_speed
        if self.pos_y < 0:
            self.pos_y = 0

    def _complete_scroll_animation(self):
        self.pos_y = 0

    def _select_option(self):
        if self.token_index == 0:
            self.is_default_game_active = True
        elif self.token_index == 1:
            self.is_custom_game_active = True
        elif self.token_index == 2:
            self.is_stage_editor_active = True
        else:
            self.is_default_game_active = True
