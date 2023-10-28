# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 16:57:53 2023

@author: A483349
"""
from Player import Player

class Actions:
    
    #checks if there is a collitoin when rotating.
    #This accurs when the brick rotates outside the playing field
    def checkCollisionRotation(self,pos,rot):
        if((rot == 0 and pos[0] == 4)or rot == 2 and pos[0] == 0):
            return True
        if((rot == 1 and pos[1] == 0)or rot == 3 and pos[1] == 4):
            return True
        return False
        
    def getPositions(self,pos,rot):
        pos1 = [0,0]
        pos2 = [0,0]
        pos1[0] = pos[0]
        pos1[1] = pos[1]
        if(rot == 0):
            pos2[0] = pos[0]
            pos2[1] = pos[1]+1
        if(rot == 1):
            pos2[0] = pos[0]+1
            pos2[1] = pos[1]
        if(rot == 2):
            pos2[0] = pos[0]
            pos2[1] = pos[1]-1
        if(rot == 3):
            pos2[0] = pos[0]-1
            pos2[1] = pos[1]
        return pos1,pos2
    
    def rotate(self,pos,rot):
        if(self.checkCollisionRotation(pos,rot)):
            return rot
        if(rot == 3):
            return 0
        else:
            rot += 1
            return rot
        
    def initAndCheckBrickOK(self,player):
        if not player.board.checkPlacementRollOK(player.placingBrick):
            print("No placec to put \n", player.placingBrick)
            return False
        player.pos = [0,0]
        player.rot = 0
        return True
    
    def choseBrickPos(self,player,keyPress,surface,rect):
        pos1,pos2 = self.getPositions(player.pos, player.rot)
        #player.board.printChosePut(player.placingBrick,pos1,pos2, player.rot)
        #move brick down or scrole
        if(keyPress == 'w' and player.pos[0] != 0 and not(player.rot == 3 and player.pos[0] == 1)):
            player.pos[0] -= 1
        elif (keyPress == 'w'):
            player.board.moveDown()
        #move brick upp or scrole
        if(keyPress == 's' and player.pos[0] != 4 and not(player.rot == 1 and player.pos[0] == 3)):
            player.pos[0] += 1
        elif (keyPress == 's'):
            player.board.moveUpp()
        #move brick right or scrole
        if(keyPress == 'd' and player.pos[1] != 4 and not(player.rot == 0 and player.pos[1] == 3)):
            player.pos[1] += 1
        elif (keyPress == 'd'):
            player.board.moveLeft()
        #move brick left or scrole
        if(keyPress == 'a' and player.pos[1] != 0 and not(player.rot == 2 and player.pos[1] == 1)):
            player.pos[1] -= 1
        elif (keyPress == 'a'):
            player.board.moveRight()
        if(keyPress == 'q'):
            player.rot = self.rotate(player.pos,player.rot)
        if keyPress == 'b':
            pos1,pos2 = self.getPositions(player.pos,player.rot)
            if player.board.put(player.placingBrick, pos1,pos2):
                return True
        pos1,pos2 = self.getPositions(player.pos,player.rot)
        #player.board.printChosePut(player.placingBrick, pos1, pos2, player.rot)
        player.board.drawBoardPlacing(surface,rect,pos1,pos2,player.placingBrick)

        return False
    
    def placeBrick(self,player,keyPress,surface,rect):
        placed = self.choseBrickPos(player,keyPress,surface,rect)
        if placed:
            player.placingBrick = player.chosenBrick
        return placed
        
    def createPlayers(self):
        players = []
        nrOfPlayers = 0
        while True:
            nrOfPlayers = int(input("How many players? "))
            if nrOfPlayers > 0 and nrOfPlayers <= 4:
                break
            print("Not valid playercount")
        
        for i in range(0, nrOfPlayers):
            name = input("Player" + str(i) + " name:")
            players.append(Player(name))
        return players
    
    def firstRound(self,pile,brick4,players):
        pile.print4(brick4)
        playerQueue = [0,0,0,0]
        for p in players:
            while True:
                value = input(p.getName() + " chose brick:")
                index = int(value) - 1
                if(playerQueue[index] == 0):
                    break
                print("Already chosen by " + playerQueue[index].getName())
            p.setPlacingBrick(brick4[index])
            playerQueue[index] = p
        playerQueue = [i for i in playerQueue if i!=0]
        return playerQueue
        
    def chooseBrick(self,player,selected,pile,brick4):
        player.setBrick(brick4[selected])
        return

    """
    This is moving a select to the next empty spot in the list chowned by 0
    Inputs
    selected: the value that is selected in a list
    moveUpp: if the selected is moving upp or down
    list: the list that is treversed. 0 is unocupied
    """
    def jumpSelect(self,selected,moveUpp,list):
        max = len(list)-1 
        empty = False
        #TODO check if the list has no empty spots
        if(moveUpp):
            while(not empty):
                if(selected != 0):
                    selected = selected - 1
                else:
                    selected = max
                if(list[selected] == 0):
                    empty = True
        if(not moveUpp):
            while(not empty):
                if(selected != max):
                    selected = selected + 1
                else:
                    selected = 0
                if(list[selected] == 0):
                    empty = True
        return selected
        
    
    #Chose brick for all player in terminal
    def nextRound(self,pile,brick4,players):
        #newqueue after wat they choose
        playerQueue = [0,0,0,0]
        for p in players:
            print(p.name)
            p.board.printBoard()
            pile.print4(brick4)
            while True:
                try:
                    value = input(p.getName() + "brick(" + p.strBrick() +") chose brick:")
                    index = int(value) - 1
                except ValueError:
                   print("Not an integer! Try again.")
                   continue
                if(index < 0 or index > 5):
                    continue
                if(playerQueue[index] == 0):
                    break
                print("Already chosen by " + playerQueue[index].getName())
            #p.chosenBrick = brick4[index]
            p.setBrick(brick4[index])
            playerQueue[index] = p
        playerQueue = [i for i in playerQueue if i!=0]
        return playerQueue
    
    def choseBrickPosPlayers(self,players):
        for p in players:
            self.choseBrickPos(p.board, p.placingBrick)
            p.placingBrick = p.chosenBrick
        return
        