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
    
    #returns true when succesfully placed
    def put(self,brick,pos1,pos2):
        if self.checkCollision(pos1, pos2):
            return False
        if not self.checkNeighboursOK(brick, pos1, pos2):
            return False
            #return True
        self.board[pos1[0]][pos1[1]] = (brick["bioms"][0],brick["crowns"][0])
        self.board[pos2[0]][pos2[1]] = (brick["bioms"][1],brick["crowns"][1])
        return True
        
    def checkCollision(self,pos1,pos2):
        if self.board[pos1[0]][pos1[1]][0] != 0:
            return True
        if self.board[pos2[0]][pos2[1]][0] != 0:
            return True
        return False
    
    def checkNeighboursOK(self,brick,pos1,pos2):
        return bool(self.checkNeighboursHalvOK(brick["bioms"][0],pos1) or self.checkNeighboursHalvOK(brick["bioms"][1],pos2))
            
    def checkNeighboursHalvOK(self,biom,pos):
        
        if biom == 0:
            joker = 0
        else:
            joker = 1
        #check if next to a good nieghbour upp 
        if pos[0] != 0 and (self.board[pos[0]-1][pos[1]][0] == biom or self.board[pos[0]-1][pos[1]][0] == joker):
               return True
        #check if next to a good nieghbour down 
        if pos[0] != 4 and (self.board[pos[0]+1][pos[1]][0] == biom or self.board[pos[0]+1][pos[1]][0] == joker):
            return True
        #check if next to a good nieghbour left 
        if pos[1] != 0 and (self.board[pos[0]][pos[1]-1][0] == biom or self.board[pos[0]][pos[1]-1][0] == joker):
            return True
        #check if next to a good nieghbour right 
        if pos[1] != 4 and (self.board[pos[0]][pos[1]+1][0] == biom or self.board[pos[0]][pos[1]+1][0] == joker):
            return True
        return False
       
    #checks if it is posible to place a brick
    def checkPlacementOK(self,brick):
        for row in range(0, len(self.board[0])):
            for column in range(0, len(self.board[0])):
                pos = [row,column]
                element = self.board[row][column]
                #if there are 2 0s next to eachother and element is 0
                if self.checkNeighboursHalvOK(0, pos) and element[0] == 0:
                    #and there is a neighbour for one of the bioms then ok
                    if self.checkNeighboursHalvOK(brick["bioms"][0], pos) or self.checkNeighboursHalvOK(brick["bioms"][1], pos):
                            return True
        return False
    
    def checkPlacementRollOK(self,brick):
        tempBoard = copy.deepcopy(self)
        if tempBoard.checkPlacementOK(brick):
            return True
        if tempBoard.moveUpp() and tempBoard.checkPlacementOK(brick):
            return True
        if tempBoard.moveDown() and tempBoard.checkPlacementOK(brick):
            return True
        if tempBoard.moveRight() and tempBoard.checkPlacementOK(brick):
            return True
        if tempBoard.moveLeft() and tempBoard.checkPlacementOK(brick):
            return True
        return False

    def getPoints(self,pos,sumTiles,sumCrowns):
        #pos = 0,0
        #kolla efter grannar
        #kalla kolla efter grannar från granne
        #inga fler grannar? då returnera cronor och mängd grsannar+1
        biom = self.board[pos[0]][pos[1]][0]
        crowns = self.board[pos[0]][pos[1]][1]
        self.board[pos[0]][pos[1]] = (8,0)
        #check if next to a good nieghbour upp 
        if pos[0] != 0 and self.board[pos[0]-1][pos[1]][0] == biom:
           sumTiles,sumCrowns = self.getPoints([pos[0]-1,pos[1]],sumTiles,sumCrowns)
        #check if next to a good nieghbour down 
        if pos[0] != 4 and self.board[pos[0]+1][pos[1]][0] == biom:
            sumTiles,sumCrowns = self.getPoints([pos[0]+1,pos[1]],sumTiles,sumCrowns)
        #check if next to a good nieghbour left 
        if pos[1] != 0 and self.board[pos[0]][pos[1]-1][0] == biom:
            sumTiles,sumCrowns = self.getPoints([pos[0],pos[1]-1],sumTiles,sumCrowns)
        #check if next to a good nieghbour right 
        if pos[1] != 4 and self.board[pos[0]][pos[1]+1][0] == biom:
            sumTiles,sumCrowns = self.getPoints([pos[0],pos[1]+1],sumTiles,sumCrowns)
        return sumTiles+1,sumCrowns + crowns
    
    def getAllPoints(self):
        total = 0
        for row in range(0, len(self.board[0])):
            for column in range(0, len(self.board[0])):
                if(self.board[row][column][0] != 8):
                    tiles,crowns = self.getPoints([row,column],0,0)
                    total += tiles*crowns
        return total
    
    def moveDown(self):
        for x in self.board[4]:
            if any(x):
                return False
        self.board = np.roll(self.board, 1,axis=0)
        return True
    
    def moveUpp(self):
        for x in self.board[0]:
            if any(x):
                return False
        self.board = np.roll(self.board, -1,axis=0)
        return True
    
    def moveRight(self):
        for x in np.array(self.board)[:,4]:
            if any(x):
                return False
        self.board = np.roll(self.board, 1,axis=1)
        return True
    
    def moveLeft(self):
        for x in np.array(self.board)[:,0]:
            if any(x):
                return False
        self.board = np.roll(self.board, -1,axis=1)
        return True
    
    def printChosePut(self, brick, pos1, pos2):
        # Create a deep copy of the current board state
        showBoard = copy.deepcopy(self)

        # Update the copied board with the new brick placements
        showBoard.board[pos1[0]][pos1[1]] = (brick["bioms"][0], brick["crowns"][0])
        showBoard.board[pos2[0]][pos2[1]] = (brick["bioms"][1], brick["crowns"][1])
        
        return showBoard
    
    def drawPlayerBoard(self, surface: pygame.Surface, player, pos1 = None, pos2 = None):
        # Unpack rect values for clarity
        posX, posY, rectWidth, rectHeight = player.boardpos
        cellWidth = rectWidth / 5
        cellHeight = rectHeight / 5

        placing_an_extra_brick = (pos1 is not None and pos2 is not None)

        # Determine the board layout to display
        if placing_an_extra_brick:
            showBoard = self.printChosePut(player.placingBrick, pos1, pos2)

        # Draw the main background rectangle
        pygame.draw.rect(surface, player.color, (posX - 5, posY - 5, rectWidth + 10, rectHeight + 10))

        # Draw each cell in the 5x5 grid
        for row in range(5):
            for column in range(5):
                cellX = posX + column * cellWidth
                cellY = posY + row * cellHeight
                cellRect = (cellX, cellY, cellWidth, cellHeight)

                if placing_an_extra_brick:
                    cellBiome, cellCrowns = showBoard.board[row][column]
                    cellColor = config.allColors[cellBiome]
                else:
                    cellColor = config.allColors[self.board[row][column][0]]
                
                # Draw the cell and its border
                pygame.draw.rect(surface, cellColor, cellRect)          # Cell color
                pygame.draw.rect(surface, (0, 0, 0), cellRect, 1)       # Cell border

                if placing_an_extra_brick:
                    self._draw_crowns(surface,cellRect,cellCrowns)
                    
    def _draw_crowns(self, surface: pygame.Surface, cellRect, cellCrowns):
        cellX, cellY, cellWidth, cellHeight = cellRect
        crownRect = pygame.Rect(cellX + cellWidth / 10, cellY + cellHeight / 10, cellWidth / 8, cellHeight / 8)
        offset = cellWidth / 7
        for _ in range(cellCrowns):
            pygame.draw.rect(surface, (0, 0, 0), crownRect)
            crownRect.left += offset
        return


    