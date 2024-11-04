from Board import Board

class Player:
    
    def __init__(self, name, color, boardpos):
        self.board:Board = Board()
        self.placingBrick = 0
        self.chosenBrick = 0
        self.name = name
        self.pos = [0,0]
        self.rot = 0
        self.color = color
        self.boardpos = boardpos
        
    def __str__(self):
        return str(self.name)
    
    def strBrick(self):
        return str(self.placingBrick['bioms'])
    
    def setBrick(self,brick):
        self.chosenBrick = brick
    
    def setPlacingBrick(self,brick):
        self.placingBrick = brick

    def nextBrick(self):
        self.placingBrick = self.chosenBrick