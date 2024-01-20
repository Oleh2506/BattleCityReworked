import pygame
import game_config as gc
from game_assets import GameAssets
from stage_data import StageData


class Button:
    def __init__(self, pos, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.is_clicked = False

    def input(self, event_list: list):
        self.is_clicked = False
        pos = pygame.mouse.get_pos()
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos):
                self.is_clicked = True

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class StageEditor:
    def __init__(self, assets: GameAssets):
        self.assets = assets
        self.is_active = True
        self.number_of_stages = gc.NUM_OF_CUSTOM_STAGES
        self.stage_data = StageData(gc.CUSTOM_STAGES_DIR, self.number_of_stages)
        self.stage_index = 0
        self.stages = self.stage_data.load_stage_data()
        self.map_editor_screen = MapEditor(assets, self.stages[self.stage_index]['map'], self.stage_index)
        self.config_editor_screen = ConfigEditor(assets, self.stages[self.stage_index]['enemy_queue'],
                                                 self.stage_index)
        self.is_map_editor_active = True

    def input(self, event_list: list):
        if self.is_map_editor_active:
            self.map_editor_screen.input(event_list)
            self.is_map_editor_active = self.map_editor_screen.is_active
            if not self.is_map_editor_active:
                self.config_editor_screen.is_active = True
        else:
            self.config_editor_screen.input(event_list)
            if self.config_editor_screen.save_button.is_clicked:
                if self._validate_stage():
                    self.stage_data.save_stage_by_num(self.stages[self.stage_index], self.stage_index)
                    self.config_editor_screen.display_successful_save_message()
                else:
                    self.config_editor_screen.display_failed_save_message()

            if self.config_editor_screen.reload_button.is_clicked:
                self.stage_index = 0
                self.stages = self.stage_data.load_stage_data()
                self._reload_stage()

            self.is_map_editor_active = not self.config_editor_screen.is_active
            if self.is_map_editor_active:
                self.map_editor_screen.is_active = True

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_ESCAPE]:
            self.is_active = False

        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    if event.key == pygame.K_a:
                        self.stage_index -= 1
                    else:
                        self.stage_index += 1
                    self.stage_index = self.stage_index % self.number_of_stages

                    self._reload_stage()

    def _reload_stage(self):
        self.map_editor_screen.load_new_stage(self.stages[self.stage_index]['map'])
        self.map_editor_screen.update_stage_num(self.stage_index)
        self.config_editor_screen.tank_queue = self.stages[self.stage_index]['enemy_queue']
        self.config_editor_screen.update_stage_num(self.stage_index)

    def draw(self, window):
        if self.is_map_editor_active:
            self.map_editor_screen.draw(window)
        else:
            self.config_editor_screen.draw(window)

    def update(self):
        self.config_editor_screen.update()

    def _validate_stage(self):
        for is_placed in self.map_editor_screen.are_big_tiles_placed:
            if not is_placed:
                return False

        if not self.map_editor_screen.does_fortify_available():
            return False

        if len(self.config_editor_screen.tank_queue) == 0:
            return False

        return True


