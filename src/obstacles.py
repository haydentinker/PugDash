import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Obstacle():
    def __init__(self, x, y, width, height, scale):
        self.x = x
        self.y = y
        self.scale = scale
        self.height = height
        self.width = width
        self.speed = 3.5
        image_path = os.path.join(BASE_DIR, 'assets', 'bush.png')
        self.treeImage = pygame.transform.scale(
            pygame.image.load(image_path).convert_alpha(),
            (int(width * scale), int(height * scale))
        )
        surface_rect = self.treeImage.get_bounding_rect()
        self.surface_rect = surface_rect
        self.rect = pygame.Rect(self.x + surface_rect.x, self.y + surface_rect.y, surface_rect.width, surface_rect.height)
        self.hitbox_padding = 12

    def get_collision_rect(self):
        collision_rect = self.rect.copy()
        collision_rect.inflate_ip(-self.hitbox_padding, -self.hitbox_padding // 2)
        return collision_rect

    def get_image(self):
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.treeImage, (0, 0))
        return image
