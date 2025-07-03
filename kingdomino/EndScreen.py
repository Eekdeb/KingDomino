import pygame
import sys

from .Player import Player
from . import config

FONT_SIZE = 100
SPACER = 110
Y_OFFSET = 1 / 4
NAME_X_FRACTION = 1 / 3
SCORE_X_FRACTION = 2 / 3


def draw_end_screen(screen: pygame.Surface, players: list[Player]):
    """Draw the end screen with players sorted by score, and wait for input."""
    screen.fill(config.BACKGROUND_COLOR)

    players_and_scores = [(player, player.board.get_all_points()) for player in players]
    players_and_scores.sort(key=lambda x: x[1], reverse=True)

    font = pygame.font.Font(None, FONT_SIZE)
    for i, (player, score) in enumerate(players_and_scores):

        name_font = font.render(f"{player.name}:", True, player.color)
        name_rect = name_font.get_rect(
            center=(
                screen.get_width()*NAME_X_FRACTION,
                screen.get_height() * Y_OFFSET + SPACER * i,
            )
        )
        screen.blit(name_font, name_rect)

        score_font = font.render(str(score), True, player.color)
        score_rect = score_font.get_rect(
            center=(
                (screen.get_width()*SCORE_X_FRACTION),
                screen.get_height() * Y_OFFSET + SPACER * i,
            )
        )
        screen.blit(score_font, score_rect)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