class ConfigEditor:
    def __init__(self, assets: GameAssets, tank_queue: list, stage_num):
        self.assets = assets
        self.is_active = False
        self.stage_num = stage_num
        self.stage_num_image = (
            self.assets.stage_editor_font.render(f'CUSTOM STAGE {self.stage_num + 1}', False, 'white'))
        self.stage_num_image_rect = self.stage_num_image.get_rect(center=gc.CE_STAGE_NUM_POS)

        self.overlay_screen = self._generate_overlay_screen()
        self.map_button = Button(gc.MAP_BUTTON_POS, self.assets.stage_editor_font.render('EDIT MAP', False, 'white'))
        self.map_button.rect.center = gc.MAP_BUTTON_POS

        self.save_button = Button(gc.SAVE_BUTTON_POS, self.assets.stage_editor_font.render('SAVE', False, 'white'))
        self.save_button.rect.midleft = gc.SAVE_BUTTON_POS
        self.reload_button = Button(gc.RELOAD_BUTTON_POS,
                                    self.assets.stage_editor_font.render('RELOAD', False, 'white'))
        self.reload_button.rect.midright = gc.RELOAD_BUTTON_POS

        self.plus_buttons = []
        for i in range(4):
            self.plus_buttons.append(Button(gc.SE_PLUSES_POS[i], self.assets.plus_image))

        self.minus_button = Button(gc.SE_MINUS_POS, self.assets.minus_image)

        self.tank_queue = tank_queue
        self.save_message = None
        self.save_message_rect = None
        self.save_message_timer = pygame.time.get_ticks()
        self.display_save_message = False

    def input(self, event_list: list):
        self.map_button.input(event_list)
        if self.map_button.is_clicked:
            self.is_active = False

        self.reload_button.input(event_list)
        self.save_button.input(event_list)

        if len(self.tank_queue) < 20:
            for i, btn in enumerate(self.plus_buttons):
                btn.input(event_list)
                if btn.is_clicked:
                    self.tank_queue.append(i)

        self.minus_button.input(event_list)
        if self.minus_button.is_clicked:
            if len(self.tank_queue) > 0:
                self.tank_queue.pop()

    def update(self):
        if self.display_save_message:
            if pygame.time.get_ticks() - self.save_message_timer >= 2000:
                self.display_save_message = False

    def update_stage_num(self, stage_num):
        self.stage_num = stage_num
        self.stage_num_image = (
            self.assets.stage_editor_font.render(f'CUSTOM STAGE {self.stage_num + 1}', False, 'white'))
        self.stage_num_image_rect = self.stage_num_image.get_rect(center=gc.CE_STAGE_NUM_POS)

    def display_successful_save_message(self):
        self.save_message = self.assets.stage_editor_font.render('SAVED STAGE SUCCESSFULLY', False, 'green')
        self.save_message_rect = self.save_message.get_rect(center=gc.SAVE_MESSAGE_POS)
        self.display_save_message = True
        self.save_message_timer = pygame.time.get_ticks()

    def display_failed_save_message(self):
        self.save_message = self.assets.stage_editor_font.render('FAILED TO SAVE STAGE', False, 'red')
        self.save_message_rect = self.save_message.get_rect(center=gc.SAVE_MESSAGE_POS)
        self.display_save_message = True
        self.save_message_timer = pygame.time.get_ticks()

    def draw(self, window):
        window.blit(self.overlay_screen, (0, 0))
        window.blit(self.stage_num_image, self.stage_num_image_rect)
        if self.display_save_message and self.save_message:
            window.blit(self.save_message, self.save_message_rect)
        self.map_button.draw(window)
        self.reload_button.draw(window)
        self.save_button.draw(window)
        self.minus_button.draw(window)
        for btn in self.plus_buttons:
            btn.draw(window)

        for i, tank in enumerate(self.tank_queue):
            if i < 10:
                window.blit(self.assets.tank_images[f'Tank_{tank + 4}']['Silver']['Right'][0],
                            (gc.IMAGE_SIZE * (2 + i), gc.IMAGE_SIZE * 2))
            else:
                window.blit(self.assets.tank_images[f'Tank_{tank + 4}']['Silver']['Right'][0],
                            (gc.IMAGE_SIZE * (2 + i % 10), gc.IMAGE_SIZE * 3))

    def _generate_overlay_screen(self):
        overlay_screen = pygame.Surface((gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT))
        overlay_screen.fill(gc.GRAY)
        for i in range(4):
            tank_img = self.assets.tank_images[f'Tank_{i + 4}']['Silver']['Up'][0]
            overlay_screen.blit(tank_img, gc.SE_TANKS_POS[i])
        ConfigEditor._draw_grid_to_overlay_screen(overlay_screen)
        return overlay_screen

    @staticmethod
    def _draw_grid_to_overlay_screen(screen):
        vert_lines_number = gc.SE_TANK_GRID_COLS + 1
        hor_lines_number = gc.SE_TANK_GRID_ROWS + 1
        for i in range(vert_lines_number):
            pygame.draw.line(screen, 'black',
                             (gc.SE_TANK_GRID[0] + i * gc.IMAGE_SIZE, gc.SE_TANK_GRID[1]),
                             (gc.SE_TANK_GRID[0] + i * gc.IMAGE_SIZE,
                              gc.SE_TANK_GRID[1] + gc.SE_TANK_GRID[3]))
        for i in range(hor_lines_number):
            pygame.draw.line(screen, 'black',
                             (gc.SE_TANK_GRID[0], gc.SE_TANK_GRID[1] + i * gc.IMAGE_SIZE),
                             (gc.SE_TANK_GRID[0] + gc.SE_TANK_GRID[2],
                              gc.SE_TANK_GRID[1] + i * gc.IMAGE_SIZE))


