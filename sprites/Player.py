import pygame
from constants import SKY_HEIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        walk_image_1 = pygame.image.load(
            "assets/graphics/Player/pig.png"
        ).convert_alpha()
        
        self.jump_image = pygame.image.load(
            "assets/graphics/Player/pig.png"
        ).convert_alpha()
        self.walk_images = [walk_image_1]
        self.frame_index = 0
        self.image = walk_image_1
        self.rect = self.image.get_rect(bottomleft=(80, SKY_HEIGHT))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound("assets/audio/jump.mp3")
        self.jump_sound.set_volume(0.4)

    def handle_jump(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= SKY_HEIGHT:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= SKY_HEIGHT:
            self.rect.bottom = SKY_HEIGHT

    def animate(self):
        if self.rect.bottom < SKY_HEIGHT:
            self.image = self.jump_image
        else:
            self.frame_index += 0.1
            if self.frame_index >= len(self.walk_images):
                self.frame_index = 0
            self.image = self.walk_images[int(self.frame_index)]

    def update(self):
        self.handle_jump()
        self.apply_gravity()
        self.animate()
