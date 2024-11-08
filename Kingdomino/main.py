import pygame
import Actions
from Player import Player
from BrickStack import BrickStack
import config  

def setup_screen(title='Game'):
    desktop_width, desktop_height = pygame.display.get_desktop_sizes()[0]
    screen_size = (desktop_width - config.SCREEN_MARGIN_X, desktop_height - config.SCREEN_MARGIN_Y)
    screen = pygame.display.set_mode(screen_size)
    brickSelectionPosition = (screen_size[0] / 2 - config.CHOOSE_BRICK_OFFSET_X, config.CHOOSE_BRICK_OFFSET_Y)
    pygame.display.set_caption(title)
    return screen, brickSelectionPosition


pygame.init()
screen,brickSelectionPosition = setup_screen("Kingdomino")

# Initialize game components
pile = BrickStack()
pile.shuffle()

# Create players
playerQueue = Actions.create_Players(screen, config.BRICK_SIZE, config.number_of_players)
screen.fill(config.background_color)

for player in playerQueue:
    player.board.draw_player_board(screen, player)
    pygame.display.flip()

# Start the game loop
brick4 = pile.get4()
playerQueue,running = Actions.choosingBricks(playerQueue, brick4, brickSelectionPosition, screen, pile, config.BRICK_SIZE)

while running:
    for i in range(12):
        pile.draw_player_bricks(playerQueue, screen, (brickSelectionPosition[0], brickSelectionPosition[1] + 100 + config.BRICK_SIZE * 4), config.BRICK_SIZE)
        if i != 11:
            brick4 = pile.get4()
            pile.take4(brick4, screen, brickSelectionPosition, config.BRICK_SIZE)
            pygame.display.flip()
            playerQueue,running = Actions.choosingBricks(playerQueue, brick4, brickSelectionPosition, screen, pile, config.BRICK_SIZE)
            if not running:
                break
        for player in playerQueue:
            if not Actions.init_and_check_brick_OK(player):
                player.nextBrick()
                continue
            Actions.place_brick(player, "§", screen, player.boardpos)
            placed = False
            while not placed:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        action_map = {
                            config.move_left: "left", 
                            config.move_down: "down",
                            config.move_up: "up", 
                            config.move_right: "right",
                            config.rotate: "rotate", 
                            config.place: "place"
                        }
                        if event.key in action_map:
                            ask = Actions.place_brick(player, action_map[event.key], screen, player.boardpos)
                            if event.key == pygame.K_b and ask:
                                placed = True
                pygame.display.flip()

    # Display points at the end of each round
    for p in playerQueue:
        print(p.name + ": " + str(p.board.get_all_points()))
    running = False
