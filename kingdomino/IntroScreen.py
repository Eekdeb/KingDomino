import pygame
import sys

from . import config

pygame.init()

# Fonts
TITLE_FONT = pygame.font.Font(None, 80)
TEXT_FONT = pygame.font.Font(None, 50)
SMALL_FONT = pygame.font.Font(None, 40)

def show_controls_screen(screen):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == config.PLACE:
                    running = False

        screen.fill(config.BACKGROUND_COLOR)

        # Title
        title_surface = TITLE_FONT.render("Controls", True, (0, 0, 0))
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 50))

        # Controls
        controls = [
            ("Move Up", pygame.key.name(config.MOVE_UP).upper()),
            ("Move Down", pygame.key.name(config.MOVE_DOWN).upper()),
            ("Move Left", pygame.key.name(config.MOVE_LEFT).upper()),
            ("Move Right", pygame.key.name(config.MOVE_RIGHT).upper()),
            ("Rotate", pygame.key.name(config.ROTATE).upper()),
            ("Place/Select", pygame.key.name(config.PLACE).upper()),
        ]

        for i, (action, key) in enumerate(controls):
            action_surface = TEXT_FONT.render(f"{action}:", True, (0, 0, 0))
            key_surface = TEXT_FONT.render(key, True, (0, 0, 0))
            y = 150 + i * 70
            screen.blit(action_surface, (WIDTH // 2 - 200, y))
            screen.blit(key_surface, (WIDTH // 2 + 100, y))

        # Instruction to continue
        continue_surface = SMALL_FONT.render(f"Press '{pygame.key.name(config.PLACE).upper()}' to continue", True, (0, 0, 0))
        screen.blit(continue_surface, (WIDTH // 2 - continue_surface.get_width() // 2, HEIGHT - 100))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 600))
    show_controls_screen(screen)
    print("Controls screen done. Continue with the game...")
