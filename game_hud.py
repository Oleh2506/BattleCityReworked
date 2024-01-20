import pygame
import game_config as gc
from game_assets import GameAssets


class GameHud:
    def __init__(self, assets: GameAssets):
        self.assets = assets
        self.images = self.assets.hud_images
        self.hud_overlay = self._generate_hud_overlay_screen()
        self.font = self.assets.hud_overlay_font

        self.level_num = 0
        self.level_image = self._generate_level_number_img(self.level_num)
        self.level_image_rect = self.level_image.get_rect(topleft=gc.LEVEL_IMAGE_POS)

        self.player_extra_lives = 0
        self.player_extra_lives_image = self._generate_player_extra_lives_img(self.player_extra_lives)
        self.player_extra_lives_image_rect = self.player_extra_lives_image.get_rect(topleft=gc.PLAYER_EXTRA_LIVES_POS)

        self.enemies_left = 0
        self.remaining_enemies_image = self._generate_remaining_tanks_img(self.enemies_left)
        self.remaining_enemies_image_rect = self.remaining_enemies_image.get_rect(topleft=gc.REMAINING_TANKS_POS)

    def _generate_hud_overlay_screen(self):
        overlay_screen = pygame.Surface((gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT))
        overlay_screen.fill(gc.GRAY)
        pygame.draw.rect(overlay_screen, 'black', gc.IN_GAME_LEVEL_SCREEN)
        overlay_screen.blit(self.images['info_panel'], (gc.INFO_PANEL_X, gc.INFO_PANEL_Y))
        return overlay_screen

    def _generate_remaining_tanks_img(self, enemies_left):
        surface = pygame.Surface((gc.IMAGE_SIZE, gc.IMAGE_SIZE * 5))
        surface.fill(gc.GRAY)

        row = 0
        for num in range(gc.DEFAULT_NUMBER_OF_ENEMIES):
            if num % 2 == 0:
                x, y = 0, row * (gc.IMAGE_SIZE // 2)
            else:
                x, y = gc.IMAGE_SIZE // 2, row * (gc.IMAGE_SIZE // 2)
                row += 1
            if num < enemies_left:
                surface.blit(self.images['enemy_life'], (x, y))
            else:
                surface.blit(self.images['grey_square'], (x, y))

        return surface

    def _generate_level_number_img(self, level):
        if level > 99:
            level = 99

        width, height = gc.IMAGE_SIZE, gc.IMAGE_SIZE // 2
        surface = pygame.Surface((width, height))
        surface.fill(gc.GRAY)
        string_image_to_display = str(level)
        if level < 10:
            string_image_to_display = '0' + string_image_to_display

        image = self.font.render(string_image_to_display, False, 'black')
        surface.blit(image, (0, 0))

        return surface

    def _generate_player_extra_lives_img(self, extra_lives_num):
        if extra_lives_num > 99:
            extra_lives_num = 99
        if extra_lives_num < 0:
            extra_lives_num = 0

        width, height = gc.IMAGE_SIZE, gc.IMAGE_SIZE // 2
        surface = pygame.Surface((width, height))
        surface.fill(gc.GRAY)

        if extra_lives_num < 10:
            surface.blit(self.images['player_life'], (0, 0))
            surface.blit(self.font.render(str(extra_lives_num), False, 'black'), (gc.IMAGE_SIZE // 2, 0))
        else:
            surface.blit(self.font.render(str(extra_lives_num), False, 'black'), (0, 0))

        return surface

    def update(self, current_level, not_spawned_enemies, extra_lives):
        if self.enemies_left != not_spawned_enemies:
            self.enemies_left = not_spawned_enemies
            self.remaining_enemies_image = self._generate_remaining_tanks_img(self.enemies_left)

        if self.player_extra_lives != extra_lives:
            self.player_extra_lives = extra_lives
            self.player_extra_lives_image = self._generate_player_extra_lives_img(self.player_extra_lives)

        if self.level_num != current_level:
            self.level_num = current_level
            self.level_image = self._generate_level_number_img(self.level_num)

    def draw(self, screen):
        screen.blit(self.hud_overlay, (0, 0))
        screen.blit(self.player_extra_lives_image, self.player_extra_lives_image_rect)
        screen.blit(self.remaining_enemies_image, self.remaining_enemies_image_rect)
        screen.blit(self.level_image, self.level_image_rect)
