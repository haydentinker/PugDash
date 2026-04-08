import pygame
import json
import os
from player import Player
from ground import Ground
from obstacles import Obstacle

try:
    import js
    _HAS_JS = True
except ImportError:
    _HAS_JS = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

character_data = {
    "Base": (0, 0),
    "Speedy": (0, 1),
    "Jumpy": (0, 2),
    "Pug4": (0, 3),
    "Pug5": (1, 0),
    "Pug6": (1, 1),
    "Pug7": (1, 2),
    "Pug8": (1, 3),
    "Pug9": (2, 0),
    "Pug10": (2, 1),
    "Pug11": (2, 2),
    "Pug12": (2, 3),
}

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
        self.gameInfo_path = os.path.join(BASE_DIR, 'gameInfo.json')
        self._load_game_info()
        self.selected_col, self.selected_row = character_data.get(self.selected_character, (0, 0))
        self.ground = Ground(height)
        self.pug = Player(0, 0.6, self.selected_col, self.selected_row)
        self.pug.y = self.ground.y - self.pug.surface_rect.height - self.pug.surface_rect.y - self.pug.ground_offset
        self.pug.rect.topleft = (self.pug.x + self.pug.surface_rect.x, self.pug.y + self.pug.surface_rect.y)
        self.obstacle = Obstacle(self.width, 0, 125, 150, 1)
        self.obstacle.y = self.ground.y - self.obstacle.surface_rect.height - self.obstacle.surface_rect.y - self.pug.ground_offset
        self.obstacle.rect.topleft = (self.obstacle.x + self.obstacle.surface_rect.x, self.obstacle.y + self.obstacle.surface_rect.y)
        self.backgroundScroll = 0
        self.font = pygame.font.Font(None, 36)
        self.screen = screen
        self.animation_steps = 4
        self.gameOver = False
   
    def _load_game_info(self):
        jsonData = None
        if _HAS_JS:
            try:
                item = js.localStorage.getItem('pugdash_gameInfo')
                if item:
                    jsonData = json.loads(item)
            except Exception:
                pass
        if jsonData is None:
            try:
                with open(self.gameInfo_path, 'r') as file:
                    jsonData = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                pass
        if jsonData:
            self.highScore = jsonData.get('HighScore', 0)
            self.UnlockedCharacters = jsonData.get('UnlockedCharacters', [])
            self.selected_character = jsonData.get('SelectedCharacter', 'Base')
        else:
            self.highScore = 0
            self.UnlockedCharacters = []
            self.selected_character = 'Base'
            self._save_game_info()

    def _save_game_info(self):
        data = {'HighScore': self.highScore, 'UnlockedCharacters': self.UnlockedCharacters, 'SelectedCharacter': self.selected_character}
        if _HAS_JS:
            try:
                js.localStorage.setItem('pugdash_gameInfo', json.dumps(data))
            except Exception:
                pass
        try:
            with open(self.gameInfo_path, 'w') as file:
                json.dump(data, file)
        except Exception:
            pass
   
    def checkNewHighScore(self):
        if self.pug.score > self.highScore:
            self.highScore = self.pug.score
            self._save_game_info()
   
    def resetGame(self):
        self.gameOver = False
        self.backgroundScroll = 0
        self.pug = Player(0, 0.6, self.selected_col, self.selected_row)
        self.pug.y = self.ground.y - self.pug.surface_rect.height - self.pug.surface_rect.y - self.pug.ground_offset
        self.pug.rect.topleft = (self.pug.x + self.pug.surface_rect.x, self.pug.y + self.pug.surface_rect.y)
        self.obstacle = Obstacle(self.width, 0, 125, 150, 1)
        self.obstacle.y = self.ground.y - self.obstacle.surface_rect.height - self.obstacle.surface_rect.y - self.pug.ground_offset
        self.obstacle.rect.topleft = (self.obstacle.x + self.obstacle.surface_rect.x, self.obstacle.y + self.obstacle.surface_rect.y)
   
    def runGame(self):
        text = f"Score: {self.pug.score}  High Score: {self.highScore}"
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_bg = pygame.Surface((text_surface.get_width() + 10, text_surface.get_height() + 5))
        text_bg.fill((255, 255, 255))
        text_bg.set_alpha(180)
        self.screen.blit(text_bg, (-5, -2))
        self.screen.blit(text_surface, (0, 0))
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
 
   
