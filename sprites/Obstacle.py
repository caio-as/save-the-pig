import pygame
from random import randint


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image1, y_pos):
        super().__init__()

        self.images = [image1]
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

        self.speed = 8

    def animate(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.images):
            self.frame_index = 0
        self.image = self.images[int(self.frame_index)]

    def update(self):
        self.animate()
        self.rect.x -= self.speed

        if self.rect.x < -50:
            self.kill()
