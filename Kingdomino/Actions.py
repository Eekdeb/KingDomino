import sys
from Player import Player
from textEditor import getName
from NameSelector import player_name_entry
import pygame
import config
import BrickStack
from pathlib import Path

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
    
def init_and_check_brick(player:Player,screen:pygame.Surface):
    if not player.board.check_placement_roll_OK(player.placingBrick):
        font = pygame.font.Font(None, 50)
        text = font.render("Can not place brick!", True, player.color)
        text_rect = text.get_rect(center=(screen.get_width()/2,screen.get_height()/2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        print("No placec to put \n", player.placingBrick)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()             
                if event.type == pygame.KEYDOWN:
                    pygame.draw.rect(screen,config.background_color,text_rect)
                    return False
    player.pos = [0,0]
    player.rot = 0
    return True

def _choose_brick_position(player: Player, key_press, surface):
    _handle_movement_rotation(player, key_press)
    return _handle_placement(player, key_press, surface)


def _handle_movement_rotation(player, key_press):
    move_actions = {
        "up": lambda: (player.pos[0] > 0 and not (player.rot == 3 and player.pos[0] == 1), -1, 0, player.board.move_down),
        "down": lambda: (player.pos[0] < 4 and not (player.rot == 1 and player.pos[0] == 3), 1, 0, player.board.move_up),
        "right": lambda: (player.pos[1] < 4 and not (player.rot == 0 and player.pos[1] == 3), 0, 1, player.board.move_left),
        "left": lambda: (player.pos[1] > 0 and not (player.rot == 2 and player.pos[1] == 1), 0, -1, player.board.move_right)
    }
    if key_press in move_actions:
        can_move, dx, dy, scroll_action = move_actions[key_press]()
        if can_move:
            player.pos[0] += dx
            player.pos[1] += dy
        else:
            scroll_action()
    if key_press == "rotate":
        player.rot = _rotate(player.pos, player.rot)

def _handle_placement(player, key_press, surface):
    if key_press == "place":
        pos1, pos2 = _get_positions(player.pos, player.rot)
        if player.board.put(player.placingBrick, pos1, pos2):
            player.board.draw_player_board(surface, player)
            return True
    pos1, pos2 = _get_positions(player.pos, player.rot)
    player.board.draw_player_board(surface, player, pos1, pos2)
    return False


def place_brick(player:Player,key_press,surface):
    placed = _choose_brick_position(player,key_press,surface)
    if placed:
        player.placingBrick = player.chosenBrick
    return placed

def create_players(screen: pygame.Surface, brick_size: int, nr_of_players: int) -> list[Player]:
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

def _jump_select(selected: int, move_up: bool, items: list[int]) -> int:
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

def choose_bricks(player_queue, brick4, pos, surface, pile: BrickStack, brick_size):
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
            placed, selected = _process_events(player, new_queue, brick4, selected, surface, pos, pile, brick_size)
            pygame.display.flip()
    return [i for i in new_queue if i != 0], True

def _process_events(player, new_queue, brick4, selected, surface, pos, pile, brick_size):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == config.move_up:
                selected = _jump_select(selected, True, new_queue)
                pile.draw4_choose(player, new_queue, brick4, selected, surface, pos, brick_size)
            elif event.key == config.move_down:
                selected = _jump_select(selected, False, new_queue)
                pile.draw4_choose(player, new_queue, brick4, selected, surface, pos, brick_size)
            elif event.key == config.place and new_queue[selected] == 0:
                new_queue[selected] = player
                player.setPlacingBrick(player.chosenBrick)
                player.setBrick(brick4[selected])
                return True, selected
    return False, selected



def draw_image(screen:pygame.Surface,rect:pygame.Rect,image_name):
    x_size,y_size,x_position,y_position = rect
    base_path = Path(__file__).parent
    json_file_path = base_path / (image_name+".png")
    image = pygame.image.load(json_file_path)
    resized_image = pygame.transform.scale(image, (x_size,y_size))
    image_rect = resized_image.get_rect()
    image_rect.x = x_position
    image_rect.y = y_position
    screen.blit(resized_image, image_rect)
            