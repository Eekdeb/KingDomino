# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 21:06:32 2023

@author: a483349
"""
from Board import Board

class Player:
    
    def __init__(self, name):
        self.board = Board()
        self.placingBrick = 0
        self.chosenBrick = 0
        self.name = name
        self.pos = [0,0]
        self.rot = 0
        
    def __str__(self):
        return str(self.name)
    
    #TODO gör så att man kan se kronor också när man printar denna
    def strBrick(self):
        return str(self.placingBrick['bioms'])
    
    def getName(self):
        return self.name
    
    def setBrick(self,brick):
        self.chosenBrick = brick
    
    def setPlacingBrick(self,brick):
        self.placingBrick = brick

    def nextBrick(self):
        self.placingBrick = self.chosenBrick