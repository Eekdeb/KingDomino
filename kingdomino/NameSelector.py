import pygame
import sys

from . import config

"""
This code is mostly written by AI with some changes to make it compatible to the game and is working
"""

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
PLAYER_COLORS = [
    config.PLAYER1_COLOR,
    config.PLAYER2_COLOR,
    config.PLAYER3_COLOR,
    config.PLAYER4_COLOR,
]

player_name_font = pygame.font.Font(None, 50)  # Smaller font for player names
instructions_font = pygame.font.Font(None, 40)  # Smaller font for instructions
number_font = pygame.font.Font(None, 50)  # Same size font for numbers
header_font = pygame.font.Font(None, 74)  # Font for header

def player_name_entry(screen):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    # --- Step 1: Select number of players ---

    # Define buttons for choosing number of players (1 to 4)
    button_width, button_height = 100, 60
    gap = 20
    total_width = 4 * button_width + 3 * gap
    start_x = WIDTH // 2 - total_width // 2
    buttons = [
        pygame.Rect(start_x + i * (button_width + gap), HEIGHT // 3, button_width, button_height)
        for i in range(4)
    ]

    instructions_font = pygame.font.Font(None, 40)
    selected_num_players = None
    active_button = 0  # Index of the currently highlighted button

    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, btn in enumerate(buttons):
                    if btn.collidepoint(event.pos):
                        selected_num_players = i + 1
                        selecting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB or event.key == config.MOVE_RIGHT:
                    active_button = (active_button + 1) % len(buttons)
                elif event.key == config.MOVE_LEFT:
                    active_button = (active_button - 1) % len(buttons)
                elif event.key == pygame.K_RETURN or event.key == config.PLACE:
                    selected_num_players = active_button + 1
                    return pick_names(screen,selected_num_players)

        screen.fill(config.BACKGROUND_COLOR)

        # Draw instruction text
        instruction_surface = instructions_font.render("Select number of players", True, BLACK)
        screen.blit(instruction_surface, (WIDTH // 2 - instruction_surface.get_width() // 2, HEIGHT // 5))

        # Draw buttons
        for i, btn in enumerate(buttons):
            if i == active_button:
                pygame.draw.rect(screen, (255, 215, 0), btn)  # Highlight with gold color
            else:
                pygame.draw.rect(screen, GRAY, btn)
            number_surface = instructions_font.render(str(i + 1), True, BLACK)
            screen.blit(number_surface, (btn.x + btn.width // 2 - number_surface.get_width() // 2,
                                         btn.y + btn.height // 2 - number_surface.get_height() // 2))

        pygame.display.flip()
        clock.tick(30)

    # --- The rest of your player name input screen goes here ---
    # (Leave your previous name input code unchanged!)
    # Just continue with:
    print(f"Number of players selected: {selected_num_players}")

    # You can return the number here or keep going to player name input:
    return selected_num_players


def pick_names(screen, number_of_players):
    WIDTH, HEIGHT = screen.get_size()

    # Player name input boxes
    input_boxes = [
        pygame.Rect(WIDTH // 2 - 200, HEIGHT // 6 * i + 150, 500, 50)
        for i in range(number_of_players)
    ]
    player_names = [""] * number_of_players
    active_box = 0

    # Continue button
    button_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 150, 200, 50)

    def draw_screen():
        screen.fill(config.BACKGROUND_COLOR)
        
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
            
            text_surface = player_name_font.render(player_names[i], True, color)
            screen.blit(text_surface, (box.x + 10, box.y + 10))

        # Draw Continue button
        pygame.draw.rect(screen, GRAY, button_box)
        button_text = instructions_font.render("Continue", True, BLACK)
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
                    running = False
                else:
                    for i, box in enumerate(input_boxes):
                        if box.collidepoint(event.pos):
                            active_box = i
                            break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    if active_box == None:
                        active_box = 0
                    else:
                        active_box = (active_box + 1) % len(input_boxes)
                elif event.key == pygame.K_RETURN:
                    running = False
                elif event.key == pygame.K_BACKSPACE and active_box is not None:
                    player_names[active_box] = player_names[active_box][:-1]
                elif active_box is not None:
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
