"""Main game loop and logic for Kingdomino."""

import sys
import pygame

from . import Actions
from . import EndScreen
from . import config
from .BrickManager import BrickManager
from . import IntroScreen

class Game:
    """Main game class for handling the game loop and player actions."""

    def __init__(self):
        """Initialize the game, setup screen, shuffle pile, and create players."""
        pygame.init()
        self.screen, self.brick_selection_position = self._setup_screen("Kingdomino")
        self.pile = BrickManager()
        self.pile.shuffle()
        self.running = True

    def _setup_screen(self, title="Game"):
        """
        Initialize the game screen.

        Args:
            title (str): The window title.

        Returns:
            tuple: The Pygame display Surface and the brick selection position.
        """
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
        """
        Create players using the Actions module.

        Returns:
            list: Queue of Player objects.
        """
        player_queue = Actions.create_players(
            self.screen, config.BRICK_SIZE
        )
        self.screen.fill(config.BACKGROUND_COLOR)
        return player_queue

    def run_game(self):
        """Run the main game loop including all rounds and final scoring."""
        IntroScreen.show_controls_screen(self.screen)
        self.player_queue = self._create_players_names()
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
        EndScreen.draw_end_screen(self.screen, self.player_queue)
        self.display_points()

    def _first_round(self):
        """Execute the first round by drawing boards and choosing the first 4 bricks."""
        for player in self.player_queue:
            Actions.draw_player_board(self.screen, player)
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
        """
        Pick and display new bricks unless it's the final round.

        Args:
            round_number (int): The current round index.
            max_rounds (int): The maximum number of rounds.
        """
        if round != max_rounds - 1:
            brick4 = self.pile.get4()
            self.pile.draw_take4(
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
        """Loop through players and let them place their bricks."""
        for player in self.player_queue:
            if not Actions.init_and_check_brick(player, self.screen):
                player.next_brick()
                continue
            Actions.place_brick(player, "§", self.screen)
            self.placing_brick(player)

    def placing_brick(self, player):
        """
        Handle the placement loop for an individual player.

        Args:
            player (Player): The current player.
        """
        placed = False
        while not placed:
            placed = self._handle_placing_events(player)
            pygame.display.flip()

    def _handle_placing_events(self, player):
        """
        Handle keyboard and quit events during brick placement.

        Args:
            player (Player): The current player.

        Returns:
            bool: True if the brick was placed, False otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()
                return False
            elif event.type == pygame.KEYDOWN:
                action_map = {
                    config.MOVE_LEFT: "left",
                    config.MOVE_DOWN: "down",
                    config.MOVE_UP: "up",
                    config.MOVE_RIGHT: "right",
                    config.ROTATE: "rotate",
                    config.PLACE: "place",
                }
                if event.key in action_map:
                    ask = Actions.place_brick(
                        player, action_map[event.key], self.screen
                    )
                    if event.key == config.PLACE and ask:
                        return True
        return False

    def display_points(self):
        """Print each player's total points after the game ends."""
        for p in self.player_queue:
            print(p.name + ": " + str(p.board.get_all_points()))