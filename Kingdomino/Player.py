from Board import Board


class Player:

    def __init__(self, name, color, boardpos):
        self.board: Board = Board()
        self.placing_brick = 0
        self.chosen_brick = 0
        self.name = name
        self.pos = [0, 0]
        self.rot = 0
        self.color = color
        self.boardpos = boardpos

    def __str__(self):
        return str(self.name)

    def strBrick(self):
        return str(self.placing_brick["bioms"])

    def setBrick(self, brick):
        self.chosen_brick = brick

    def set_placing_brick(self, brick):
        self.placing_brick = brick

    def nextBrick(self):
        self.placing_brick = self.chosen_brick
