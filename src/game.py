import pygame
import json
import os
from player import Player
from ground import Ground
from obstacles import Obstacle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Game():
    def __init__(self, screen, width, height):
        bg_image_path = os.path.join(BASE_DIR, 'assets', 'Summer.jpg')
        bg_image = pygame.image.load(bg_image_path)
        self.bg_image = pygame.transform.scale(bg_image, (width, height))
        self.width = width
        self.height = height
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.frame = 0
        self.ground = Ground(height)
        self.pug = Player(0, 0.6)
        self.pug.y = self.ground.y - self.pug.surface_rect.height - self.pug.surface_rect.y - self.pug.ground_offset
        self.pug.rect.topleft = (self.pug.x + self.pug.surface_rect.x, self.pug.y + self.pug.surface_rect.y)
        self.obstacle = Obstacle(self.width, 0, 125, 150, 1)
        self.obstacle.y = self.ground.y - self.obstacle.surface_rect.height - self.obstacle.surface_rect.y - self.pug.ground_offset
        self.obstacle.rect.topleft = (self.obstacle.x + self.obstacle.surface_rect.x, self.obstacle.y + self.obstacle.surface_rect.y)
        self.backgroundScroll = 0
        self.font = pygame.font.SysFont(None, 36)
        self.screen = screen
        self.animation_steps = 4
        self.gameOver = False
        self.highScore = 0
        self.UnlockedCharacters = []
        self.gameInfo_path = os.path.join(BASE_DIR, 'gameInfo.json')
        self._load_game_info()
   
    def _load_game_info(self):
        try:
            with open(self.gameInfo_path, 'r') as file:
                jsonData = json.load(file)
                self.highScore = jsonData.get('HighScore', 0)
                self.UnlockedCharacters = jsonData.get('UnlockedCharacters', [])
        except (FileNotFoundError, json.JSONDecodeError):
            self.highScore = 0
            self.UnlockedCharacters = []
            self._save_game_info()
   
    def _save_game_info(self):
        with open(self.gameInfo_path, 'w') as file:
            json.dump({'HighScore': self.highScore, 'UnlockedCharacters': self.UnlockedCharacters}, file)
   
    def checkNewHighScore(self):
        if self.pug.score > self.highScore:
            self.highScore = self.pug.score
            self._save_game_info()
   
    def resetGame(self):
        self.gameOver = False
        self.backgroundScroll = 0
        self.pug = Player(0, 0.6)
        self.pug.y = self.ground.y - self.pug.surface_rect.height - self.pug.surface_rect.y - self.pug.ground_offset
        self.pug.rect.topleft = (self.pug.x + self.pug.surface_rect.x, self.pug.y + self.pug.surface_rect.y)
        self.obstacle = Obstacle(self.width, 0, 125, 150, 1)
        self.obstacle.y = self.ground.y - self.obstacle.surface_rect.height - self.obstacle.surface_rect.y - self.pug.ground_offset
        self.obstacle.rect.topleft = (self.obstacle.x + self.obstacle.surface_rect.x, self.obstacle.y + self.obstacle.surface_rect.y)
   
    def runGame(self):
        text = f"Score: {self.pug.score}  High Score: {self.highScore}"
        text_surface = self.font.render(text, True, (255, 255, 255))
        keys = pygame.key.get_pressed()
        self.obstacle.x -= self.obstacle.speed
        if keys[pygame.K_SPACE] and self.pug.jump_counter == 1:
            self.pug.velocity = self.pug.jump_strength
            self.pug.jump_counter = 0
        self.pug.y += self.pug.velocity
        self.pug.velocity += self.pug.acceleration
        if self.pug.y >= self.ground.y - self.pug.surface_rect.height - self.pug.surface_rect.y - self.pug.ground_offset:
            self.pug.y = self.ground.y - self.pug.surface_rect.height - self.pug.surface_rect.y - self.pug.ground_offset
            self.pug.velocity = 0
            self.pug.jump_counter = 1

        jumping = self.pug.jump_counter == 0 or self.pug.velocity != 0
        if jumping:
            self.pug.air_velocity = min(self.pug.air_velocity + self.pug.air_acceleration, self.pug.max_air_offset)
            self.pug.x = min(self.pug.x + self.pug.air_velocity, self.pug.base_x + self.pug.max_air_offset)
        else:
            self.pug.air_velocity = 0
            self.pug.x = max(self.pug.x - self.pug.air_return_speed, self.pug.base_x)

        current_time = pygame.time.get_ticks()
        dt = current_time - self.last_update
        self.pug.update_animation(dt, jumping=jumping)
        self.last_update = current_time
        current_frame = self.pug.get_frame(jumping=jumping)
        frame_rect = current_frame.get_bounding_rect()
        self.pug.rect = pygame.Rect(self.pug.x + frame_rect.x, self.pug.y + frame_rect.y, frame_rect.width, frame_rect.height)

        self.obstacle.y = self.ground.y - self.obstacle.surface_rect.height - self.obstacle.surface_rect.y - self.pug.ground_offset
        self.obstacle.rect.topleft = (self.obstacle.x + self.obstacle.surface_rect.x, self.obstacle.y + self.obstacle.surface_rect.y)
        if self.obstacle.get_collision_rect().colliderect(self.pug.get_collision_rect()):
            self.gameOver = True

        self.screen.fill((0, 0, 255))

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame = (self.frame + 1) % self.animation_steps
            self.last_update = current_time

        self.screen.blit(self.bg_image, (self.backgroundScroll, 0))
        self.screen.blit(self.bg_image, (self.backgroundScroll + self.width, 0))
        self.backgroundScroll -= self.obstacle.speed
        if self.backgroundScroll <= -self.width:
            self.backgroundScroll += self.width

        self.screen.blit(current_frame, (self.pug.x, self.pug.y))
   
        if self.gameOver:
            self.checkNewHighScore()
            return
        if self.obstacle.x > -self.obstacle.rect.width:
            self.screen.blit(self.obstacle.treeImage, (self.obstacle.x, self.obstacle.y))
        else:
            self.pug.score += 1
            self.obstacle.x = self.width
            self.obstacle.y = self.ground.y - self.obstacle.surface_rect.height - self.obstacle.surface_rect.y - self.pug.ground_offset
            self.obstacle.rect.topleft = (self.obstacle.x + self.obstacle.surface_rect.x, self.obstacle.y + self.obstacle.surface_rect.y)
            if self.pug.score % 5 == 0:
                self.obstacle.speed += 1
        self.screen.blit(text_surface, (0, 0))
 
   
