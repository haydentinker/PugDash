import pygame

class Obstacle():
    def __init__(self,x,y,height,width):
        self.x=x
        self.y=y
        self.height=height
        self.width=width
        self.speed=3
    
    def getRect(self):
        return pygame.Rect(self.x,self.y,self.width,self.height)