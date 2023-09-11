import pygame
from spriteSheet import SpriteSheet
from player import Player
from ground import Ground
from obstacles import Obstacle
from game import Game

def main():
    pygame.init()
    gameStarted = False
    screen_height = 600
    screen_width = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pug Dash")
    running = True
    newGame = Game(screen, screen_width, screen_height)
    
    item_font = pygame.font.Font("freesansbold.ttf", 50)
    start_text = "Start"
    store_text = "Store"
    quit_text = "Quit"
    
    while running:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not gameStarted:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if startBtn.collidepoint(pygame.mouse.get_pos()):
                        gameStarted = True
                    elif storeBtn.collidepoint(pygame.mouse.get_pos()):
                        running = False
                    elif quitBtn.collidepoint(pygame.mouse.get_pos()):
                        running = False

        if not gameStarted:
            pygame.draw.rect(newGame.screen, (60, 179, 113), (0, 0, newGame.width, newGame.height))
            # Title
            title_font = pygame.font.Font("freesansbold.ttf", 100)
            title = title_font.render("Pug Dash", True, (255, 255, 255))
            newGame.screen.blit(title, (180, 50))

            # Menu Buttons
            item1 = item_font.render(start_text, True, (255, 255, 255))
            newGame.screen.blit(item1, (325, 200))
            item2 = item_font.render(store_text, True, (255, 255, 255))
            newGame.screen.blit(item2, (325, 300))
            item3 = item_font.render(quit_text, True, (255, 255, 255))
            newGame.screen.blit(item3, (325, 400))

            startBtn = pygame.Rect(325, 200, item1.get_width(), item1.get_height())
            storeBtn = pygame.Rect(325, 300, item2.get_width(), item2.get_height())
            quitBtn = pygame.Rect(325, 400, item3.get_width(), item3.get_height())

        else:
            newGame.runGame()
            if newGame.gameOver:
                gameStarted = False
                newGame.resetGame()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
