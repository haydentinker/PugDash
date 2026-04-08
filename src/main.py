import pygame
import os
import math
from game import Game, character_data
from spriteSheet import SpriteSheet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

characters = [
    {"name": "Base", "col": 0, "row": 0},
    {"name": "Pug2", "col": 0, "row": 1},
    {"name": "Pug3", "col": 0, "row": 2},
    {"name": "Pug4", "col": 0, "row": 3},
    {"name": "Pug5", "col": 1, "row": 0},
    {"name": "Pug6", "col": 1, "row": 1},
    {"name": "Pug7", "col": 1, "row": 2},
    {"name": "Pug8", "col": 1, "row": 3},
    {"name": "Pug9", "col": 2, "row": 0},
    {"name": "Pug10", "col": 2, "row": 1},
    {"name": "Pug11", "col": 2, "row": 2},
    {"name": "Pug12", "col": 2, "row": 3},
]

def main():
    pygame.init()
    gameStarted = False
    characterSelect = False
    screen_height = 600
    screen_width = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Maple's Adventure")
    running = True
    newGame = Game(screen, screen_width, screen_height)
    
    item_font = pygame.font.SysFont("freesansbold", 50)
    title_font = pygame.font.SysFont("freesansbold", 100)
    start_text = "Start"
    store_text = "Character Select"
    quit_text = "Quit"
    back_text = "Back"
    
    # Load sprite sheet for previews
    sprite_sheet_image = pygame.image.load(os.path.join(BASE_DIR, 'assets', 'pugCharacterSheet.png')).convert_alpha()
    spriteSheet = SpriteSheet(sprite_sheet_image)
    preview_images = [spriteSheet.get_image(char['col'], char['row'], 0, 0, 32, 32, 3, (0, 174, 0)) for char in characters]
    
    # Load background
    bg_image = pygame.image.load(os.path.join(BASE_DIR, 'assets', 'Summer.jpg')).convert()
    bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))
    
    # Selected character preview
    selected_col, selected_row = character_data.get(newGame.selected_character, (0, 0))
    selected_preview = spriteSheet.get_image(selected_col, selected_row, 0, 0, 32, 32, 3, (0, 174, 0))  # Match game scale
    
    while running:
        if not gameStarted and not characterSelect:
            # Define button rects with fixed sizes
            startBtn = pygame.Rect(325, 200, 150, 50)
            storeBtn = pygame.Rect(250, 300, 300, 50)  # Wider for "Character Select"
            quitBtn = pygame.Rect(325, 400, 150, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not gameStarted and not characterSelect and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if startBtn.collidepoint(pos):
                    gameStarted = True
                elif storeBtn.collidepoint(pos):
                    characterSelect = True
                elif quitBtn.collidepoint(pos):
                    running = False
            elif characterSelect and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Handle character selection
                for i, char in enumerate(characters):
                    if char['name'] in newGame.UnlockedCharacters:
                        col = i % 4
                        row = i // 4
                        x = 100 + col * 170
                        y = 150 + row * 120
                        char_btn = pygame.Rect(x, y, 100, 100)
                        if char_btn.collidepoint(pos):
                            newGame.selected_character = char['name']
                            newGame.selected_col, newGame.selected_row = character_data[char['name']]
                            newGame._save_game_info()
                            # Update preview
                            selected_col, selected_row = character_data[char['name']]
                            selected_preview = spriteSheet.get_image(selected_col, selected_row, 0, 0, 32, 32, 3, (0, 174, 0))
                            # Update in-game character
                            newGame.resetGame()
                            characterSelect = False
                            break
                # Back button
                back_btn_event = pygame.Rect(350, 500, 100, 50)
                if back_btn_event.collidepoint(pos):
                    characterSelect = False

        if not gameStarted and not characterSelect:
            # Background
            screen.blit(bg_image, (0, 0))
            
            # Animated title
            title_offset = math.sin(pygame.time.get_ticks() * 0.005) * 10
            title_y = 50 + title_offset
            title = title_font.render("Maple's Adventure", True, (255, 255, 255))
            # Add glow effect
            glow_title = title_font.render("Maple's Adventure", True, (255, 215, 0))
            for dx, dy in [(-2,-2), (2,-2), (-2,2), (2,2)]:
                screen.blit(glow_title, (100 + dx, title_y + dy))
            screen.blit(title, (100, title_y))
            
            # Subtitle
            subtitle_font = pygame.font.SysFont("freesansbold", 30)
            subtitle = subtitle_font.render("An exciting adventure awaits!", True, (0, 0, 0))
            subtitle_bg = pygame.Surface((subtitle.get_width() + 20, subtitle.get_height() + 10))
            subtitle_bg.fill((255, 255, 255))
            subtitle_bg.set_alpha(180)
            subtitle_x = (screen_width - subtitle_bg.get_width()) // 2
            screen.blit(subtitle_bg, (subtitle_x, title_y + 75))
            screen.blit(subtitle, (subtitle_x + 10, title_y + 80))
            
            # Selected character preview
            screen.blit(selected_preview, (50, 470))  # Lower for visual alignment
            
            # Mouse position for hover
            mouse_pos = pygame.mouse.get_pos()
            
            # Start button
            start_color = (0, 255, 0) if startBtn.collidepoint(mouse_pos) else (255, 255, 255)
            pygame.draw.rect(screen, start_color, startBtn, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), startBtn, 2, border_radius=10)
            start_text_color = (255, 255, 255) if startBtn.collidepoint(mouse_pos) else (0, 0, 0)
            item1 = item_font.render(start_text, True, start_text_color)
            screen.blit(item1, (startBtn.x + (startBtn.width - item1.get_width()) // 2, startBtn.y + (startBtn.height - item1.get_height()) // 2))
            
            # Character Select button
            select_color = (0, 255, 255) if storeBtn.collidepoint(mouse_pos) else (255, 255, 255)
            pygame.draw.rect(screen, select_color, storeBtn, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), storeBtn, 2, border_radius=10)
            select_text_color = (255, 255, 255) if storeBtn.collidepoint(mouse_pos) else (0, 0, 0)
            item2 = item_font.render(store_text, True, select_text_color)
            screen.blit(item2, (storeBtn.x + (storeBtn.width - item2.get_width()) // 2, storeBtn.y + (storeBtn.height - item2.get_height()) // 2))
            
            # Quit button
            quit_color = (255, 0, 0) if quitBtn.collidepoint(mouse_pos) else (255, 255, 255)
            pygame.draw.rect(screen, quit_color, quitBtn, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), quitBtn, 2, border_radius=10)
            quit_text_color = (255, 255, 255) if quitBtn.collidepoint(mouse_pos) else (0, 0, 0)
            item3 = item_font.render(quit_text, True, quit_text_color)
            screen.blit(item3, (quitBtn.x + (quitBtn.width - item3.get_width()) // 2, quitBtn.y + (quitBtn.height - item3.get_height()) // 2))
        elif characterSelect:
            # Background
            screen.blit(bg_image, (0, 0))
            
            # Animated title
            title_offset = math.sin(pygame.time.get_ticks() * 0.005) * 10
            title_y = 50 + title_offset
            select_title = title_font.render("Select Character", True, (0, 0, 0))
            # Add glow effect
            glow_title = title_font.render("Select Character", True, (255, 215, 0))
            for dx, dy in [(-2,-2), (2,-2), (-2,2), (2,2)]:
                screen.blit(glow_title, (150 + dx, title_y + dy))
            select_title_bg = pygame.Surface((select_title.get_width() + 20, select_title.get_height() + 10))
            select_title_bg.fill((255, 255, 255))
            select_title_bg.set_alpha(180)
            screen.blit(select_title_bg, (150 - 10, title_y - 5))
            screen.blit(select_title, (150, title_y))

            
            # Mouse position for hover
            mouse_pos = pygame.mouse.get_pos()
            
            for i, char in enumerate(characters):
                if char['name'] in newGame.UnlockedCharacters:
                    col = i % 4
                    row = i // 4
                    x = 100 + col * 170
                    y = 150 + row * 120
                    char_rect = pygame.Rect(x, y, 96, 96)  # Adjusted for preview size
                    
                    # Hover effect
                    is_hovered = char_rect.collidepoint(mouse_pos)
                    is_selected = char['name'] == newGame.selected_character
                    
                    # Frame color based on state
                    if is_selected:
                        frame_color = (255, 215, 0)  # Gold for selected
                        frame_width = 4
                    elif is_hovered:
                        frame_color = (0, 255, 255)  # Cyan for hover
                        frame_width = 3
                    else:
                        frame_color = (255, 255, 255)  # White default
                        frame_width = 2
                    
                    # Draw frame
                    pygame.draw.rect(screen, frame_color, (x - 5, y - 5, 106, 106), frame_width, border_radius=10)
                    
                    # Draw preview
                    screen.blit(preview_images[i], (x, y))
            
            # Back button with styling
            back_btn = pygame.Rect(350, 500, 100, 50)  # Fixed size
            back_render = item_font.render(back_text, True, (0, 0, 0) if not back_btn.collidepoint(mouse_pos) else (255, 255, 255))
            back_color = (255, 255, 255) if not back_btn.collidepoint(mouse_pos) else (255, 0, 0)
            pygame.draw.rect(screen, back_color, back_btn, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), back_btn, 2, border_radius=10)
            screen.blit(back_render, (350 + (back_btn.width - back_render.get_width()) // 2, 500 + (back_btn.height - back_render.get_height()) // 2))
        elif gameStarted:
            newGame.runGame()
            if newGame.gameOver:
                gameStarted = False
                newGame.resetGame()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
