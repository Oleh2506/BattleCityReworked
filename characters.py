import pygame
import game_config as gc
from game_assets import GameAssets
from bullet import Bullet
from explosion import Explosion
import random
from shield import Shield
from powerups import PowerUp


class Tank(pygame.sprite.Sprite):
    def __init__(self, pos, direction, color, level, assets: GameAssets, groups: dict):
        self.obstacle_group = groups['obstacles']
        self.tank_group = groups['tanks']
        self.groups = groups

        super().__init__(self.tank_group)

        self.pos_x, self.pos_y = pos
        self.spawn_pos = pos
        self.direction = direction
        self.color = color
        self.level = level
        self.health = gc.TANK_HEALTH
        self.assets = assets

        self.tank_images = assets.tank_images
        self.spawn_images = assets.spawn_star_images
        self.is_spawning = True
        self.is_special = False
        self.speed = gc.TANK_SPEED
        self.bullet_speed = gc.BULLET_SPEED
        self.bullet_damage = gc.BULLET_DAMAGE
        self.bullet_limit = gc.BULLET_LIMIT
        self.bullet_sum = 0
        self.is_player = False
        self.score = 0

        self._adjust_parameters()

        self.spawn_frame_index = 0
        self.spawn_animation_counter = 0
        self.image = self.spawn_images[f'star_{self.spawn_frame_index}']
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.width, self.height = self.image.get_size()

        self.frame_index = 0

        self.spawn_counter = 0
        self.spawn_animation_duration = 30

        self.mask_dict = self._get_mask_dict()
        self.mask = self.mask_dict[self.direction]
        self.mask_direction = self.direction
        self.score_list = []
        self.extra_lives = 0
        self.is_shielded = False
        self.shield_start = False
        self.start_fortify = False

        self.is_paralysed = False
        self.paralysis_counter = 0

    def _adjust_parameters(self):
        criterion = gc.TANK_CRITERIA[self.level]
        self.bullet_limit = criterion['bullet_limit']
        self.bullet_speed = gc.BULLET_SPEED * criterion['bullet_speed']
        self.speed = gc.TANK_SPEED * criterion['speed']
        self.bullet_damage = criterion['bullet_power']
        self.health = criterion['health']
        self.score = criterion['score']

    def update_level(self):
        if self.level <= 2:
            self.level += 1
        self._adjust_parameters()

    def _get_mask_dict(self):
        images = {}
        for direction in ['Up', 'Down', 'Left', 'Right']:
            image_to_mask = self.tank_images[f'Tank_{self.level}'][self.color][direction][0]
            images[direction] = pygame.mask.from_surface(image_to_mask)
        return images

    def _animate_spawning(self):
        self.spawn_frame_index += 1
        self.spawn_frame_index = self.spawn_frame_index % len(self.spawn_images)
        self.spawn_animation_counter = 0
        self.image = self.spawn_images[f'star_{self.spawn_frame_index}']
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

    @staticmethod
    def _smooth_movement(pos):
        if pos % (gc.IMAGE_SIZE // 2) != 0:
            if pos % (gc.IMAGE_SIZE // 2) < gc.IMAGE_SIZE // 4:
                pos -= (pos % (gc.IMAGE_SIZE // 4))
            else:
                pos += (gc.IMAGE_SIZE // 4) - (pos % (gc.IMAGE_SIZE // 4))
        return pos

    def _move(self, direction):
        if self.is_spawning:
            return

        self.direction = direction

        if direction == 'Up':
            self.pos_y -= self.speed
            self.pos_x = self._smooth_movement(self.pos_x)
            if self.pos_y < gc.IN_GAME_LEVEL_SCREEN_BORDER_TOP:
                self.pos_y = gc.IN_GAME_LEVEL_SCREEN_BORDER_TOP
        elif direction == 'Down':
            self.pos_y += self.speed
            self.pos_x = self._smooth_movement(self.pos_x)
            if self.pos_y + self.height > gc.IN_GAME_LEVEL_SCREEN_BORDER_BOTTOM:
                self.pos_y = gc.IN_GAME_LEVEL_SCREEN_BORDER_BOTTOM - self.height
        elif direction == 'Left':
            self.pos_x -= self.speed
            self.pos_y = self._smooth_movement(self.pos_y)
            if self.pos_x < gc.IN_GAME_LEVEL_SCREEN_BORDER_LEFT:
                self.pos_x = gc.IN_GAME_LEVEL_SCREEN_BORDER_LEFT
        elif direction == 'Right':
            self.pos_x += self.speed
            self.pos_y = self._smooth_movement(self.pos_y)
            if self.pos_x + self.width > gc.IN_GAME_LEVEL_SCREEN_BORDER_RIGHT:
                self.pos_x = gc.IN_GAME_LEVEL_SCREEN_BORDER_RIGHT - self.width

        self.rect.topleft = (self.pos_x, self.pos_y)
        self._animate_movement()
        self._collide_with_tanks()
        self._collide_with_impassable_tiles()

    def _shoot(self):
        if self.bullet_sum >= self.bullet_limit:
            return

        Bullet(self.rect.center, self.direction, self.assets, self, self.groups)
        self.bullet_sum += 1

    def _animate_movement(self):
        self.frame_index += 0.5
        img_list_length = len(self.tank_images[f'Tank_{self.level}'][self.color][self.direction])
        if self.frame_index >= img_list_length:
            self.frame_index = 0
        self.image = self.tank_images[f'Tank_{self.level}'][self.color][self.direction][int(self.frame_index)]
        if self.mask_direction != self.direction:
            self.mask_direction = self.direction
            self.mask = self.mask_dict[self.mask_direction]

    def _collide_with_tanks(self):
        collided_tanks = pygame.sprite.spritecollide(self, self.tank_group, False)

        if len(collided_tanks) == 1:
            return

        for tank in collided_tanks:
            if tank == self or tank.is_spawning:
                continue

            if self.direction == 'Right':
                if self.rect.right >= tank.rect.left and self.rect.bottom > tank.rect.top \
                        and self.rect.top < tank.rect.bottom:
                    self.rect.right = tank.rect.left
                    self.pos_x = self.rect.x
            elif self.direction == 'Left':
                if self.rect.left <= tank.rect.right and self.rect.bottom > tank.rect.top \
                        and self.rect.top < tank.rect.bottom:
                    self.rect.left = tank.rect.right
                    self.pos_x = self.rect.x
            elif self.direction == 'Up':
                if self.rect.top <= tank.rect.bottom and self.rect.left < tank.rect.right \
                        and self.rect.right > tank.rect.left:
                    self.rect.top = tank.rect.bottom
                    self.pos_y = self.rect.y
            elif self.direction == 'Down':
                if self.rect.bottom >= tank.rect.top and self.rect.left < tank.rect.right \
                        and self.rect.right > tank.rect.left:
                    self.rect.bottom = tank.rect.top
                    self.pos_y = self.rect.y

    def _collide_on_spawn(self):
        if not self.is_spawning:
            return

        collided_tanks = pygame.sprite.spritecollide(self, self.tank_group, False)
        if len(collided_tanks) == 1:
            return

        for tank in collided_tanks:
            if tank == self or tank.is_spawning:
                continue

            if self.spawn_counter == self.spawn_animation_duration:
                tank.get_destroyed()

    def _collide_with_impassable_tiles(self):
        collided_obstacles = pygame.sprite.spritecollide(self, self.obstacle_group, False)
        collided_obstacles += pygame.sprite.spritecollide(self, self.groups['waters'], False)
        collided_obstacles += pygame.sprite.spritecollide(self, self.groups['eagle'], False)

        for obstacle in collided_obstacles:
            if self.direction == 'Right' and self.rect.right >= obstacle.rect.left:
                self.rect.right = obstacle.rect.left
                self.pos_x = self.rect.x
            elif self.direction == 'Left' and self.rect.left <= obstacle.rect.right:
                self.rect.left = obstacle.rect.right
                self.pos_x = self.rect.x
            elif self.direction == 'Down' and self.rect.bottom >= obstacle.rect.top:
                self.rect.bottom = obstacle.rect.top
                self.pos_y = self.rect.y
            elif self.direction == 'Up' and self.rect.top <= obstacle.rect.bottom:
                self.rect.top = obstacle.rect.bottom
                self.pos_y = self.rect.y

    def input(self):
        pass

    def update(self):
        if self.is_spawning:
            if self.spawn_animation_counter >= 1:
                self._animate_spawning()
            else:
                self.spawn_animation_counter += 1

            if self.spawn_counter == self.spawn_animation_duration:
                self._collide_on_spawn()
                self.is_spawning = False
                self.image = self.tank_images[f'Tank_{self.level}'][self.color][self.direction][int(self.frame_index)]
                self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

            self.spawn_counter += 1
        else:
            if not self.is_paralysed:
                self.input()
            else:
                if self.paralysis_counter >= 240:
                    self.paralysis_counter = 0
                    self.is_paralysed = False
                else:
                    self.paralysis_counter += 1

    def get_damaged(self):
        self.health -= 1

        if self.health <= 0:
            self.get_destroyed()
            return True

        if self.health == 3:
            self.color = 'Green'
        elif self.health == 2:
            self.color = 'Gold'
        elif self.health == 1:
            self.color = 'Silver'

        return False

    def get_destroyed(self):
        Explosion(self.rect.center, 'big', self.assets, self.groups['explosions'])
        self.kill()


class PlayerTank(Tank):
    def __init__(self, pos, direction, color, level, assets: GameAssets, groups: dict):
        super().__init__(pos, direction, color, level, assets, groups)

        self.shield_group = groups['shields']
        self.is_shielded = True
        self.shield_start = True
        self.shield_images = self.assets.shield_images
        self.is_player = True
        self.event_list = []
        self.extra_lives = gc.DEFAULT_EXTRA_LIVES

    def get_damaged(self):
        if not self.is_shielded:
            super().get_damaged()

    def get_destroyed(self):
        Explosion(self.rect.center, 'big', self.assets, self.groups['explosions'])

        self.shield_group.empty()
        self.extra_lives -= 1
        if self.extra_lives < 0:
            self.kill()
            return

        self._respawn()

    def input(self):
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_w]:
            self._move('Up')
        elif key_pressed[pygame.K_s]:
            self._move('Down')
        elif key_pressed[pygame.K_a]:
            self._move('Left')
        elif key_pressed[pygame.K_d]:
            self._move('Right')
        else:
            collided_ices = pygame.sprite.spritecollide(self, self.groups['ices'], False)
            if len(collided_ices) >= 3:
                self._move(self.direction)

        for event in self.event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._shoot()

    def update(self):
        super().update()

        if not self.is_spawning:
            if self.is_shielded:
                if self.shield_start:
                    Shield(self, self.shield_group)
                    self.shield_start = False

                if len(self.shield_group) == 0:
                    self.is_shielded = False

    def _respawn(self):
        self.is_spawning = True
        self.spawn_counter = 0
        self.direction = 'Up'
        self.pos_x, self.pos_y = self.spawn_pos
        self.spawn_frame_index = 0
        self.spawn_animation_counter = 0
        self.image = self.spawn_images[f'star_{self.spawn_frame_index}']
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.frame_index = 0
        self.is_shielded = True
        self.shield_start = True
        self.health = gc.TANK_HEALTH
        self.level = 0
        self._adjust_parameters()

    def new_stage_spawn(self, pos):
        self.tank_group.add(self)
        self.is_spawning = True
        self.spawn_counter = 0
        self.direction = 'Up'
        self.spawn_pos = pos
        self.pos_x, self.pos_y = self.spawn_pos
        self.is_shielded = True
        self.shield_start = True
        self.image = self.spawn_images[f'star_{self.spawn_frame_index}']
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.score_list.clear()
        self.frame_index = 0
        self.spawn_frame_index = 0
        self.spawn_animation_counter = 0


class MyRect(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = None
        self.rect = pygame.Rect(x, y, width, height)


class EnemyTank(Tank):
    def __init__(self, pos, direction, color, level, assets: GameAssets, groups: dict):
        super().__init__(pos, direction, color, level, assets, groups)

        self.dir_rect_dict = {
            'Left': MyRect(self.pos_x - (self.width // 2), self.pos_y, self.width // 2, self.height),
            'Right': MyRect(self.pos_x + self.width, self.pos_y, self.width // 2, self.height),
            'Up': MyRect(self.pos_x, self.pos_y - (self.height // 2), self.width, self.height // 2),
            'Down': MyRect(self.pos_x, self.pos_y + self.height, self.width, self.height // 2)
        }
        self.change_direction_counter = 0
        self.between_shots_counter = 0
        self.intervals_between_shots = [45, 60, 90]
        self.shot_interval = self.intervals_between_shots[0]
        self.level_screen_rect = pygame.Rect(gc.IN_GAME_LEVEL_SCREEN)
        self.move_directions = []

    def input(self):
        self._choose_direction()
        self._move(self.direction)
        if self.between_shots_counter >= self.shot_interval:
            self._shoot()
            self.between_shots_counter = 0
            self.shot_interval = random.choice(self.intervals_between_shots)
        else:
            self.between_shots_counter += 1

    def _move(self, direction):
        super()._move(direction)
        self.dir_rect_dict['Left'].rect.update(self.pos_x - (self.width // 2), self.pos_y, self.width // 2, self.height)
        self.dir_rect_dict['Right'].rect.update(self.pos_x + self.width, self.pos_y, self.width // 2, self.height)
        self.dir_rect_dict['Up'].rect.update(self.pos_x, self.pos_y - (self.height // 2), self.width, self.height // 2)
        self.dir_rect_dict['Down'].rect.update(self.pos_x, self.pos_y + self.height, self.width, self.height // 2)

    def _choose_direction(self):
        directional_list_copy = self.move_directions.copy()
        if self.change_direction_counter <= 60:
            self.change_direction_counter += 1
            return

        self.change_direction_counter = 0

        for key, value in self.dir_rect_dict.items():
            if pygame.Rect.contains(self.level_screen_rect, value):
                obst = pygame.sprite.spritecollideany(value, self.groups['obstacles'])
                if not obst:
                    obst = pygame.sprite.spritecollideany(value, self.groups['waters'])

                if not obst:
                    if key not in directional_list_copy:
                        directional_list_copy.append(key)
                elif obst:
                    if value.rect.contains(obst.rect) and key in directional_list_copy:
                        directional_list_copy.remove(key)
                    else:
                        if key in directional_list_copy and key != self.direction:
                            directional_list_copy.remove(key)

                eagle = pygame.sprite.spritecollideany(value, self.groups['eagle'])
                if eagle:
                    if key in directional_list_copy:
                        directional_list_copy.remove(key)

                tank = pygame.sprite.spritecollideany(value, self.groups['tanks'])
                if tank:
                    if key in directional_list_copy:
                        directional_list_copy.remove(key)
            else:
                if key in directional_list_copy:
                    directional_list_copy.remove(key)

        if self.move_directions != directional_list_copy or (self.direction not in directional_list_copy):
            self.move_directions = directional_list_copy.copy()
            if len(self.move_directions) > 0:
                self.direction = random.choice(self.move_directions)


class SpecialTank(EnemyTank):
    def __init__(self, pos, direction, color, level, assets: GameAssets, groups: dict):
        super().__init__(pos, direction, color, level, assets, groups)

        self.color_swap_counter = 0
        self.is_special = True
        self.base_color = self.color

    def update(self):
        super().update()

        self.color_swap_counter += 1
        if self.color_swap_counter > 6:
            self.color = 'Red' if self.color == self.base_color else self.base_color
            self.color_swap_counter = 0

    def get_destroyed(self):
        PowerUp(self.assets, self.groups)
        super().get_destroyed()
