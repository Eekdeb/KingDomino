# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 16:57:53 2023

@author: A483349
"""
from Player import Player
from textEditor import getName
from NameSelector import player_name_entry
import pygame

class Actions:
    
    #checks if there is a collitoin when rotating.
    #This accurs when the brick rotates outside the playing field
    def check_collision_rotation(self,pos,rot):
        if((rot == 0 and pos[0] == 4)or rot == 2 and pos[0] == 0):
            return True
        if((rot == 1 and pos[1] == 0)or rot == 3 and pos[1] == 4):
            return True
        return False
        
    def get_positions(self, pos, rot):
        offsets = {
            0: (0, 1),   # Up
            1: (1, 0),   # Right
            2: (0, -1),  # Down
            3: (-1, 0)   # Left
        }
        # pos1 is the original position
        pos1 = pos[:]
        # pos2 is determined based on rotation offset
        pos2 = [pos[0] + offsets[rot][0], pos[1] + offsets[rot][1]]
        
        return pos1, pos2
    
    def rotate(self,pos,rot):
        if self.check_collision_rotation(pos,rot):
            return rot
        return (rot + 1) % 4
        
    def init_and_check_brick_OK(self,player):
        if not player.board.checkPlacementRollOK(player.placingBrick):
            print("No placec to put \n", player.placingBrick)
            return False
        player.pos = [0,0]
        player.rot = 0
        return True
    
    def choose_brick_position(self, player: Player, keyPress, surface, rect):
        pos1, pos2 = self.get_positions(player.pos, player.rot)
        # Define movement behavior for each key press
        move_actions = {
            'w': lambda: (player.pos[0] > 0 and not (player.rot == 3 and player.pos[0] == 1), -1, 0, player.board.moveDown),
            's': lambda: (player.pos[0] < 4 and not (player.rot == 1 and player.pos[0] == 3), 1, 0, player.board.moveUpp),
            'd': lambda: (player.pos[1] < 4 and not (player.rot == 0 and player.pos[1] == 3), 0, 1, player.board.moveLeft),
            'a': lambda: (player.pos[1] > 0 and not (player.rot == 2 and player.pos[1] == 1), 0, -1, player.board.moveRight)
        }
        # Handle key movements for 'w', 's', 'd', and 'a'
        if keyPress in move_actions:
            can_move, dx, dy, scroll_action = move_actions[keyPress]()
            if can_move:
                player.pos[0] += dx
                player.pos[1] += dy
            else:
                scroll_action()
        # Handle rotation
        if keyPress == 'q':
            player.rot = self.rotate(player.pos, player.rot)
        # Place brick
        if keyPress == 'b':
            pos1, pos2 = self.get_positions(player.pos, player.rot)
            if player.board.put(player.placingBrick, pos1, pos2):
                return True
        # Update and draw player's position on the board
        pos1, pos2 = self.get_positions(player.pos, player.rot)
        player.board.drawPlayerBoard(surface, player, pos1, pos2)
        return False

    
    def place_brick(self,player,keyPress,surface,rect):
        placed = self.choose_brick_position(player,keyPress,surface,rect)
        if placed:
            player.placingBrick = player.chosenBrick
        return placed
    
    def createPlayers(self, screen: pygame.Surface, brickSize:int, nrOfPlayers: int) -> list[Player]:
        # Get screen dimensions directly from the screen surface
        screen_width, screen_height = screen.get_width(), screen.get_height()

        # Define board positions based on the screen dimensions and brick size
        boardpos1 = (screen_width / 12, screen_height / 12, brickSize * 5, brickSize * 5)
        boardpos2 = (screen_width / 12, 6 * (screen_height / 12), brickSize * 5, brickSize * 5)
        boardpos3 = (8 * (screen_width / 12), screen_height / 12, brickSize * 5, brickSize * 5)
        boardpos4 = (8 * (screen_width / 12), 6 * (screen_height / 12), brickSize * 5, brickSize * 5)
        boardpositions = [boardpos1, boardpos2, boardpos3, boardpos4]

        player_names,colors = player_name_entry(screen)
        players = []
        for i in range(0, nrOfPlayers):
            players.append(Player(player_names[i],colors[i],boardpositions[i]))
        return players
        
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
        