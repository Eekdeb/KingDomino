import pygame
import Actions
from Player import Player
from BrickStack import BrickStack
import config
import end_screen
import sys

class game:
    def __init__(self):
        pygame.init()
        self.screen,self.brickSelectionPosition = self._setup_screen("Kingdomino")
        self.pile = BrickStack()
        self.pile.shuffle() 
        self.running = True
        self.playerQueue = self._create_players_names()
    
    def _setup_screen(self,title='Game'):
        desktop_width, desktop_height = pygame.display.get_desktop_sizes()[0]
        screen_size = (desktop_width - config.SCREEN_MARGIN_X, desktop_height - config.SCREEN_MARGIN_Y)
        screen = pygame.display.set_mode(screen_size)
        brickSelectionPosition = (screen_size[0] / 2 - config.CHOOSE_BRICK_OFFSET_X, config.CHOOSE_BRICK_OFFSET_Y)
        pygame.display.set_caption(title)
        return screen, brickSelectionPosition

    def _create_players_names(self):
        playerQueue = Actions.create_Players(self.screen, config.BRICK_SIZE, config.number_of_players)
        self.screen.fill(config.background_color)
        return playerQueue
    
    def run_game(self):
        self._first_round()
        nr_of_rounds = 12
        for round in range(nr_of_rounds):
            self.pile.draw_player_bricks(self.playerQueue, self.screen, (self.brickSelectionPosition[0], self.brickSelectionPosition[1] + 100 + config.BRICK_SIZE * 4), config.BRICK_SIZE)
            self.pick_new_bricks(round,nr_of_rounds)
            if not self.running:
                break
            self.placing_bricks() 
        end_screen.draw_end_screen(self.screen,self.playerQueue) 
        self.display_points()

    def _first_round(self):
        for player in self.playerQueue:
            player.board.draw_player_board(self.screen, player)
            pygame.display.flip()
        brick4 = self.pile.get4()
        self.playerQueue,self.running = Actions.choosingBricks(self.playerQueue, brick4, self.brickSelectionPosition, self.screen, self.pile, config.BRICK_SIZE)

    def pick_new_bricks(self,round,max_rounds):
        if round != max_rounds-1:
            brick4 = self.pile.get4()
            self.pile.take4(brick4, self.screen, self.brickSelectionPosition, config.BRICK_SIZE)
            pygame.display.flip()
            self.playerQueue,self.running = Actions.choosingBricks(self.playerQueue, brick4, self.brickSelectionPosition, self.screen, self.pile, config.BRICK_SIZE)
    
    def placing_bricks(self):
        for player in self.playerQueue:
            if not Actions.init_and_check_brick_OK(player,self.screen):
                player.nextBrick()
                continue
            Actions.place_brick(player, "§", self.screen, player.boardpos)
            self.placing_brick(player)
    
    def placing_brick(self,player):
        placed = False
        while not placed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                    return
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
                        ask = Actions.place_brick(player, action_map[event.key], self.screen, player.boardpos)
                        if event.key == pygame.K_b and ask:
                            placed = True
            pygame.display.flip()

    def display_points(self):
        # Display points at the end of each round
        for p in self.playerQueue:
            print(p.name + ": " + str(p.board.get_all_points()))

thegame = game()
thegame.run_game()