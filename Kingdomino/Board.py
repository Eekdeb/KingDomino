import numpy as np
import copy
import pygame
import config
import Player

class Board:
    def __init__(self):
        self.board = [[(0,0),(0,0),(0,0),(0,0),(0,0)],
            [(0,0),(0,0),(0,0),(0,0),(0,0)],
            [(0,0),(0,0),(1,0),(0,0),(0,0)],
            [(0,0),(0,0),(0,0),(0,0),(0,0)],
            [(0,0),(0,0),(0,0),(0,0),(0,0)]]
        
    def __str__(self):
        string = ""
        for row in self.board:
            string += "\n"
            for column in row:
                string += str(column) + " "
        string += "\n"
        return string
    
    def put(self,brick,pos1,pos2):
        if self._check_collision(pos1, pos2):
            return False
        if not self._check_neighbors_OK(brick, pos1, pos2):
            return False
        self.board[pos1[0]][pos1[1]] = (brick["bioms"][0],brick["crowns"][0])
        self.board[pos2[0]][pos2[1]] = (brick["bioms"][1],brick["crowns"][1])
        return True
        
    def _check_collision(self,pos1,pos2):
        if self.board[pos1[0]][pos1[1]][0] != 0:
            return True
        if self.board[pos2[0]][pos2[1]][0] != 0:
            return True
        return False
    
    def _check_neighbors_OK(self,brick,pos1,pos2):
        return bool(self._check_neighbors_half_OK(brick["bioms"][0],pos1) or 
                    self._check_neighbors_half_OK(brick["bioms"][1],pos2))
            
    def _check_neighbors_half_OK(self,biome,pos):  
        joker = 0 if biome == 0 else 1
        board_size = len(self.board)
        directions = [
            (-1, 0), 
            (1, 0), 
            (0, -1), 
            (0, 1)    
        ]

        for dx, dy in directions:
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if 0 <= new_x < board_size and 0 <= new_y < board_size:
                neighbor_biome = self.board[new_x][new_y][0]
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
        board_size = len(self.board)   
        for x in range(board_size):
            for y in range(board_size):
                pos = [x, y]
                current_cell = self.board[x][y]
                if self._check_neighbors_half_OK(0, pos) and current_cell[0] == 0:
                    if (self._check_neighbors_half_OK(brick["bioms"][0], pos) or
                            self._check_neighbors_half_OK(brick["bioms"][1], pos)):
                        return True
        return False
    
    def check_placement_roll_OK(self,brick):
        temp_board = Board()
        temp_board.board = self.board
        if temp_board._check_placement_OK(brick):
            return True
        moves = [temp_board.move_up, temp_board.move_down, temp_board.move_right, temp_board.move_left]
        for move in moves:
            if move() and temp_board._check_placement_OK(brick):
                return True
        return False
    
    def _get_Points(self, pos, sumTiles=0, sumCrowns=0, visited=None):
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
        board_size_x = len(self.board)
        board_size_y = len(self.board[0]) if board_size_x > 0 else 0
        biome = self.board[pos[0]][pos[1]][0]
        crowns = self.board[pos[0]][pos[1]][1]
        visited.add(tuple(pos))

        sumTiles += 1
        sumCrowns += crowns
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if (0 <= new_x < board_size_x and 0 <= new_y < board_size_y):
                neighbor_pos = (new_x, new_y)
                if neighbor_pos not in visited and self.board[new_x][new_y][0] == biome:
                    sumTiles, sumCrowns = self._get_Points([new_x, new_y], sumTiles, sumCrowns, visited)
        return sumTiles, sumCrowns

    
    def get_all_points(self):
        total = 0
        visited = set()
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                if (row, column) not in visited and self.board[row][column][0] != 0:
                    tiles, crowns = self._get_Points([row, column],0,0, visited)
                    total += tiles * crowns
        return total
    
    def move_down(self):
        for x in self.board[4]:
            if any(x):
                return False
        self.board = np.roll(self.board, 1,axis=0)
        return True
    
    def move_up(self):
        for x in self.board[0]:
            if any(x):
                return False
        self.board = np.roll(self.board, -1,axis=0)
        return True
    
    def move_right(self):
        for x in np.array(self.board)[:,4]:
            if any(x):
                return False
        self.board = np.roll(self.board, 1,axis=1)
        return True
    
    def move_left(self):
        for x in np.array(self.board)[:,0]:
            if any(x):
                return False
        self.board = np.roll(self.board, -1,axis=1)
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
                cell_biome, cell_crowns = self.board[row][column]
                return config.allColors[cell_biome], (0, 0, 0), cell_crowns
        
        posX, posY, rect_width, rect_height = player.boardpos
        cell_width = rect_width / 5
        cell_height = rect_height / 5

        placing_an_extra_brick = (pos1 is not None and pos2 is not None)
        pygame.draw.rect(surface, player.color, (posX - 5, posY - 5, rect_width + 10, rect_height + 10))
        for row in range(5):
            for column in range(5):
                border_color = (0,0,0)
                cellX = posX + column * cell_width
                cellY = posY + row * cell_height
                cellRect = (cellX, cellY, cell_width, cell_height)
                cell_color,border_color,cell_crowns = get_cell_properties(row,column)

                pygame.draw.rect(surface, cell_color, cellRect)
                pygame.draw.rect(surface, border_color, cellRect, 2)
                self._draw_crowns(surface,cellRect,cell_crowns)
                    
    def _draw_crowns(self, surface: pygame.Surface, cell_rect, cell_crowns):
        cellX, cellY, cell_width, cell_height = cell_rect
        crown_rect = pygame.Rect(cellX + cell_width / 10, cellY + cell_height / 10, cell_width / 8, cell_height / 8)
        offset = cell_width / 7
        for _ in range(cell_crowns):
            pygame.draw.rect(surface, (0, 0, 0), crown_rect)
            crown_rect.left += offset
        return


    