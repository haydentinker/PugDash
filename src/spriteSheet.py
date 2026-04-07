import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, char_col, char_row, frame_col, frame_row, width, height, scale, color):
        frame_x = char_col * (width * 4) + frame_col * width
        frame_y = char_row * (height * 4) + frame_row * height
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), (frame_x, frame_y, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image