import pygame

from sprites.Obstacle import Obstacle


class Knife(Obstacle):
    def __init__(self):
        image1 = pygame.image.load("assets/graphics/Knife/knife.png").convert_alpha()

        super().__init__(image1, 200)
