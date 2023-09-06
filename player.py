import pygame
from spriteSheet import SpriteSheet
class Player():
    def __init__(self,velocity,acceleration):
        self.x=0
        self.y=0
        self.sprite_width=32
        self.sprite_height=25
        self.acceleration=acceleration
        self.velocity=velocity
        self.jump_counter=1
        self.score=0
        sprite_sheet_image=pygame.image.load('assets/pugCharacterSheet.png').convert_alpha()
        self.spriteSheet=SpriteSheet(sprite_sheet_image)
        self.runFrames=[]
        for x in range(4):
            self.runFrames.append(self.spriteSheet.get_image(x,32,25,3,(0,174,0)))

    def getRunFrame(self,frame):
        return self.runFrames[frame]
