import pygame
import os
from spriteSheet import SpriteSheet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Player():
    def __init__(self, velocity, acceleration, char_col=0, char_row=0):
        self.x = 50
        self.base_x = 50
        self.y = 0
        self.scale = 3
        self.sprite_width = 32 * self.scale
        self.sprite_height = 32 * self.scale
        self.ground_offset = 45
        self.acceleration = acceleration
        self.velocity = velocity
        self.air_velocity = 0
        self.air_acceleration = 0.4
        self.air_return_speed = 0.8
        self.max_air_offset = 18
        self.jump_strength = -18
        self.jump_counter = 1
        self.score = 0
        sprite_sheet_image = pygame.image.load(os.path.join(BASE_DIR, 'assets', 'pugCharacterSheet.png')).convert_alpha()
        self.spriteSheet = SpriteSheet(sprite_sheet_image)
        self.runFrames = [
            self.spriteSheet.get_image(char_col, char_row, frame_index, 0, 32, 32, self.scale, (0, 174, 0))
            for frame_index in range(4)
        ]
        self.jumpFrame = self.spriteSheet.get_image(char_col, char_row, 0, 1, 32, 32, self.scale, (0, 174, 0))
        self.surface_rect = self.runFrames[0].get_bounding_rect()
        self.rect = pygame.Rect(self.x + self.surface_rect.x, self.y + self.surface_rect.y, self.surface_rect.width, self.surface_rect.height)
        self.frame = 0
        self.last_anim_update = pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.hitCounter = 0
        self.hitbox_padding = 8

    def get_frame(self, jumping=False):
        if jumping:
            return self.jumpFrame
        return self.runFrames[self.frame]

    def update_animation(self, dt, jumping=False):
        if jumping:
            return
        self.last_anim_update += dt
        if self.last_anim_update >= self.animation_cooldown:
            self.last_anim_update %= self.animation_cooldown
            self.frame = (self.frame + 1) % len(self.runFrames)

    def get_collision_rect(self):
        collision_rect = self.rect.copy()
        collision_rect.inflate_ip(-self.hitbox_padding, -self.hitbox_padding)
        return collision_rect
