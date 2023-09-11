import pygame
from player import Player
from ground import Ground
from obstacles import Obstacle
class Game():
    def __init__(self,screen,width,height):
        bg_image=pygame.image.load('assets/Summer.jpg')
        self.bg_image=pygame.transform.scale(bg_image,(width,height))
        self.width=width
        self.height=height
        self.last_update=pygame.time.get_ticks()
        self.animation_cooldown=100
        self.frame=0
        self.ground=Ground(height)
        self.pug=Player(0,0.5)
        self.obstacle=Obstacle(self.width,0,100,200,1)
        self.backgroundScroll=0
        self.font=pygame.font.Font(None, 36)
        self.screen=screen
        self.animation_steps=4
        self.gameOver=False

    def resetGame(self):
        self.gameOver=False
        self.backgroundScroll=0
        self.pug=Player(0,0.5)
        self.obstacle=Obstacle(self.width,0,100,200,1)
    def runGame(self):
    
        pos=pygame.mouse.get_pos()
        text=f"Score: {self.pug.score}"
        text_surface=self.font.render(text,True,(255,255,255))
        keys=pygame.key.get_pressed()
        self.obstacle.x-=self.obstacle.speed
        if keys[pygame.K_SPACE]:
            if self.pug.jump_counter==1:
                self.pug.velocity=-14
                self.pug.jump_counter-=1
        self.pug.y += self.pug.velocity
        self.pug.velocity += self.pug.acceleration
        if self.pug.y >= (self.ground.y - self.pug.sprite_height):
            self.pug.y = self.ground.y - self.pug.sprite_height
            self.pug.velocity = 0
            self.pug.jump_counter = 1

        self.pug.rect.x = self.pug.x
        self.pug.rect.y = self.pug.y+20 
        self.obstacle.rect.x = self.obstacle.x  
        self.obstacle.rect.y = 440
        if self.obstacle.rect.colliderect(self.pug.rect):
            self.gameOver=True
        self.screen.fill((0, 0, 255))
        self.screen.fill((0, 0, 255))
        current_time=pygame.time.get_ticks()
        if current_time-self.last_update>=self.animation_cooldown:
            self.frame+=1
            self.last_update=current_time
            if self.frame >=self.animation_steps:
                self.frame=0

        self.screen.blit(self.bg_image,(self.backgroundScroll,0))
        self.screen.blit(self.bg_image,(self.width+self.backgroundScroll,0))
        if(self.backgroundScroll==-self.width):
            self.screen.blit(self.bg_image,(self.width+self.backgroundScroll,0))
            self.backgroundScroll=0
        self.backgroundScroll-=1
        self.screen.blit(self.pug.getRunFrame(self.frame),(self.pug.x,self.pug.y-4*self.pug.sprite_height))
    
        if self.gameOver:
            return
        if(not self.obstacle.x<=-self.obstacle.width):
            self.screen.blit(self.obstacle.treeImage,(self.obstacle.x,420)) 
        else:
            self.pug.score+=1
            self.obstacle.x=self.width
            if (self.pug.score%5==0):
                self.obstacle.speed+=1
        self.screen.blit(text_surface, (0, 0))
    
   
