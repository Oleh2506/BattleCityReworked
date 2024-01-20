import pygame
import game_config as gc
from game_assets import GameAssets


class StageIntro:
    def __init__(self, assets: GameAssets, max_stage_num, is_start_stage_chosen):
        self.assets = assets
        self.images = self.assets.hud_images
        self.speed = 10
        self.stage_index = 0
        self.max_stage_num = max_stage_num
        self.is_start_stage_chosen = is_start_stage_chosen

        self.is_active = True
        self.fade_in = True
        self.fade_out = False
        self.transition = False
        self.timer = pygame.time.get_ticks()

        self.top_rect = pygame.Rect(0, 0 - gc.SCREEN_HEIGHT//2, gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT//2)
        self.top_rect_start_y = self.top_rect.bottom
        self.top_rect_end_y = gc.SCREEN_HEIGHT // 2
        self.top_y = self.top_rect.bottom

        self.bot_rect = pygame.Rect(0, gc.SCREEN_HEIGHT, gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT//2)
        self.bot_rect_start_y = self.bot_rect.top
        self.bot_rect_end_y = gc.SCREEN_HEIGHT // 2
        self.bot_y = self.bot_rect.top

        self.stage_image = self.assets.hud_overlay_font.render(f'STAGE {self.stage_index + 1}', False, 'black')
        self.stage_image_rect = self.stage_image.get_rect(center=(gc.SCREEN_WIDTH//2, gc.SCREEN_HEIGHT//2))

    def update_stage_index(self, stage_index):
        self.stage_index = stage_index
        self.stage_image = self.assets.hud_overlay_font.render(f'STAGE {self.stage_index + 1}', False, 'black')
        self.stage_image_rect = self.stage_image.get_rect(center=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2))

    def input(self, event_list: list):
        if self.is_start_stage_chosen:
            return

        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    if event.key == pygame.K_a:
                        self.stage_index -= 1
                        self.stage_index %= self.max_stage_num
                    else:
                        self.stage_index += 1
                        self.stage_index %= self.max_stage_num

                    self.stage_image = self.assets.hud_overlay_font.render(f'STAGE {self.stage_index + 1}', False,
                                                                           'black')
                    self.stage_image_rect = self.stage_image.get_rect(
                        center=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2))
                if event.key == pygame.K_RETURN:
                    self.is_start_stage_chosen = True

    def update(self):
        if not self.is_active:
            return
        if self.fade_in:
            self.top_y = self._move_y_fade(self.top_y, self.top_rect_start_y, self.top_rect_end_y, self.speed)
            self.top_rect.bottom = self.top_y

            self.bot_y = self._move_y_fade(self.bot_y, self.bot_rect_start_y, self.bot_rect_end_y, self.speed)
            self.bot_rect.top = self.bot_y

            if self.top_rect.bottom == self.top_rect_end_y and self.bot_rect.top == self.bot_rect_end_y:
                self.fade_in = False
                self.fade_out = False
                self.transition = True
                self.timer = pygame.time.get_ticks()

        elif self.transition:
            if self.is_start_stage_chosen and pygame.time.get_ticks() - self.timer >= 1000:
                self.fade_in = False
                self.fade_out = True
                self.transition = False

        elif self.fade_out:
            self.top_y = self._move_y_fade(self.top_y, self.top_rect_end_y, self.top_rect_start_y, self.speed)
            self.top_rect.bottom = self.top_y

            self.bot_y = self._move_y_fade(self.bot_y, self.bot_rect_end_y, self.bot_rect_start_y, self.speed)
            self.bot_rect.top = self.bot_y

            if self.top_rect.bottom == self.top_rect_start_y and \
                    self.bot_rect.top == self.bot_rect_start_y:
                self.fade_in = True
                self.fade_out = False
                self.transition = False
                self.is_active = False
                return

    def draw(self, window):
        pygame.draw.rect(window, gc.GRAY, self.top_rect)
        pygame.draw.rect(window, gc.GRAY, self.bot_rect)
        if self.transition:
            window.blit(self.stage_image, self.stage_image_rect)

    @staticmethod
    def _move_y_fade(y, start_pos, end_pos, speed):
        if start_pos > end_pos:
            y -= speed
            if y < end_pos:
                y = end_pos
        elif start_pos < end_pos:
            y += speed
            if y > end_pos:
                y = end_pos
        return y
