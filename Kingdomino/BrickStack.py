import json
from pathlib import Path
import random
import pygame
from operator import itemgetter
import config


class BrickStack:

    def __init__(self):
        base_path = Path(__file__).parent
        json_file_path = base_path / "Bricks.json"
        try:
            with open(json_file_path) as f:
                data = json.load(f)
                self.bricks = data["bricks"]
        except FileNotFoundError:
            raise RuntimeError("Bricks.json file not found.")
        except json.JSONDecodeError:
            raise RuntimeError("Error decoding JSON from Bricks.json.")

    def __str__(self):
        string = str(self.bricks["bioms"][0]) + " "
        string += self._crown_to_stars(self.bricks["crowns"][0])
        string += str(self.bricks["bioms"][1])
        string += self._crown_to_stars(self.bricks["crowns"][1])
        return string

    def _crown_to_stars(self, crown):
        if crown == 0:
            return "   "
        if crown == 1:
            return "*  "
        if crown == 2:
            return "** "
        if crown == 3:
            return "***"

    def pull(self):
        if not self.bricks:
            raise RuntimeError("No more bricks in the stack.")
        return self.bricks.pop(0)

    def shuffle(self):
        random.shuffle(self.bricks)

    def get4(self):
        bricks4 = [self.pull() for _ in range(4)]
        bricks4 = sorted(bricks4, key=itemgetter("value"))
        return bricks4

    def draw(self, brick, player, surface, rect):
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

        pygame.draw.rect(surface, config.allColors[brick["bioms"][0]], rect_biome1)
        pygame.draw.rect(surface, color, rect_biome1, 3)
        for _ in range(brick["crowns"][0]):
            pygame.draw.rect(surface, (0, 0, 0), rect_crown1)
            rect_crown1.left += offset

        pygame.draw.rect(surface, config.allColors[brick["bioms"][1]], rect_biome2)
        pygame.draw.rect(surface, color, rect_biome2, 3)
        for _ in range(brick["crowns"][1]):
            pygame.draw.rect(surface, (0, 0, 0), rect_crown2)
            rect_crown2.left += offset

    def take4(self, brick4, surface, pos, brick_size):
        pos_x, pos_y = pos
        for brick in brick4:
            self.draw(brick, 0, surface, (pos_x, pos_y, brick_size, brick_size))
            pos_y = pos_y + brick_size + brick_size / 10

    def draw4_choose(self, player, chosen, brick4, selected, surface, pos, brick_size):
        i = 0
        pos_x = pos[0]
        pos_y = pos[1]
        for brick in brick4:
            if i == selected:
                self.draw(
                    brick, player, surface, (pos_x, pos_y, brick_size, brick_size)
                )
            else:
                self.draw(
                    brick, chosen[i], surface, (pos_x, pos_y, brick_size, brick_size)
                )
            pos_y = pos_y + brick_size + brick_size / 10
            i = i + 1

    def draw_player_bricks(self, player_queue, surface, pos, brick_size):
        pos_x, pos_y = pos
        for player in player_queue:
            self.draw(
                player.chosen_brick,
                player,
                surface,
                (pos_x, pos_y, brick_size, brick_size),
            )
            pos_y = pos_y + brick_size + brick_size / 10
