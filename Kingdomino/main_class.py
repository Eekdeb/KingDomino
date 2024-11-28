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
        self.screen, self.brick_selection_position = self._setup_screen("Kingdomino")
        self.pile = BrickStack()
        self.pile.shuffle()
        self.running = True
        self.player_queue = self._create_players_names()

    def _setup_screen(self, title="Game"):
        desktop_width, desktop_height = pygame.display.get_desktop_sizes()[0]
        screen_size = (
            desktop_width - config.SCREEN_MARGIN_X,
            desktop_height - config.SCREEN_MARGIN_Y,
        )
        screen = pygame.display.set_mode(screen_size)
        brick_selection_position = (
            screen_size[0] / 2 - config.CHOOSE_BRICK_OFFSET_X,
            config.CHOOSE_BRICK_OFFSET_Y,
        )
        pygame.display.set_caption(title)
        return screen, brick_selection_position

    def _create_players_names(self):
        player_queue = Actions.create_players(
            self.screen, config.BRICK_SIZE, config.number_of_players
        )
        self.screen.fill(config.background_color)
        return player_queue

    def run_game(self):
        self._first_round()
        nr_of_rounds = 12
        for round in range(nr_of_rounds):
            self.pile.draw_player_bricks(
                self.player_queue,
                self.screen,
                (
                    self.brick_selection_position[0],
                    self.brick_selection_position[1] + 100 + config.BRICK_SIZE * 4,
                ),
                config.BRICK_SIZE,
            )
            self.pick_new_bricks(round, nr_of_rounds)
            if not self.running:
                break
            self.placing_bricks()
        end_screen.draw_end_screen(self.screen, self.player_queue)
        self.display_points()

    def _first_round(self):
        for player in self.player_queue:
            player.board.draw_player_board(self.screen, player)
            pygame.display.flip()
        brick4 = self.pile.get4()
        self.player_queue, self.running = Actions.choose_bricks(
            self.player_queue,
            brick4,
            self.brick_selection_position,
            self.screen,
            self.pile,
            config.BRICK_SIZE,
        )

    def pick_new_bricks(self, round, max_rounds):
        if round != max_rounds - 1:
            brick4 = self.pile.get4()
            self.pile.take4(
                brick4, self.screen, self.brick_selection_position, config.BRICK_SIZE
            )
            pygame.display.flip()
            self.player_queue, self.running = Actions.choose_bricks(
                self.player_queue,
                brick4,
                self.brick_selection_position,
                self.screen,
                self.pile,
                config.BRICK_SIZE,
            )

    def placing_bricks(self):
        for player in self.player_queue:
            if not Actions.init_and_check_brick(player, self.screen):
                player.nextBrick()
                continue
            Actions.place_brick(player, "§", self.screen)
            self.placing_brick(player)

    def placing_brick(self, player):
        placed = False
        while not placed:
            placed = self._handle_placing_events(player)
            pygame.display.flip()

    def _handle_placing_events(self, player):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()
                return False
            elif event.type == pygame.KEYDOWN:
                action_map = {
                    config.move_left: "left",
                    config.move_down: "down",
                    config.move_up: "up",
                    config.move_right: "right",
                    config.rotate: "rotate",
                    config.place: "place",
                }
                if event.key in action_map:
                    ask = Actions.place_brick(
                        player, action_map[event.key], self.screen
                    )
                    if event.key == pygame.K_b and ask:
                        return True
        return False

    def display_points(self):
        # Display points at the end of each round
        for p in self.player_queue:
            print(p.name + ": " + str(p.board.get_all_points()))


thegame = game()
thegame.run_game()
