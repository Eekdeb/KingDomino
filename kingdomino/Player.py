from .Board import Board


class Player:
    """
    Represents a player in the game.

    Attributes:
        name (str): The player's name.
        color (str): The player's color.
        board (Board): The game board the player interacts with.
        placing_brick: The brick the player is currently placing.
        chosen_brick: The brick the player has chosen to place next.
        tile_pos (tuple[int, int]): The (x, y) position on the board grid.
        rotation_steps (int): The rotation of the brick in 90-degree steps.
        board_pos: The possition of the players board in the game.
    """

    def __init__(self, name, color, board_pos):
        """
        Initialize a new player.

        Args:
            name (str): The player's name.
            color (str): The player's color.
            board_pos: The player's position on the board.
        """
        self.board: Board = Board()
        self.placing_brick = 0
        self.chosen_brick = 0
        self.name = name
        self.tile_pos = [0, 0] 
        self.rot = 0  # 0=0°, 1=90°, 2=180°, 3=270°
        self.color = color
        self.board_pos = board_pos

    def __str__(self):
        """Return the player's name."""
        return str(self.name)

    def str_brick(self):
        """Return the current placing brick's 'bioms' value as a string."""
        return str(self.placing_brick["bioms"])

    def set_brick(self, brick):
        """Set the chosen brick."""
        self.chosen_brick = brick

    def set_placing_brick(self, brick):
        """Set the current placing brick."""
        self.placing_brick = brick

    def next_brick(self):
        """Update the placing brick to the chosen brick."""
        self.placing_brick = self.chosen_brick
