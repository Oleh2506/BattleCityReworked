from __future__ import annotations
import pygame
import characters


class Shield(pygame.sprite.Sprite):
    def __init__(self, owner: characters.PlayerTank, shield_group):
        super().__init__(shield_group)

        self.owner = owner
        self.pos_x, self.pos_y = owner.pos_x, owner.pos_y
        self.frame_index = 0
        self.shield_images = owner.shield_images
        self.shield_counter = 0

        self.image = self.shield_images[f'shield_{int(self.frame_index)}']
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

    def _animate(self):
        self.frame_index += 0.25
        if self.frame_index >= len(self.shield_images):
            self.frame_index = 0
        self.image = self.shield_images[f'shield_{int(self.frame_index)}']

    def update(self):
        self.rect.topleft = (self.owner.pos_x, self.owner.pos_y)

        if self.shield_counter >= 240:
            self.kill()
            return

        self.shield_counter += 1

        self._animate()
