import pygame
from game_assets import GameAssets


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, explosion_type, assets: GameAssets, explosion_group):
        super().__init__(explosion_group)

        self.assets = assets
        self.explosion_type = explosion_type
        self.pos = pos
        self.frame_index = 0
        self.images = self.assets.explosions
        self.image = self.images['explode_0']
        self.rect = self.image.get_rect(center=self.pos)

        self.animation_counter = 0

    def update(self):
        if self.animation_counter >= 5:
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
                return

            if self.explosion_type == 'small' and self.frame_index == 2:
                self.kill()
                return

            self.image = self.images[f'explode_{self.frame_index}']
            self.rect = self.image.get_rect(center=self.pos)

            self.animation_counter = 0

        self.animation_counter += 1
