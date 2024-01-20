from __future__ import annotations
import pygame
import game_config as gc
from game_assets import GameAssets
import characters
from explosion import Explosion


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, assets: GameAssets, owner: characters.Tank, groups: dict):
        self.bullet_group = groups['bullets']
        self.tank_group = groups['tanks']
        self.groups = groups

        super().__init__(self.bullet_group)

        self.pos_x, self.pos_y = pos
        self.direction = direction
        self.assets = assets

        self.owner = owner
        self.speed = owner.bullet_speed
        self.damage = owner.bullet_damage

        self.image = self.assets.bullet_images[self.direction]
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.mask = pygame.mask.from_surface(self.image)

    def _move(self):
        if self.direction == 'Up':
            self.pos_y -= self.speed
        elif self.direction == 'Down':
            self.pos_y += self.speed
        elif self.direction == 'Right':
            self.pos_x += self.speed
        elif self.direction == 'Left':
            self.pos_x -= self.speed

        self.rect.center = (self.pos_x, self.pos_y)

    def _collide_with_screen_edge(self):
        if self.rect.top <= gc.IN_GAME_LEVEL_SCREEN_BORDER_TOP \
                or self.rect.bottom >= gc.IN_GAME_LEVEL_SCREEN_BORDER_BOTTOM \
                or self.rect.left <= gc.IN_GAME_LEVEL_SCREEN_BORDER_LEFT \
                or self.rect.right >= gc.IN_GAME_LEVEL_SCREEN_BORDER_RIGHT:

            Explosion(self.rect.center, 'small', self.assets, self.groups['explosions'])
            self.update_owner()
            self.kill()

    def _collide_with_bullets(self):
        collided_bullets = pygame.sprite.spritecollide(self, self.bullet_group, False)

        if len(collided_bullets) == 1:
            return

        for bullet in collided_bullets:
            if bullet == self:
                continue

            if pygame.sprite.collide_mask(self, bullet):
                bullet.update_owner()
                bullet.kill()
                self.update_owner()
                self.kill()
                break

    def _collide_with_obstacles(self):
        collided_obstacles = pygame.sprite.spritecollide(self, self.groups['obstacles'], False)

        for obstacle in collided_obstacles:
            obstacle.get_hit_by_bullet(self)

        if len(collided_obstacles) > 0:
            Explosion(self.rect.center, 'small', self.assets, self.groups['explosions'])
            self.update_owner()
            self.kill()

    def _collide_with_eagle(self):
        if self.rect.colliderect(self.groups['eagle'].sprite.rect) and not self.groups['eagle'].sprite.is_destroyed:
            self.groups['eagle'].sprite.get_destroyed()
            Explosion(self.rect.center, 'small', self.assets, self.groups['explosions'])
            self.update_owner()
            self.kill()

    def _collide_with_tanks(self):
        collided_tanks = pygame.sprite.spritecollide(self, self.tank_group, False)

        for tank in collided_tanks:
            if self.owner == tank or tank.is_spawning:
                continue

            if (self.owner.is_player and not tank.is_player) or (not self.owner.is_player and tank.is_player):
                if pygame.sprite.collide_mask(self, tank):
                    Explosion(self.rect.center, 'small', self.assets, self.groups['explosions'])
                    is_destroyed = tank.get_damaged()
                    if is_destroyed and self.owner.is_player:
                        self.owner.score_list.append(tank.score)
                    self.update_owner()
                    self.kill()
                    break

    def update(self):
        self._move()
        self._collide_with_screen_edge()
        self._collide_with_bullets()
        self._collide_with_obstacles()
        self._collide_with_tanks()
        self._collide_with_eagle()

    def update_owner(self):
        if self.owner.bullet_sum > 0:
            self.owner.bullet_sum -= 1
