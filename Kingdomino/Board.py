import numpy as np
import copy
import pygame

background_colour = (117, 115, 89) 
startBrickColor = (255,255,255)
wheatColor = (212, 204, 59)
forestColor = (25, 115, 49)
waterColor = (45, 116, 179)
fieldColor = (36, 201, 80)
desertColor = (144, 150, 123)
mineColor = (64, 69, 49)

allColors =  [background_colour,startBrickColor,wheatColor,forestColor,waterColor,fieldColor,desertColor,mineColor]

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
        
    def printBoard(self):
        for row in self.board:
            print("\n")
            for column in row:
                if(column[1] == 0):
                    print(column[0],"   ", end="", sep="") 
                if(column[1] == 1):
                    print(column[0],"*  ", end="", sep="")
                if(column[1] == 2):
                    print(column[0],"** ", end="", sep="")
                if(column[1] == 3):
                    print(column[0],"***", end="", sep="")
        print("\n")
        
    def printBoardBrick(self,pos1,pos2):
        for row in range(0, len(self.board[0])):
            print("\n")
            for column in range(0, len(self.board[0])):
                if(self.board[row][column][1] == 0):
                    print(self.board[row][column][0],"  ", end="  ", sep="") 
                if(self.board[row][column][1] == 1):
                    print(self.board[row][column][0],"* ", end="  ", sep="")
                if(self.board[row][column][1] == 2):
                    print(self.board[row][column][0],"**", end="  ", sep="") 
                if(self.board[row][column][1] == 3):
                    print(self.board[row][column][0],"***", end="", sep="") 
        print("\n")
    
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
    
    def printChosePut(self,brick,pos1,pos2):
        showBoard = Board()
        showBoard = copy.deepcopy(self)
        showBoard.board[pos1[0]][pos1[1]] = (brick["bioms"][0],brick["crowns"][0])
        showBoard.board[pos2[0]][pos2[1]] = (brick["bioms"][1],brick["crowns"][1])
        showBoard.printBoard()
        return showBoard
        
    def drawBoard(self,surface,rect):
        posX = rect[0]
        posY = rect[1]
        width = rect[2]/5
        hight = rect[3]/5
        pygame.draw.rect(surface,allColors[1],rect)
        for row in range(0,5):
            changY = posY + row * hight
            for column in range(0,5):
                changX = posX + column * width
                partRect = (changX,changY,width,hight)
                color = allColors[self.board[row][column][0]]
                pygame.draw.rect(surface,color,partRect)
                pygame.draw.rect(surface,(0,0,0),partRect,1)
        return
    
    def drawBoardPlacing(self,surface,rect,pos1,pos2,brick):
        posX = rect[0]
        posY = rect[1]
        width = rect[2]/5
        hight = rect[3]/5
        showBoard = self.printChosePut(brick,pos1,pos2)
        pygame.draw.rect(surface,allColors[1],rect)
        for row in range(0,5):
            changY = posY + row * hight
            for column in range(0,5):
                changX = posX + column * width
                partRect = (changX,changY,width,hight)
                color = allColors[showBoard.board[row][column][0]]
                pygame.draw.rect(surface,color,partRect)
                pygame.draw.rect(surface,(0,0,0),partRect,1)
        return
    