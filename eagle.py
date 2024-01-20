import pygame
from explosion import Explosion


class Eagle(pygame.sprite.Sprite):
    def __init__(self, pos, assets, groups: dict):
        self.groups = groups
        self.eagle_group = self.groups['eagle']
        super().__init__(self.eagle_group)
        self.assets = assets
        self.pos_x, self.pos_y = pos

        self.is_destroyed = False
        self.timer = pygame.time.get_ticks()

        self.image = self.assets.eagle['intact']
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

    def update(self):
        pass

    def get_destroyed(self):
        Explosion(self.rect.center, 'big', self.assets, self.groups['explosions'])
        self.is_destroyed = True
        self.image = self.assets.eagle['destroyed']
