import sys
import pygame
from pathlib import Path

from .Player import Player
from .NameSelector import player_name_entry
from .BrickManager import BrickManager
from . import config

def _check_collision_rotation(pos, rot):
    """Checking if rotating at the given position would hit the board edge."""
    if (rot == 0 and pos[0] == 4) or rot == 2 and pos[0] == 0:
        return True
    if (rot == 1 and pos[1] == 0) or rot == 3 and pos[1] == 4:
        return True
    return False


def _get_positions(pos, rot):
    """Returns the 2 grid positions a domino covers based on its position and rotation."""
    offsets = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}
    pos1 = pos[:]
    pos2 = [pos[0] + offsets[rot][0], pos[1] + offsets[rot][1]]
    return pos1, pos2


def _rotate(pos, rot):
    """Rotate the domino if possible, otherwise keep rotation unchanged."""
    if _check_collision_rotation(pos, rot):
        return rot
    return (rot + 1) % 4


def init_and_check_brick(player: Player, screen: pygame.Surface):
    """Initialize a player's brick placement and show an error if it's invalid."""
    if not player.board.check_placement_roll_OK(player.placing_brick):
        font = pygame.font.Font(None, 50)
        text = font.render("Cannot place brick!", True, player.color)
        text_rect = text.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2)
        )
        screen.blit(text, text_rect)
        pygame.display.flip()
        print("No placec to put \n", player.placing_brick)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    pygame.draw.rect(screen, config.BACKGROUND_COLOR, text_rect)
                    return False
    player.grid_pos = (0, 0)
    player.rot = 0
    return True


def _choose_brick_position(player: Player, key_press, surface):
    """Handle player input for choosing a brick's placement."""
    _handle_movement_rotation(player, key_press)
    return _handle_placement(player, key_press, surface)


def _handle_movement_rotation(player, key_press):
    """Handle movement or rotation input for the current brick."""
    move_actions = {
        "up": lambda: (
            player.tile_pos[0] > 0 and not (player.rot == 3 and player.tile_pos[0] == 1),
            -1,
            0,
            player.board.move_down,
        ),
        "down": lambda: (
            player.tile_pos[0] < 4 and not (player.rot == 1 and player.tile_pos[0] == 3),
            1,
            0,
            player.board.move_up,
        ),
        "right": lambda: (
            player.tile_pos[1] < 4 and not (player.rot == 0 and player.tile_pos[1] == 3),
            0,
            1,
            player.board.move_left,
        ),
        "left": lambda: (
            player.tile_pos[1] > 0 and not (player.rot == 2 and player.tile_pos[1] == 1),
            0,
            -1,
            player.board.move_right,
        ),
    }
    if key_press in move_actions:
        can_move, dx, dy, scroll_action = move_actions[key_press]()
        if can_move:
            player.tile_pos[0] += dx
            player.tile_pos[1] += dy
        else:
            scroll_action()
    if key_press == "rotate":
        player.rot = _rotate(player.tile_pos, player.rot)


def _handle_placement(player, key_press, surface):
    """Attempt to place the brick on the board."""
    if key_press == "place":
        pos1, pos2 = _get_positions(player.tile_pos, player.rot)
        if player.board.put(player.placing_brick, pos1, pos2):
            draw_player_board(surface, player)
            return True
    pos1, pos2 = _get_positions(player.tile_pos, player.rot)
    draw_player_board(surface, player, pos1, pos2)
    return False


def place_brick(player: Player, key_press, surface):
    """High -level entry to handle placement."""
    placed = _choose_brick_position(player, key_press, surface)
    if placed:
        player.placing_brick = player.chosen_brick
    return placed


def create_players(
    screen: pygame.Surface, brick_size: int
) -> list[Player]:
    """Create players and assign names, colors, and board positions."""
    screen_width, screen_height = screen.get_width(), screen.get_height()
    board_positions = [
        (screen_width / 12, screen_height / 12, brick_size * 5, brick_size * 5),
        (screen_width / 12, 6 * (screen_height / 12), brick_size * 5, brick_size * 5),
        (8 * (screen_width / 12), screen_height / 12, brick_size * 5, brick_size * 5),
        (
            8 * (screen_width / 12),
            6 * (screen_height / 12),
            brick_size * 5,
            brick_size * 5,
        ),
    ]
    player_names, colors = player_name_entry(screen)
    nr_of_players = len(player_names)
    if nr_of_players > len(board_positions):
        raise ValueError(
            f"Maximum supported players is {len(board_positions)}. You provided {nr_of_players}."
        )
    if nr_of_players > len(player_names) or nr_of_players > len(colors):
        raise ValueError(
            "Not enough names or colors provided for the number of players."
        )
    players = [
        Player(player_names[i], colors[i], board_positions[i])
        for i in range(nr_of_players)
    ]

    return players


