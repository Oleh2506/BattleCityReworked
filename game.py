import pygame
import game_config as gc
from game_assets import GameAssets
from characters import PlayerTank, EnemyTank, SpecialTank
from tiles import BrickTile, SteelTile, IceTile, ForestTile, WaterTile
from game_hud import GameHud
from score_screen import ScoreScreen
from game_over import GameOver, EndGameScreen
from eagle import Eagle
from stage_intro import StageIntro


class Game:
    def __init__(self, assets: GameAssets, stages):
        # Common game attributes
        self.assets = assets
        self.stages = stages
        self.stage_index = 0
        self.is_active = True
        self.is_game_over = False

        # Game over
        self.game_over_slide_screen = None
        self.is_game_over_slide_screen_active = False

        # End Game Screen
        self.end_game_screen = None
        self.is_end_game_screen_active = False

        # HUD
        self.hud = GameHud(self.assets)

        # Stage Intro
        self.stage_intro = StageIntro(self.assets, len(stages), False)
        self.is_stage_intro_active = True

        # Stage Score Screen
        self.score_screen = ScoreScreen(self.assets)
        self.is_score_screen_active = False

        # In-game stage info
        # Groups
        self.tanks = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.shields = pygame.sprite.GroupSingle()
        self.bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.ices = pygame.sprite.Group()
        self.forests = pygame.sprite.Group()
        self.waters = pygame.sprite.Group()
        self.powerups = pygame.sprite.GroupSingle()
        self.eagles = pygame.sprite.GroupSingle()
        self.groups = {'tanks': self.tanks,
                       'obstacles': self.obstacles,
                       'shields': self.shields,
                       'bullets': self.bullets,
                       'explosions': self.explosions,
                       'ices': self.ices,
                       'forests': self.forests,
                       'waters': self.waters,
                       'powerup': self.powerups,
                       'eagle': self.eagles}

        # Pause
        self.pause_img = self.assets.context['pause']
        self.pause_img_rect = self.pause_img.get_rect(center=gc.PAUSE_POS)

        # Common stage attributes
        self.is_stage_active = False
        self.curr_stage_num = 1
        self.enemy_spawns_pos_list = gc.DEFAULT_ENEMIES_SPAWN_POS
        self.enemy_queue = self.stages[self.stage_index]['enemy_queue']
        self.not_spawned_enemies_num = len(self.enemy_queue)
        self.player_spawn_pos = gc.DEFAULT_PLAYER_SPAWN_POS
        self.is_paused = False
        self.enemy_spawn_counter = 240
        self.enemies_limit = gc.MAX_ENEMIES_AT_TIME
        self.enemy_spawn_pos_index = 1
        self.enemy_spawn_index = 0
        self.transition_counter = 0
        self.high_score = gc.DEFAULT_HIGH_SCORE
        self.player_score = 0
        self.extra_lives_score = 0
        self.fort_pos_list = []
        self.fort_counter = 0
        self.do_fortify = False

        self._load_stage_map()
        self.player = PlayerTank(self.player_spawn_pos, 'Up', 'Gold', 0, self.assets, self.groups)

    def input(self, event_list):
        if self.is_stage_active and not self.is_game_over and not self.is_game_over_slide_screen_active:
            for event in event_list:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.is_paused = not self.is_paused
                    if event.key == pygame.K_ESCAPE:
                        self.is_active = False

        if self.is_stage_active:
            self.player.event_list = event_list

        if self.is_stage_intro_active and not self.stage_intro.is_start_stage_chosen:
            self.stage_intro.input(event_list)
            if self.stage_intro.is_start_stage_chosen:
                self.stage_index = self.stage_intro.stage_index
                self._start_new_stage()

    def _update_for_score_screen(self):
        self.is_stage_active = False
        self.is_score_screen_active = True
        self.score_screen.is_active = True
        self.score_screen.view_results_timer = pygame.time.get_ticks()
        self.player_score += sum(self.player.score_list)
        add_extra_life = (self.player_score - self.extra_lives_score) // self.high_score
        self.player.extra_lives += add_extra_life
        self.extra_lives_score = add_extra_life * self.high_score
        self.score_screen.update_values(self.player.score_list, self.player_score, self.stage_index)

    def update(self):
        if self.is_stage_active:
            if not self.is_paused:
                self.hud.update(self.stage_index + 1, self.not_spawned_enemies_num, self.player.extra_lives)
                self.tanks.update()
                self.shields.update()
                self.bullets.update()
                self.explosions.update()
                self.waters.update()
                self.powerups.update()

                self._spawn_enemies()

                if self.player.start_fortify:
                    self.do_fortify = True
                    self._fortify(False)
                    self.fort_counter = 0
                    self.player.start_fortify = False

                if self.do_fortify:
                    self.fort_counter += 1
                    if self.fort_counter >= 240:
                        self._fortify(True)
                        self.fort_counter = 0
                        self.do_fortify = False

                if (self.player.extra_lives < 0 or self.eagles.sprite.is_destroyed) and not self.is_game_over:
                    self.is_game_over = True
                    self.game_over_slide_screen = GameOver(self.assets)
                    self.is_game_over_slide_screen_active = self.game_over_slide_screen.is_active
                elif self.not_spawned_enemies_num == 0 and len(self.tanks.sprites()) == 1:
                    self.transition_counter += 1
                    if self.transition_counter >= 120:
                        self._update_for_score_screen()
                        self.transition_counter = 0

            if self.game_over_slide_screen and self.is_game_over and self.is_game_over_slide_screen_active:
                self.game_over_slide_screen.update()
                self.is_game_over_slide_screen_active = self.game_over_slide_screen.is_active
                if not self.is_game_over_slide_screen_active:
                    self._update_for_score_screen()

        elif self.is_stage_intro_active:
            self.stage_intro.update()
            self.is_stage_intro_active = self.stage_intro.is_active
            if not self.is_stage_intro_active:
                self.is_stage_active = True

        elif self.is_score_screen_active:
            self.score_screen.update()
            self.is_score_screen_active = self.score_screen.is_active
            if self.is_game_over and not self.is_score_screen_active:
                self.is_end_game_screen_active = True
                self.end_game_screen = EndGameScreen(self.assets, True)
            elif not self.is_game_over and not self.is_score_screen_active:
                self.stage_index += 1
                if self.stage_index < len(self.stages):
                    self.stage_intro.is_active = True
                    self.is_stage_intro_active = True
                    self.stage_intro.update_stage_index(self.stage_index)
                    self._start_new_stage()
                else:
                    self.is_end_game_screen_active = True
                    self.end_game_screen = EndGameScreen(self.assets, False)

        elif self.end_game_screen and self.is_end_game_screen_active:
            self.end_game_screen.update()
            self.is_end_game_screen_active = self.end_game_screen.is_active
            if not self.is_end_game_screen_active:
                self.is_active = False

    def draw(self, screen):
        self.hud.draw(screen)
        if self.is_stage_active:

            self.eagles.draw(screen)
            self.ices.draw(screen)
            self.waters.draw(screen)
            self.tanks.draw(screen)
            self.shields.draw(screen)
            self.obstacles.draw(screen)
            self.powerups.draw(screen)
            self.bullets.draw(screen)
            self.forests.draw(screen)
            self.explosions.draw(screen)

            if self.is_paused:
                screen.blit(self.pause_img, self.pause_img_rect)

            if self.is_game_over_slide_screen_active and self.game_over_slide_screen:
                self.game_over_slide_screen.draw(screen)

        elif self.is_stage_intro_active:
            self.stage_intro.draw(screen)

        elif self.is_score_screen_active:
            self.score_screen.draw(screen)

        elif self.is_end_game_screen_active and self.end_game_screen:
            self.end_game_screen.draw(screen)

    def _spawn_enemies(self):
        if self.not_spawned_enemies_num == 0:
            return

        tanks_on_the_screen_num = len(self.tanks.sprites())

        if tanks_on_the_screen_num < (self.enemies_limit + 1):
            self.enemy_spawn_counter += 1

            if self.enemy_spawn_counter >= 240:
                pos = self.enemy_spawns_pos_list[self.enemy_spawn_pos_index]
                self.enemy_spawn_pos_index += 1
                self.enemy_spawn_pos_index %= len(self.enemy_spawns_pos_list)
                if self.enemy_spawn_index in [3, 10, 17]:
                    SpecialTank(pos, 'Down', 'Silver', self.enemy_queue[self.enemy_spawn_index] + 4,
                                self.assets, self.groups)
                else:
                    EnemyTank(pos, 'Down', 'Silver', self.enemy_queue[self.enemy_spawn_index] + 4,
                              self.assets, self.groups)
                self.enemy_spawn_index += 1
                self.not_spawned_enemies_num -= 1
                self.enemy_spawn_counter = 0

    def _fortify(self, is_brick):
        for pos in self.fort_pos_list:
            for tile in self.groups['obstacles']:
                if (tile.pos_x, tile.pos_y) == pos:
                    tile.kill()

            for tile in self.groups['waters']:
                if (tile.pos_x, tile.pos_y) == pos:
                    tile.kill()

            for tile in self.groups['ices']:
                if (tile.pos_x, tile.pos_y) == pos:
                    tile.kill()

            for tile in self.groups['forests']:
                if (tile.pos_x, tile.pos_y) == pos:
                    tile.kill()

        if is_brick:
            for pos in self.fort_pos_list:
                BrickTile(pos, self.assets, self.obstacles)
        else:
            for pos in self.fort_pos_list:
                SteelTile(pos, self.assets, self.obstacles)

    @staticmethod
    def _get_fortify_pos(eagle_pos, stage_map):
        fortify_pos_list = []
        for (x, y) in eagle_pos:
            for x_offset in [-1, 0, 1]:
                for y_offset in [-1, 0, 1]:
                    if (0 <= x + x_offset < 26) and (0 <= y + y_offset < 26):
                        if stage_map[x + x_offset][y + y_offset] < 5:
                            pos = (gc.IN_GAME_LEVEL_SCREEN_BORDER_LEFT + ((y + y_offset) * gc.SMALL_TILE_SIZE),
                                   gc.IN_GAME_LEVEL_SCREEN_BORDER_TOP + ((x + x_offset) * gc.SMALL_TILE_SIZE))
                            if pos not in fortify_pos_list:
                                fortify_pos_list.append(pos)
        return fortify_pos_list

    def _start_new_stage(self):
        for key, group in self.groups.items():
            group.empty()

        self._load_stage_map()
        self.enemy_queue = self.stages[self.stage_index]['enemy_queue']
        self.not_spawned_enemies_num = len(self.enemy_queue)
        self.enemy_spawn_pos_index = 1
        self.enemy_spawn_index = 0
        self.enemy_spawn_counter = 240
        self.fort_counter = 0
        self.do_fortify = False
        self.player.new_stage_spawn(self.player_spawn_pos)

    def _load_stage_map(self):
        stage_map = self.stages[self.stage_index]['map']

        ignore_list = []
        enemy_spawn_pos_0 = gc.DEFAULT_ENEMIES_SPAWN_POS[0]
        enemy_spawn_pos_1 = gc.DEFAULT_ENEMIES_SPAWN_POS[1]
        enemy_spawn_pos_2 = gc.DEFAULT_ENEMIES_SPAWN_POS[2]
        eagle_pos = []
        for i, row in enumerate(stage_map):
            for j, tile_index in enumerate(row):
                if (i, j) not in ignore_list:
                    pos = (gc.IN_GAME_LEVEL_SCREEN_BORDER_LEFT + (j * gc.SMALL_TILE_SIZE),
                           gc.IN_GAME_LEVEL_SCREEN_BORDER_TOP + (i * gc.SMALL_TILE_SIZE))

                    if int(tile_index) >= 5:
                        ignore_list.append((i + 1, j))
                        ignore_list.append((i, j + 1))
                        ignore_list.append((i + 1, j + 1))

                        if int(tile_index) == 5:
                            eagle_pos.append((i, j))
                            eagle_pos.append((i + 1, j))
                            eagle_pos.append((i, j + 1))
                            eagle_pos.append((i + 1, j + 1))

                            self.fort_pos_list = self._get_fortify_pos(eagle_pos, stage_map)

                    if int(tile_index) == 0:
                        BrickTile(pos, self.assets, self.obstacles)
                    elif int(tile_index) == 1:
                        SteelTile(pos, self.assets, self.obstacles)
                    elif int(tile_index) == 2:
                        ForestTile(pos, self.assets, self.forests)
                    elif int(tile_index) == 3:
                        IceTile(pos, self.assets, self.ices)
                    elif int(tile_index) == 4:
                        WaterTile(pos, self.assets, self.waters)
                    elif int(tile_index) == 5:
                        Eagle(pos, self.assets, self.groups)
                    elif int(tile_index) == 6:
                        self.player_spawn_pos = pos
                    elif int(tile_index) == 7:
                        enemy_spawn_pos_0 = pos
                    elif int(tile_index) == 8:
                        enemy_spawn_pos_1 = pos
                    elif int(tile_index) == 9:
                        enemy_spawn_pos_2 = pos

        self.enemy_spawns_pos_list = [enemy_spawn_pos_0, enemy_spawn_pos_1, enemy_spawn_pos_2]
