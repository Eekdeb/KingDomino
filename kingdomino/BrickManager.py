import json
from pathlib import Path
import random
import pygame
from operator import itemgetter

from . import config


class BrickManager:
    """
    Manages a stack of bricks loaded from a JSON file.
    Provides functionality to shuffle, draw, and display bricks.
    """

    def __init__(self):
        """Initialize the stack by loading bricks from Bricks.json."""
        base_path = Path(__file__).parent
        json_file_path = base_path / "data" / "Bricks.json"
        try:
            with open(json_file_path) as f:
                data = json.load(f)
                self.bricks = data["bricks"]
        except FileNotFoundError:
            raise RuntimeError("Bricks.json file not found.")
        except json.JSONDecodeError:
            raise RuntimeError("Error decoding JSON from Bricks.json.")

    def __str__(self):
        """Return a string representation of the first brick in the stack."""
        if not self.bricks:
            return "No bricks left"
        string = str(self.bricks["bioms"][0]) + " "
        string += self._crown_to_stars(self.bricks["crowns"][0])
        string += str(self.bricks["bioms"][1])
        string += self._crown_to_stars(self.bricks["crowns"][1])
        return string

    def _crown_to_stars(self, crown):
        """Convert crown count to a string of stars for display."""
        return crown * "*" + " " * (3 - crown)

    def pull(self):
        """Remove and return the top brick from the stack."""
        if not self.bricks:
            raise RuntimeError("No more bricks in the stack.")
        return self.bricks.pop(0)

    def shuffle(self):
        """Shuffle the stack of bricks."""
        random.shuffle(self.bricks)

    def get4(self):
        """Pull 4 bricks from the stack and return them sorted by value."""
        bricks4 = [self.pull() for _ in range(4)]
        bricks4 = sorted(bricks4, key=itemgetter("value"))
        return bricks4

    def draw(self, brick, player, surface, rect):
        """
        Draw a single brick on the given surface.

        Parameters:
            brick (dict): The brick data.
            player: Player object or 0 for no owner.
            surface (pygame.Surface): Surface to draw on.
            rect (tuple): (x, y, width, height) of the brick.
        """
        pos_x, pos_y, width, height = rect
        color = (0, 0, 0) if player == 0 else player.color

        rect_biome1 = pygame.Rect(pos_x, pos_y, width, height)
        rect_biome2 = pygame.Rect(pos_x + width, pos_y, width, height)

        rect_crown1 = pygame.Rect(
            pos_x + width / 10, pos_y + height / 10, width / 8, height / 8
        )
        rect_crown2 = pygame.Rect(
            pos_x + width + width / 10, pos_y + height / 10, width / 8, height / 8
        )
        offset = width / 7

        pygame.draw.rect(surface, config.ALL_COLORS[brick["bioms"][0]], rect_biome1)
        pygame.draw.rect(surface, color, rect_biome1, 3)
        for _ in range(brick["crowns"][0]):
            pygame.draw.rect(surface, (0, 0, 0), rect_crown1)
            rect_crown1.left += offset

        pygame.draw.rect(surface, config.ALL_COLORS[brick["bioms"][1]], rect_biome2)
        pygame.draw.rect(surface, color, rect_biome2, 3)
        for _ in range(brick["crowns"][1]):
            pygame.draw.rect(surface, (0, 0, 0), rect_crown2)
            rect_crown2.left += offset

    def draw_take4(self, brick4, surface, pos, brick_size):
        """
        Draw 4 bricks vertically on the surface.

        Parameters:
            bricks4 (list): List of 4 brick dicts.
            surface (pygame.Surface): Surface to draw on.
            pos (tuple): Starting (x, y) position.
            brick_size (float): Size of each brick.
        """
        pos_x, pos_y = pos
        for brick in brick4:
            self.draw(brick, 0, surface, (pos_x, pos_y, brick_size, brick_size))
            pos_y = pos_y + brick_size + brick_size / 10

    def draw4_choose(self, player, chosen, brick4, selected, surface, pos, brick_size):
        """
        Draw 4 bricks vertically, highlighting the selected one.

        Parameters:
            player: The current player.
            chosen (list): Players who chose each brick.
            bricks4 (list): The 4 brick dicts.
            selected (int): Index of the selected brick.
            surface (pygame.Surface): Surface to draw on.
            pos (tuple): Starting (x, y) position.
            brick_size (float): Size of each brick.
        """
        pos_x, pos_y = pos
        for i, brick in enumerate(brick4):
            owner = player if i == selected else chosen[i]
            self.draw(brick, owner, surface, (pos_x, pos_y, brick_size, brick_size))
            pos_y += brick_size + brick_size / 10

    def draw_player_bricks(self, player_queue, surface, pos, brick_size):
        """
        Draw each player's chosen brick vertically.

        Parameters:
            player_queue (list): List of player objects.
            surface (pygame.Surface): Surface to draw on.
            pos (tuple): Starting (x, y) position.
            brick_size (float): Size of each brick.
        """
        pos_x, pos_y = pos
        for player in player_queue:
            self.draw(
                player.chosen_brick,
                player,
                surface,
                (pos_x, pos_y, brick_size, brick_size),
            )
            pos_y = pos_y + brick_size + brick_size / 10
