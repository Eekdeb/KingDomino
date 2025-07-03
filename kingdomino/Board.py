import numpy as np

class Board:
    """
    Represents a player's game board.

    The board is a 5x5 grid where each cell is a tuple: (biome, crowns).
    """

    def __init__(self):
        """ Initialize the board with a central starting tile. """
        self.game_board: list[list[tuple[int, int]]] = [
            [(0, 0) for _ in range(5)] for _ in range(5)
        ]
        self.game_board[2][2] = (1, 0)  # Starting tile in the center

    def __str__(self):
        """Return a string representation of the board."""
        string = ""
        for row in self.game_board:
            string += "\n"
            for column in row:
                string += str(column) + " "
        string += "\n"
        return string

    def put(self, brick, pos1, pos2) -> bool:
        """
        Attempt to place a brick on the board.

        Parameters:
            brick (dict): The brick to place.
            pos1 (tuple): First tile position.
            pos2 (tuple): Second tile position.

        Returns:
            bool: True if placement was successful.
        """
        if self._check_collision(pos1, pos2):
            return False
        if not self._validate_neighbors(brick, pos1, pos2):
            return False
        self.game_board[pos1[0]][pos1[1]] = (brick["bioms"][0], brick["crowns"][0])
        self.game_board[pos2[0]][pos2[1]] = (brick["bioms"][1], brick["crowns"][1])
        return True

    def _check_collision(self, pos1, pos2) -> bool:
        """Check if the positions are already occupied."""
        if self.game_board[pos1[0]][pos1[1]][0] != 0:
            return True
        if self.game_board[pos2[0]][pos2[1]][0] != 0:
            return True
        return False

    def _validate_neighbors(self, brick, pos1, pos2) -> bool:
        """Check if at least one half has valid neighbors."""
        return bool(
            self._check_neighbors_half_OK(brick["bioms"][0], pos1)
            or self._check_neighbors_half_OK(brick["bioms"][1], pos2)
        )

    def _check_neighbors_half_OK(self, biome, pos) -> bool:
        """Check if one tile half matches neighbors or the joker."""
        joker = 0 if biome == 0 else 1
        board_size = len(self.game_board)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in directions:
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if 0 <= new_x < board_size and 0 <= new_y < board_size:
                neighbor_biome = self.game_board[new_x][new_y][0]
                if neighbor_biome == biome or neighbor_biome == joker:
                    return True
        return False

    def _check_placement_OK(self, brick) -> bool:
        """
        Check if there is any valid placement for the given brick.

        Returns:
            bool: True if a valid placement exists.
        """
        board_size = len(self.game_board)
        for x in range(board_size):
            for y in range(board_size):
                pos = [x, y]
                current_cell = self.game_board[x][y]
                if self._check_neighbors_half_OK(0, pos) and current_cell[0] == 0:
                    if self._check_neighbors_half_OK(
                        brick["bioms"][0], pos
                    ) or self._check_neighbors_half_OK(brick["bioms"][1], pos):
                        return True
        return False

    def check_placement_roll_OK(self, brick) -> bool:
        """Check if there is any valid placement for the given brick."""
        temp_board = Board()
        temp_board.game_board = self.game_board
        if temp_board._check_placement_OK(brick):
            return True
        moves = [
            temp_board.move_up,
            temp_board.move_down,
            temp_board.move_right,
            temp_board.move_left,
        ]
        for move in moves:
            if move() and temp_board._check_placement_OK(brick):
                return True
        return False
    
    def get_all_points(self) -> int:
        """Calculate the total score for the board."""
        total = 0
        visited = set()
        for row in range(len(self.game_board)):
            for column in range(len(self.game_board[0])):
                if (row, column) not in visited and self.game_board[row][column][
                    0
                ] != 0:
                    tiles, crowns = self._get_points([row, column], 0, 0, visited)
                    total += tiles * crowns
        return total

    def _get_points(self, pos, sum_tiles=0, sum_crowns=0, visited=None) -> tuple[int, int]:
        """Recursively calculate connected tiles and crowns."""
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
            if 0 <= new_x < board_size_x and 0 <= new_y < board_size_y:
                neighbor_pos = (new_x, new_y)
                if (
                    neighbor_pos not in visited
                    and self.game_board[new_x][new_y][0] == biome
                ):
                    sum_tiles, sum_crowns = self._get_points(
                        [new_x, new_y], sum_tiles, sum_crowns, visited
                    )
        return sum_tiles, sum_crowns

    def move_down(self) -> bool:
        """Shift the board down if possible."""
        for x in self.game_board[4]:
            if any(x):
                return False
        self.game_board = np.roll(self.game_board, 1, axis=0)
        return True

    def move_up(self) -> bool:
        """Shift the board up if possible."""
        for x in self.game_board[0]:
            if any(x):
                return False
        self.game_board = np.roll(self.game_board, -1, axis=0)
        return True

    def move_right(self) -> bool:
        """Shift the board right if possible."""
        for x in np.array(self.game_board)[:, 4]:
            if any(x):
                return False
        self.game_board = np.roll(self.game_board, 1, axis=1)
        return True

    def move_left(self) -> bool:
        """Shift the board left if possible."""
        for x in np.array(self.game_board)[:, 0]:
            if any(x):
                return False
        self.game_board = np.roll(self.game_board, -1, axis=1)
        return True