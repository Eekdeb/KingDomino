import pygame
import sys
import config

'''
This code is mostly written by AI with some changes to make it compatible to the game and is working
'''

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
PLAYER_COLORS = [config.player1,config.player2,config.player3,config.player4]  # Colors for each player

# Fonts
font = pygame.font.Font(None, 50)  # Smaller font for player names
small_font = pygame.font.Font(None, 40)  # Smaller font for instructions
number_font = pygame.font.Font(None, 50)  # Same size font for numbers
header_font = pygame.font.Font(None, 74)  # Font for header

def player_name_entry(screen):
    WIDTH, HEIGHT = screen.get_size()

    # Player name input boxes
    input_boxes = [
        pygame.Rect(WIDTH // 2 - 200, HEIGHT // 6 * i + 150, 500, 50)
        for i in range(4)
    ]
    player_names = ["", "", "", ""]
    active_box = None

    # Continue button
    button_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 150, 200, 50)

    def draw_screen():
        screen.fill(WHITE)
        
        # Draw header
        header_surface = header_font.render("Players", True, BLACK)
        screen.blit(header_surface, (WIDTH // 2 - header_surface.get_width() // 2, 50))

        # Draw input boxes and player numbers
        for i, box in enumerate(input_boxes):
            color = PLAYER_COLORS[i]
            number_surface = number_font.render(f"{i + 1}", True, BLACK)
            screen.blit(number_surface, (box.x - 50, box.y + 10))
            
            if i == active_box:
                pygame.draw.rect(screen, BLACK, box, 2)  # Highlight active box
            else:
                pygame.draw.rect(screen, GRAY, box, 2)
            
            text_surface = font.render(player_names[i], True, color)
            screen.blit(text_surface, (box.x + 10, box.y + 10))

        # Draw Continue button
        pygame.draw.rect(screen, GRAY, button_box)
        button_text = small_font.render("Continue", True, BLACK)
        screen.blit(button_text, (button_box.x + button_box.width // 2 - button_text.get_width() // 2, button_box.y + button_box.height // 2 - button_text.get_height() // 2))

        pygame.display.flip()

    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_box.collidepoint(event.pos):
                    running = False  # Clicked Continue button
                else:
                    for i, box in enumerate(input_boxes):
                        if box.collidepoint(event.pos):
                            active_box = i
                            break
            elif event.type == pygame.KEYDOWN and active_box is not None:
                if event.key == pygame.K_RETURN:
                    running = False
                elif event.key == pygame.K_TAB:
                    active_box = (active_box + 1) % len(input_boxes)
                elif event.key == pygame.K_BACKSPACE:
                    player_names[active_box] = player_names[active_box][:-1]
                else:
                    if len(player_names[active_box]) < 8:  # Limit to 8 characters
                        player_names[active_box] += event.unicode
        
        draw_screen()
        clock.tick(30)

    print("Player names are:", player_names)
    return player_names,PLAYER_COLORS

if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 600))
    player_names = player_name_entry(screen)
    print(player_names)
