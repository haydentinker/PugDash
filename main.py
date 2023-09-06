import pygame
from spriteSheet import SpriteSheet
from player import Player
from ground import Ground
from obstacles import Obstacle

pygame.init()
gameOver=True
screen_height = 600
screen_width = 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Pug Dash")
running = True
font = pygame.font.Font(None, 36)

ground = Ground(screen_height)
pug = Player(0, 0.5)
obstacle= Obstacle(screen_width,ground.y-100,50,50)
bg_image=pygame.image.load('assets/Summer.jpg')
bg_image=pygame.transform.scale(bg_image,(screen_width,screen_height))
last_update=pygame.time.get_ticks()
animation_cooldown=100
frame=0
animation_list=[]
animation_steps=4
backgroundScroll=0
while running:
    text=f"Score: {pug.score}"
    text_surface=font.render(text,True,(255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys=pygame.key.get_pressed()
    obstacle.x-=obstacle.speed
    if keys[pygame.K_SPACE]:
        if pug.jump_counter==1:
            pug.velocity=-12
            pug.jump_counter-=1
        
    pug.y += pug.velocity
    pug.velocity += pug.acceleration

   
    if pug.y >= (ground.y - pug.sprite_height):
        pug.y = ground.y - pug.sprite_height
        pug.velocity = 0
        pug.jump_counter = 1
    if (
        obstacle.x <= (pug.x + pug.sprite_width) and
        (pug.y + pug.sprite_height) >= ground.y - pug.sprite_height and
        (pug.x <= obstacle.x + obstacle.width)
    ):
        gameOver=True
    screen.fill((0, 0, 255))
    current_time=pygame.time.get_ticks()
    if current_time-last_update>=animation_cooldown:
        frame+=1
        last_update=current_time
        if frame >=animation_steps:
            frame=0
    # for x in background:
    #     screen.blit(x,(0,0))

    screen.blit(bg_image,(backgroundScroll,0))
    screen.blit(bg_image,(screen_width+backgroundScroll,0))
    if(backgroundScroll==-screen_width):
        screen.blit(bg_image,(screen_width+backgroundScroll,0))
        backgroundScroll=0
    backgroundScroll-=1
    # pygame.draw.rect(screen, (0, 250, 0), (0, ground.y, screen_width, screen_height - ground.y))
    screen.blit(pug.getRunFrame(frame),(pug.x,pug.y-4*pug.sprite_height))
    # if gameOver:
    
    # else:
    if(not obstacle.x<=-obstacle.width):
        pygame.draw.rect(screen, (0, 0, 0), obstacle.getRect()) 
            
    else:
        pug.score+=1
        obstacle.x=screen_width
        obstacle.speed+=1
    screen.blit(text_surface, (0, 0))
   
   
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

