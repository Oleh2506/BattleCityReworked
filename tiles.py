import pygame
from game_assets import GameAssets
from bullet import Bullet
from abc import ABC, abstractmethod


class Obstacle(ABC):
    @abstractmethod
    def get_hit_by_bullet(self, bullet: Bullet):
        pass


class BrickTile(Obstacle, pygame.sprite.Sprite):
    def __init__(self, pos, assets: GameAssets, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)

        self.pos_x, self.pos_y = pos
        self.assets = assets

        self.image = self.assets.brick_tiles['small']
        self.images = self.assets.brick_tiles
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

        self.health = 2

    def get_hit_by_bullet(self, bullet: Bullet):
        self.health -= 1
        if self.health <= 0 or bullet.damage >= 2:
            self.kill()
            return

        if bullet.direction == 'Left':
            self.image = self.images['small_left']
        elif bullet.direction == 'Right':
            self.image = self.images['small_right']
        elif bullet.direction == 'Up':
            self.image = self.images['small_top']
        elif bullet.direction == 'Down':
            self.image = self.images['small_bot']


class SteelTile(Obstacle, pygame.sprite.Sprite):
    def __init__(self, pos, assets: GameAssets, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)

        self.pos_x, self.pos_y = pos
        self.assets = assets

        self.image = self.assets.steel_tiles['small']
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

    def get_hit_by_bullet(self, bullet: Bullet):
        if bullet.damage >= 2:
            self.kill()
            return


class IceTile(pygame.sprite.Sprite):
    def __init__(self, pos, assets: GameAssets, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)

        self.pos_x, self.pos_y = pos
        self.assets = assets

        self.image = self.assets.ice_tiles['small']
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))


class ForestTile(pygame.sprite.Sprite):
    def __init__(self, pos, assets: GameAssets, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)

        self.pos_x, self.pos_y = pos
        self.assets = assets

        self.image = self.assets.forest_tiles['small']
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))


class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, assets: GameAssets, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)

        self.pos_x, self.pos_y = pos
        self.assets = assets

        self.frame_index = 0
        self.images = self.assets.water_tiles
        self.image = self.assets.water_tiles['small_0']
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

    def update(self):
        self.frame_index += 0.05
        if self.frame_index >= len(self.images):
            self.frame_index = 0

        self.image = self.images[f'small_{int(self.frame_index)}']
