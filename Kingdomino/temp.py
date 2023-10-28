# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#from Board import Board
from Actions import Actions
from Player import Player
from operator import itemgetter
from BrickStack import BrickStack
import random
import time

"""
Types
1: starting brick   
2: wheat field      
3: forest      
4: water
5: grass field
6: desert
7: mine
"""

#Initialis
ac = Actions()
pile = BrickStack()
pile.shuffle()
#create players
playerQueue = ac.createPlayers()

#Start the game
##Payers Pick the first card
brick4 = pile.get4()
##First round of chosing
playerQueue = ac.firstRound(pile,brick4,playerQueue)

for i in range(0, 11):
    #Draw new bricks
    brick4 = pile.get4()
    #Next round chosing
    playerQueue = ac.nextRound(pile,brick4,playerQueue)
    #Place the Bricks chosen
    ac.choseBrickPosPlayers(playerQueue)
    
#placing last brick
ac.choseBrickPosPlayers(playerQueue)
#print out the points
for p in playerQueue:
    print(p.name + ": " + str(p.board.getAllPoints()))
    
"""
pile.print4(brick4)
for p in playerQueue:
    while True:
        value = input(p.getName() + " chose brick:")
        index = int(value) - 1
        if(playerQueue2[index] == 0):
            break
        print("Already chosen by " + playerQueue2[index].getName())
    p.setPlacingBrick(brick4[index])
    playerQueue2[index] = p
"""



"""
#tmp = copy.deepcopy(board)
for i in range(0, 2):
    brick4 = pile.get4()
    brick4 = sorted(brick4,key = itemgetter('value'))
    pile.print4(brick4)
    string = str(playerQueue[0]) + " chose brick:"
    value = input(string)
    ac.choseBrickPos(board, brick4[int(value)-1])
    time.sleep(0.5)
#ac.choseBrickPos(board, newBrick)
point = board.getAllPoints()
print("The total points are: ",point)
"""