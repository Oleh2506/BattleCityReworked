import pygame
import random
import game_config as gc
from game_assets import GameAssets


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, assets: GameAssets, groups: dict):
        self.groups = groups
        self.powerup_group = self.groups['powerup']
        super().__init__(self.powerup_group)
        self.assets = assets
        self.images = self.assets.powerups

        self.pos_x = random.randint(gc.IN_GAME_LEVEL_SCREEN_BORDER_LEFT,
                                    gc.IN_GAME_LEVEL_SCREEN_BORDER_RIGHT - gc.IMAGE_SIZE)
        self.pos_y = random.randint(gc.IN_GAME_LEVEL_SCREEN_BORDER_TOP,
                                    gc.IN_GAME_LEVEL_SCREEN_BORDER_BOTTOM - gc.IMAGE_SIZE)

        self.type = random.choice(['shield', 'freeze', 'fortify', 'power', 'explosion', 'extra_life'])
        self.image = self.images[self.type]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

    def update(self):
        tank_group = self.groups['tanks']
        collided_tanks = pygame.sprite.spritecollide(self, tank_group, False)
        for tank in collided_tanks:
            if tank.is_player:
                tank.score_list.append(500)
                self._activate()

    def _activate(self):
        if self.type == 'freeze':
            self._freeze()
        elif self.type == 'power':
            self._power()
        elif self.type == 'extra_life':
            self._extra_life()
        elif self.type == 'shield':
            self._shield()
        elif self.type == 'explosion':
            self._explosion()
        elif self.type == 'fortify':
            self._fortify()

        self.kill()

    def _freeze(self):
        for tank in self.groups['tanks']:
            if not tank.is_player:
                tank.is_paralysed = True

    def _power(self):
        for tank in self.groups['tanks']:
            if tank.is_player:
                tank.update_level()

    def _extra_life(self):
        for tank in self.groups['tanks']:
            if tank.is_player:
                tank.extra_lives += 1

    def _shield(self):
        for tank in self.groups['tanks']:
            if tank.is_player:
                tank.shield_start = True
                tank.is_shielded = True

    def _explosion(self):
        for tank in self.groups['tanks']:
            if not tank.is_player:
                tank.get_destroyed()

    def _fortify(self):
        for tank in self.groups['tanks']:
            if tank.is_player:
                tank.start_fortify = True
