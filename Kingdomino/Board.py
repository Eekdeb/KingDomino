import numpy as np
import copy
import pygame
import config
import Player

class Board:
    def __init__(self):
        self.game_board = [[(0,0),(0,0),(0,0),(0,0),(0,0)],
            [(0,0),(0,0),(0,0),(0,0),(0,0)],
            [(0,0),(0,0),(1,0),(0,0),(0,0)],
            [(0,0),(0,0),(0,0),(0,0),(0,0)],
            [(0,0),(0,0),(0,0),(0,0),(0,0)]]
        
    def __str__(self):
        string = ""
        for row in self.game_board:
            string += "\n"
            for column in row:
                string += str(column) + " "
        string += "\n"
        return string
    
    def put(self,brick,pos1,pos2):
        if self._check_collision(pos1, pos2):
            return False
        if not self._validate_neighbors(brick, pos1, pos2):
            return False
        self.game_board[pos1[0]][pos1[1]] = (brick["bioms"][0],brick["crowns"][0])
        self.game_board[pos2[0]][pos2[1]] = (brick["bioms"][1],brick["crowns"][1])
        return True
        
    def _check_collision(self,pos1,pos2):
        if self.game_board[pos1[0]][pos1[1]][0] != 0:
            return True
        if self.game_board[pos2[0]][pos2[1]][0] != 0:
            return True
        return False
    
    def _validate_neighbors(self,brick,pos1,pos2):
        return bool(self._check_neighbors_half_OK(brick["bioms"][0],pos1) or 
                    self._check_neighbors_half_OK(brick["bioms"][1],pos2))
            
    def _check_neighbors_half_OK(self,biome,pos):  
        joker = 0 if biome == 0 else 1
        board_size = len(self.game_board)
        directions = [
            (-1, 0), 
            (1, 0), 
            (0, -1), 
            (0, 1)    
        ]

        for dx, dy in directions:
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if 0 <= new_x < board_size and 0 <= new_y < board_size:
                neighbor_biome = self.game_board[new_x][new_y][0]
                if neighbor_biome == biome or neighbor_biome == joker:
                    return True
        return False

    def _check_placement_OK(self, brick):
        """
        Check if there is a valid placement for the given brick on the board.

        Parameters:
        brick (dict): A dictionary with keys 'bioms' (a list of two biomes).

        Returns:
        bool: True if a valid placement exists, False otherwise.
        """
        board_size = len(self.game_board)   
        for x in range(board_size):
            for y in range(board_size):
                pos = [x, y]
                current_cell = self.game_board[x][y]
                if self._check_neighbors_half_OK(0, pos) and current_cell[0] == 0:
                    if (self._check_neighbors_half_OK(brick["bioms"][0], pos) or
                            self._check_neighbors_half_OK(brick["bioms"][1], pos)):
                        return True
        return False
    
    def check_placement_roll_OK(self,brick):
        temp_board = Board()
        temp_board.game_board = self.game_board
        if temp_board._check_placement_OK(brick):
            return True
        moves = [temp_board.move_up, temp_board.move_down, temp_board.move_right, temp_board.move_left]
        for move in moves:
            if move() and temp_board._check_placement_OK(brick):
                return True
        return False
    
    def _get_Points(self, pos, sum_tiles=0, sum_crowns=0, visited=None):
        """
        Recursively calculates the total number of connected tiles of the same biome
        and the total crowns within those tiles, starting from a given position.

        Parameters:
        pos (list): The starting position [x, y] on the board.
        sumTiles (int): Accumulated count of tiles (default is 0).
        sumCrowns (int): Accumulated count of crowns (default is 0).
        visited (set): Set of visited positions to prevent revisiting tiles (default is None).

        Returns:
        tuple: (total_tiles, total_crowns) for connected tiles of the same biome.
        """
        if visited is None:
            visited = set()
        board_size_x = len(self.game_board)
        board_size_y = len(self.game_board[0]) if board_size_x > 0 else 0
        biome = self.game_board[pos[0]][pos[1]][0]
        crowns = self.game_board[pos[0]][pos[1]][1]
        visited.add(tuple(pos))

        sum_tiles += 1
        sum_crowns += crowns
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if (0 <= new_x < board_size_x and 0 <= new_y < board_size_y):
                neighbor_pos = (new_x, new_y)
                if neighbor_pos not in visited and self.game_board[new_x][new_y][0] == biome:
                    sum_tiles, sum_crowns = self._get_Points([new_x, new_y], sum_tiles, sum_crowns, visited)
        return sum_tiles, sum_crowns

    
    def get_all_points(self):
        total = 0
        visited = set()
        for row in range(len(self.game_board)):
            for column in range(len(self.game_board[0])):
                if (row, column) not in visited and self.game_board[row][column][0] != 0:
                    tiles, crowns = self._get_Points([row, column],0,0, visited)
                    total += tiles * crowns
        return total
    
    def move_down(self):
        for x in self.game_board[4]:
            if any(x):
                return False
        self.game_board = np.roll(self.game_board, 1,axis=0)
        return True
    
    def move_up(self):
        for x in self.game_board[0]:
            if any(x):
                return False
        self.game_board = np.roll(self.game_board, -1,axis=0)
        return True
    
    def move_right(self):
        for x in np.array(self.game_board)[:,4]:
            if any(x):
                return False
        self.game_board = np.roll(self.game_board, 1,axis=1)
        return True
    
    def move_left(self):
        for x in np.array(self.game_board)[:,0]:
            if any(x):
                return False
        self.game_board = np.roll(self.game_board, -1,axis=1)
        return True
    
    def draw_player_board(self, surface: pygame.Surface, player:Player, pos1 = None, pos2 = None):
        def get_cell_properties(row, column):
            if placing_an_extra_brick and pos1[0] == row and pos1[1] == column:
                cell_biome, cell_crowns = player.placingBrick["bioms"][0], player.placingBrick["crowns"][0]
                return config.allColors[cell_biome], config.select_color, cell_crowns
            elif placing_an_extra_brick and pos2[0] == row and pos2[1] == column:
                cell_biome, cell_crowns = player.placingBrick["bioms"][1], player.placingBrick["crowns"][1]
                return config.allColors[cell_biome], config.select_color, cell_crowns
            else:
                cell_biome, cell_crowns = self.game_board[row][column]
                return config.allColors[cell_biome], (0, 0, 0), cell_crowns
        
        pos_x, pos_y, rect_width, rect_height = player.boardpos
        cell_width = rect_width / 5
        cell_height = rect_height / 5

        placing_an_extra_brick = (pos1 is not None and pos2 is not None)
        pygame.draw.rect(surface, player.color, (pos_x - 5, pos_y - 5, rect_width + 10, rect_height + 10))
        for row in range(5):
            for column in range(5):
                cell_x = pos_x + column * cell_width
                cell_y = pos_y + row * cell_height
                cell_rectangle = (cell_x, cell_y, cell_width, cell_height)
                cell_color,border_color,cell_crowns = get_cell_properties(row,column)

                pygame.draw.rect(surface, cell_color, cell_rectangle)
                pygame.draw.rect(surface, border_color, cell_rectangle, 2)
                self._draw_crowns(surface,cell_rectangle,cell_crowns)
                    
    def _draw_crowns(self, surface: pygame.Surface, cell_rect, cell_crowns):
        cell_x, cell_y, cell_width, cell_height = cell_rect
        crown_rect = pygame.Rect(cell_x + cell_width / 10, cell_y + cell_height / 10, cell_width / 8, cell_height / 8)
        offset = cell_width / 7
        for _ in range(cell_crowns):
            pygame.draw.rect(surface, (0, 0, 0), crown_rect)
            crown_rect.left += offset

    