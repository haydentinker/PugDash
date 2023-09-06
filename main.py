import pygame
from spriteSheet import SpriteSheet
from player import Player
from ground import Ground
from obstacles import Obstacle
from game import Game

def main():
    pygame.init()
    gameStarted=False
    screen_height = 600
    screen_width = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pug Dash")
    running = True
    newGame=Game(screen,screen_width,screen_height)
    while running:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not gameStarted:
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if 325<= mouse[0] <= 470 and 200 <= mouse[1] <= 240:
                        gameStarted=True
                    elif 325<= mouse[0] <= 470 and 300 <= mouse[1] <= 340:
                        running=False
                    elif 330<= mouse[0] <= 470 and 400 <= mouse[1] <= 440:
                        running=False
                
        if not gameStarted:
            pygame.draw.rect(newGame.screen,(60,179,113),(0,0,newGame.width,newGame.height))
            #Title
            title_font = pygame.font.Font("freesansbold.ttf", 100)
            title = title_font.render("Pug Dash", True, (255, 255, 255))
            newGame.screen.blit(title, (180, 50))
            
            #Menu Buttons
            item_font = pygame.font.Font("freesansbold.ttf", 50)
            item1 = item_font.render("Start", True, (255, 255, 255))
            newGame.screen.blit(item1, (325, 200))
            item2 = item_font.render("Store", True, (255, 255, 255))
            newGame.screen.blit(item2, (325, 300))
            item3 = item_font.render("Quit", True, (255, 255, 255))
            newGame.screen.blit(item3, (325, 400))
            newGame.gameOver=False
        else:
            newGame.runGame()
            if newGame.gameOver:
                gameStarted=False    
        pygame.display.flip()
        clock.tick(60)
        

    pygame.quit()
if __name__ == "__main__":
    main()
