from Player import Player
from textEditor import getName
from NameSelector import player_name_entry
import pygame
import config
import BrickStack


def _check_collision_rotation(pos,rot):
    if((rot == 0 and pos[0] == 4)or rot == 2 and pos[0] == 0):
        return True
    if((rot == 1 and pos[1] == 0)or rot == 3 and pos[1] == 4):
        return True
    return False
    
def _get_positions(pos, rot):
    offsets = {
        0: (0, 1),
        1: (1, 0),
        2: (0, -1),
        3: (-1, 0)
    }
    pos1 = pos[:]
    pos2 = [pos[0] + offsets[rot][0], pos[1] + offsets[rot][1]]
    return pos1, pos2

def _rotate(pos,rot):
    if _check_collision_rotation(pos,rot):
        return rot
    return (rot + 1) % 4
    
def init_and_check_brick_OK(player:Player):
    if not player.board.check_placement_roll_OK(player.placingBrick):
        print("No placec to put \n", player.placingBrick)
        return False
    player.pos = [0,0]
    player.rot = 0
    return True

def _choose_brick_position(player: Player, keyPress, surface, rect):
    pos1, pos2 = _get_positions(player.pos, player.rot)
    move_actions = {
        "up": lambda: (player.pos[0] > 0 and not (player.rot == 3 and player.pos[0] == 1), -1, 0, player.board.move_down),
        "down": lambda: (player.pos[0] < 4 and not (player.rot == 1 and player.pos[0] == 3), 1, 0, player.board.move_up),
        "right": lambda: (player.pos[1] < 4 and not (player.rot == 0 and player.pos[1] == 3), 0, 1, player.board.move_left),
        "left": lambda: (player.pos[1] > 0 and not (player.rot == 2 and player.pos[1] == 1), 0, -1, player.board.move_right)
    }
    if keyPress in move_actions:
        can_move, dx, dy, scroll_action = move_actions[keyPress]()
        if can_move:
            player.pos[0] += dx
            player.pos[1] += dy
        else:
            scroll_action()
    if keyPress == "rotate":
        player.rot = _rotate(player.pos, player.rot)
    if keyPress == "place":
        pos1, pos2 = _get_positions(player.pos, player.rot)
        if player.board.put(player.placingBrick, pos1, pos2):
            player.board.draw_player_board(surface, player)
            return True
    pos1, pos2 = _get_positions(player.pos, player.rot)
    player.board.draw_player_board(surface, player, pos1, pos2)
    return False


def place_brick(player:Player,keyPress,surface,rect):
    placed = _choose_brick_position(player,keyPress,surface,rect)
    if placed:
        player.placingBrick = player.chosenBrick
    return placed

def create_Players(screen: pygame.Surface, brick_size: int, nr_of_players: int) -> list[Player]:
    screen_width, screen_height = screen.get_width(), screen.get_height()
    board_positions = [
        (screen_width / 12, screen_height / 12, brick_size * 5, brick_size * 5),
        (screen_width / 12, 6 * (screen_height / 12), brick_size * 5, brick_size * 5),
        (8 * (screen_width / 12), screen_height / 12, brick_size * 5, brick_size * 5),
        (8 * (screen_width / 12), 6 * (screen_height / 12), brick_size * 5, brick_size * 5)
    ]
    if nr_of_players > len(board_positions):
        raise ValueError(f"Maximum supported players is {len(board_positions)}. You provided {nr_of_players}.")
    player_names, colors = player_name_entry(screen)
    if nr_of_players > len(player_names) or nr_of_players > len(colors):
        raise ValueError("Not enough names or colors provided for the number of players.")
    players = [
        Player(player_names[i], colors[i], board_positions[i]) 
        for i in range(nr_of_players)
    ]
    
    return players

def _jump_Select(selected: int, move_up: bool, items: list[int]) -> int:
    """
    Move selection to the next empty spot (value 0) in the list.
    Parameters:
    selected (int): The current index of the selected item.
    move_up (bool): Whether to move up (True) or down (False) in the list.
    items (list[int]): The list being traversed, where 0 indicates an unoccupied spot.

    Returns:
    int: The index of the next empty spot.
    """
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

def choosingBricks(player_queue, brick4, pos, surface, pile:BrickStack, brick_size):
    newQueue = [0, 0, 0, 0]
    for player in player_queue:
        placed = False
        selected = len(newQueue) - 1
        selected = _jump_Select(selected, False, newQueue)
        pile.draw4_choose(player, newQueue, brick4, selected, surface, pos, brick_size)
        pygame.display.flip()
        while not placed:
            if all(newQueue):
                return newQueue, True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return player_queue,False
                if event.type == pygame.KEYDOWN:
                    if event.key == config.move_up:
                        selected = _jump_Select(selected, True, newQueue)
                        pile.draw4_choose(player, newQueue, brick4, selected, surface, pos, brick_size)
                    elif event.key == config.move_down:
                        selected = _jump_Select(selected, False, newQueue)
                        pile.draw4_choose(player, newQueue, brick4, selected, surface, pos, brick_size)
                    elif event.key == config.place and newQueue[selected] == 0:
                        newQueue[selected] = player
                        player.setPlacingBrick(player.chosenBrick)
                        player.setBrick(brick4[selected])
                        placed = True
            pygame.display.flip()
    return [i for i in newQueue if i != 0],True
            