class MapEditor:
    def __init__(self, assets: GameAssets, matrix, stage_num):
        self.assets = assets
        self.is_active = True
        self.stage_num = stage_num
        self.stage_num_image = (
            self.assets.stage_editor_small_font.render(f'CUSTOM STAGE {self.stage_num + 1}', False, 'white'))
        self.stage_num_image_rect = self.stage_num_image.get_rect(center=gc.ME_STAGE_NUM_POS)

        self.matrix = matrix
        self.brick = self.assets.brick_tiles['small']
        self.transparent_steel = self.assets.steel_tiles['small'].copy()
        self.transparent_steel.set_alpha(128)
        self.is_selected_scalable = True
        self.is_selected_small = True

        self.brick_option = MapEditor._generate_big_tile(self.assets.brick_tiles['small'])
        self.steel_option = MapEditor._generate_big_tile(self.assets.steel_tiles['small'])
        self.forest_option = MapEditor._generate_big_tile(self.assets.forest_tiles['small'])
        self.ice_option = MapEditor._generate_big_tile(self.assets.ice_tiles['small'])
        self.water_option = MapEditor._generate_big_tile(self.assets.water_tiles['small_0'])
        self.eagle_option = self.assets.eagle['intact']
        self.player_spawn_option = self.assets.tank_images['Tank_0']['Gold']['Up'][0]
        self.enemy_spawn_option_1 = self.assets.spawn_star_images['star_1']
        self.enemy_spawn_option_2 = self.assets.spawn_star_images['star_2']
        self.enemy_spawn_option_3 = self.assets.spawn_star_images['star_3']

        self.tile_buttons_images = [self.brick_option, self.steel_option, self.forest_option, self.ice_option,
                                    self.water_option, self.eagle_option, self.player_spawn_option,
                                    self.enemy_spawn_option_1, self.enemy_spawn_option_2, self.enemy_spawn_option_3]

        self.selected_tile_index = 0
        self.tile_images = [self.assets.brick_tiles['small'],
                            self.assets.steel_tiles['small'],
                            self.assets.forest_tiles['small'],
                            self.assets.ice_tiles['small'],
                            self.assets.water_tiles['small_0'],
                            self.assets.eagle['intact'],
                            self.assets.tank_images['Tank_0']['Gold']['Up'][0],
                            self.assets.spawn_star_images['star_1'],
                            self.assets.spawn_star_images['star_2'],
                            self.assets.spawn_star_images['star_3']]

        self.selected_tile_image = self.tile_images[self.selected_tile_index]
        self.are_big_tiles_placed = [False for _ in range(5)]
        self.big_tiles_location = self._get_big_tiles_locations(self.matrix)

        # self.config_button = generate_labeled_btn('EDIT CONFIG', self.assets.stage_editor_font, gc.CONFIG_BUTTON_POS)
        self.config_button = Button(gc.CONFIG_BUTTON_POS,
                                    self.assets.stage_editor_font.render('EDIT CONFIG', False, 'white'))
        self.config_button.rect.center = gc.CONFIG_BUTTON_POS

        self.tile_buttons = []
        for i, option in enumerate(self.tile_buttons_images):
            self.tile_buttons.append(Button(gc.TILE_OPTIONS_POS[i], option))

        self.overlay_screen = self._generate_overlay_screen()

    def load_new_stage(self, map_matrix):
        self.matrix = map_matrix
        self.are_big_tiles_placed = [False for _ in range(5)]
        self.big_tiles_location = self._get_big_tiles_locations(self.matrix)

    def update_stage_num(self, stage_num):
        self.stage_num = stage_num
        self.stage_num_image = (
            self.assets.stage_editor_small_font.render(f'CUSTOM STAGE {self.stage_num + 1}', False, 'white'))
        self.stage_num_image_rect = self.stage_num_image.get_rect(center=gc.ME_STAGE_NUM_POS)

    def does_fortify_available(self):
        eagle_pos = self.big_tiles_location[0]
        for (x, y) in eagle_pos:
            for x_offset in [-1, 0, 1]:
                for y_offset in [-1, 0, 1]:
                    if MapEditor._is_cord_in_range(x + x_offset, y + y_offset):
                        if self.matrix[y + y_offset][x + x_offset] > 5:
                            return False
        return True

    @staticmethod
    def _is_cord_in_range(x, y):
        if (0 <= x < 26) and (0 <= y < 26):
            return True
        else:
            return False

    @staticmethod
    def _draw_grid_to_overlay_screen(screen):
        vert_lines_number = (gc.SE_LEVEL_SCREEN[2]) // gc.IMAGE_SIZE * 2 + 1
        hor_lines_number = (gc.SE_LEVEL_SCREEN[3]) // gc.IMAGE_SIZE * 2 + 1
        for i in range(vert_lines_number):
            pygame.draw.line(screen, 'red',
                             (gc.SE_LEVEL_SCREEN[0] + (i * gc.IMAGE_SIZE // 2), gc.SE_LEVEL_SCREEN[1]),
                             (gc.SE_LEVEL_SCREEN[0] + (i * gc.IMAGE_SIZE // 2),
                              gc.SE_LEVEL_SCREEN_BORDER_BOTTOM))
        for i in range(hor_lines_number):
            pygame.draw.line(screen, 'red',
                             (gc.SE_LEVEL_SCREEN[0], gc.SE_LEVEL_SCREEN[1] + (i * gc.IMAGE_SIZE // 2)),
                             (gc.SE_LEVEL_SCREEN_BORDER_RIGHT,
                              gc.SE_LEVEL_SCREEN[1] + (i * gc.IMAGE_SIZE // 2)))

    def _generate_overlay_screen(self):
        overlay_screen = pygame.Surface((gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT))
        overlay_screen.fill(gc.GRAY)
        pygame.draw.rect(overlay_screen, 'black', gc.SE_LEVEL_SCREEN)
        MapEditor._draw_grid_to_overlay_screen(overlay_screen)
        for button in self.tile_buttons:
            button.draw(overlay_screen)
        return overlay_screen

    @staticmethod
    def _generate_map_matrix():
        rows = gc.STAGE_MAP_ROWS
        columns = gc.STAGE_MAP_COLS
        matrix = []
        for row in range(rows):
            line = []
            for col in range(columns):
                line.append(-1)
            matrix.append(line)
        return matrix

    @staticmethod
    def _generate_big_tile(small_tile_image):
        surface = pygame.Surface((gc.IMAGE_SIZE, gc. IMAGE_SIZE))
        surface.fill('black')
        surface.blit(small_tile_image, (0, 0))
        surface.blit(small_tile_image, (0, gc.IMAGE_SIZE // 2))
        surface.blit(small_tile_image, (gc.IMAGE_SIZE // 2, 0))
        surface.blit(small_tile_image, (gc.IMAGE_SIZE // 2, gc.IMAGE_SIZE // 2))
        surface.set_colorkey('black')

        return surface

    def input(self, event_list: list):
        for i, button in enumerate(self.tile_buttons):
            button.input(event_list)
            if button.is_clicked:
                if self.selected_tile_index != i:
                    self.selected_tile_image = self.tile_images[i]
                    if i > 4:
                        self.is_selected_scalable = False
                    else:
                        self.is_selected_scalable = True
                self.selected_tile_index = i

        self.config_button.input(event_list)
        if self.config_button.is_clicked:
            self.is_active = False

        mouse_pos = pygame.mouse.get_pos()

        if (gc.SE_LEVEL_SCREEN_BORDER_RIGHT > mouse_pos[0] > gc.SE_LEVEL_SCREEN_BORDER_LEFT and
                gc.SE_LEVEL_SCREEN_BORDER_BOTTOM > mouse_pos[1] > gc.SE_LEVEL_SCREEN_BORDER_TOP):
            if self.is_selected_scalable:
                if self.is_selected_small:
                    x = mouse_pos[0] // gc.SMALL_TILE_SIZE
                    y = mouse_pos[1] // gc.SMALL_TILE_SIZE
                    if pygame.mouse.get_pressed()[0] and self.matrix[y][x] <= 4:
                        if self.matrix[y][x] != self.selected_tile_index:
                            self.matrix[y][x] = self.selected_tile_index
                    if pygame.mouse.get_pressed()[2] and self.matrix[y][x] <= 4:
                        self.matrix[y][x] = -1
                else:
                    big_tile_cursor_list = MapEditor._get_big_tile_cursor_list(mouse_pos)
                    for (x, y) in big_tile_cursor_list:
                        if pygame.mouse.get_pressed()[0] and self.matrix[y][x] <= 4:
                            if self.matrix[y][x] != self.selected_tile_index:
                                self.matrix[y][x] = self.selected_tile_index
                        if pygame.mouse.get_pressed()[2] and self.matrix[y][x] <= 4:
                            self.matrix[y][x] = -1
            else:
                if pygame.mouse.get_pressed()[0]:
                    big_tile_cursor_list = MapEditor._get_big_tile_cursor_list(mouse_pos)
                    if not self._do_collide_with_big_tiles(big_tile_cursor_list):
                        if self.are_big_tiles_placed[self.selected_tile_index - 5]:
                            for (x, y) in self.big_tiles_location[self.selected_tile_index - 5]:
                                self.matrix[y][x] = -1
                        else:
                            self.are_big_tiles_placed[self.selected_tile_index - 5] = True

                        for (x, y) in big_tile_cursor_list:
                            self.matrix[y][x] = self.selected_tile_index

                        self.big_tiles_location[self.selected_tile_index - 5] = big_tile_cursor_list

        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and self.is_selected_scalable:
                    self.is_selected_small = not self.is_selected_small

    def _do_collide_with_big_tiles(self, big_tile_cursor_list):
        for i in range(5, 10):
            if i == self.selected_tile_index:
                continue
            if self.are_big_tiles_placed[i - 5]:
                for (x, y) in big_tile_cursor_list:
                    if (x, y) in self.big_tiles_location[i - 5]:
                        return True

        return False

    def _get_big_tiles_locations(self, matrix):
        big_tiles_loc_list = [[] for _ in range(5)]

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if 5 <= matrix[j][i] < 10:
                    big_tiles_loc_list[matrix[j][i] - 5].append((i, j))
                    self.are_big_tiles_placed[matrix[j][i] - 5] = True
        return big_tiles_loc_list

    def draw(self, window):
        window.blit(self.overlay_screen, (0, 0))
        window.blit(self.stage_num_image, self.stage_num_image_rect)

        self.config_button.draw(window)

        pygame.draw.rect(window, 'red', self.tile_buttons[self.selected_tile_index].rect, 2)

        ignore_list = []
        for i, row in enumerate(self.matrix):
            for j, tile in enumerate(row):
                if tile == -1:
                    continue
                else:
                    if (i, j) not in ignore_list:
                        if tile > 4:
                            ignore_list.append((i + 1, j))
                            ignore_list.append((i, j + 1))
                            ignore_list.append((i + 1, j + 1))
                        window.blit(self.tile_images[tile], (gc.SE_LEVEL_SCREEN[0] + (j * gc.SMALL_TILE_SIZE),
                                                             gc.SE_LEVEL_SCREEN[1] + (i * gc.SMALL_TILE_SIZE)))

        mouse_pos = pygame.mouse.get_pos()
        cursor_image = self.selected_tile_image.copy()
        cursor_image.set_alpha(128)
        if (gc.SE_LEVEL_SCREEN_BORDER_RIGHT > mouse_pos[0] > gc.SE_LEVEL_SCREEN_BORDER_LEFT and
                gc.SE_LEVEL_SCREEN_BORDER_BOTTOM > mouse_pos[1] > gc.SE_LEVEL_SCREEN_BORDER_TOP):
            if self.is_selected_scalable:
                if self.is_selected_small:
                    x = mouse_pos[0] // gc.SMALL_TILE_SIZE
                    y = mouse_pos[1] // gc.SMALL_TILE_SIZE
                    window.blit(cursor_image, (gc.SE_LEVEL_SCREEN[0] + (x * gc.SMALL_TILE_SIZE),
                                               gc.SE_LEVEL_SCREEN[1] + (y * gc.SMALL_TILE_SIZE)))
                else:
                    big_tile_cursor_list = MapEditor._get_big_tile_cursor_list(mouse_pos)
                    for (x, y) in big_tile_cursor_list:
                        window.blit(cursor_image, (gc.SE_LEVEL_SCREEN[0] + (x * gc.SMALL_TILE_SIZE),
                                                   gc.SE_LEVEL_SCREEN[1] + (y * gc.SMALL_TILE_SIZE)))
            else:
                x = round(mouse_pos[0] / gc.SMALL_TILE_SIZE)
                x = x + 1 if x <= 0 else x
                x = x - 1 if x >= 26 else x
                y = round(mouse_pos[1] / gc.SMALL_TILE_SIZE)
                y = y + 1 if y <= 0 else y
                y = y - 1 if y >= 26 else y
                window.blit(cursor_image,
                            cursor_image.get_rect(center=(gc.SE_LEVEL_SCREEN[0] + (x * gc.SMALL_TILE_SIZE),
                                                          gc.SE_LEVEL_SCREEN[1] + (y * gc.SMALL_TILE_SIZE))))

    @staticmethod
    def _get_big_tile_cursor_list(mouse_pos):
        big_tile_cursor_list = []
        x = mouse_pos[0] // gc.SMALL_TILE_SIZE
        y = mouse_pos[1] // gc.SMALL_TILE_SIZE
        closest_x = round(mouse_pos[0] / gc.SMALL_TILE_SIZE)
        closest_x = closest_x + 1 if closest_x <= 0 else closest_x
        closest_x = closest_x - 1 if closest_x >= 26 else closest_x
        closest_y = round(mouse_pos[1] / gc.SMALL_TILE_SIZE)
        closest_y = closest_y + 1 if closest_y <= 0 else closest_y
        closest_y = closest_y - 1 if closest_y >= 26 else closest_y
        right = True if closest_x > x else False
        bottom = True if closest_y > y else False

        big_tile_cursor_list.append((x, y))
        if right:
            big_tile_cursor_list.append((x + 1, y))
        else:
            big_tile_cursor_list.append((x-1, y))

        if bottom:
            big_tile_cursor_list.append((x, y + 1))
        else:
            big_tile_cursor_list.append((x, y - 1))

        if bottom and right:
            big_tile_cursor_list.append((x + 1, y + 1))
        elif bottom and not right:
            big_tile_cursor_list.append((x - 1, y + 1))
        elif not bottom and right:
            big_tile_cursor_list.append((x + 1, y - 1))
        elif not bottom and not right:
            big_tile_cursor_list.append((x - 1, y - 1))

        return big_tile_cursor_list
