from Player import Player
from textEditor import getName
from NameSelector import player_name_entry
import pygame

class Actions:
    
    #checks if there is a collision when rotating.
    #This accurse when the brick rotates outside the playing field
    def check_collision_rotation(self,pos,rot):
        if((rot == 0 and pos[0] == 4)or rot == 2 and pos[0] == 0):
            return True
        if((rot == 1 and pos[1] == 0)or rot == 3 and pos[1] == 4):
            return True
        return False
        
    def get_positions(self, pos, rot):
        offsets = {
            0: (0, 1),   # Up
            1: (1, 0),   # Right
            2: (0, -1),  # Down
            3: (-1, 0)   # Left
        }
        # pos1 is the original position
        pos1 = pos[:]
        # pos2 is determined based on rotation offset
        pos2 = [pos[0] + offsets[rot][0], pos[1] + offsets[rot][1]]
        
        return pos1, pos2
    
    def rotate(self,pos,rot):
        if self.check_collision_rotation(pos,rot):
            return rot
        return (rot + 1) % 4
        
    def init_and_check_brick_OK(self,player):
        if not player.board.checkPlacementRollOK(player.placingBrick):
            print("No placec to put \n", player.placingBrick)
            return False
        player.pos = [0,0]
        player.rot = 0
        return True
    
    def choose_brick_position(self, player: Player, keyPress, surface, rect):
        pos1, pos2 = self.get_positions(player.pos, player.rot)
        # Define movement behavior for each key press
        move_actions = {
            'w': lambda: (player.pos[0] > 0 and not (player.rot == 3 and player.pos[0] == 1), -1, 0, player.board.moveDown),
            's': lambda: (player.pos[0] < 4 and not (player.rot == 1 and player.pos[0] == 3), 1, 0, player.board.moveUpp),
            'd': lambda: (player.pos[1] < 4 and not (player.rot == 0 and player.pos[1] == 3), 0, 1, player.board.moveLeft),
            'a': lambda: (player.pos[1] > 0 and not (player.rot == 2 and player.pos[1] == 1), 0, -1, player.board.moveRight)
        }
        # Handle key movements for 'w', 's', 'd', and 'a'
        if keyPress in move_actions:
            can_move, dx, dy, scroll_action = move_actions[keyPress]()
            if can_move:
                player.pos[0] += dx
                player.pos[1] += dy
            else:
                scroll_action()
        # Handle rotation
        if keyPress == 'q':
            player.rot = self.rotate(player.pos, player.rot)
        # Place brick
        if keyPress == 'b':
            pos1, pos2 = self.get_positions(player.pos, player.rot)
            if player.board.put(player.placingBrick, pos1, pos2):
                return True
        # Update and draw player's position on the board
        pos1, pos2 = self.get_positions(player.pos, player.rot)
        player.board.drawPlayerBoard(surface, player, pos1, pos2)
        return False

    
    def place_brick(self,player,keyPress,surface,rect):
        placed = self.choose_brick_position(player,keyPress,surface,rect)
        if placed:
            player.placingBrick = player.chosenBrick
        return placed
    
    def create_Players(self, screen: pygame.Surface, brick_size: int, nr_of_players: int) -> list[Player]:
        # Get screen dimensions directly from the screen surface
        screen_width, screen_height = screen.get_width(), screen.get_height()

        board_positions = [
            (screen_width / 12, screen_height / 12, brick_size * 5, brick_size * 5),
            (screen_width / 12, 6 * (screen_height / 12), brick_size * 5, brick_size * 5),
            (8 * (screen_width / 12), screen_height / 12, brick_size * 5, brick_size * 5),
            (8 * (screen_width / 12), 6 * (screen_height / 12), brick_size * 5, brick_size * 5)
        ]

        if nr_of_players > len(board_positions):
            raise ValueError(f"Maximum supported players is {len(board_positions)}. You provided {nrOfPlayers}.")

        player_names, colors = player_name_entry(screen)
        if nr_of_players > len(player_names) or nr_of_players > len(colors):
            raise ValueError("Not enough names or colors provided for the number of players.")

        # Create players and assign names, colors, and board positions
        players = [
            Player(player_names[i], colors[i], board_positions[i]) 
            for i in range(nr_of_players)
        ]
        
        return players

    def jump_Select(self, selected: int, move_Up: bool, items: list[int]) -> int:
        """
        Move selection to the next empty spot (value 0) in the list.
        Parameters:
        selected (int): The current index of the selected item.
        move_Up (bool): Whether to move up (True) or down (False) in the list.
        items (list[int]): The list being traversed, where 0 indicates an unoccupied spot.

        Returns:
        int: The index of the next empty spot.
        """
        max_index = len(items) - 1
        
        if 0 not in items:
            return selected
        
        while True:
            if move_Up:
                selected = selected - 1 if selected > 0 else max_index
            else:
                selected = selected + 1 if selected < max_index else 0
            if items[selected] == 0:
                break
        return selected
        