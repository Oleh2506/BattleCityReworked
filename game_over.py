import pygame
import game_config as gc
from game_assets import GameAssets


class GameOver:
    def __init__(self, assets: GameAssets):
        self.assets = assets

        self.game_over_image = self.assets.context['game_over']
        self.width, self.height = self.game_over_image.get_size()
        self.game_over_rect = self.game_over_image.get_rect(center=(gc.IN_GAME_LEVEL_SCREEN_BORDER_LEFT
                                                            + gc.IN_GAME_LEVEL_SCREEN[2] // 2,
                                                            gc.SCREEN_HEIGHT + self.height))
        self.timer = pygame.time.get_ticks()
        self.is_active = True

    def update(self):
        if self.game_over_rect.y > gc.SCREEN_HEIGHT // 2 - self.height//2:
            self.game_over_rect.y -= 10
        elif self.game_over_rect.y < gc.SCREEN_HEIGHT // 2 - self.height//2:
            self.game_over_rect.y = gc.SCREEN_HEIGHT // 2 - self.height//2
            self.timer = pygame.time.get_ticks()

        if self.game_over_rect.y == gc.SCREEN_HEIGHT//2 - self.height//2:
            if pygame.time.get_ticks() - self.timer >= 5000:
                self.is_active = False

    def draw(self, window):
        window.blit(self.game_over_image, self.game_over_rect)


class EndGameScreen:
    def __init__(self, assets: GameAssets, is_game_over):
        self.assets = assets
        self.is_gave_over = is_game_over
        self.overlay_screen = self._generate_overlay_screen()
        self.is_active = True
        self.timer = pygame.time.get_ticks()

    def draw(self, window):
        window.blit(self.overlay_screen, (0, 0))

    def update(self):
        if pygame.time.get_ticks() - self.timer >= 3000:
            self.is_active = False

    def _generate_overlay_screen(self):
        overlay_screen = pygame.Surface((gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT))
        overlay_screen.fill('black')
        line_1 = self.assets.gave_over_screen_font.render('GAME', False, 'white')
        line_1_rect = line_1.get_rect(center=gc.GO_LINE_1_POS)
        if self.is_gave_over:
            line_2 = self.assets.gave_over_screen_font.render('OVER', False, 'white')
        else:
            line_2 = self.assets.gave_over_screen_font.render('COMPLETED', False, 'white')
        line_2_rect = line_2.get_rect(center=gc.GO_LINE_2_POS)
        overlay_screen.blit(line_1, line_1_rect)
        overlay_screen.blit(line_2, line_2_rect)

        return overlay_screen