def _jump_select(selected: int, move_up: bool, items: list[int]) -> int:
    """Move selection to the next empty spot (value 0) in the list."""
    max_index = len(items) - 1

    if 0 not in items:
        return selected

    while True:
        if move_up:
            selected = selected - 1 if selected > 0 else max_index
        else:
            selected = selected + 1 if selected < max_index else 0
        if items[selected] == 0:
            break
    return selected


def choose_bricks(player_queue, brick4, pos, surface, pile: BrickManager, brick_size):
    """Allow each player to choose a brick."""
    new_queue = [0, 0, 0, 0]
    for player in player_queue:
        placed = False
        selected = len(new_queue) - 1
        selected = _jump_select(selected, False, new_queue)
        pile.draw4_choose(player, new_queue, brick4, selected, surface, pos, brick_size)
        pygame.display.flip()
        while not placed:
            if all(new_queue):
                return new_queue, True
            placed, selected = _process_events(
                player, new_queue, brick4, selected, surface, pos, pile, brick_size
            )
            pygame.display.flip()
    return [i for i in new_queue if i != 0], True


def _process_events(
    player, new_queue, brick4, selected, surface, pos, pile, brick_size
):
    """Handle input for choosing brick."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == config.MOVE_UP:
                selected = _jump_select(selected, True, new_queue)
                pile.draw4_choose(
                    player, new_queue, brick4, selected, surface, pos, brick_size
                )
            elif event.key == config.MOVE_DOWN:
                selected = _jump_select(selected, False, new_queue)
                pile.draw4_choose(
                    player, new_queue, brick4, selected, surface, pos, brick_size
                )
            elif event.key == config.PLACE and new_queue[selected] == 0:
                new_queue[selected] = player
                player.set_placing_brick(player.chosen_brick)
                player.set_brick(brick4[selected])
                return True, selected
    return False, selected


def draw_image(screen: pygame.Surface, rect: pygame.Rect, image_name):
    """Draw an image on screen."""
    x_size, y_size, x_position, y_position = rect
    base_path = Path(__file__).parent
    json_path = base_path / (image_name + ".png")
    image = pygame.image.load(json_path)
    resized_image = pygame.transform.scale(image, (x_size, y_size))
    image_rect = resized_image.get_rect()
    image_rect.x = x_position
    image_rect.y = y_position
    screen.blit(resized_image, image_rect)

def draw_player_board(
    surface: pygame.Surface, player: Player, pos1=None, pos2=None
):
    """
    Draw the player's board, showing any placing brick.

    Parameters:
        surface (pygame.Surface): The surface to draw on.
        player (Player): The player.
        pos1, pos2: Positions for the brick halves (optional).
    """
    def get_cell_properties(row, column):
        if placing_an_extra_brick and pos1[0] == row and pos1[1] == column:
            cell_biome, cell_crowns = (
                player.placing_brick["bioms"][0],
                player.placing_brick["crowns"][0],
            )
            return config.ALL_COLORS[cell_biome], config.SELECT_COLOR, cell_crowns
        elif placing_an_extra_brick and pos2[0] == row and pos2[1] == column:
            cell_biome, cell_crowns = (
                player.placing_brick["bioms"][1],
                player.placing_brick["crowns"][1],
            )
            return config.ALL_COLORS[cell_biome], config.SELECT_COLOR, cell_crowns
        else:
            cell_biome, cell_crowns = player.board.game_board[row][column]
            return config.ALL_COLORS[cell_biome], (0, 0, 0), cell_crowns

    pos_x, pos_y, rect_width, rect_height = player.board_pos
    cell_width = rect_width / 5
    cell_height = rect_height / 5

    placing_an_extra_brick = pos1 is not None and pos2 is not None
    pygame.draw.rect(
        surface,
        player.color,
        (pos_x - 5, pos_y - 5, rect_width + 10, rect_height + 10),
    )
    for row in range(5):
        for column in range(5):
            cell_x = pos_x + column * cell_width
            cell_y = pos_y + row * cell_height
            cell_rectangle = (cell_x, cell_y, cell_width, cell_height)
            cell_color, border_color, cell_crowns = get_cell_properties(row, column)

            pygame.draw.rect(surface, cell_color, cell_rectangle)
            pygame.draw.rect(surface, border_color, cell_rectangle, 2)
            _draw_crowns(surface, cell_rectangle, cell_crowns)

def _draw_crowns(surface: pygame.Surface, cell_rect, cell_crowns):
    """Draw crowns inside a single cell."""
    cell_x, cell_y, cell_width, cell_height = cell_rect
    crown_rect = pygame.Rect(
        cell_x + cell_width / 10,
        cell_y + cell_height / 10,
        cell_width / 8,
        cell_height / 8,
    )
    offset = cell_width / 7
    for _ in range(cell_crowns):
        pygame.draw.rect(surface, (0, 0, 0), crown_rect)
        crown_rect.left += offset

