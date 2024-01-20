import pygame
import game_config as gc
from game_assets import GameAssets


class ScoreScreen:
    def __init__(self, assets: GameAssets):
        self.assets = assets
        self.font = self.assets.score_screen_font
        self.is_active = False
        self.images = self.assets.score_screen_images
        self.view_results_timer = 0
        self.high_score = gc.DEFAULT_HIGH_SCORE
        self.score_list = []
        self.tanks_num_list = [0] * 4
        self.tank_scores_list = [0] * 4
        self.tanks_total_score = 0
        self.total_stage_player_score = 0
        self.total_player_score = 0
        self.stage_index = 0
        self.total_tanks_num = 0
        self.score_sheet = self._generate_score_sheet()

    def update(self):
        if pygame.time.get_ticks() - self.view_results_timer >= 3000:
            self.is_active = False

    def update_values(self, score_list, player_score, stage_index):
        if player_score > self.high_score:
            self.high_score = player_score
        self.total_player_score = player_score

        self.score_list = score_list
        self.score_list.sort()
        self.tanks_num_list = []
        self.tanks_num_list.append(self.score_list.count(100))
        self.tanks_num_list.append(self.score_list.count(200))
        self.tanks_num_list.append(self.score_list.count(300))
        self.tanks_num_list.append(self.score_list.count(400))
        self.total_tanks_num = sum(self.tanks_num_list)
        self.tank_scores_list = []
        self.tank_scores_list.append(self.tanks_num_list[0] * 100)
        self.tank_scores_list.append(self.tanks_num_list[1] * 200)
        self.tank_scores_list.append(self.tanks_num_list[2] * 300)
        self.tank_scores_list.append(self.tanks_num_list[3] * 400)
        self.tanks_total_score = sum(self.tank_scores_list)
        self.total_stage_player_score = sum(score_list)
        self.stage_index = stage_index
        self.score_sheet = self._generate_score_sheet()

    def _generate_score_sheet(self):
        surface = pygame.Surface((gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT))
        surface.fill('black')
        new_img_size = gc.IMAGE_SIZE // 2
        surface.blit(self.images['hiScore'], (new_img_size * 8, new_img_size * 4))
        surface.blit(self.images['stage'], (new_img_size * 12, new_img_size * 6))
        surface.blit(self.images['player1'], (new_img_size * 3, new_img_size * 8))
        total_player_score_image = self.font.render(str(self.total_player_score), False, 'orange')
        total_player_score_image_rect = total_player_score_image.get_rect(topright=(new_img_size * 11,
                                                                                    new_img_size * 10))
        surface.blit(total_player_score_image, total_player_score_image_rect)

        arrow_left = self.images['arrow']

        for num, pos_y in enumerate([12.5, 15, 17.5, 20]):
            pts_img = self.font.render(str(self.tank_scores_list[num]), False, 'white')
            pts_img_rect = pts_img.get_rect(topright=(new_img_size * 7.5, new_img_size * pos_y))
            surface.blit(pts_img, pts_img_rect)

            surface.blit(self.images['pts'], (new_img_size * 8, new_img_size * pos_y))

            tank_num_img = self.font.render(str(self.tanks_num_list[num]), False, 'white')
            tank_num_img_rect = tank_num_img.get_rect(topright=(new_img_size * 13.5, new_img_size * pos_y))
            surface.blit(tank_num_img, tank_num_img_rect)

            surface.blit(arrow_left, (new_img_size * 14, new_img_size * pos_y))
            surface.blit(self.assets.tank_images[f'Tank_{num + 4}']['Silver']['Up'][0],
                         (new_img_size * 15, new_img_size * (pos_y - 0.5)))

        surface.blit(self.images['total'], (new_img_size * 6, new_img_size * 22))
        surface.blit(self.font.render(str(self.high_score), False, 'orange'), (new_img_size * 18, new_img_size * 4))
        surface.blit(self.font.render(str(self.stage_index + 1), False, 'white'), (new_img_size * 18, new_img_size * 6))

        total_tanks_num_img = self.font.render(str(self.total_tanks_num), False, 'white')
        total_tanks_num_img_rect = total_tanks_num_img.get_rect(topright=(new_img_size * 13.5, new_img_size * 22.5))
        surface.blit(total_tanks_num_img, total_tanks_num_img_rect)

        return surface

    def draw(self, screen):
        screen.blit(self.score_sheet, (0, 0))
