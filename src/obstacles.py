import pygame

class Obstacle():
    def __init__(self, x, y, height, width, scale):
        self.x = x
        self.y = y
        self.scale = scale
        self.height = height
        self.width = width
        self.speed = 3.5
        self.treeImage = pygame.transform.scale(pygame.image.load('assets/bush.png'), (125, 150))
        self.rect=self.treeImage.get_rect().scale_by(.5,.95)
    

    def get_image(self):
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        image.blit(self.treeImage, (self.x, self.y))
        image.set_colorkey((255, 255, 255))
        return image
